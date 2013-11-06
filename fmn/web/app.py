import os

import flask
from flask_fas_openid import FAS
from flask.ext.mako import MakoTemplates

import fmn.lib
import fmn.lib.models

# Create the application.
APP = flask.Flask(__name__)

# set up FAS
APP.config.from_object('fmn.web.default_config')
if 'FMN_WEB_CONFIG' in os.environ:  # pragma: no cover
    APP.config.from_envvar('FMN_WEB_CONFIG')

FAS = FAS(APP)
mako = MakoTemplates(APP)
SESSION = fmn.lib.models.init(APP.config['DB_URL'], debug=False, create=False)


@APP.teardown_request
def shutdown_session(exception=None):
    """ Remove the DB session at the end of each request. """
    SESSION.remove()


@APP.route('/')
def index():
    return "hello world"
