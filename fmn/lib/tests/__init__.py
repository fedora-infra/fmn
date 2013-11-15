import os
import fmn.lib.models

DB_PATH = 'sqlite:////var/tmp/test-fmn-lib.sqlite'


class Base(object):
    def setUp(self):
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)
        self.sess = fmn.lib.models.init(DB_PATH, debug=False, create=True)

        self.config = {}
        self.valid_paths = fmn.lib.load_filters(
            root='fmn.lib.tests.example_filters')

    def tearDown(self):
        """ Remove the test.db database if there is one. """
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)

        self.sess.rollback()
