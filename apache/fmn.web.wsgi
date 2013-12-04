#-*- coding: utf-8 -*-

# The three lines below are required to run on EL6 as EL6 has
# two possible version of python-sqlalchemy and python-jinja2
# These lines make sure the application uses the correct version.
import __main__
__main__.__requires__ = ['SQLAlchemy >= 0.7', 'jinja2 >= 2.4']
import pkg_resources

# The most import line to make the wsgi working
from fmn.web.app import app as application
# Dangerous.. only use when testing.
#application.debug = True
