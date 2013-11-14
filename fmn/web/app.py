import os

import flask
from flask_fas_openid import FAS
from flask.ext.mako import MakoTemplates
from flask.ext.mako import render_template

import fedora.client
import fedmsg.config

import fmn.lib
import fmn.lib.models
import fmn.web.converters

# Create the application.
app = flask.Flask(__name__)

app.url_map.converters['not_reserved'] = fmn.web.converters.NotReserved

# set up FAS
app.config.from_object('fmn.web.default_config')
if 'FMN_WEB_CONFIG' in os.environ:  # pragma: no cover
    app.config.from_envvar('FMN_WEB_CONFIG')

FAS = FAS(app)
mako = MakoTemplates(app)

fedmsg_config = fedmsg.config.load_config()
db_url = fedmsg_config.get('fmn.sqlalchemy.uri')
if not db_url:
    raise ValueError("fmn.sqlalchemy.uri must be present")

SESSION = fmn.lib.models.init(db_url, debug=False, create=False)


@app.teardown_request
def shutdown_session(exception=None):
    """ Remove the DB session at the end of each request. """
    SESSION.remove()


def admin(user):
    return any([team.name in app.config.get('ADMIN_GROUPS', [])
                for team in user.approved_memberships])


def template_arguments(**kwargs):
    arguments = dict(
        fas_user=flask.g.fas_user,
        url_for=flask.url_for,
        contexts=fmn.lib.models.Context.all(SESSION),
    )
    arguments.update(kwargs)
    return arguments


@app.route('/_heartbeat')
def heartbeat():
    """ An endpoint so haproxy can know we're alive. """
    return "Lub-Dub"


@app.route('/')
def index():
    username = getattr(flask.g.fas_user, 'username', None)
    d = template_arguments(username=username, current='index')
    return render_template('index.mak', **d)


@app.route('/<not_reserved:username>')
@app.route('/<not_reserved:username>/')
def profile(username):

    if (not flask.g.fas_user or (
        flask.g.fas_user.username != username and
        not admin(flask.g.fas_user))):

        flask.abort(403)

    fas = fedora.client.AccountSystem()
    avatar = fas.avatar_url(
        username, lookup_email=False, service='libravatar', size=140)

    d = template_arguments(username=username, current='profile', avatar=avatar)
    return render_template('profile.mak', **d)


@app.route('/<not_reserved:username>/<context>')
@app.route('/<not_reserved:username>/<context>/')
def context(username, context):
    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    d = template_arguments(username=username, current=context)
    return render_template('context.mak', **d)


@app.route('/<not_reserved:username>/<context>/<chain_name>')
@app.route('/<not_reserved:username>/<context>/<chain_name>/')
def chain(username, context, chain_name):
    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    pref = fmn.lib.models.Preference.load(user, context)
    chain = None
    for _chain in pref.chains:
        if _chain.name == chain_name:
            chain = _chain
            break

    d = template_arguments(username=username, current=context, chain=chain)
    return render_template('chain.mak', **d)


@app.route('/login/', methods=('GET', 'POST'))
def login():
    """ Method to log into the application. """

    default = flask.url_for('index')
    next_url = flask.request.args.get('next', default)

    # If user is already logged in, return them to where they were last
    if flask.g.fas_user:
        return flask.redirect(next_url)

    return FAS.login(return_url=next_url)


@app.route('/logout/', methods=('GET', 'POST'))
def logout():
    """ Method to log out of the application. """
    next_url = flask.request.args.get('next', flask.url_for('index'))

    # If user is already logged out, return them to where they were last
    if not flask.g.fas_user:
        return flask.redirect(next_url)

    FAS.logout()
    return flask.redirect(next_url)
