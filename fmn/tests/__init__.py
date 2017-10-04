import unittest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import vcr

import fmn.lib.models


DB_PATH = 'sqlite:////var/tmp/test-fmn-lib.sqlite'


class Base(unittest.TestCase):
    def setUp(self):
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)

        self._old_engine = fmn.lib.models.engine
        self._old_session = fmn.lib.models.Session
        fmn.lib.models.engine = create_engine(DB_PATH, echo=False)
        fmn.lib.models.Session = scoped_session(sessionmaker(bind=fmn.lib.models.engine))
        fmn.lib.models.BASE.metadata.create_all(fmn.lib.models.engine)
        # Be sure to use the new session on the query property
        fmn.lib.models.BASE.query = fmn.lib.models.Session.query_property()
        self.sess = fmn.lib.models.Session

        cwd = os.path.dirname(os.path.realpath(__file__))
        context_manager = vcr.use_cassette(os.path.join(cwd, 'fixtures/', self.id()))
        self.vcr = context_manager.__enter__()
        self.addCleanup(context_manager.__exit__)

        self.config = {
            'fmn.backends': ['irc', 'email', 'android'],
            'topic_prefix_re': '',
        }
        self.valid_paths = fmn.lib.load_rules(
            root='fmn.tests.example_rules')

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

        # Remove the session from the session registry and roll back any
        # transaction state.
        fmn.lib.models.Session.remove()

        fmn.lib.models.FMNBase.notify = self.original_notify
        fmn.lib.models.engine = self._old_engine
        fmn.lib.models.Session = self._old_session
