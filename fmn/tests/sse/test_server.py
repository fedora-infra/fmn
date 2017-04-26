# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
import unittest

import mock
import six
from twisted.web.test.requesthelper import DummyRequest
from twisted.web import server as twisted_server
from twisted.trial import unittest as twisted_unittest

from fmn.sse import server


class TestSSEServer(twisted_unittest.TestCase):
    def setUp(self):
        self.sse = server.SSEServer()
        self.sse.whitelist = None
        self.sse.blacklist = None
        self.sse.channel = mock.Mock()
        self.sse.connection = mock.Mock()

    def test_render_GET(self):
        """Assert a "good" request is handled without error"""
        request = mock.Mock(postpath=['myqueue'])
        queue_name = 'myqueue'

        result = self.sse.render_GET(request)
        self.assertEqual(result, twisted_server.NOT_DONE_YET)
        # TODO some asserts about headers
        request.write.assert_called_once_with(b'')
        request.notifyFinish.return_value.addBoth.assert_called_once_with(
            self.sse.request_closed, request, queue_name)
        self.assertTrue(queue_name in self.sse.subscribers)

    def test_render_GET_trailing_slash(self):
        """Assert a "good" request is handled without error"""
        request = mock.Mock(postpath=['myqueue', ''])
        queue_name = 'myqueue'

        result = self.sse.render_GET(request)
        self.assertEqual(result, twisted_server.NOT_DONE_YET)
        self.assertTrue(queue_name in self.sse.subscribers)

    def test_render_GET_whitelist(self):
        """Assert that requests that don't match the whitelist fail"""
        self.sse.whitelist = re.compile('multipass$')
        bad_req = DummyRequest(postpath=['cannot_pass'])
        good_req = DummyRequest(postpath=['multipass'])

        self.sse.render_GET(bad_req)
        self.assertEqual(bad_req.responseCode, 403)

        good_result = self.sse.render_GET(good_req)
        self.assertEqual(good_result, twisted_server.NOT_DONE_YET)

    def test_render_GET_blacklist(self):
        """Assert requests that match the blacklist regex fail"""
        self.sse.blacklist = re.compile('none_shall_pass$')
        bad_req = DummyRequest(postpath=['none_shall_pass'])
        good_req = DummyRequest(postpath=['multipass'])

        self.sse.render_GET(bad_req)
        self.assertEqual(bad_req.responseCode, 403)

        good_result = self.sse.render_GET(good_req)
        self.assertEqual(good_result, twisted_server.NOT_DONE_YET)

    def test_render_GET_whitelist_blacklist(self):
        """Assert that the blacklist overrules the whitelist"""
        self.sse.whitelist = re.compile('pass$')
        self.sse.blacklist = re.compile('pass$')
        bad_req = DummyRequest(postpath=['pass'])
        other_bad_req = DummyRequest(postpath=['multipass'])

        self.sse.render_GET(bad_req)
        self.assertEqual(bad_req.responseCode, 403)
        self.sse.render_GET(other_bad_req)
        self.assertEqual(other_bad_req.responseCode, 403)

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
        queue_name = 'myqueue'
        self.sse.queue = mock.Mock()

        self.sse.new_subscription(queue_name)
        self.sse.queue.assert_called_once_with(queue_name)

    def test_request_closed(self):
        """
        Assert that when the request is finished we clean up the subscriber's list
        """
        mock_request = mock.Mock()
        self.sse.subscribers['myqueue'] = {
            'queue': server.RabbitQueue(mock.Mock(), 'mytag'),
            'requests': [mock_request]
        }

        def assertions(*args, **kwargs):
            self.assertEqual(self.sse.subscribers, {})
            self.sse.channel.basic_cancel.assert_called_once_with(consumer_tag='mytag')

        d = self.sse.request_closed(None, mock_request, 'myqueue')
        d.addCallback(assertions)
        return d


class TestJsonNotFound(unittest.TestCase):
    """
    Unit tests for fmn.sse.server.JsonNotFound.
    """

    def test_init(self):
        """Assert the default status is 404."""
        not_found = server.JsonNotFound()
        self.assertEqual(404, not_found.code)
        self.assertEqual(u'Not Found', not_found.brief)

    def test_render_html(self):
        """Assert that when details isn't a dict, an HTML page is rendered"""
        not_found = server.JsonNotFound(detail='Some text')
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


class TestJsonForbidden(unittest.TestCase):
    """
    Unit tests for fmn.sse.server.JsonForbidden.
    """

    def test_init(self):
        """Assert the default status is 404."""
        not_found = server.JsonForbidden()
        self.assertEqual(403, not_found.code)
        self.assertEqual(u'Forbidden', not_found.brief)


if __name__ == '__main__':
    unittest.main()
