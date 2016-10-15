import unittest
from mock import patch, Mock

import six
from twisted.web.test.requesthelper import DummyRequest

from fmn.sse.sse_webserver import SSEServer, JsonNotFound
from fmn.sse.subscriber import SSESubscriber


class SSEWebServerTest(unittest.TestCase):
    def setUp(self):
        self.sse = SSEServer()
        self.key = ['user', 'bob']
        self.sse.subscribers.connections = {}
        self.sse.subscribers.looping_calls = {}

    def tearDown(self):
        self.sse = None

    def test_path_valid(self):
        path = [b'user', b'bob']
        self.assertTrue(self.sse.is_valid_path(path))
        path = [b'group', b'bob']
        self.assertTrue(self.sse.is_valid_path(path))

    def test_path_invalid(self):
        path = ['invalid']
        self.assertFalse(self.sse.is_valid_path(path))
        path = [b'invalid', b'bob']
        self.assertFalse(self.sse.is_valid_path(path))
        path = [b'group']
        self.assertFalse(self.sse.is_valid_path(path))
        path = [b'user']
        self.assertFalse(self.sse.is_valid_path(path))

    @patch.object(SSESubscriber, 'add_looping_call')
    @patch.object(SSESubscriber, 'does_loopingcall_exist')
    def test_handle_request_valid(self, alc_mock, dlce_mock):
        alc_mock.return_value = None
        dlce_mock.return_value = True

        request = DummyRequest(postpath=['user', 'bob'])
        self.sse.handle_request(request)
        # handle request does not format the path
        self.assertTrue('user' in self.sse.subscribers.connections)
        self.assertTrue('bob'
                        in self.sse.subscribers.connections['user'])

    @patch.object(SSESubscriber, 'get_payload', return_value=b"unittest")
    def test_render_get(self, pay_mock):
        # add requests
        request1 = DummyRequest(postpath=[b'user', b'bob'])
        request2 = DummyRequest(postpath=[b'user', b'bob'])
        self.sse.render_GET(request=request1)
        self.sse.render_GET(request=request2)
        self.assertEqual(
            len(self.sse.subscribers.connections['user']
                ['bob.id.fedoraproject.org']), 2)

        # req1 started the looping call so it gets an extra message
        self.assertEqual(request1.written, [b"data: unittest\r\n\r\n",
                                            ])
        # req2 is waiting for the next cycle for it to be sent a message so its
        # empty
        self.assertEqual(request2.written, [])

    def test_render_invalid_path(self):
        pp = [b'turtle', b'turtle', b'turtle', b'turtle']
        req = DummyRequest(postpath=pp)
        self.sse.render_GET(request=req)
        self.assertEqual(req.responseCode, 404)


class TestJsonNotFound(unittest.TestCase):
    """
    Unit tests for fmn.sse.sse_webserver.JsonNotFound.
    """

    def test_init(self):
        """Assert the default status is 404."""
        not_found = JsonNotFound()
        self.assertEqual(404, not_found.code)
        self.assertEqual(u'Not Found', not_found.brief)
        self.assertEqual(None, not_found.detail)

    def test_render_html(self):
        """Assert that when no details are provided an HTML page is rendered"""
        not_found = JsonNotFound()
        request = Mock()
        body = not_found.render(request)

        request.setHeader.assert_called_once_with(
            u'content-type'.encode('utf-8'),
            u'text/html; charset=utf-8'.encode('utf-8'),
        )
        self.assertTrue(isinstance(body, six.binary_type))
        self.assertIn(u'Not Found', body.decode('utf-8'))

    def test_render_json(self):
        """Assert that when details are provided, they are rendered as JSON"""
        not_found = JsonNotFound(detail={u'x': u'y'})
        request = Mock()
        body = not_found.render(request)

        request.setHeader.assert_called_once_with(
            u'content-type'.encode('utf-8'),
            u'application/json; charset=utf-8'.encode('utf-8'),
        )
        self.assertTrue(isinstance(body, six.binary_type))
        self.assertEqual(u'{"x": "y"}', body.decode('utf-8'))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
        SSEWebServerTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
