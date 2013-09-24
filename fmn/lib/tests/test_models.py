from nose.tools import eq_, assert_not_equals
import os
import fmn.lib.models
import fmn.lib.tests


class TestBasics(fmn.lib.tests.Base):
    def test_setup_and_teardown(self):
        pass

    def test_user_get_or_create(self):
        user1 = fmn.lib.models.User.get_or_create(self.sess, username="ralph")
        user2 = fmn.lib.models.User.get_or_create(self.sess, username="ralph")
        user3 = fmn.lib.models.User.get_or_create(self.sess, username="toshio")
        eq_(user1.username, user2.username)
        eq_(user1, user2)
        assert_not_equals(user1, user3)

    def test_context_create(self):
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat")
        context2 = fmn.lib.models.Context.get(self.sess, name="irc")
        context3 = fmn.lib.models.Context.create(
            self.sess, name="gcm", description="Google Cloud Messaging")
        eq_(context1, context2)
        assert_not_equals(context1, context3)

    def test_user_all(self):
        user1 = fmn.lib.models.User.get_or_create(self.sess, username="ralph")
        user2 = fmn.lib.models.User.get_or_create(self.sess, username="ralph")
        user3 = fmn.lib.models.User.get_or_create(self.sess, username="toshio")
        eq_(len(fmn.lib.models.User.all(self.sess)), 2)

    def test_context_all(self):
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat")
        context2 = fmn.lib.models.Context.create(
            self.sess, name="gcm", description="Google Cloud Messaging")
        eq_(len(fmn.lib.models.Context.all(self.sess)), 2)
