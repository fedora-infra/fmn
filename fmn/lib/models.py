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
import functools
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

import fedmsg.utils

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
        return session.query(cls).filter_by(name=name).first()

    get = by_name

    @classmethod
    def by_user(cls, session, username):
        return session.query(
            cls
        ).join(
            Preference,
            User
        ).filter(
            User.username == username
        ).all()

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

    def _recipients(self, session, config, message):
        """ Returns the list of recipients for a message. """
        for user in User.all(session):
            preference = Preference.load(session, user, self)
            if preference and preference.prefers(session, config, message):
                result = dict(user=user.username)
                result.update(preference.delivery_detail)
                yield result

    def recipients(self, session, config, message):
        return list(self._recipients(session, config, message))


class User(BASE):
    __tablename__ = 'users'

    username = sa.Column(sa.String(50), primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()

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


class Filter(BASE):
    __tablename__ = 'filters'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    chain_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('chains.id'))
    chain = relation('Chain', backref=('filters'))

    # This is something of the form 'fmn.filters:some_function'
    # We need to do major validation to make sure only *our* code_paths
    # make it in the database.
    code_path = sa.Column(sa.String(50), nullable=False)
    # JSON-encoded kw
    _arguments = sa.Column(sa.String(256))

    @hybrid_property
    def arguments(self):
        return json.loads(self._arguments)

    @arguments.setter
    def arguments(self, kw):
        if not kw is None:
            self._arguments = json.dumps(kw)

    def _instantiate_callable(self):
        # This is a bit of a misnomer, load_class can load anything.
        fn = fedmsg.utils.load_class(self.code_path)
        # Now, partially apply our keyword arguments.
        fn = functools.partial(fn, **self.arguments)
        return fn

    @staticmethod
    def validate_code_path(config, code_path, **kw):
        """ Raise an exception if code_path is not one of our
        whitelisted code_paths in the fedmsg config.
        """

        if code_path not in config['fmn.valid_code_paths']:
            raise ValueError("%r is not a valid code_path" % code_path)

    @classmethod
    def create_from_code_path(cls, session, config, code_path, **kw):

        # This will raise an exception if invalid
        Filter.validate_code_path(config, code_path, **kw)

        filt = cls(code_path=code_path)
        filt.arguments = kw

        session.add(filt)
        session.flush()
        session.commit()
        return filt

    def execute(self, session, config, message):
        """ Load our callable and execute it.

        Note, we validate the code_path again here for the second time.  Once
        before it is inserted into the db, and once again before we execute it.
        This is mitigation in case other code is vulnerable to injecting
        arbitrary data into the db.
        """

        Filter.validate_code_path(config, self.code_path, **self.arguments)

        fn = self._instantiate_callable()
        try:
            return fn(config, message)
        except Exception as e:
            log.warning(
                "filter %r(config=%r, message=%r, **kw=%r) raised %r" % (
                    self.code_path, config, message, self.arguments, e))
            return False


class Chain(BASE):
    __tablename__ = 'chains'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    name = sa.Column(sa.String(50))

    preference_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('preferences.id'))
    preference = relation('Preference', backref=backref('chains'))

    @classmethod
    def create(cls, session, name):
        chain = cls(name=name)
        session.add(chain)
        session.flush()
        session.commit()
        return chain

    def add_filter(self, session, config, filt, **kw):
        if isinstance(filt, basestring):
            filt = Filter.create_from_code_path(session, config, filt, **kw)
        elif kw:
            raise ValueError("Cannot handle filter with non-empty kw")

        self.filters.append(filt)
        return filt

    def matches(self, session, config, message):
        """ Return true if this chain matches the given message.

        This is the case if *all* of the associated filters match.

        ...with one exception.  If no filters are defined, the chain does not
        match (even though technically, all of its zero filters match).
        """

        if not self.filters:
            return False

        for filt in self.filters:
            if not filt.execute(session, config, message):
                return False

        return True


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
        if not isinstance(user, User):
            user = User.by_username(session, user)
        if not isinstance(context, Context):
            context = Context.by_name(session, context)
        pref = cls()
        pref.user = user
        pref.context = context
        pref.delivery_detail = delivery_detail
        session.add(pref)
        session.flush()
        return pref

    @classmethod
    def get_or_create(cls, session, user, context):
        user = User.get_or_create(session, user)
        result = cls.load(session, user, context)

        if not result:
            cls.create(session, user, context, {})
            result = cls.load(session, user, context)

        return result

    @classmethod
    def load(cls, session, user, context):

        if hasattr(user, 'username'):
            user = user.username

        if hasattr(context, 'name'):
            context = context.name

        return session.query(cls)\
            .filter_by(user_name=user)\
            .filter_by(context_name=context)\
            .first()

    def add_chain(self, session, chain):
        self.chains.append(chain)
        session.flush()
        session.commit()

    def has_chain(self, session, chain_name):
        for chain in self.chains:
            if chain.name == chain_name:
                return True

        return False

    def get_chain(self, session, chain_name):
        for chain in self.chains:
            if chain.name == chain_name:
                return chain

        raise ValueError("No such chain %r" % chain_name)

    def prefers(self, session, config, message):
        """ Return true or not if this preference "prefers" this message.

        That is the case if *any* of the associated chains match.
        """

        for chain in self.chains:
            if chain.matches(session, config, message):
                return True

        return False
