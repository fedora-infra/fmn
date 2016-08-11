import unittest
from mock import patch, Mock
from twisted.web.test.requesthelper import DummyRequest
from fmn.sse.subscriber import SSESubscriber


class MockLoopingCall(object):
    def __init__(self, running=False):
        self.running = running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


class SSESubscriberTest(unittest.TestCase):
    def setUp(self):
        self.sse_sub = SSESubscriber()
        self.key = ['user', 'bob']
        self.sse_sub.connections = {}
        self.sse_sub.looping_calls = {}

    def tearDown(self):
        self.sse_sub = None

    def test_does_loopingcall_exist(self):
        # Looping call does not exist
        self.assertFalse(self.sse_sub.does_loopingcall_exist(['does not', 'exist']))
        self.assertFalse(self.sse_sub.does_loopingcall_exist(['does not']))

        # Add a fake placeholder for a loopingcall
        self.sse_sub.looping_calls['user'] = {'bob': True}
        self.sse_sub.looping_calls['group'] = {'infra': True}

        # Looping call does exist
        self.assertTrue(self.sse_sub.does_loopingcall_exist(['user', 'bob']))
        self.assertTrue(self.sse_sub.does_loopingcall_exist(['group', 'infra']))

    @patch.object(SSESubscriber, 'start_looping_call')
    def test_add_looping_call_initial(self, slc):
        slc.return_value = None
        self.sse_sub.add_looping_call(self.key)
        self.assertIsNotNone(self.sse_sub.looping_calls[self.key[0]][self.key[1]])

    @patch.object(SSESubscriber, 'start_looping_call')
    def test_add_looping_call_empty_user(self, slc):
        self.sse_sub.looping_calls = {}
        slc.return_value = None
        self.sse_sub.looping_calls['user'] = {}
        self.sse_sub.add_looping_call(self.key)
        self.assertIsNotNone(self.sse_sub.looping_calls[self.key[0]][self.key[1]])

    def test_start_looping_call(self):
        lc_mock = MockLoopingCall()
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}
        self.assertFalse(self.sse_sub.looping_calls['user']['bob'].running)
        self.test_start_looping_call()
        self.assertTrue(self.sse_sub.looping_calls['user']['bob'].running)

    def test_stop_looping_call_not_running(self):
        lc_mock = MockLoopingCall()
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}
        self.sse_sub.stop_looping_call(self.key)
        self.assertNotIn('bob', self.sse_sub.looping_calls['user'])

    def test_stop_looping_call_running(self):
        lc_mock = Mock(spec=MockLoopingCall(running=True))
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}
        self.sse_sub.stop_looping_call(self.key)
        self.assertNotIn('bob', self.sse_sub.looping_calls['user'])

    def test_start_looping_call(self):
        lc_mock = MockLoopingCall(running=True)
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}
        self.sse_sub.start_looping_call(self.key)
        self.assertEqual(self.sse_sub.looping_calls['user']['bob'].running, True)

    def test_add_connection(self):
        lc_mock = MockLoopingCall(running=True)
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}
        request = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request, request.postpath)
        self.assertEqual(request, self.sse_sub.connections['user']['bob'][0])

        # Add another connection to the same feed
        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request2, request2.postpath)
        self.assertEqual(request2, self.sse_sub.connections['user']['bob'][1])

    def test_remove_connection(self):
        # add the looping call and two connections
        lc_mock = MockLoopingCall(running=True)
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}

        request = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request, request.postpath)

        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request2, request2.postpath)

        # remove the first connection
        self.sse_sub.remove_connection(request, self.key)
        self.assertEqual(len(self.sse_sub.connections['user']['bob']), 1)

        # remove the second connection
        self.sse_sub.remove_connection(request2, self.key)
        self.assertEqual(len(self.sse_sub.connections['user']['bob']), 0)

        # since we removed all the connections the looping_call is removed
        self.assertEqual(self.sse_sub.looping_calls['user'], {})

        # so we need to add it back in for testing purposes
        self.sse_sub.looping_calls['user'] = {'bob': lc_mock}
        # add a third connection
        request3 = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request3, request3.postpath)
        self.assertEqual(len(self.sse_sub.connections['user']['bob']), 1)

    @patch.object(SSESubscriber, 'get_payload', return_value={'msg': 'unittest'})
    def test_write_messages_all_connections(self, pay_mock):
        # add requests
        request1 = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request1, request1.postpath)
        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse_sub.add_connection(request2, request2.postpath)

        self.assertEqual(len(self.sse_sub.connections['user']['bob']), 2)

        self.sse_sub.write_messages_all_connections(['user', 'bob'])

        # req1 started the looping call so it gets an extra message
        self.assertEqual(request1.written, [b"data: {'msg': 'unittest'}\r\n\r\n",
                                            b"data: {'msg': 'unittest'}\r\n\r\n",
                                            ])
        self.assertEqual(request2.written, [
            b"data: {'msg': 'unittest'}\r\n\r\n",
        ])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
        SSESubscriber)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
