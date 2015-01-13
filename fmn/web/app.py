import codecs
import copy
import datetime
import functools
import os
from bunch import Bunch
from pkg_resources import get_distribution

import arrow
import docutils
import docutils.examples
import fedmsg.config
import fedmsg.meta
import jinja2
import libravatar
import markupsafe

import flask
from flask.ext.openid import OpenID

import fmn.lib
import fmn.lib.hinting
import fmn.lib.models
import fmn.web.converters
import fmn.web.forms

import datanommer.models

# Create the application.
app = flask.Flask(__name__)
log = app.logger

app.url_map.converters['not_reserved'] = fmn.web.converters.NotReserved

# set up FAS
app.config.from_object('fmn.web.default_config')
if 'FMN_WEB_CONFIG' in os.environ:  # pragma: no cover
    app.config.from_envvar('FMN_WEB_CONFIG')

# Set up OpenID in stateless mode
oid = OpenID(app, safe_roots=[], store_factory=lambda: None,
             url_root_as_trust_root=True)

# Inject a simple jinja2 test -- it is surprising jinja2 does not have this.
app.jinja_env.tests['equalto'] = lambda x, y: x == y

# Also, allow 'continue' and 'break' statements in jinja loops
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

fedmsg_config = fedmsg.config.load_config()
db_url = fedmsg_config.get('fmn.sqlalchemy.uri')
if not db_url:
    raise ValueError("fmn.sqlalchemy.uri must be present")

fedmsg.meta.make_processors(**fedmsg_config)

valid_paths = fmn.lib.load_rules(root="fmn.rules")

# Pick out the submodules so we can group rules nicely in the UI
# Order them alphabetically, except for 'generic' which comes first.
rule_types = list(set([
    d[path]['submodule'] for _, d in valid_paths.items() for path in d
]))


def _rule_type_comparator(x, y):
    if x == 'generic':
        return -1
    elif y == 'generic':
        return 1
    return cmp(x, y)

rule_types.sort(_rule_type_comparator)

# Initialize our own db connection
SESSION = fmn.lib.models.init(db_url, debug=False, create=False)

# Initialize a datanommer session.
try:
    datanommer.models.init(fedmsg_config['datanommer.sqlalchemy.url'])
except Exception as e:
    log.warning("Could not initialize datanommer db connection:")
    log.exception(e)


def extract_openid_identifier(openid_url):
    openid = openid_url.split('://')[1]
    if openid.endswith('/'):
        openid = openid[:-1]
    if 'id?id=' in openid:
        openid = openid.split('id?id=')[1]
    if 'me.yahoo.com/a/' in openid:
        openid = openid.split('me.yahoo.com/a/')[1]
    openid = openid.replace('/', '_')
    return openid


@app.before_request
def check_auth():
    flask.g.fedmsg_config = fedmsg_config
    flask.g.auth = Bunch(
        logged_in=False,
        method=None,
        id=None,
    )
    if 'openid' in flask.session:
        openid = extract_openid_identifier(flask.session.get('openid'))
        flask.g.auth.logged_in = True
        flask.g.auth.method = u'openid'
        flask.g.auth.openid = openid
        flask.g.auth.openid_url = flask.session.get('openid')
        flask.g.auth.fullname = flask.session.get('fullname', None)
        flask.g.auth.nickname = flask.session.get('nickname', None)
        flask.g.auth.email = flask.session.get('email', None)


@oid.after_login
def after_openid_login(resp):
    default = flask.url_for('index')
    if resp.identity_url:
        openid_url = resp.identity_url
        flask.session['openid'] = openid_url
        flask.session['fullname'] = resp.fullname
        flask.session['nickname'] = resp.nickname or resp.fullname
        flask.session['email'] = resp.email
        next_url = flask.request.args.get('next', default)
        return flask.redirect(next_url)
    else:
        return flask.redirect(default)


@app.teardown_request
def shutdown_session(exception=None):
    """ Remove the DB session at the end of each request. """
    SESSION.remove()


def admin(user):
    return user in app.config.get('FMN_ADMINS', [])


class APIError(Exception):
    def __init__(self, status_code, errors):
        self.status_code = status_code
        self.errors = errors


def login_required(function):
    """ Flask decorator to restrict access to logged-in users. """
    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        """ Decorated function, actually does the work. """
        if not flask.g.auth.logged_in:
            flask.flash('Login required', 'errors')
            return flask.redirect(flask.url_for(
                fedmsg_config.get('fmn.web.default_login', 'login'),
                next=flask.request.url))

        # Ensure that the logged in user exists before we proceed.
        fmn.lib.models.User.get_or_create(
            SESSION,
            openid=flask.g.auth.openid,
            openid_url=flask.g.auth.openid_url,
        )

        return function(*args, **kwargs)
    return decorated_function


def api_method(function):
    """ A decorator to handle common API output stuff. """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except APIError as e:
            log.exception(e)
            response = flask.jsonify(e.errors)
            response.status_code = e.status_code
        else:
            # Redirect browsers to the object.
            # otherwise, return json response to api clients.
            if 'url' in result and request_wants_html():
                response = flask.redirect(result['url'])
            else:
                # Here we use fedmsg's encoder instead of flask.jsonify since
                # fedmsg can handle things like datetime objects buried in the
                # messages.
                if flask.request.is_xhr:
                    encoder = fedmsg.encoding.dumps
                else:
                    encoder = fedmsg.encoding.pretty_dumps

                response = flask.Response(
                    encoder(result), mimetype='application/json')
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
        flask.request.accept_mimetypes[best] > (
            flask.request.accept_mimetypes['application/json'] or
            flask.request.accept_mimetypes['text/plain'])


@app.context_processor
def inject_variable():
    """ Inject into all templates variables that we would like to have all
    the time.
    """
    openid = None
    contexts = []
    if flask.g.auth.logged_in:
        openid = flask.g.auth.openid
        contexts = fmn.lib.models.Context.all(SESSION)

    web_version = get_distribution('fmn.web').version
    lib_version = get_distribution('fmn.lib').version
    rules_version = get_distribution('fmn.rules').version

    return dict(openid=openid,
                contexts=contexts,
                valid_paths=valid_paths,
                rule_types=rule_types,
                web_version=web_version,
                lib_version=lib_version,
                rules_version=rules_version)


@app.route('/_heartbeat')
def heartbeat():
    """ An endpoint so haproxy can know we're alive. """
    return "Lub-Dub"


@app.route('/')
def index():
    if flask.g.auth.logged_in:
        return flask.redirect(flask.url_for('profile_redirect'))

    return flask.render_template(
        'index.html',
        current='index',
        contexts=fmn.lib.models.Context.all(SESSION),
    )


@app.route('/about')
def about():
    return flask.render_template(
        'docs.html',
        current='about',
        docs=load_docs(flask.request),
    )

@app.route('/link-fedora-mobile/<not_reserved:openid>/<not_reserved:api_key>/<not_reserved:registration_id>')
@app.route('/link-fedora-mobile/<not_reserved:openid>/<not_reserved:api_key>/<not_reserved:registration_id>/')
@api_method
def link_fedora_mobile(openid, api_key, registration_id):
    '''The workflow for using this endpoint works like this:

    - Nancy installs Fedora Mobile and wants notifications
    - She hits a button in the app which takes her to a login page for fmn
    - She logs in and taps a link to tell Mobile her fmn API key
    - Mobile gets the key and shows a button for actually registering the
      device on fmn (i.e. using *this* endpoint)
    - She taps the button - now FMN knows about her registration id and it is
      pending her confirmation
    - Consumer sends her a notification which renders with two buttons
      (accept, reject)
    - She taps one of these buttons which hits the normal accept/reject URL,
      or perhaps a modified version of them which takes the registration ID
      and API key, so the app can hit them instead of opening a browser.
    '''

    user = fmn.lib.models.User.by_openid(SESSION, openid)
    if not user or user.api_key != api_key:
        raise APIError(403, dict(reason="Invalid login"))

    # At this point, we can reasonably assume the user is who they say they are
    # (or that their phone got stolen and someone decided to show them how
    # awesome Fedora Mobile is before giving their phone back).
    #
    # Now we can add an Android context to the user's account.
    # Much of this is copied from /api/details below. :(
    ctx = fmn.lib.models.Context.by_name(SESSION, "android")
    if not ctx:
        raise APIError(403, dict(reason="android is not a context"))

    # Ensure that the preference exists before we proceed.
    fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=ctx)

    try:
        fmn.lib.validate_detail_value(ctx, registration_id)
    except Exception as e:
        raise APIError(403, dict(reason=str(e)))

    # Make sure no one else has this one in play yet
    if fmn.lib.models.DetailValue.exists(SESSION, registration_id):
        raise APIError(403, dict(reason="That value is already claimed."))

    # We need to *VERIFY* that they really have this delivery detail
    # before we start doing stuff.  Otherwise, ralph could put in pingou's
    # email address and spam the crap out of him.
    con = fmn.lib.models.Confirmation.get_or_create(
        SESSION, openid=openid, context=ctx)
    con.set_value(SESSION, registration_id)
    con.set_status(SESSION, 'pending')

    return {"status": "ok"}

@app.route('/confirm/<action>/<not_reserved:openid>/<secret>/<api_key>/')
@app.route('/confirm/<action>/<not_reserved:openid>/<secret>/<api_key>')
@api_method
def handle_confirmation_api_mobile(action, openid, secret, api_key):
    '''This is an *unauthenticated* endpoint to confirm registration. Or
    rather, it's authenticated via the api key in the URL instead of by the
    normal Flask auth mechanism.

    This is for Fedora Mobile and should not be relied upon to always exist.'''

    if action not in ['accept', 'reject']:
        flask.abort(404)

    user = fmn.lib.models.User.by_openid(SESSION, openid)
    if not user or user.api_key != api_key:
        raise APIError(403, dict(reason="Invalid login"))

    confirmation = fmn.lib.models.Confirmation.by_secret(SESSION, secret)

    if not confirmation:
        flask.abort(404)

    if action == 'accept':
        confirmation.set_status(SESSION, 'accepted')
    else:
        confirmation.set_status(SESSION, 'rejected')

    return {"status": "ok"}

@app.route('/home')
@app.route('/home/')
@login_required
def profile_redirect():
    # Simply redirect a user to their profile
    return flask.redirect(flask.url_for('profile', openid=flask.g.auth.openid))


@app.route('/<not_reserved:openid>')
@app.route('/<not_reserved:openid>/')
@login_required
def profile(openid):

    if (not flask.g.auth.logged_in or (
        flask.g.auth.openid != openid and
            not admin(flask.g.auth.openid))):

        flask.abort(403)

    user = fmn.lib.models.User.get_or_create(
        SESSION,
        openid=flask.g.auth.openid,
        openid_url=flask.g.auth.openid_url,
    )
    avatar = libravatar.libravatar_url(
        openid=user.openid_url,
        https=app.config.get('FMN_SSL', False),
        size=140)

    prefs = fmn.lib.models.Preference.by_user(SESSION, openid)

    icons = {}
    for context in fmn.lib.models.Context.all(SESSION):
        icons[context.name] = context.icon

    return flask.render_template(
        'profile.html',
        current='profile',
        avatar=avatar,
        prefs=prefs,
        icons=icons,
        api_key=user.api_key,
        fedora_mobile=flask.request.args.get('fedora_mobile') == 'true',
        openid_url=flask.g.auth.openid)


@app.route('/reset-api-key')
@app.route('/reset-api-key/')
@login_required
def reset_api_key():
    if not flask.g.auth.logged_in:
        flask.abort(403)

    user = fmn.lib.models.User.get_or_create(
        SESSION,
        openid=flask.g.auth.openid,
        openid_url=flask.g.auth.openid_url,
    )

    user.reset_api_key(SESSION)
    return flask.redirect(flask.url_for('profile', openid=flask.g.auth.openid))


@app.route('/api/<openid>/<context>')
@app.route('/api/<openid>/<context>/')
@login_required
def context_json(openid, context):
    context, pref = _get_context(openid, context)

    pref = pref.__json__()

    # Stuff nice extra info in there for human readability
    for filter in pref['filters']:
        for rule in filter['rules']:
            prefix, key = rule['code_path'].split(':', 1)
            rule['info'] = copy.copy(valid_paths[prefix][key])
            del rule['info']['func']

    return flask.jsonify(pref)


@app.route('/<not_reserved:openid>/<context>')
@app.route('/<not_reserved:openid>/<context>/')
@login_required
def context(openid, context):
    context, pref = _get_context(openid, context)
    return flask.render_template(
        'context.html',
        current=context.name,
        context=context,
        confirmation=context.get_confirmation(openid),
        preference=pref)


def _get_context(openid, context):
    if flask.g.auth.openid != openid and not admin(flask.g.auth.openid):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    if context.name not in fedmsg_config['fmn.backends']:
        # TODO - is there a better status code for this?  More like
        # "temporariliy unavailable" or "under construction"
        flask.abort(404)

    pref = fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=context)

    return context, pref


@app.route('/api/<openid>/<context>/<int:filter_id>')
@app.route('/api/<openid>/<context>/<int:filter_id>/')
@login_required
def filter_json(openid, context, filter_id):
    filter = _get_filter(openid, context, filter_id).__json__()

    # Stuff nice extra info in there for human readability
    for rule in filter['rules']:
        prefix, key = rule['code_path'].split(':', 1)
        rule['info'] = copy.copy(valid_paths[prefix][key])
        del rule['info']['func']

    return flask.jsonify(filter)


@app.route('/<not_reserved:openid>/<context>/<int:filter_id>')
@app.route('/<not_reserved:openid>/<context>/<int:filter_id>/')
@login_required
def filter(openid, context, filter_id):
    filter = _get_filter(openid, context, filter_id)
    return flask.render_template(
        'filter.html',
        current=context,
        filter=filter)


def _get_filter(openid, context, filter_id):
    if flask.g.auth.openid != openid and not admin(flask.g.auth.openid):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    pref = fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=context)

    if not pref.has_filter(SESSION, filter_id):
        flask.abort(404)

    filter = pref.get_filter(SESSION, filter_id)
    return filter


@app.route('/<not_reserved:openid>/<context>/<int:filter_id>/ex/<int:page>')
@app.route('/<not_reserved:openid>/<context>/<int:filter_id>/ex/<int:page>')
@api_method
@login_required
def example_messages(openid, context, filter_id, page):
    if flask.g.auth.openid != openid and not admin(flask.g.auth.openid):
        flask.abort(403)

    context = fmn.lib.models.Context.by_name(SESSION, context)
    if not context:
        flask.abort(404)

    pref = fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=context)

    if not pref.has_filter(SESSION, filter_id):
        flask.abort(404)

    filter = pref.get_filter(SESSION, filter_id)

    hinting = fmn.lib.hinting.gather_hinting(filter, valid_paths)

    # Now, connect to datanommer and get the latest bazillion messages
    # (adjusting by any hinting the rules we're evalulating might provide).
    bazillion = 400
    try:
        total, pages, messages = datanommer.models.Message.grep(
            start=datetime.datetime.fromtimestamp(1),
            end=datetime.datetime.now(),
            rows_per_page=bazillion,
            page=page,
            order='desc',
            **hinting
        )
    except Exception as e:
        log.exception(e)
        raise APIError(500, dict(
            reason="Error talking to datanommer",
            furthermore=str(e),
        ))

    def _make_result(msg, d):
        """ Little utility used inside the loop below """
        return {
            'icon': fedmsg.meta.msg2icon(d, **fedmsg_config),
            'icon2': fedmsg.meta.msg2secondary_icon(d, **fedmsg_config),
            'subtitle': fedmsg.meta.msg2subtitle(d, **fedmsg_config),
            'link': fedmsg.meta.msg2link(d, **fedmsg_config),
            'time': arrow.get(msg.timestamp).humanize(),
        }

    # Mock out a fake 'cached preferences' object like we have in the consumer,
    # but really it just consists of the one preferences and its *one* filter
    # for which we're trying to find example messages.
    preferences = [pref.__json__()]
    preferences[0]['detail_values'] = ['mock']
    preferences[0]['filters'] = [filter.__json__(reify=True)]

    results = []
    for message in messages:
        original = message.__json__()
        recips = fmn.lib.recipients(
            preferences, message.__json__(), valid_paths, fedmsg_config)
        if recips:
            results.append(_make_result(message, original))

    next_page = page + 1
    if page > pages:
        next_page = None
    return dict(
        results=results,
        next_page=next_page,
    )


@app.route('/confirm/<action>/<secret>')
@app.route('/confirm/<action>/<secret>/')
@login_required
def handle_confirmation(action, secret):

    if action not in ['accept', 'reject']:
        flask.abort(404)

    confirmation = fmn.lib.models.Confirmation.by_secret(SESSION, secret)

    if not confirmation:
        flask.abort(404)

    if flask.g.auth.openid != confirmation.openid:
        flask.abort(403)

    if action == 'accept':
        confirmation.set_status(SESSION, 'accepted')
    else:
        confirmation.set_status(SESSION, 'rejected')

    return flask.redirect(flask.url_for(
        'context',
        openid=confirmation.openid,
        context=confirmation.context_name))


@app.route('/api/filter', methods=['POST', 'DELETE'])
@api_method
def handle_filter():
    form = fmn.web.forms.FilterForm(flask.request.form)

    if not form.validate():
        raise APIError(400, form.errors)

    openid = form.openid.data
    context = form.context.data
    filter_name = form.filter_name.data
    method = (form.method.data or flask.request.method).upper()

    if flask.g.auth.openid != openid and not admin(flask.g.auth.openid):
        raise APIError(403, dict(reason="%r is not %r" % (
            flask.g.auth.openid, openid
        )))
    if method not in ['POST', 'DISABLE', 'ENABLE', 'DELETE']:
        raise APIError(405, dict(reason="Only POST, ENABLE, DISABLE, and DELETE accepted"))

    user = fmn.lib.models.User.by_openid(SESSION, openid)
    if not user:
        raise APIError(403, dict(reason="%r is not a user" % openid))

    ctx = fmn.lib.models.Context.by_name(SESSION, context)
    if not ctx:
        raise APIError(403, dict(reason="%r is not a context" % context))

    pref = fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=ctx)

    try:
        if method == 'POST':
            # Ensure that a filter with this name doesn't already exist.
            if pref.has_filter_name(SESSION, filter_name):
                raise APIError(404, dict(
                    reason="%r already exists" % filter_name))

            filter = fmn.lib.models.Filter.create(SESSION, filter_name)
            pref.add_filter(SESSION, filter)
            next_url = flask.url_for(
                'filter',
                openid=openid,
                context=context,
                filter_id=filter.id,
            )
        elif method == 'DISABLE':
            pref.set_filter_active(SESSION, filter_name, False)
            next_url = flask.url_for(
                'context',
                openid=openid,
                context=context,
            )
        elif method == 'ENABLE':
            pref.set_filter_active(SESSION, filter_name, True)
            next_url = flask.url_for(
                'context',
                openid=openid,
                context=context,
            )
        elif method == 'DELETE':
            pref.delete_filter(SESSION, filter_name)
            next_url = flask.url_for(
                'context',
                openid=openid,
                context=context,
            )
        else:
            raise NotImplementedError("This is impossible.")
    except (ValueError, KeyError) as e:
        app.logger.exception(e)
        raise APIError(403, dict(reason=str(e)))

    return dict(message="ok", url=next_url)


def int_or_none(value):
    """ Cast form fields to integers ourselves.

    form.validate() could potentially do this for us, but I don't know how to
    make an IntegerField also accept None.
    """
    if value == "<disabled>":
        return None

    try:
        return int(value)
    except TypeError:
        raise APIError(400, dict(batch_delta=["Not a valid integer value"]))


@app.route('/api/details', methods=['POST'])
@api_method
def handle_details():
    form = fmn.web.forms.DetailsForm(flask.request.form)

    if not form.validate():
        raise APIError(400, form.errors)

    openid = form.openid.data
    context = form.context.data
    detail_value = form.detail_value.data
    batch_delta = form.batch_delta.data
    batch_count = form.batch_count.data
    toggle_enable = form.toggle_enable.data
    toggle_triggered_by = form.toggle_triggered_by.data
    toggle_shorten = form.toggle_shorten.data
    toggle_markup = form.toggle_markup.data
    next_url = form.next_url.data
    reset_to_defaults = form.reset_to_defaults.data

    if flask.g.auth.openid != openid and not admin(flask.g.auth.openid):
        raise APIError(403, dict(reason="%r is not %r" % (
            flask.g.auth.openid, openid
        )))

    user = fmn.lib.models.User.by_openid(SESSION, openid)
    if not user:
        raise APIError(403, dict(reason="%r is not a user" % openid))

    ctx = fmn.lib.models.Context.by_name(SESSION, context)
    if not ctx:
        raise APIError(403, dict(reason="%r is not a context" % context))

    pref = fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=ctx)

    # Check to see if they pressed a delete button.
    delete_value = flask.request.form.get('delete', None)

    # Are they deleting a delivery detail?
    if delete_value:
        # Primarily, delete the value from this user
        if delete_value in [value.value for value in pref.detail_values]:
            pref.delete_details(SESSION, delete_value)

        # Also, if they have a confirmation hanging around, delete that too.
        # XXX - Make sure that they cannot delete someone ELSE's confirmation.
        confirmations = fmn.lib.models.Confirmation.by_detail(
            SESSION, ctx, delete_value)
        for confirmation in confirmations:
            if confirmation.user == user:
                user.confirmations.remove(confirmation)
                SESSION.delete(confirmation)
                SESSION.flush()

        # Finalize all of that.
        SESSION.commit()

    # Are they changing a delivery detail?
    if detail_value:
        # Do some validation on the specifics of the value before we commit.
        try:
            fmn.lib.validate_detail_value(ctx, detail_value)
        except Exception as e:
            raise APIError(403, dict(reason=str(e)))

        # Make sure no one else has this one in play yet
        if fmn.lib.models.DetailValue.exists(SESSION, detail_value):
            raise APIError(403, dict(reason="That value is already claimed."))

        # We need to *VERIFY* that they really have this delivery detail
        # before we start doing stuff.  Otherwise, ralph could put in pingou's
        # email address and spam the crap out of him.
        con = fmn.lib.models.Confirmation.get_or_create(
            SESSION, openid=openid, context=ctx)
        con.set_value(SESSION, detail_value)
        con.set_status(SESSION, 'pending')

    # Let them change batch_delta and batch_count as they please.
    if batch_delta or batch_count:
        batch_delta = int_or_none(batch_delta)
        batch_count = int_or_none(batch_count)
        pref.set_batch_values(SESSION, delta=batch_delta, count=batch_count)

    # Also, let them enable or disable as they please.
    if toggle_enable:
        pref.set_enabled(SESSION, not pref.enabled)

    if toggle_triggered_by:
        pref.set_triggered_by_links(SESSION, not pref.triggered_by_links)

    if toggle_shorten:
        pref.set_shorten_links(SESSION, not pref.shorten_links)

    if toggle_markup:
        pref.set_markup_messages(SESSION, not pref.markup_messages)

    if reset_to_defaults:
        for flt in pref.filters:
            SESSION.delete(flt)
        SESSION.flush()
        fmn.lib.defaults.create_defaults_for(SESSION, user, pref.context)

    next_url = next_url or flask.url_for(
        'context',
        openid=openid,
        context=context,
    )

    return dict(message="ok", url=next_url)


@app.route('/api/rule', methods=['POST'])
@api_method
def handle_rule():
    form = fmn.web.forms.RuleForm(flask.request.form)

    if not form.validate():
        raise APIError(400, form.errors)

    openid = form.openid.data
    context = form.context.data
    filter_id = form.filter_id.data
    code_path = form.rule_name.data
    method = (form.method.data or flask.request.method).upper()
    # Extract arguments to rules using the extra information provided
    known_args = ['openid', 'filter_id', 'context', 'rule_name']
    arguments = {}
    for args in flask.request.form:
        if args not in known_args:
            arguments[args] = flask.request.form[args]

    if flask.g.auth.openid != openid and not admin(flask.g.auth.openid):
        raise APIError(403, dict(reason="%r is not %r" % (
            flask.g.auth.openid, openid
        )))

    if method not in ['POST', 'DELETE', 'NEGATE']:
        raise APIError(405, dict(
            reason="Only POST, NEGATE and DELETE accepted"))

    user = fmn.lib.models.User.by_openid(SESSION, openid)
    if not user:
        raise APIError(403, dict(reason="%r is not a user" % openid))

    ctx = fmn.lib.models.Context.by_name(SESSION, context)
    if not ctx:
        raise APIError(403, dict(reason="%r is not a context" % context))

    pref = fmn.lib.models.Preference.get_or_create(
        SESSION, openid=openid, context=ctx)

    if not pref.has_filter(SESSION, filter_id):
        raise APIError(403, dict(reason="%r is not a filter" % filter_id))

    filter = pref.get_filter(SESSION, filter_id)

    try:
        if method == 'POST':
            filter.add_rule(SESSION, valid_paths, code_path, **arguments)
        elif method == 'NEGATE':
            filter.negate_rule(SESSION, code_path)
        elif method == 'DELETE':
            filter.remove_rule(SESSION, code_path)  # , **arguments)
        else:
            raise NotImplementedError("This is impossible.")
    except (ValueError, KeyError) as e:
        app.logger.exception(e)
        raise APIError(403, dict(reason=str(e)))

    next_url = flask.url_for(
        'filter',
        openid=openid,
        context=context,
        filter_id=filter_id,
    )

    return dict(message="ok", url=next_url)


@app.route('/login/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
@oid.loginhandler
def login():
    default = flask.url_for('index')
    next_url = flask.request.args.get('next', default)
    if flask.g.auth.logged_in:
        return flask.redirect(next_url)

    openid_server = flask.request.form.get('openid', None)
    if openid_server:
        return oid.try_login(
            openid_server, ask_for=['email', 'fullname', 'nickname'],
            ask_for_optional=[])

    return flask.render_template(
        'login.html', next=oid.get_next_url(), error=oid.fetch_error())


@app.route('/login/fedora/')
@app.route('/login/fedora')
@oid.loginhandler
def fedora_login():
    default = flask.url_for('profile_redirect')
    next_url = flask.request.args.get('next', default)
    return oid.try_login(
        app.config['FMN_FEDORA_OPENID'],
        ask_for=['email', 'fullname', 'nickname'],
        ask_for_optional=[])

@app.route('/login/google/')
@app.route('/login/google')
@oid.loginhandler
def google_login():
    default = flask.url_for('index')
    next_url = flask.request.args.get('next', default)
    return oid.try_login(
        "https://www.google.com/accounts/o8/id",
        ask_for=['email', 'fullname'],
        ask_for_optional=[])

@app.route('/login/yahoo/')
@app.route('/login/yahoo')
@oid.loginhandler
def yahoo_login():
    default = flask.url_for('index')
    next_url = flask.request.args.get('next', default)
    return oid.try_login(
        "https://me.yahoo.com/",
        ask_for=['email', 'fullname'],
        ask_for_optional=[])


@app.route('/logout/')
@app.route('/logout')
def logout():
    if 'openid' in flask.session:
        flask.session.pop('openid')
    return flask.redirect(flask.url_for('index'))


def modify_rst(rst):
    """ Downgrade some of our rst directives if docutils is too old. """

    try:
        # The rst features we need were introduced in this version
        minimum = [0, 9]
        version = map(int, docutils.__version__.split('.'))

        # If we're at or later than that version, no need to downgrade
        if version >= minimum:
            return rst
    except Exception:
        # If there was some error parsing or comparing versions, run the
        # substitutions just to be safe.
        pass

    # Otherwise, make code-blocks into just literal blocks.
    substitutions = {
        '.. code-block:: javascript': '::',
    }
    for old, new in substitutions.items():
        rst = rst.replace(old, new)

    return rst


def modify_html(html):
    """ Perform style substitutions where docutils doesn't do what we want.
    """

    substitutions = {
        '<tt class="docutils literal">': '<code>',
        '</tt>': '</code>',
    }
    for old, new in substitutions.items():
        html = html.replace(old, new)

    return html


def preload_docs(endpoint):
    """ Utility to load an RST file and turn it into fancy HTML. """

    here = os.path.dirname(os.path.abspath(__file__))
    fname = os.path.join(here, 'docs', endpoint + '.rst')
    with codecs.open(fname, 'r', 'utf-8') as f:
        rst = f.read()

    rst = modify_rst(rst)
    api_docs = docutils.examples.html_body(rst)
    api_docs = modify_html(api_docs)
    api_docs = markupsafe.Markup(api_docs)
    return api_docs

htmldocs = dict.fromkeys(['about'])
for key in htmldocs:
    htmldocs[key] = preload_docs(key)


def load_docs(request):
    URL = fedmsg_config.get('fmn.base_url', request.url_root)
    docs = htmldocs[request.endpoint]
    docs = jinja2.Template(docs).render(URL=URL)
    return markupsafe.Markup(docs)
