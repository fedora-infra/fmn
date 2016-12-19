import fmn.lib.models
import fmn.tests


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
        filter.oneshot = True
        self.assertEqual(filter.active, True)
        self.assertEqual(filter.oneshot, True)
        filter.fired(self.sess)
        self.assertEqual(filter.active, False)

        filter = fmn.lib.models.Filter.create(self.sess, name="test filter 2")
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
        batching = fmn.lib.models.Preference.list_batching(self.sess)
        self.assertEqual(len(batching), 2)
        self.assertEqual(set([self.pref1, self.pref4]), set(batching))


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
