import json

from messaging_system.client.forward_handler import ForwardHandler
from messaging_system.resources import MAGIC_NUMBER_1, MAGIC_NUMBER_2, opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException

class ResponseHandler:
    def __init__(self, state_transition_manager):
        self.forward_handler = ForwardHandler()
        self.state_transition_manager = state_transition_manager

    def handle_response(self, response):
        decoded_payload = json.loads( response.decode() )
        print("Response received: {}".format(decoded_payload))

        self.is_response_valid_initial_check(decoded_payload)

        if( decoded_payload[header_keys['OPCODE']] == opcodes['SESSION_RESET'] ):
            self.state_transition_manager.reset()
        elif( not self.forward_handler.handle_forwarding( decoded_payload )):
            self.state_transition_manager.process_response(decoded_payload)

    def is_response_valid_initial_check(self, response):
        if( not header_keys['MAGIC_NUM_1'] in response 
            or not header_keys['MAGIC_NUM_2'] in response 
            or response[header_keys['MAGIC_NUM_1']] != MAGIC_NUMBER_1
            or response[header_keys['MAGIC_NUM_2']] != MAGIC_NUMBER_2 ):
            raise MalformedRequestException("Magic Numbers Set Incorrectly")

        if( not header_keys['OPCODE'] in response ):
            raise MalformedRequestException("Missing OPCODE in response")