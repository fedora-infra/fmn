from nose.tools import eq_, assert_not_equals
import os
import fmn.lib.models
import fmn.lib.tests


class TestBasics(fmn.lib.tests.Base):
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
        eq_(user1.openid, user2.openid)
        eq_(user1, user2)
        assert_not_equals(user1, user3)

    def test_context_create(self):
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user")
        context2 = fmn.lib.models.Context.get(self.sess, name="irc")
        context3 = fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone")
        eq_(context1, context2)
        assert_not_equals(context1, context3)

    def test_user_all(self):
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
        eq_(len(fmn.lib.models.User.all(self.sess)), 2)

    def test_context_all(self):
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user")
        context2 = fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone")
        eq_(len(fmn.lib.models.Context.all(self.sess)), 2)

class TestQueuedMessages(fmn.lib.tests.Base):
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
        eq_(fmn.lib.models.QueuedMessage.count_for(
            self.sess, self.user1, self.context1), 3)

    def test_queued_message_earliest(self):
        eq_(fmn.lib.models.QueuedMessage.earliest_for(
            self.sess, self.user1, self.context1), self.obj1)

    def test_queued_message_list(self):
        queued_messages = fmn.lib.models.QueuedMessage.list_for(
            self.sess, self.user1, self.context1)
        eq_(queued_messages, [self.obj1, self.obj2, self.obj3])

    def test_queued_message_dequeue(self):
        self.obj1.dequeue(self.sess)
        eq_(fmn.lib.models.QueuedMessage.count_for(
            self.sess, self.user1, self.context1), 2)
        eq_(fmn.lib.models.QueuedMessage.earliest_for(
            self.sess, self.user1, self.context1), self.obj2)
