import os

import flask
from flask_fas_openid import FAS

from functools import wraps

import fedora.client
import fedmsg.config

import fmn.lib
import fmn.lib.models
import fmn.web.converters
import fmn.web.forms


__version__ = '0.1.0'

# Create the application.
app = flask.Flask(__name__)

app.url_map.converters['not_reserved'] = fmn.web.converters.NotReserved

# set up FAS
app.config.from_object('fmn.web.default_config')
if 'FMN_WEB_CONFIG' in os.environ:  # pragma: no cover
    app.config.from_envvar('FMN_WEB_CONFIG')

FAS = FAS(app)

fedmsg_config = fedmsg.config.load_config()
db_url = fedmsg_config.get('fmn.sqlalchemy.uri')
if not db_url:
    raise ValueError("fmn.sqlalchemy.uri must be present")

valid_paths = fmn.lib.load_filters(root="fmn.filters")

SESSION = fmn.lib.models.init(db_url, debug=False, create=False)


@app.teardown_request
def shutdown_session(exception=None):
    """ Remove the DB session at the end of each request. """
    SESSION.remove()


def admin(user):
    return any([team.name in app.config.get('ADMIN_GROUPS', [])
                for team in user.approved_memberships])


class APIError(Exception):
    def __init__(self, status_code, errors):
        self.status_code = status_code
        self.errors = errors


def api_method(function):
    """ A decorator to handle common API output stuff. """

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except APIError as e:
            app.logger.exception(e)
            response = flask.jsonify(e.errors)
            response.status_code = e.status_code
        else:
            # Redirect browsers to the object.
            # otherwise, return json response to api clients.
            if 'url' in result and request_wants_html():
                response = flask.redirect(result['url'])
            else:
                response = flask.jsonify(result)
                response.status_code = 200
        return response

    return wrapper


def request_wants_html():
    """ accept header returns json type content only
    http://flask.pocoo.org/snippets/45/
    """
    best = flask.request.accept_mimetypes \
        .best_match(['application/json', 'text/html', 'text/plain'])
    return best == 'text/html' and \
        flask.request.accept_mimetypes[best] > \
        (flask.request.accept_mimetypes['application/json'] or \
        flask.request.accept_mimetypes['text/plain'])


@app.context_processor
def inject_variable():
    """ Inject into all templates variables that we would like to have all
    the time.
    """
    username = None
    contexts = []
    if flask.g.fas_user and flask.g.fas_user.username:
        username = flask.g.fas_user.username
        contexts = fmn.lib.models.Context.all(SESSION)
    return dict(username=username,
                contexts=contexts,
                valid_paths=valid_paths,
                version=__version__)


@app.route('/_heartbeat')
def heartbeat():
    """ An endpoint so haproxy can know we're alive. """
    return "Lub-Dub"


@app.route('/')
def index():
    username = getattr(flask.g.fas_user, 'username', None)
    contexts = fmn.lib.models.Context.all(SESSION)

    return flask.render_template(
        'index.html',
        current='index')


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

    return flask.render_template(
        'profile.html',
        current='profile',
        avatar=avatar)


@app.route('/<not_reserved:username>/<context>')
@app.route('/<not_reserved:username>/<context>/')
def context(username, context):
    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    pref = fmn.lib.models.Preference.get_or_create(SESSION, username, context)
    return flask.render_template(
        'context.html',
        current=context.name,
        context=context,
        preference=pref)


@app.route('/<not_reserved:username>/<context>/<chain_name>')
@app.route('/<not_reserved:username>/<context>/<chain_name>/')
def chain(username, context, chain_name):
    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    pref = fmn.lib.models.Preference.get_or_create(SESSION, username, context)

    chain = None
    for _chain in pref.chains:
        if _chain.name == chain_name:
            chain = _chain
            break

    if not pref.has_chain(SESSION, chain_name):
        flask.abort(404)

    chain = pref.get_chain(SESSION, chain_name)

    return flask.render_template(
        'chain.html',
        current=context.name,
        chain=chain)


@app.route('/api/chain', methods=['POST', 'DELETE'])
@api_method
def handle_chain():
    form = fmn.web.forms.ChainForm(flask.request.form)

    if not form.validate():
        raise APIError(400, form.errors)

    username = form.username.data
    context = form.context.data
    chain_name = form.chain_name.data
    method = (form.method.data or flask.request.method).upper()

    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        raise APIError(403, dict(reason="%r is not %r" % (
            flask.g.fas_user.username, username
        )))

    if method not in ['POST', 'DELETE']:
        raise APIError(405, dict(reason="Only POST and DELETE accepted"))

    user = fmn.lib.models.User.by_username(SESSION, username)
    if not user:
        raise APIError(403, dict(reason="%r is not a user" % username))

    ctx = fmn.lib.models.Context.by_name(SESSION, context)
    if not ctx:
        raise APIError(403, dict(reason="%r is not a context" % context))

    pref = fmn.lib.models.Preference.get_or_create(SESSION, username, ctx)

    try:
        if method == 'POST':
            # Ensure that a chain with this name doesn't already exist.
            if pref.has_chain(SESSION, chain_name):
                raise APIError(404, dict(
                    reason="%r already exists" % chain_name))

            chain = fmn.lib.models.Chain.create(SESSION, chain_name)
            pref.add_chain(SESSION, chain)
            next_url = flask.url_for(
                'chain',
                username=username,
                context=context,
                chain_name=chain_name,
            )
        elif method == 'DELETE':
            chain = pref.get_chain(SESSION, chain_name)
            SESSION.delete(chain)
            SESSION.commit()
            next_url = flask.url_for(
                'context',
                username=username,
                context=context,
            )
        else:
            raise NotImplementedError("This is impossible.")
    except (ValueError, KeyError) as e:
        app.logger.exception(e)
        raise APIError(403, dict(reason=str(e)))


    return dict(message="ok", url=next_url)


@app.route('/api/details', methods=['POST'])
@api_method
def handle_details():
    form = fmn.web.forms.DetailsForm(flask.request.form)

    if not form.validate():
        raise APIError(400, form.errors)

    username = form.username.data
    context = form.context.data
    detail_value = form.detail_value.data

    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        raise APIError(403, dict(reason="%r is not %r" % (
            flask.g.fas_user.username, username
        )))

    user = fmn.lib.models.User.by_username(SESSION, username)
    if not user:
        raise APIError(403, dict(reason="%r is not a user" % username))

    ctx = fmn.lib.models.Context.by_name(SESSION, context)
    if not ctx:
        raise APIError(403, dict(reason="%r is not a context" % context))

    pref = fmn.lib.models.Preference.get_or_create(SESSION, username, ctx)

    # TODO -- we need to *VERIFY* that they really have this delivery detail
    # before we start doing stuff.  Otherwise, ralph could put in pingou's
    # email address and spam the crap out of him.
    pref.update_details(SESSION, detail_value)

    next_url = flask.url_for(
        'context',
        username=username,
        context=context,
    )

    return dict(message="ok", url=next_url)


@app.route('/api/filter', methods=['POST'])
@api_method
def handle_filter():
    form = fmn.web.forms.FilterForm(flask.request.form)

    if not form.validate():
        raise APIError(400, form.errors)

    username = form.username.data
    context = form.context.data
    chain_name = form.chain_name.data
    code_path = form.filter_name.data
    method = (form.method.data or flask.request.method).upper()
    # TODO -- how to extract arguments to filters

    if flask.g.fas_user.username != username and not admin(flask.g.fas_user):
        raise APIError(403, dict(reason="%r is not %r" % (
            flask.g.fas_user.username, username
        )))

    if method not in ['POST', 'DELETE']:
        raise APIError(405, dict(reason="Only POST and DELETE accepted"))

    user = fmn.lib.models.User.by_username(SESSION, username)
    if not user:
        raise APIError(403, dict(reason="%r is not a user" % username))

    ctx = fmn.lib.models.Context.by_name(SESSION, context)
    if not ctx:
        raise APIError(403, dict(reason="%r is not a context" % context))

    pref = fmn.lib.models.Preference.get_or_create(SESSION, username, ctx)

    if not pref.has_chain(SESSION, chain_name):
        raise APIError(403, dict(reason="%r is not a chain" % chain_name))

    chain = pref.get_chain(SESSION, chain_name)

    try:
        if method == 'POST':
            chain.add_filter(SESSION, valid_paths, code_path)# ,**arguments)
        elif method == 'DELETE':
            chain.remove_filter(SESSION, code_path)#, **arguments)
        else:
            raise NotImplementedError("This is impossible.")
    except (ValueError, KeyError) as e:
        app.logger.exception(e)
        raise APIError(403, dict(reason=str(e)))

    next_url = flask.url_for(
        'chain',
        username=username,
        context=context,
        chain_name=chain_name,
    )

    return dict(message="ok", url=next_url)


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
