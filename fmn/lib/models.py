# -*- coding: utf-8 -*-
#
# Copyright © 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU Lesser General Public License (LGPL) version 2, or
# (at your option) any later version.  This program is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY expressed or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
# more details.  You should have received a copy of the GNU Lesser General
# Public License along with this program; if not, write to the Free
# Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

"""
Mapping of python classes to Database Tables.
"""

import datetime
import hashlib
import json
import logging
import uuid

import six

import sqlalchemy as sa
from dogpile.cache import make_region
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, scoped_session, backref, relation

import fedmsg
import fedmsg.utils

import fmn.lib.defaults

_config = fedmsg.config.load_config()

#: The SQLAlchemy database engine, initialized with the URL in the fedmsg config key
#: ``fmn.sqlalchemy.uri`` and ``fmn.sqlalchemy.debug`` (bool). If the debug setting is
#: true, SQLAlchemy will log all the raw SQL statements it generates.
engine = create_engine(
    _config.get('fmn.sqlalchemy.uri'), echo=_config.get('fmn.sqlalchemy.debug', False))

#: An SQLAlchemy scoped session. This session can be optionally called to return
#: the thread-local session or used directly (in which case it creates or uses the
#: existing thread-local session). Call ``Session.remove()`` to remove the session
#: once you are done with it. A new one will be created on next use.
Session = scoped_session(sessionmaker(bind=engine))


class FMNBase(object):
    """
    Base class for the SQLAlchemy model base class.

    Attributes:
        query (sqlalchemy.orm.query.Query): a class property which produces a
            Query object against the class and the current Session when called.
    """

    query = Session.query_property()

    def notify(self, openid, context, changed):
        obj = type(self).__name__.lower()
        topic = obj + ".update"
        fedmsg.publish(
            topic=topic,
            msg=dict(
                openid=openid,
                context=context,
                changed=changed,
            )
        )


BASE = declarative_base(cls=FMNBase)

log = logging.getLogger(__name__)


def init(db_url, alembic_ini=None, debug=False, create=False):
    """ Create the tables in the database using the information from the
    url obtained.

    .. deprecated:: 1.2.0
       Use the session created in this module and the fmn-createdb script instead

    Args:
        db_url (str): URL used to connect to the database. The URL contains
            information with regards to the database engine, the host to
            connect to, the user and password and the database name.
            ie: <engine>://<user>:<password>@<host>/<dbname>
        alembic_ini (str): path to the alembic ini file. This is necessary
            to be able to use alembic correctly, but not for the unit-tests.
        debug (bool): a boolean specifying wether we should have the verbose
            output of sqlalchemy or not.

    Returns:
        scopedsession: An SQLAlchemy scoped session.
    """
    if create:
        BASE.metadata.create_all(engine)

    if alembic_ini is not None:  # pragma: no cover
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")

    # Return the scoped session created in the db module for code still using
    # this funciton
    return Session


class Context(BASE):
    __tablename__ = 'contexts'
    name = sa.Column(sa.String(50), primary_key=True)
    description = sa.Column(sa.String(1024), unique=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    detail_name = sa.Column(sa.String(64), nullable=False)
    icon = sa.Column(sa.String(32), nullable=False)
    placeholder = sa.Column(sa.String(256))

    def __json__(self, reify=False):
        return {
            'name': self.name,
            'detail_name': self.detail_name,
            'description': self.description,
            'created_on': self.created_on,
            'icon': self.icon,
            'placeholder': self.placeholder,
        }

    def get_confirmation(self, openid):
        for confirmation in self.confirmations:
            if confirmation.openid == openid:
                return confirmation

        return None

    @classmethod
    def by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).first()

    get = by_name

    @classmethod
    def by_user(cls, session, openid):
        return session.query(
            cls
        ).join(
            Preference,
            User
        ).filter(
            User.openid == openid
        ).all()

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def create(cls, session, name, description,
               detail_name, icon, placeholder=None):

        context = cls(name=name, description=description,
                      detail_name=detail_name, icon=icon,
                      placeholder=placeholder)
        session.add(context)
        session.flush()
        session.commit()
        return context


class User(BASE):
    __tablename__ = 'users'

    openid = sa.Column(sa.Text, primary_key=True)
    openid_url = sa.Column(sa.Text, unique=True)
    # doesn't have to be unique, because we'll require the openid url, too.
    api_key = sa.Column(sa.Text)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    def __json__(self, reify=False):
        return {
            'openid': self.openid,
            'openid_url': self.openid_url,
            'created_on': self.created_on,
        }

    def __repr__(self):
        return "<fmn.lib.models.User: %r %r>" % (self.openid, self.openid_url)

    @classmethod
    def by_openid(cls, session, openid):
        return session.query(cls).filter_by(openid=openid).first()

    get = by_openid

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    def reset_api_key(self, session):
        self.api_key = str(uuid.uuid4())
        session.flush()
        session.commit()

    @classmethod
    def get_or_create(cls, session, openid, openid_url,
                      create_defaults=True, detail_values=None):
        user = cls.by_openid(session, openid)
        if not user:
            user = cls.create(session, openid, openid_url,
                              create_defaults, detail_values)
        return user

    @classmethod
    def create(cls, session, openid, openid_url,
               create_defaults, detail_values=None):
        user = cls(
            openid=openid,
            openid_url=openid_url,
            api_key=str(uuid.uuid4()),
        )
        session.add(user)
        session.flush()

        if create_defaults:
            fmn.lib.defaults.create_defaults_for(
                session, user, detail_values=detail_values)

        return user


#: A dictionary-backed cache that maps Python paths to the objects
#: themselves. Although this cache is never expired, that's not problematic
#: since the total number of rules is on the order of a few hundred.
_rule_class_cache = make_region().configure('dogpile.cache.memory')


@_rule_class_cache.cache_on_arguments()
def _cached_load_class(load_path):
    """
    Wrap the expensive fedmsg load_class utility to cache results.

    This is a short-term work-around to the problem of slow initial preference
    loading. When a preference is loaded, all its filters are fetched and the
    rules are converted to dictionaries via ``__json__``. This triggers the
    ``code_path`` string to be loaded via ``__import__`` repeatedly for every
    rule. A new rule row is added for every rule in every preference for every
    user.

    The longer-term work-around is probably to adjust the database models and
    rule-loading design so this is not a problem, but that is a significant
    amount of work.

    Args:
        rule_path (str): A string that maps to a Python class to import. For
            example, "fmn.lib.models:Rule".

    Return:
        object: The class pointed to by ``rule_path``.
    """
    return fedmsg.utils.load_class(load_path)


class Rule(BASE):
    __tablename__ = 'rules'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    filter_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('filters.id'))
    filter = relation(
        'Filter', backref=backref('rules', order_by=('Rule.created_on')))

    # This is something of the form 'fmn.rules:some_function'
    # We need to do major validation to make sure only *our* code_paths
    # make it in the database.
    code_path = sa.Column(sa.String(100), nullable=False)
    # JSON-encoded kw
    _arguments = sa.Column(sa.String(256))
    # Should we negate the output of the computed rule?
    negated = sa.Column(sa.Boolean, default=False)

    def __json__(self, reify=False):
        result = {
            'created_on': self.created_on,
            'code_path': self.code_path,
            'arguments': self.arguments,
            'cache_key': self.cache_key,
            'negated': self.negated,
        }
        if reify:
            result['fn'] = _cached_load_class(str(self.code_path))
        return result

    def __repr__(self):
        negation = self.negated and '!' or ''
        return "<fmn.lib.models.Rule: %s%r(**%r)>" % (
            negation, self.code_path, self.arguments)

    @property
    def cache_key(self):
        return hashlib.sha256((
            self.code_path + six.text_type(self.negated) + self._arguments
        ).encode('utf-8')).hexdigest()

    @hybrid_property
    def arguments(self):
        return json.loads(self._arguments)

    @arguments.setter
    def arguments(self, kw):
        if not kw is None:
            self._arguments = json.dumps(kw)

    @staticmethod
    def validate_code_path(valid_paths, code_path, **kw):
        """ Raise an exception if code_path is not one of our
        whitelisted valid_paths.
        """

        root, name = code_path.split(':', 1)
        if name not in valid_paths[root]:
            raise ValueError("%r is not a valid code_path" % code_path)

    @classmethod
    def create_from_code_path(cls, session, valid_paths, code_path,
                              negated=False, **kw):

        # This will raise an exception if invalid
        Rule.validate_code_path(valid_paths, code_path, **kw)

        rule = cls(code_path=code_path, negated=negated)
        rule.arguments = kw

        session.add(rule)
        session.flush()
        session.commit()
        return rule

    def set_argument(self, session, key, value):
        args = self.arguments
        args[key] = value
        self.arguments = args
        session.flush()
        session.commit()
        self.notify(
            self.filter.preference.openid,
            self.filter.preference.context.name,
            "filters")

    def title(self, valid_paths):
        root, name = self.code_path.split(':', 1)
        return valid_paths[root][name]['title']

    def doc(self, valid_paths, no_links=False):
        root, name = self.code_path.split(':', 1)
        if no_links:
            return valid_paths[root][name]['doc-no-links']
        else:
            return valid_paths[root][name]['doc']


class Filter(BASE):
    __tablename__ = 'filters'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    name = sa.Column(sa.String(50))
    active = sa.Column(sa.Boolean, default=True, nullable=False)
    oneshot = sa.Column(sa.Boolean, default=False, nullable=False)

    preference_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('preferences.id'))
    preference = relation('Preference', backref=backref('filters'))

    def __json__(self, reify=False):
        return {
            'id': self.id,
            'name': self.name,
            'created_on': self.created_on,
            'rules': [r.__json__(reify=reify) for r in self.rules],
            'oneshot': self.oneshot
        }

    def __repr__(self):
        return "<fmn.lib.models.Filter: %r>" % (self.name)

    @classmethod
    def create(cls, session, name):
        filter = cls(name=name)
        session.add(filter)
        session.flush()
        session.commit()
        return filter

    def fired(self, session):
        if self.oneshot:
            self.active = False
            session.flush()
            session.commit()

            pref = self.preference
            if pref:
                self.notify(pref.openid, pref.context_name, "filters")

    def get_rule(self, session, code_path, rule_id, **kw):
        for r in self.rules:
            if r.code_path == code_path and r.id == rule_id:
                return r
        raise ValueError("No such rule found: %r" % code_path)

    def has_rule(self, session, code_path, rule_id, **kw):
        for r in self.rules:
            if r.code_path == code_path and r.id == rule_id:
                return True
        return False

    def add_rule(self, session, paths, rule, **kw):
        if isinstance(rule, six.string_types):
            rule = Rule.create_from_code_path(session, paths, rule, **kw)
        elif kw:
            raise ValueError("Cannot handle rule with non-empty kw")

        self.rules.append(rule)
        session.flush()
        session.commit()

        pref = self.preference
        if pref:
            self.notify(pref.openid, pref.context_name, "rules")

        return rule

    def remove_rule(self, session, code_path, rule_id, **kw):
        for r in self.rules:
            if r.code_path == code_path and r.id == rule_id:
                session.delete(r)
                session.commit()

                pref = self.preference
                if pref:
                    self.notify(pref.openid, pref.context_name, "rules")

                return

        raise ValueError("No such rule found: %r with id=%d"
                         % (code_path, rule_id))

    def negate_rule(self, session, code_path, rule_id, **kw):
        for r in self.rules:
            if r.code_path == code_path and r.id == rule_id:
                r.negated = not r.negated
                session.commit()

                pref = self.preference
                if pref:
                    self.notify(pref.openid, pref.context_name, "rules")

                return

        raise ValueError("No such rule found: %r with id=%d"
                         % (code_path, rule_id))


class DetailValue(BASE):
    __tablename__ = 'detail_values'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    value = sa.Column(sa.String(1024), unique=True)
    preference_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('preferences.id'))
    preference = relation('Preference', backref=backref('detail_values'))

    @classmethod
    def get(cls, session, value):
        return session.query(cls).filter(cls.value==value).first()

    @classmethod
    def create(cls, session, value):
        obj = cls()
        obj.value = value
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def exists(cls, session, value):
        return (
            session.query(cls).filter(
                cls.value == value).count() > 0 or
            session.query(Confirmation).filter(
                Confirmation.detail_value == value).count() > 0
        )


class Preference(BASE):
    __tablename__ = 'preferences'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    # Number of seconds that have elapsed since the earliest queued message
    # before we send a digest over whatever medium.
    batch_delta = sa.Column(sa.Integer, nullable=True)
    # Number of messages that are queued before we send a digest over whatever
    # medium.
    batch_count = sa.Column(sa.Integer, nullable=True)

    # Hold the state of start/stop commands to the irc bot and others.
    # Disabled by default so that we can provide robust default filters without
    # forcing new users into an opt-out situation.
    enabled = sa.Column(sa.Boolean, default=False, nullable=False)

    # Various presentation booleans
    markup_messages = sa.Column(sa.Boolean, default=False)
    triggered_by_links = sa.Column(sa.Boolean, default=True)
    shorten_links = sa.Column(sa.Boolean, default=False)
    verbose = sa.Column(sa.Boolean, default=True)

    openid = sa.Column(
        sa.Text,
        sa.ForeignKey('users.openid'),
        nullable=False)
    context_name = sa.Column(
        sa.String(50),
        sa.ForeignKey('contexts.name'),
        nullable=False)

    user = relation('User', backref=backref('preferences'))
    context = relation('Context', backref=backref('preferences'))

    __table_args__ = (
        sa.UniqueConstraint('openid', 'context_name'),
    )

    def __json__(self, reify=False):
        return {
            'created_on': self.created_on,
            'batch_delta': self.batch_delta,
            'batch_count': self.batch_count,
            'markup_messages': self.markup_messages,
            'triggered_by_links': self.triggered_by_links,
            'shorten_links': self.shorten_links,
            'verbose': self.verbose,
            'enabled': self.enabled,
            'context': self.context.__json__(reify=reify),
            'user': self.user.__json__(reify=reify),
            'filters': [
                f.__json__(reify=reify)
                for f in self.filters
                if f.active],
            'detail_values': [v.value for v in self.detail_values],
        }

    def __repr__(self):
        return "<fmn.lib.models.Preference: %r %r>" % (
            self.openid, self.context_name)

    @property
    def can_send(self):
        return self.enabled and (
            bool(self.detail_values) or
            self.context.detail_name == "None"
        )

    @property
    def should_batch(self):
        """ If the user has any batching preferences at all, then we should """
        return self.batch_delta is not None or self.batch_count is not None

    @classmethod
    def list_batching(cls, session):
        return session.query(cls)\
            .filter(sa.or_(
                cls.batch_delta != None,
                cls.batch_count != None,
            )).all()

    def set_batch_values(self, session, delta, count):
        self.batch_delta = delta
        self.batch_count = count
        session.add(self)
        session.commit()
        self.notify(self.openid, self.context_name, "batch_values")

    def set_markup_messages(self, session, value):
        self.markup_messages = value
        session.add(self)
        session.commit()
        self.notify(self.openid, self.context_name, "markup_messages")

    def set_triggered_by_links(self, session, value):
        self.triggered_by_links = value
        session.add(self)
        session.commit()
        self.notify(self.openid, self.context_name, "triggered_by_links")

    def set_shorten_links(self, session, value):
        self.shorten_links = value
        session.add(self)
        session.commit()
        self.notify(self.openid, self.context_name, "shorten_links")

    def set_verbose(self, session, value):
        self.verbose = value
        session.add(self)
        session.commit()
        self.notify(self.openid, self.context_name, "verbose")

    @classmethod
    def by_user(cls, session, openid):
        query = session.query(
            cls
        ).filter(
            cls.openid == openid
        ).order_by(
            cls.context_name
        )

        return query.all()

    @classmethod
    def by_detail(cls, session, detail_value):
        value = DetailValue.get(session, detail_value)
        if value:
            return value.preference
        else:
            return None

    @classmethod
    def create(cls, session, user, context, detail_value=None):
        if not isinstance(user, User):
            user = User.by_openid(session, user)
        if not isinstance(context, Context):
            context = Context.by_name(session, context)
        pref = cls()
        pref.user = user
        pref.context = context

        if detail_value:
            value = DetailValue.create(session, detail_value)
            pref.detail_values.append(value)
            pref.enabled = True
            session.add(value)

        session.add(pref)
        session.flush()
        return pref

    @classmethod
    def get_or_create(cls, session, openid, context):
        user = User.get(session, openid=openid)

        if not user:
            raise ValueError("No such user %r" % openid)

        result = cls.load(session, user, context)

        if not result:
            cls.create(session, user, context)
            result = cls.load(session, user, context)
            session.commit()

        return result

    @classmethod
    def load(cls, session, user, context):

        if hasattr(user, 'openid'):
            user = user.openid

        if hasattr(context, 'name'):
            context = context.name

        return session.query(cls)\
            .filter_by(openid=user)\
            .filter_by(context_name=context)\
            .first()

    def delete_details(self, session, detail_value):
        log.debug("Deleting %r from %r" % (detail_value, self))
        detail_value = detail_value.strip()
        value = DetailValue.get(session, detail_value)
        self.detail_values.remove(value)
        session.delete(value)
        session.flush()
        session.commit()
        self.notify(self.openid, self.context_name, "details")

    def update_details(self, session, detail_value):
        log.debug("Adding %r to %r" % (detail_value, self))
        detail_value = detail_value.strip()
        value = DetailValue.create(session, detail_value)
        self.detail_values.append(value)
        session.flush()
        session.commit()
        self.notify(self.openid, self.context_name, "details")

    def set_enabled(self, session, enabled):
        self.enabled = enabled
        session.flush()
        session.commit()
        self.notify(self.openid, self.context_name, "enabled")

    def delete_filter(self, session, filter_name):
        filter = self.get_filter_name(session, filter_name)
        session.delete(filter)
        session.commit()
        self.notify(self.openid, self.context_name, "filters")

    def add_filter(self, session, filter, notify=True):
        self.filters.append(filter)
        session.flush()
        session.commit()
        if notify:
            self.notify(self.openid, self.context_name, "filters")

    def set_filter_active(self, session, filter_name, active):
        filter = self.get_filter_name(session, filter_name)
        filter.active = active
        session.commit()
        self.notify(self.openid, self.context_name, "filters")

    def set_filter_oneshot(self, session, filter_name, oneshot):
        filter = self.get_filter_name(session, filter_name)
        filter.oneshot = oneshot
        session.commit()
        self.notify(self.openid, self.context_name, "filters")

    def has_filter_name(self, session, filter_name):
        for filter in self.filters:
            if filter.name == filter_name:
                return True

        return False

    def get_filter_name(self, session, filter_name):
        for filter in self.filters:
            if filter.name == filter_name:
                return filter

        raise ValueError("No such filter %r" % filter_name)

    def has_filter(self, session, filter_id):
        for filter in self.filters:
            if filter.id == filter_id:
                return True

        return False

    def get_filter(self, session, filter_id):
        for filter in self.filters:
            if filter.id == filter_id:
                return filter

        raise ValueError("No such filter %r" % filter_id)


def hash_producer(*args, **kwargs):
    """ Returns a random hash for a confirmation secret. """
    return hashlib.md5(six.text_type(uuid.uuid4()).encode('utf-8')).hexdigest()


class Confirmation(BASE):
    __tablename__ = 'confirmations'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    STATUSES = ['pending', 'valid', 'accepted', 'rejected', 'invalid']
    status = sa.Column(sa.String(16), default="pending")
    secret = sa.Column(sa.String(32), default=hash_producer)
    detail_value = sa.Column(sa.String(1024))

    openid = sa.Column(
        sa.Text,
        sa.ForeignKey('users.openid'),
        nullable=False)
    context_name = sa.Column(
        sa.String(50),
        sa.ForeignKey('contexts.name'),
        nullable=False)

    user = relation('User', backref=backref('confirmations'))
    context = relation('Context', backref=backref('confirmations'))

    __table_args__ = (
        sa.UniqueConstraint('openid', 'context_name'),
    )

    def __repr__(self):
        return "<fmn.lib.models.Confirmation: %r %r %r>" % (
            self.openid, self.context_name, self.status)

    @classmethod
    def create(cls, session, openid, context, detail_value=None):
        if not isinstance(openid, User):
            openid = User.by_openid(session, openid)
        if not isinstance(context, Context):
            context = Context.by_name(session, context)
        confirmation = cls()
        confirmation.user = openid
        confirmation.context = context

        confirmation.detail_value = detail_value

        session.add(confirmation)
        session.flush()
        return confirmation

    @classmethod
    def get_or_create(cls, session, openid, context):
        user = User.get(session, openid=openid)

        if not user:
            raise ValueError("No such user %r" % openid)

        result = cls.load(session, user, context)

        if not result:
            cls.create(session, openid, context)
            result = cls.load(session, user, context)
            session.commit()

        return result

    @classmethod
    def load(cls, session, user, context):

        if hasattr(user, 'openid'):
            user = user.openid

        if hasattr(context, 'name'):
            context = context.name

        return session.query(cls)\
            .filter_by(openid=user)\
            .filter_by(context_name=context)\
            .first()

    @classmethod
    def by_detail(cls, session, context, value):
        if hasattr(context, 'name'):
            context = context.name
        return session.query(cls)\
            .filter_by(context_name=context)\
            .filter_by(detail_value=value)\
            .all()

    @classmethod
    def by_secret(cls, session, secret):
        return session.query(cls).filter_by(secret=secret).first()

    @classmethod
    def list_pending(cls, session):
        return session.query(cls).filter_by(status='pending').all()

    @classmethod
    def delete_expired(cls, session):
        too_old = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        expired = session.query(cls).filter(cls.created_on < too_old).all()
        if expired:
            log.info("Deleting %i expired confirmations" % len(expired))
            for confirmation in expired:
                session.delete(confirmation)
            session.flush()
            session.commit()

    def set_value(self, session, value):
        self.detail_value = value
        session.flush()
        session.commit()
        self.notify(self.openid, self.context_name, "value")

    def set_status(self, session, status):
        assert status in self.STATUSES
        log.info("Setting %r status to %r" % (self, status))
        self.status = status

        # Propagate back to the Preference if everything is good.
        if self.status == 'accepted':
            pref = Preference.load(session, self.openid, self.context_name)
            pref.update_details(session, self.detail_value)

        session.flush()
        session.commit()
        self.notify(self.openid, self.context_name, "status")


class QueuedMessage(BASE):
    __tablename__ = 'queued_messages'
    id = sa.Column(sa.Integer, primary_key=True)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    _message = sa.Column(sa.Text, nullable=False)

    @hybrid_property
    def message(self):
        return fedmsg.encoding.loads(self._message)

    @message.setter
    def message(self, kw):
        if not kw is None:
            self._message = fedmsg.encoding.dumps(kw)

    openid = sa.Column(
        sa.Text,
        sa.ForeignKey('users.openid'),
        nullable=False)
    context_name = sa.Column(
        sa.String(50),
        sa.ForeignKey('contexts.name'),
        nullable=False)

    user = relation('User', backref=backref('queued_messages'))
    context = relation('Context', backref=backref('queued_messages'))

    @classmethod
    def enqueue(cls, session, user, context, message):
        if not isinstance(user, User):
            user = User.by_openid(session, openid=user)
        if not isinstance(context, Context):
            context = Context.by_name(session, context)
        queued_message = cls(
            openid=user.openid,
            context_name=context.name)
        queued_message.message = message
        session.add(queued_message)
        session.commit()
        return queued_message

    def dequeue(self, session):
        session.delete(self)
        session.flush()
        session.commit()

    @classmethod
    def earliest_for(cls, session, user, context):
        return session.query(cls)\
            .filter_by(openid=user.openid)\
            .filter_by(context_name=context.name)\
            .order_by(cls.created_on)\
            .first()

    @classmethod
    def list_for(cls, session, user, context):
        return session.query(cls)\
            .filter_by(openid=user.openid)\
            .filter_by(context_name=context.name)\
            .order_by(cls.created_on)\
            .all()

    @classmethod
    def count_for(cls, session, user, context):
        return session.query(cls)\
            .filter_by(openid=user.openid)\
            .filter_by(context_name=context.name)\
            .count()
