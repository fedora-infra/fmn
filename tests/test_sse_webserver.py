import unittest
from mock import patch, Mock
from twisted.web.test.requesthelper import DummyRequest
from fmn.sse.sse_webserver import SSEServer


class MockLoopingCall(object):
    def __init__(self, running=False):
        self.running = running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


class SSEWebServerTest(unittest.TestCase):
    def setUp(self):
        self.sse = SSEServer()
        self.key = ['user', 'bob']
        self.sse.connections = {}
        self.sse.looping_calls = {}

    def tearDown(self):
        self.sse = None

    def test_path_valid(self):
        path = ['user', 'bob']
        self.assertTrue(self.sse.is_valid_path(path))
        path = ['group', 'bob']
        self.assertTrue(self.sse.is_valid_path(path))

    def test_path_invalid(self):
        path = ['invalid']
        self.assertFalse(self.sse.is_valid_path(path))
        path = ['invalid', 'bob']
        self.assertFalse(self.sse.is_valid_path(path))
        path = ['group']
        self.assertFalse(self.sse.is_valid_path(path))
        path = ['user']
        self.assertFalse(self.sse.is_valid_path(path))

    def test_does_loopingcall_exist(self):
        # Looping call does not exist
        self.assertFalse(self.sse.does_loopingcall_exist(['does not', 'exist']))
        self.assertFalse(self.sse.does_loopingcall_exist(['does not']))

        # Add a fake placeholder for a loopingcall
        self.sse.looping_calls['user'] = {'bob': True}
        self.sse.looping_calls['group'] = {'infra': True}

        # Looping call does exist
        self.assertTrue(self.sse.does_loopingcall_exist(['user', 'bob']))
        self.assertTrue(self.sse.does_loopingcall_exist(['group', 'infra']))

    @patch.object(SSEServer, 'start_looping_call')
    def test_add_looping_call_initial(self, slc):
        slc.return_value = None
        self.sse.add_looping_call(self.key)
        self.assertIsNotNone(self.sse.looping_calls[self.key[0]][self.key[1]])

    @patch.object(SSEServer, 'start_looping_call')
    def test_add_looping_call_empty_user(self, slc):
        self.sse.looping_calls = {}
        slc.return_value = None
        self.sse.looping_calls['user'] = {}
        self.sse.add_looping_call(self.key)
        self.assertIsNotNone(self.sse.looping_calls[self.key[0]][self.key[1]])

    def test_start_looping_call(self):
        lc_mock = MockLoopingCall()
        self.sse.looping_calls['user'] = {'bob': lc_mock}
        self.assertFalse(self.sse.looping_calls['user']['bob'].running)
        self.test_start_looping_call()
        self.assertTrue(self.sse.looping_calls['user']['bob'].running)

    def test_stop_looping_call_not_running(self):
        lc_mock = MockLoopingCall()
        self.sse.looping_calls['user'] = {'bob': lc_mock}
        self.sse.stop_looping_call(self.key)
        self.assertNotIn('bob', self.sse.looping_calls['user'])

    def test_stop_looping_call_running(self):
        lc_mock = Mock(spec=MockLoopingCall(running=True))
        self.sse.looping_calls['user'] = {'bob': lc_mock}
        self.sse.stop_looping_call(self.key)
        self.assertNotIn('bob', self.sse.looping_calls['user'])

    def test_start_looping_call(self):
        lc_mock = MockLoopingCall(running=True)
        self.sse.looping_calls['user'] = {'bob': lc_mock}
        self.sse.start_looping_call(self.key)
        self.assertEqual(self.sse.looping_calls['user']['bob'].running, True)

    def test_add_connection(self):
        lc_mock = MockLoopingCall(running=True)
        self.sse.looping_calls['user'] = {'bob': lc_mock}
        request = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request, request.postpath)
        self.assertEqual(request, self.sse.connections['user']['bob'][0])

        # Add another connection to the same feed
        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request2, request2.postpath)
        self.assertEqual(request2, self.sse.connections['user']['bob'][1])

    def test_remove_connection(self):
        # add the looping call and two connections
        lc_mock = MockLoopingCall(running=True)
        self.sse.looping_calls['user'] = {'bob': lc_mock}

        request = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request, request.postpath)

        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request2, request2.postpath)

        # remove the first connection
        self.sse.remove_connection(request, self.key)
        self.assertEqual(len(self.sse.connections['user']['bob']), 1)

        # remove the second connection
        self.sse.remove_connection(request2, self.key)
        self.assertEqual(len(self.sse.connections['user']['bob']), 0)

        # since we removed all the connections the looping_call is removed
        self.assertEqual(self.sse.looping_calls['user'], {})

        # so we need to add it back in for testing purposes
        self.sse.looping_calls['user'] = {'bob': lc_mock}
        # add a third connection
        request3 = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request3, request3.postpath)
        self.assertEqual(len(self.sse.connections['user']['bob']), 1)

    def test_handle_request_invalid_path(self):
        request = DummyRequest(postpath=['not', 'valid'])
        self.sse.handle_request(request)
        self.assertFalse('not' in self.sse.connections)

    @patch.object(SSEServer, 'add_looping_call')
    @patch.object(SSEServer, 'does_loopingcall_exist')
    def test_handle_request_valid(self, alc_mock, dlce_mock):
        alc_mock.return_value = None
        dlce_mock.return_value = True

        request = DummyRequest(postpath=['user', 'bob'])
        self.sse.handle_request(request)

        self.assertTrue('user' in self.sse.connections)
        self.assertTrue('bob.id.fedoraproject.org'
                        in self.sse.connections['user'])

    @patch.object(SSEServer, 'get_payload', return_value={'msg': 'unittest'})
    def test_write_messages_all_connections(self, pay_mock):
        # add requests
        request1 = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request1, request1.postpath)
        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse.add_connection(request2, request2.postpath)

        self.assertEqual(len(self.sse.connections['user']['bob']), 2)

        self.sse.write_messages_all_connections(['user', 'bob'])

        # req1 started the looping call so it gets an extra message
        self.assertEqual(request1.written, ["data: {'msg': 'unittest'}\r\n\r\n",
                                            "data: {'msg': 'unittest'}\r\n\r\n",
                                            ])
        self.assertEqual(request2.written, [
            "data: {'msg': 'unittest'}\r\n\r\n",
        ])

    @patch.object(SSEServer, 'get_payload', return_value={'msg': 'unittest'})
    def test_render_get(self, pay_mock):
        # add requests
        request1 = DummyRequest(postpath=['user', 'bob'])
        request2 = DummyRequest(postpath=['user', 'bob'])
        self.sse.render_GET(request=request1)
        self.sse.render_GET(request=request2)
        self.assertEqual(
            len(self.sse.connections['user']['bob.id.fedoraproject.org']), 2)

        # req1 started the looping call so it gets an extra message
        self.assertEqual(request1.written, ['',
                                            "data: {'msg': 'unittest'}\r\n\r\n",
                                            ])
        # req2 is waiting for the next cycle for it to be sent a message so its
        # empty
        self.assertEqual(request2.written, [''])
