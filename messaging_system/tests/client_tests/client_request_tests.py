
from messaging_system.client.state_transition_manager import StateTransitionManager
from messaging_system.client.input_handler import InputHandler
from messaging_system.client.response_handler import ResponseHandler
from messaging_system.client.exceptions import MalformedRequestException, MalformedUserInputException
from messaging_system.resources import opcodes, header_keys, MAGIC_NUMBER_1, MAGIC_NUMBER_2
from messaging_system.server.server_message_factory import ServerMessageFactory
import messaging_system.client.token_holder

import json
import unittest

class ClientRequestTests(unittest.TestCase):
    def setUp(self):
        messaging_system.client.token_holder.token = None
        self.state_transition_manager = StateTransitionManager()
        self.input_handler = InputHandler( self.state_transition_manager )
        self.response_handler = ResponseHandler( self.state_transition_manager )

    def test_invalid_login(self):
        input = "login#ac1&wrong_pass"
        self.input_handler.handle_input(input)

        response = ServerMessageFactory.failed_login_ack("Incorrect Login Information")
        response = json.dumps(response).encode()

        with self.assertRaises(MalformedRequestException) as err:
            self.response_handler.handle_response(response)

        self.assertTrue("Login Failed from Server" in str(err.exception))

    def test_valid_login(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

        token_number = 324
        response = ServerMessageFactory.successful_login_ack(token_number)
        response = json.dumps(response).encode()
        self.response_handler.handle_response(response)
        
        self.assertTrue(self.state_transition_manager.curr_state.state_completed)
        self.assertEqual(messaging_system.client.token_holder.token, token_number)

    def test_missing_token(self):
        input = "subscribe#client"

        with self.assertRaises(MalformedUserInputException) as err:
            self.input_handler.handle_input(input)

        self.assertTrue("Cannot make that type of request until logged in" in str(err.exception))

    def test_subscribe(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

        token_number = 123
        response = ServerMessageFactory.successful_login_ack(token_number)
        response = json.dumps(response).encode()
        self.response_handler.handle_response(response)

        input_2 = "subscribe#ac2"
        self.input_handler.handle_input(input_2)

        response_2 = ServerMessageFactory.successful_subscribe_ack()
        response_2 = json.dumps(response_2).encode()
        self.response_handler.handle_response(response_2)

        self.assertTrue(self.state_transition_manager.curr_state.state_completed)

    def test_server_err_subscribe(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

        token_number = 123
        response = ServerMessageFactory.successful_login_ack(token_number)
        response = json.dumps(response).encode()
        self.response_handler.handle_response(response)

        input_2 = "subscribe#ac2"
        self.input_handler.handle_input(input_2)

        response_2 = ServerMessageFactory.failed_subscribe_ack("Invalid subscribe")
        response_2 = json.dumps(response_2).encode()

        with self.assertRaises(MalformedRequestException) as err:
            self.response_handler.handle_response(response_2)

        self.assertTrue("Subscribe Failed from Server" in str(err.exception))
        self.assertFalse(self.state_transition_manager.curr_state.state_completed)

    def test_unsubscribe(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

        token_number = 123
        response = ServerMessageFactory.successful_login_ack(token_number)
        response = json.dumps(response).encode()
        self.response_handler.handle_response(response)

        input_2 = "unsubscribe#ac2"
        self.input_handler.handle_input(input_2)

        response_2 = ServerMessageFactory.successful_unsubscribe_ack()
        response_2 = json.dumps(response_2).encode()
        self.response_handler.handle_response(response_2)

        self.assertTrue(self.state_transition_manager.curr_state.state_completed)

    def test_server_err_unsubscribe(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

        token_number = 123
        response = ServerMessageFactory.successful_login_ack(token_number)
        response = json.dumps(response).encode()
        self.response_handler.handle_response(response)

        input_2 = "unsubscribe#ac2"
        self.input_handler.handle_input(input_2)

        response_2 = ServerMessageFactory.failed_unsubscribe_ack("Invalid unsubscribe")
        response_2 = json.dumps(response_2).encode()

        with self.assertRaises(MalformedRequestException) as err:
            self.response_handler.handle_response(response_2)

        self.assertTrue("Unsubscribe Failed from Server" in str(err.exception))
        self.assertFalse(self.state_transition_manager.curr_state.state_completed)

    def test_post(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

        token_number = 123
        response = ServerMessageFactory.successful_login_ack(token_number)
        response = json.dumps(response).encode()
        self.response_handler.handle_response(response)

        input_2 = "post#message"
        self.input_handler.handle_input(input_2)

        response_2 = ServerMessageFactory.successful_post_ack()
        response_2 = json.dumps(response_2).encode()
        self.response_handler.handle_response(response_2)

        self.assertTrue(self.state_transition_manager.curr_state.state_completed)

if __name__ == '__main__':
    unittest.main()