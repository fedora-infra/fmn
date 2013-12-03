# -*- coding: utf-8 -*-
""" The flask application """

## These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.7', 'jinja2 >= 2.4']
import pkg_resources

from fmn.web.app import app

if __name__ == '__main__':
    app.debug = True
    app.run()
