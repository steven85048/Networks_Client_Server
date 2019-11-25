import json

class ResponseHandler:
    def __init__(self, state_transition_manager):
        self.state_transition_manager = state_transition_manager

    def handle_response(self, response):
        decoded_payload = json.loads( response.decode() )
        print(decoded_payload)
        self.state_transition_manager.process_response(decoded_payload)