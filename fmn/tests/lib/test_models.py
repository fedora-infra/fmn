# -*- coding: utf-8 -*-
#
# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""Unit tests for the :mod:`fmn.lib.models` module."""

import unittest

from sqlalchemy.orm.query import Query
import mock

from fmn.rules import user_package_filter
import fmn.lib.models
import fmn.tests


class TestFMNBase(unittest.TestCase):

    def test_scoped_session(self):
        """Assert the module creates a scoped session"""
        session1 = fmn.lib.models.Session()
        session2 = fmn.lib.models.Session()

        self.assertTrue(session1 is session2)

    @mock.patch('fmn.lib.models.fedmsg.publish')
    def test_base_has_notify(self, mock_publish):
        """Assert the model base class has a notify method"""
        fmn.lib.models.BASE.notify(fmn.lib.models.BASE(), 'jcline', 'email', 'change')
        mock_publish.assert_called_once_with(
            topic='base.update',
            msg={'openid': 'jcline', 'context': 'email', 'changed': 'change'},
        )

    def test_has_query_property(self):
        """Assert that models inheriting from the base class have a query propery"""
        pref = fmn.lib.models.Preference()
        self.assertTrue(isinstance(pref.query, Query))


class TestBasics(fmn.tests.Base):
    def test_setup_and_teardown(self):
        pass

    def test_user_get_or_create(self):
        user1 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        user2 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        user3 = fmn.lib.models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject",
            openid_url="http://toshio.id.fedoraproject.org/",
        )
        self.assertEqual(user1.openid, user2.openid)
        self.assertEqual(user1, user2)
        self.assertNotEqual(user1, user3)

    def test_context_create(self):
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user")
        context2 = fmn.lib.models.Context.get(self.sess, name="irc")
        context3 = fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone")
        self.assertEqual(context1, context2)
        self.assertNotEqual(context1, context3)

    def test_user_all(self):
        fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        fmn.lib.models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject",
            openid_url="http://toshio.id.fedoraproject.org/",
        )
        self.assertEqual(len(fmn.lib.models.User.all(self.sess)), 2)

    def test_context_all(self):
        fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user")
        fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone")
        self.assertEqual(len(fmn.lib.models.Context.all(self.sess)), 2)

    def test_filter_oneshot(self):
        filter = fmn.lib.models.Filter.create(self.sess, name="test filter")
        # looks like we need to access the object a first time when running the
        # tests in tox
        filter.oneshot
        filter.oneshot = True
        self.assertEqual(filter.active, True)
        self.assertEqual(filter.oneshot, True)
        filter.fired(self.sess)
        self.assertEqual(filter.active, False)

        filter = fmn.lib.models.Filter.create(self.sess, name="test filter 2")
        # looks like we need to access the object a first time when running the
        # tests in tox
        filter.oneshot
        filter.oneshot = False
        self.assertEqual(filter.active, True)
        self.assertEqual(filter.oneshot, False)
        filter.fired(self.sess)
        self.assertEqual(filter.active, True)


class TestPreferences(fmn.tests.Base):
    def setUp(self):
        super(TestPreferences, self).setUp()
        self.user1 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        self.user2 = fmn.lib.models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject",
            openid_url="http://toshio.id.fedoraproject.org/",
        )
        self.context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user")
        self.context2 = fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone")

        self.pref1 = fmn.lib.models.Preference.get_or_create(
            self.sess, self.user1.openid, self.context1.name)
        self.pref2 = fmn.lib.models.Preference.get_or_create(
            self.sess, self.user1.openid, self.context2.name)
        self.pref3 = fmn.lib.models.Preference.get_or_create(
            self.sess, self.user2.openid, self.context1.name)
        self.pref4 = fmn.lib.models.Preference.get_or_create(
            self.sess, self.user2.openid, self.context2.name)

        assert self.pref1 != self.pref2
        assert self.pref1 != self.pref3
        assert self.pref1 != self.pref4
        assert self.pref2 != self.pref3
        assert self.pref2 != self.pref4
        assert self.pref3 != self.pref4

        self.pref1.batch_delta = 1
        self.pref4.batch_count = 2

        self.sess.add(self.pref1)
        self.sess.add(self.pref4)
        self.sess.commit()

    def test_list_batching(self):
        """Assert preferences with batching on are returned when listing batching."""
        self.pref1.enabled = True
        self.sess.commit()

        batching = fmn.lib.models.Preference.list_batching(self.sess)
        self.assertEqual(len(batching), 1)
        self.assertEqual(self.pref1, batching[0])

    def test_list_batching_disabled(self):
        """Assert disabled preferences aren't returned when listing batching."""
        batching = fmn.lib.models.Preference.list_batching(self.sess)
        self.assertEqual(len(batching), 0)


class TestQueuedMessages(fmn.tests.Base):
    def setUp(self):
        super(TestQueuedMessages, self).setUp()
        self.user1 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        self.user2 = fmn.lib.models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject",
            openid_url="http://toshio.id.fedoraproject.org/",
        )
        self.context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user")
        self.context2 = fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone")

        raw_msg = {'testing': 'foobar'}

        self.obj1 = fmn.lib.models.QueuedMessage.enqueue(
            self.sess, self.user1, self.context1, raw_msg)
        self.obj2 = fmn.lib.models.QueuedMessage.enqueue(
            self.sess, self.user1, self.context1, raw_msg)
        self.obj3 = fmn.lib.models.QueuedMessage.enqueue(
            self.sess, self.user1, self.context1, raw_msg)
        self.obj4 = fmn.lib.models.QueuedMessage.enqueue(
            self.sess, self.user2, self.context1, raw_msg)
        self.obj5 = fmn.lib.models.QueuedMessage.enqueue(
            self.sess, self.user1, self.context2, raw_msg)

    def test_queued_message_enqueue(self):
        assert self.obj1 != self.obj2
        assert self.obj2 != self.obj3
        assert self.obj1 != self.obj3
        self.assertEqual(fmn.lib.models.QueuedMessage.count_for(
            self.sess, self.user1, self.context1), 3)

    def test_queued_message_earliest(self):
        self.assertEqual(fmn.lib.models.QueuedMessage.earliest_for(
            self.sess, self.user1, self.context1), self.obj1)

    def test_queued_message_list(self):
        queued_messages = fmn.lib.models.QueuedMessage.list_for(
            self.sess, self.user1, self.context1)
        self.assertEqual(queued_messages, [self.obj1, self.obj2, self.obj3])

    def test_queued_message_dequeue(self):
        self.obj1.dequeue(self.sess)
        self.assertEqual(fmn.lib.models.QueuedMessage.count_for(
            self.sess, self.user1, self.context1), 2)
        self.assertEqual(fmn.lib.models.QueuedMessage.earliest_for(
            self.sess, self.user1, self.context1), self.obj2)


class CachedLoadClassTests(unittest.TestCase):
    """Tests for the :func:`fmn.lib.models._cached_load_class`."""

    @mock.patch('fmn.lib.models.fedmsg.utils.load_class',
                wraps=fmn.lib.models.fedmsg.utils.load_class)
    def test_results_cached_on_args(self, mock_load_class):
        """Assert multiple calls with the same path result in a single load."""
        # First, reset the cache to make sure there's no previous results.
        fmn.lib.models._rule_class_cache.backend._cache = {}

        fmn.lib.models._cached_load_class('fmn.rules:user_package_filter')
        fmn.lib.models._cached_load_class('fmn.rules:user_package_filter')

        mock_load_class.assert_called_once_with('fmn.rules:user_package_filter')

    def test_results_same_object(self):
        """Assert that the exact same object is returned from multiple calls."""
        r1 = fmn.lib.models._cached_load_class('fmn.rules:user_package_filter')
        r2 = fmn.lib.models._cached_load_class('fmn.rules:user_package_filter')

        self.assertTrue(r1 is r2)

    def test_results_expected_object(self):
        """Assert the object loaded is what we expect it to be."""
        r1 = fmn.lib.models._cached_load_class('fmn.rules:user_package_filter')

        self.assertTrue(r1 is user_package_filter)
