
from messaging_system.client.state_transition_manager import StateTransitionManager
from messaging_system.client.input_handler import InputHandler
from messaging_system.client.response_handler import ResponseHandler
from messaging_system.client.exceptions import MalformedRequestException, MalformedUserInputException
from messaging_system.resources import opcodes, header_keys, MAGIC_NUMBER_1, MAGIC_NUMBER_2
from messaging_system.server.server_message_factory import ServerMessageFactory

import json
import unittest

class ClientRequestTests(unittest.TestCase):
    def setUp(self):
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
        input = "login#ac1&wrong_pass"
        self.input_handler.handle_input(input)

        response = ServerMessageFactory.successful_login_ack(324)
        response = json.dumps(response).encode()

        self.response_handler.handle_response(response)
        self.assertTrue(self.state_transition_manager.curr_state.state_completed)

if __name__ == '__main__':
    unittest.main()