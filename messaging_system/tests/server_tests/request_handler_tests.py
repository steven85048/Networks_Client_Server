import unittest
import json

from messaging_system.server.request_handler import RequestHandler
from messaging_system.server.client_connection_service import ClientConnectionService
from messaging_system.resources import opcodes, header_keys, MAGIC_NUMBER_1, MAGIC_NUMBER_2
from messaging_system.server.db_model import drop_all, create_all

class RequestHandlerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection_service = ClientConnectionService()

    def setUp(self):
        self.request_handler = RequestHandler(self.connection_service)

        self.connection_service.reset_session()
        drop_all(self.connection_service.engine)
        create_all(self.connection_service.engine)
        self._add_test_accounts()

        self.dummy_addr = ('127.0.0.1', 2000)

    def test_invalid_magic_number(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : 'X'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['HEADER_IDENTITY_INVALID'])
        self.assertEqual("Request Header Identity Incorrect: Invalid Magic Numbers in Request",
                         self.request_handler.curr_response[0][0][header_keys['ERROR_MESSAGE']])
        
    def test_invalid_login(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'wrong_pass'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['FAILED_LOGIN_ACK'])
        self.assertEqual("Request provided is malformed -- Error is: Login credentials invalid",
                         self.request_handler.curr_response[0][0][header_keys['ERROR_MESSAGE']])
        
    def test_valid_login(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['SUCCESSFUL_LOGIN_ACK'])

    def test_valid_logout(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGOUT'],
                              header_keys['TOKEN'] : token_val}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['LOGOUT_ACK'])

        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['MUST_LOGIN_FIRST_ERROR'])

    def test_missing_token_error(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)
        self.assertEqual("Request provided is malformed -- Error is: Token missing from request",
                         self.request_handler.curr_response[0][0][header_keys['ERROR_MESSAGE']])

    def test_invalid_subscribe_username_not_exists(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac5'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['FAILED_SUBSCRIBE_ACK'])
        self.assertEqual("Request provided is malformed -- Error is: Subscription error - The provided username does not exist",
                         self.request_handler.curr_response[0][0][header_keys['ERROR_MESSAGE']])
        
    def test_valid_subscribe(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['SUCCESSFUL_SUBSCRIBE_ACK'])
    
    def test_invalid_subscribe_duplicate(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)
        
        self.assertEqual("Request provided is malformed -- Error is: Subscription error - Already subscribed to this user",
                         self.request_handler.curr_response[0][0][header_keys['ERROR_MESSAGE']])
        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['FAILED_SUBSCRIBE_ACK'])

    def test_invalid_unsubscribe_not_exist(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['UNSUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['UNSUBSCRIBE_USERNAME'] : 'ac3'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual("Request provided is malformed -- Error is: Unsubscription error - Cannot unsubscribe from someone you are not already subscribed to",
                          self.request_handler.curr_response[0][0][header_keys['ERROR_MESSAGE']] )
        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['FAILED_UNSUBSCRIBE_ACK'])

    def test_valid_unsubscribe(self):
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['UNSUBSCRIBE'],
                              header_keys['TOKEN'] : token_val,
                              header_keys['UNSUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['SUCCESSFUL_UNSUBSCRIBE_ACK'])

    def test_post(self):
        # Login users ac1 and ac2
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val_1 = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac2',
                              header_keys['PASSWORD'] : 'pass2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val_2 = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        
        # Have user ac1 subscribe to user ac2
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val_1,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        # Have user ac2 post a message
        post_message = 'post_test'
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['POST'],
                              header_keys['TOKEN'] : token_val_2,
                              header_keys['MESSAGE'] : post_message}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['SUCCESSFUL_POST_ACK'])
        self.assertEqual(self.request_handler.curr_response[1][0][header_keys['OPCODE']], opcodes['FORWARD'])
        self.assertEqual(self.request_handler.curr_response[1][0][header_keys['MESSAGE']], post_message)
        self.assertEqual(self.request_handler.curr_response[1][0][header_keys['FROM_USERNAME']], 'ac2')

    def test_retrieve(self):
        # Login users ac1 and ac2
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac1',
                              header_keys['PASSWORD'] : 'pass1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val_1 = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac2',
                              header_keys['PASSWORD'] : 'pass2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val_2 = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]

        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['LOGIN'],
                              header_keys['USERNAME'] : 'ac3',
                              header_keys['PASSWORD'] : 'pass3'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        token_val_3 = self.request_handler.curr_response[0][0][header_keys["TOKEN"]]
        
        # Have user ac3 subscribe to user ac1
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val_3,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac1'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        # Have user ac3 subscribe to user ac2
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['SUBSCRIBE'],
                              header_keys['TOKEN'] : token_val_3,
                              header_keys['SUBSCRIBE_USERNAME'] : 'ac2'}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        # Have user ac1 post a message
        message_1 = "hello_from_1"
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['POST'],
                              header_keys['TOKEN'] : token_val_1,
                              header_keys['MESSAGE'] : message_1}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        # Have user ac2 post a message
        message_2 = "hello_from_2"
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['POST'],
                              header_keys['TOKEN'] : token_val_2,
                              header_keys['MESSAGE'] : message_2}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        # Have user ac3 get the two previous messages with a retrieve
        num_retrieve = 3
        payload = json.dumps({header_keys['MAGIC_NUM_1'] : MAGIC_NUMBER_1, 
                              header_keys['MAGIC_NUM_2'] : MAGIC_NUMBER_2,
                              header_keys['OPCODE'] : opcodes['RETRIEVE'],
                              header_keys['TOKEN'] : token_val_3,
                              header_keys['NUM_MESSAGES'] : num_retrieve}).encode()
        self.request_handler.handle_request(payload, self.dummy_addr)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['OPCODE']], opcodes['RETRIEVE_ACK'])
        self.assertEqual(self.request_handler.curr_response[1][0][header_keys['OPCODE']], opcodes['RETRIEVE_ACK'])
        self.assertEqual(self.request_handler.curr_response[2][0][header_keys['OPCODE']], opcodes['END_OF_RETRIEVE_ACK'])

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['MESSAGE']], message_2)
        self.assertEqual(self.request_handler.curr_response[1][0][header_keys['MESSAGE']], message_1)

        self.assertEqual(self.request_handler.curr_response[0][0][header_keys['FROM_USERNAME']], 'ac2')
        self.assertEqual(self.request_handler.curr_response[1][0][header_keys['FROM_USERNAME']], 'ac1')

    def _add_test_accounts(self):
        self.connection_service.add_account('ac1', 'pass1')
        self.connection_service.add_account('ac2', 'pass2')
        self.connection_service.add_account('ac3', 'pass3')
        self.connection_service.add_account('ac4', 'pass4')

if __name__ == '__main__':
    unittest.main()