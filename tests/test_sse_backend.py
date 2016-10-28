"""
Unit tests for the SSE backend.
"""
from __future__ import unicode_literals, absolute_import

import json
import unittest

import mock

from fmn.consumer.backends import SSEBackend


@mock.patch('fmn.consumer.backends.sse.protocol.ClientCreator', mock.Mock())
class TestSSEBackend(unittest.TestCase):

    def test_format_message_conglomerated(self):
        """Assert conglomerated messages are formatted"""
        message = {
            'subtitle': 'relrod pushed commits to ghc and 487 other packages',
            'link': 'http://example.com/',
            'icon': 'https://that-git-logo',
            'secondary_icon': 'https://that-relrod-avatar',
            'start_time': 0,
            'end_time': 100,
            'human_time': '5 minutes ago',
            'usernames': ['relrod'],
            'packages': ['ghc', 'nethack'],
            'topics': ['org.fedoraproject.prod.git.receive'],
            'categories': ['git'],
            'msg_ids': {
                '2014-abcde': {
                    'subtitle': 'relrod pushed some commits to ghc',
                    'title': 'git.receive',
                    'link': 'http://...',
                    'icon': 'http://...',
                },
                '2014-bcdef': {
                    'subtitle': 'relrod pushed some commits to nethack',
                    'title': 'git.receive',
                    'link': 'http://...',
                    'icon': 'http://...',
                },
            },
        }
        recipient = {
            "triggered_by_links": True,
            "markup_messages": True,
            "user": "jcline.id.fedoraproject.org",
            "filter_name": "firehose",
            "filter_oneshot": True,
            "filter_id": 7,
            "shorten_links": False,
            "verbose": True,
        }
        backend = SSEBackend({})

        formatted_message = backend._format_message(message, recipient)
        self.assertTrue(isinstance(formatted_message, bytes))
        formatted_message = json.loads(formatted_message)
        for key in ('dom_id', 'date_time', 'icon', 'link', 'markup', 'secondary_icon'):
            self.assertTrue(key in formatted_message)
        self.assertEqual(formatted_message['link'], message['link'])
        self.assertEqual(formatted_message['markup'], message['subtitle'])

    @mock.patch('fmn.consumer.backends.sse.fedmsg.meta')
    def test_format_message_raw(self, mock_meta):
        """Assert raw messages are formatted"""
        message = {
            u'username': u'apache',
            u'i': 1,
            u'timestamp': 1478281861,
            u'msg_id': u'2016-c2184569-f9c4-4c52-affd-79e28848d70f',
            u'crypto': u'x509',
            u'topic': u'org.fedoraproject.prod.buildsys.task.state.change',
            u'msg': {
                u'info': {
                    u'children': [],
                    u'parent': None,
                    u'channel_id': 1,
                    u'start_time': u'2016-11-04 17:51:01.254871',
                    u'request': [
                        u'../packages/eclipse/4.5.0/1.fc26/src/eclipse-4.5.0-1.fc26.src.rpm',
                        u'f26',
                        {u'scratch': True, u'arch_override': u'x86_64'}
                    ],
                    u'state': 1,
                    u'awaited': None,
                    u'method': u'build',
                    u'priority': 50,
                    u'completion_time': None,
                    u'waiting': None,
                    u'create_time': u'2016-11-04 17:50:57.825631',
                    u'owner': 3199,
                    u'host_id': 82,
                    u'label': None,
                    u'arch': u'noarch',
                    u'id': 16289846
                },
                u'old': u'FREE',
                u'attribute': u'state',
                u'method': u'build',
                u'instance': u'primary',
                u'owner': u'koschei',
                u'new': u'OPEN',
                u'srpm': u'eclipse-4.5.0-1.fc26.src.rpm',
                u'id': 16289846
            }
        }
        recipient = {
            "triggered_by_links": True,
            "markup_messages": True,
            "user": "jcline.id.fedoraproject.org",
            "filter_name": "firehose",
            "filter_oneshot": True,
            "filter_id": 7,
            "shorten_links": False,
            "verbose": True,
        }
        mock_meta.msg2icon.return_value = 'http://example.com/icon.png'
        mock_meta.msg2link.return_value = 'http://example.com/link'
        mock_meta.msg2secondary_icon.return_value = None
        mock_meta.msg2agent.return_value = 'koschei'
        mock_meta.msg2title.return_value = 'Some title'
        mock_meta.msg2subtitle.return_value = 'Some subtitle'
        backend = SSEBackend({})

        formatted_message = backend._format_message(message, recipient)
        self.assertTrue(isinstance(formatted_message, bytes))
        formatted_message = json.loads(formatted_message)
        for key in ('dom_id', 'date_time', 'icon', 'link', 'markup', 'secondary_icon'):
            self.assertTrue(key in formatted_message)

        self.assertEqual(mock_meta.msg2icon.return_value, formatted_message['icon'])
        self.assertEqual(mock_meta.msg2link.return_value, formatted_message['link'])
        self.assertEqual(
            mock_meta.msg2secondary_icon.return_value, formatted_message['secondary_icon'])


if __name__ == '__main__':
    unittest.main()
