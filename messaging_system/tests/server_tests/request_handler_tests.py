import unittest
import json

from messaging_system.server.request_handler import RequestHandler
from messaging_system.server.client_connection_service import ClientConnectionService
from messaging_system.resources import opcodes, header_keys, MAGIC_NUMBER_1, MAGIC_NUMBER_2

class RequestHandlerTests(unittest.TestCase):
    def setUp(self):
        self.connection_service = ClientConnectionService()

        #Add dummy accounts
        self.connection_service.add_account('ac1', 'pass1')
        self.connection_service.add_account('ac2', 'pass2')
        self.connection_service.add_account('ac3', 'pass3')
        self.connection_service.add_account('ac4', 'pass4')

        self.request_handler = RequestHandler(self.connection_service)
        self.dummy_addr = ('127.0.0.1', 2000)

    def test_invalid_magic_number(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : 'X'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][header_keys['OPCODE']], opcodes['HEADER_IDENTITY_INVALID'])

    def test_invalid_login(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'wrong_pass'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][header_keys['OPCODE']], opcodes['FAILED_LOGIN_ACK'])

    def test_valid_login(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][header_keys['OPCODE']], opcodes['SUCCESSFUL_LOGIN_ACK'])


if __name__ == '__main__':
    unittest.main()