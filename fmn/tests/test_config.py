
import unittest

import mock

from fmn import config


class _FmnConfigGetItemTests(unittest.TestCase):
    """Tests for the ``__getitem__`` method on the :class:`_FmnConfig` class."""

    def setUp(self):
        self.config = config._FmnConfig()
        self.config.load_config = mock.Mock()
        self.config['fmn.irc.nickserv_pass'] = 'hunter2'

    def test_not_loaded(self):
        """Assert calling ``__getitem__`` causes the config to load."""
        self.assertFalse(self.config.loaded)
        self.assertEqual('hunter2', self.config['fmn.irc.nickserv_pass'])
        self.config.load_config.assert_called_once()

    def test_loaded(self):
        """Assert calling ``__getitem__`` when the config is loaded doesn't reload the config."""
        self.config.loaded = True

        self.assertEqual('hunter2', self.config['fmn.irc.nickserv_pass'])
        self.assertEqual(0, self.config.load_config.call_count)

    def test_missing(self):
        """Assert you still get normal dictionary errors from the config."""
        self.assertRaises(KeyError, self.config.__getitem__, 'somemissingkey')


class _FmnConfigGetTests(unittest.TestCase):
    """Tests for the ``get`` method on the :class:`_FmnConfig` class."""

    def setUp(self):
        self.config = config._FmnConfig()
        self.config.load_config = mock.Mock()
        self.config['fmn.irc.nickserv_pass'] = 'hunter2'

    def test_not_loaded(self):
        """Assert calling ``get`` causes the config to load."""
        self.assertFalse(self.config.loaded)
        self.assertEqual('hunter2', self.config.get('fmn.irc.nickserv_pass'))
        self.config.load_config.assert_called_once()

    def test_loaded(self):
        """Assert calling ``get`` when the config is loaded doesn't reload the config."""
        self.config.loaded = True

        self.assertEqual('hunter2', self.config.get('fmn.irc.nickserv_pass'))
        self.assertEqual(0, self.config.load_config.call_count)

    def test_missing(self):
        """Assert you get ``None`` when the key is missing."""
        self.assertEqual(None, self.config.get('somemissingkey'))


class _FmnConfigPopItemTests(unittest.TestCase):
    """Tests for the ``pop`` method on the :class:`_FmnConfig` class."""

    def setUp(self):
        self.config = config._FmnConfig()
        self.config.load_config = mock.Mock()
        self.config['fmn.irc.nickserv_pass'] = 'hunter2'

    def test_not_loaded(self):
        """Assert calling ``pop`` causes the config to load."""
        self.assertFalse(self.config.loaded)
        self.assertEqual('hunter2', self.config.pop('fmn.irc.nickserv_pass'))
        self.config.load_config.assert_called_once()

    def test_loaded(self):
        """Assert calling ``pop`` when the config is loaded doesn't reload the config."""
        self.config.loaded = True

        self.assertEqual('hunter2', self.config.pop('fmn.irc.nickserv_pass'))
        self.assertEqual(0, self.config.load_config.call_count)

    def test_removes(self):
        """Assert the configuration is removed with ``pop``."""
        self.assertEqual('hunter2', self.config.pop('fmn.irc.nickserv_pass'))
        self.assertRaises(KeyError, self.config.pop, 'fmn.irc.nickserv_pass')

    def test_get_missing(self):
        """Assert you still get normal dictionary errors from the config."""
        self.assertRaises(KeyError, self.config.pop, 'somemissingkey')


class _FmnConfigCopyTests(unittest.TestCase):
    """Tests for the ``copy`` method on the :class:`_FmnConfig` class."""

    def setUp(self):
        self.config = config._FmnConfig()
        self.config.load_config = mock.Mock()
        self.config['fmn.irc.nickserv_pass'] = 'hunter2'

    def test_not_loaded(self):
        """Assert calling ``copy`` causes the config to load."""
        self.assertFalse(self.config.loaded)
        self.assertEqual({'fmn.irc.nickserv_pass': 'hunter2'}, self.config.copy())
        self.config.load_config.assert_called_once()

    def test_loaded(self):
        """Assert calling ``copy`` when the config is loaded doesn't reload the config."""
        self.config.loaded = True

        self.assertEqual({'fmn.irc.nickserv_pass': 'hunter2'}, self.config.copy())
        self.assertEqual(0, self.config.load_config.call_count)


class _FmnConfigLoadConfig(unittest.TestCase):

    @mock.patch('fmn.config.fedmsg.config.load_config')
    def test_loads_defaults(self, get_appsettings):
        """Test that defaults are loaded."""
        c = config._FmnConfig()

        c.load_config({})

        self.assertEqual(c['fmn.autocreate'], False)

    @mock.patch('fmn.config.fedmsg.config.load_config')
    def test_marks_loaded(self, fedmsg_load):
        c = config._FmnConfig()
        fedmsg_load.return_value = {'fmn.irc.nickserv_pass': 'hunter2'}

        c.load_config()

        fedmsg_load.assert_called_once_with()
        self.assertTrue(('fmn.irc.nickserv_pass', 'hunter2') in c.items())
        self.assertTrue(c.loaded)

    @mock.patch('fmn.config.fedmsg.config.load_config')
    def test_validates(self, get_appsettings):
        """Test that the config is validated."""
        c = config._FmnConfig()

        with self.assertRaises(ValueError) as exc:
            c.load_config({'fmn.junk_suffixes': 'notalist'})

        self.assertEqual(
            str(exc.exception),
            ('Invalid config values were set: \n\tfmn.junk_suffixes: "notalist"'
             ' is not "<class \'list\'>"'))

    @mock.patch('fmn.config.fedmsg.config.load_config')
    def test_with_settings(self, fedmsg_load):
        """Test with the optional settings parameter."""
        c = config._FmnConfig()

        c.load_config({'fmn.irc.nickserv_pass': 'hunter2'})

        self.assertEqual(c['fmn.irc.nickserv_pass'], 'hunter2')
        self.assertEqual(fedmsg_load.call_count, 0)
