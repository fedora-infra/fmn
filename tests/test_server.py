import unittest
import mock

import six
from twisted.web.test.requesthelper import DummyRequest
from twisted.web import server as twisted_server

from fmn.sse import server


class TestSSEServer(unittest.TestCase):
    def setUp(self):
        self.sse = server.SSEServer()

    def test_render_GET(self):
        """Assert a "good" request is handled without error"""
        request = mock.Mock(postpath=['myexchange', 'myqueue'])
        request_key = server.RequestKey('myexchange', 'myqueue')

        result = self.sse.render_GET(request)
        self.assertEqual(result, twisted_server.NOT_DONE_YET)
        # TODO some asserts about headers
        request.write.assert_called_once_with(b'')
        request.notifyFinish.return_value.addBoth.assert_called_once_with(
            self.sse.request_closed, request, request_key)
        self.assertTrue(request_key in self.sse.subscribers)

    def test_render_GET_trailing_slash(self):
        """Assert a "good" request is handled without error"""
        request = mock.Mock(postpath=['myexchange', 'myqueue', ''])
        request_key = server.RequestKey('myexchange', 'myqueue')

        result = self.sse.render_GET(request)
        self.assertEqual(result, twisted_server.NOT_DONE_YET)
        self.assertTrue(request_key in self.sse.subscribers)

    def test_render_GET_no_exchange(self):
        """Assert that requesting an exchange that doesn't exist is a 404"""
        pass

    def test_render_GET_no_queue(self):
        """Assert that requesting a queue that doesn't exist is a 404"""
        pass

    def test_render_GET_nonsense_url(self):
        """Assert a request not for /<exchange>/<queue> fails"""
        path_parts = [b'turtle', b'turtle', b'turtle', b'turtle']
        req = DummyRequest(postpath=path_parts)
        self.sse.render_GET(request=req)
        self.assertEqual(req.responseCode, 404)

    def test_new_subscription(self):
        """Assert SSEServer.new_subscription adds a subscription entry"""
        request_key = server.RequestKey('myexchange', 'myqueue')
        self.sse.queue = mock.Mock()

        self.sse.new_subscription(request_key)
        self.sse.queue.assert_called_once_with(*request_key)


class TestJsonNotFound(unittest.TestCase):
    """
    Unit tests for fmn.sse.server.JsonNotFound.
    """

    def test_init(self):
        """Assert the default status is 404."""
        not_found = server.JsonNotFound()
        self.assertEqual(404, not_found.code)
        self.assertEqual(u'Not Found', not_found.brief)
        self.assertEqual(None, not_found.detail)

    def test_render_html(self):
        """Assert that when no details are provided an HTML page is rendered"""
        not_found = server.JsonNotFound()
        request = mock.Mock()
        body = not_found.render(request)

        request.setHeader.assert_called_once_with(
            u'content-type'.encode('utf-8'),
            u'text/html; charset=utf-8'.encode('utf-8'),
        )
        self.assertTrue(isinstance(body, six.binary_type))
        self.assertIn(u'Not Found', body.decode('utf-8'))

    def test_render_json(self):
        """Assert that when details are provided, they are rendered as JSON"""
        not_found = server.JsonNotFound(detail={u'x': u'y'})
        request = mock.Mock()
        body = not_found.render(request)

        request.setHeader.assert_called_once_with(
            u'content-type'.encode('utf-8'),
            u'application/json; charset=utf-8'.encode('utf-8'),
        )
        self.assertTrue(isinstance(body, six.binary_type))
        self.assertEqual(u'{"x": "y"}', body.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
