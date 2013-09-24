# -*- coding: utf-8 -*-
#
# Copyright © 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

"""
Mapping of python classes to Database Tables.
"""

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

import datetime
import logging
import json

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relation
from sqlalchemy.orm import backref

BASE = declarative_base()

log = logging.getLogger(__name__)


def init(db_url, alembic_ini=None, debug=False, create=False):
    """ Create the tables in the database using the information from the
    url obtained.

    :arg db_url, URL used to connect to the database. The URL contains
        information with regards to the database engine, the host to
        connect to, the user and password and the database name.
          ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg alembic_ini, path to the alembic ini file. This is necessary
        to be able to use alembic correctly, but not for the unit-tests.
    :kwarg debug, a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a session that can be used to query the database.

    """
    engine = create_engine(db_url, echo=debug)

    if create:
        BASE.metadata.create_all(engine)

    # This... "causes problems"
    #if db_url.startswith('sqlite:'):
    #    def _fk_pragma_on_connect(dbapi_con, con_record):
    #        dbapi_con.execute('pragma foreign_keys=ON')
    #    sa.event.listen(engine, 'connect', _fk_pragma_on_connect)

    if alembic_ini is not None:  # pragma: no cover
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


class Context(BASE):
    __tablename__ = 'contexts'
    name = sa.Column(sa.String(50), primary_key=True)
    description = sa.Column(sa.String(1024), primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_name(cls, session, name):
        query = session.query(cls).filter_by(name=name)
        if query.count():
            return query.first()
        else:
            return None

    get = by_name

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def create(cls, session, name, description):
        context = cls(name=name, description=description)
        session.add(context)
        session.flush()
        session.commit()
        return context

    def _recipients(self, session, message):
        """ Returns the list of recipients for a message. """
        for user in User.all(session):
            preference = Preference.load(session, user, self)
            if preference and preference.prefers(session, message):
                yield {user.username: preference.delivery_detail}

    def recipients(self, session, message):
        return list(self._recipients(session, message))


class User(BASE):
    __tablename__ = 'users'

    username = sa.Column(sa.String(50), primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_username(cls, session, username):
        query = session.query(cls).filter_by(username=username)
        if query.count():
            return query.first()
        else:
            return None

    get = by_username

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_or_create(cls, session, username):
        user = cls.by_username(session, username)
        if not user:
            user = cls(username=username)
            session.add(user)
            session.flush()
        return user


class Preference(BASE):
    __tablename__ = 'preferences'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    # This is the important piece, a JSON string.
    _delivery_detail = sa.Column(sa.String(1024))

    user_name = sa.Column(
        sa.String(50),
        sa.ForeignKey('users.username'),
        nullable=False)
    context_name = sa.Column(
        sa.String(50),
        sa.ForeignKey('contexts.name'),
        nullable=False)

    user = relation('User', backref=backref('preferences'))
    context = relation('Context', backref=backref('preferences'))

    __table_args__ = (
        sa.UniqueConstraint('user_name', 'context_name'),
    )

    @hybrid_property
    def delivery_detail(self):
        return json.loads(self._delivery_detail)

    @delivery_detail.setter
    def delivery_detail(self, delivery_detail):
        self._delivery_detail = json.dumps(delivery_detail)

    @classmethod
    def create(cls, session, user, context, delivery_detail):
        pref = cls()
        pref.user = user
        pref.context = context
        pref.delivery_detail = delivery_detail
        session.add(pref)
        session.flush()
        return pref

    @classmethod
    def load(cls, session, user, context):
        query = session.query(cls)\
            .filter_by(user_name=user.username)\
            .filter_by(context_name=context.name)
        count = query.count()
        if count == 0:
            return None
        else:
            return query.one()

    # TODO -- how to represent a preference?
    # A series of filters?  Of whitelists?
    def prefers(self, session, message):
        """ Return true or not if this preference "prefers" this message. """
        # TODO -- actually implement this.
        # for now, return True for every user in the db.
        return True
