import json

from messaging_system.client.forward_handler import ForwardHandler

class ResponseHandler:
    def __init__(self, state_transition_manager):
        self.forward_handler = ForwardHandler()
        self.state_transition_manager = state_transition_manager

    def handle_response(self, response):
        decoded_payload = json.loads( response.decode() )
        print("Response received: {}".format(decoded_payload))

        if( not self.forward_handler.handle_forwarding( decoded_payload )):
            self.state_transition_manager.process_response(decoded_payload)