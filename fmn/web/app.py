import os

import flask
from flask_fas_openid import FAS
from flask.ext.mako import MakoTemplates
from flask.ext.mako import render_template

import fmn.lib
import fmn.lib.models

# Create the application.
app = flask.Flask(__name__)

# set up FAS
app.config.from_object('fmn.web.default_config')
if 'FMN_WEB_CONFIG' in os.environ:  # pragma: no cover
    app.config.from_envvar('FMN_WEB_CONFIG')

FAS = FAS(app)
mako = MakoTemplates(app)
SESSION = fmn.lib.models.init(app.config['DB_URL'], debug=False, create=False)


@app.teardown_request
def shutdown_session(exception=None):
    """ Remove the DB session at the end of each request. """
    SESSION.remove()


@app.route('/')
def index():
    if flask.g.fas_user:
        url = flask.url_for('profile', username=flask.g.fas_user.username)
        return flask.redirect(url)

    return "hello world"


def is_admin(user):
    return any([team.name in app.config.get('ADMIN_GROUPS', [])
                for team in user.approved_memberships])


@app.route('/<username>')
@app.route('/<username>/')
def profile(username):
    if flask.g.fas_user.username != username and not is_admin(flask.g.fas_user):
        flask.abort(403)
    return render_template('profile.mak')


@app.route('/login/', methods=('GET', 'POST'))
def auth_login():
    """ Method to log into the application. """

    default = flask.url_for('index')
    next_url = flask.request.args.get('next', default)

    # If user is already logged in, return them to where they were last
    if flask.g.fas_user:
        return flask.redirect(next_url)

    return FAS.login(return_url=next_url)


@app.route('/logout/', methods=('GET', 'POST'))
def auth_logout():
    """ Method to log out of the application. """
    next_url = flask.request.args.get('next', flask.url_for('index'))

    # If user is already logged out, return them to where they were last
    if not flask.g.fas_user:
        return flask.redirect(next_url)

    FAS.logout()
    return flask.redirect(next_url)
