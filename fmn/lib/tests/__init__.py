import os
import fmn.lib.models

DB_PATH = 'sqlite:////var/tmp/test-fmn-lib.sqlite'

class Base(object):
    def setUp(self):
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)
        self.sess = fmn.lib.models.init(DB_PATH, debug=False, create=True)

    def tearDown(self):
        """ Remove the test.db database if there is one. """
        dbfile = DB_PATH.split('///')[1]
        if os.path.exists(dbfile):
            os.unlink(dbfile)

        self.sess.rollback()
