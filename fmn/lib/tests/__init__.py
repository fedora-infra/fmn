import os
import fmn.lib.models

import unittest

DB_PATH = 'sqlite:////var/tmp/test-fmn-lib.sqlite'


class Base(unittest.TestCase):
    def setUp(self):
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)
        self.sess = fmn.lib.models.init(DB_PATH, debug=False, create=True)

        self.config = {
            'fmn.backends': ['irc', 'email', 'android'],
        }
        self.valid_paths = fmn.lib.load_rules(
            root='fmn.lib.tests.example_rules')

        def mock_notify(self, openid, context, changed):
            if not hasattr(self, 'notified'):
                self.notified = []
            self.notified.append([openid, context, changed])

        self.original_notify = fmn.lib.models.FMNBase.notify
        fmn.lib.models.FMNBase.notify = mock_notify

    def tearDown(self):
        """ Remove the test.db database if there is one. """
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)

        self.sess.rollback()

        fmn.lib.models.FMNBase.notify = self.original_notify
