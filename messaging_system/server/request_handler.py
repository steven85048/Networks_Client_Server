# This class handles miscellaneous requests from clients and calls various more specific handlers

import json

from messaging_system.resources import opcodes
from messaging_system.server.exceptions import MalformedRequestHeaderException

class RequestHandler:
    def __init__(self, client_connection_service):
        self.client_connection_service = client_connection_service

    def handle_request(self, data, addr):
        print("Read thread processing request")

        # The input comes in as a json string encoded as bytes, so we decode it and deserialize the json from a string
        decoded_payload = json.loads( data.decode() )
        print(decoded_payload)

        self._multiplex_request(decoded_payload)

    # Depending on the opcode, handle the request in a different manner
    def _multiplex_request(self, payload):
        if( not payload.opcode ):
            raise MalformedRequestHeaderException("Missing Opcode in request")

        if( payload.opcode == opcodes['LOGIN'] ):
            self._handle_login(payload)
        elif( payload.opcode == opcodes['SUBSCRIBE']):
            self._handle_subscribe(payload)
        elif( payload.opcode == opcodes['UNSUBSCRIBE']):
            self._handle_unsubscribe(payload)
        elif( payload.opcode == opcodes['POST']):
            self._handle_post(payload)
        elif( payload.opcode == opcodes['FORWARD_ACK']):
            self._handle_forward_ack(payload)
        elif( payload.opcode == opcodes['RETRIEVE']):
            self._handle_retrieve(payload)
        elif( payload.opcode == opcodes['LOGOUT'] ):
            self._handle_logout(payload)
        else
            raise MalformedRequestHeaderException("Opcode {payload.opcode} is invalid")
        
    def validate_token_exists(func):
        def validate(self, payload):
            if( not 'token' in payload):
                raise MalformedRequestHeaderException("Token missing from request")
            return func(self, payload)

        return validate

    def _handle_login(self, payload):
        if( not( 'username' in payload or 'password' in payload ) ):
            raise MalformedRequestHeaderException("Missing login information in LOGIN request")

        self.client_connection_service.login(payload['username'], payload['password'])

    @validate_token_exists
    def _handle_subscribe(self, payload):
        if( not 'subscribe_username' in payload ):
            raise MalformedRequestHeaderException("Missing subscribe_username in SUBSCRIBE request")
    
        self.client_connection_service.subscribe(payload['token'], payload['subscribe_username'])

    @validate_token_exists
    def _handle_unsubscribe(self, payload):
        if( not 'unsubscribe_username' in payload ):
            raise MalformedRequestHeaderException("Missing unsubscribe_username in SUBSCRIBE request")

        self.client_connection_service.unsubscribe(payload['token'], payload['unsubscribe_username'])

    @validate_token_exists
    def _handle_post(self, payload):
        if( not 'message' in payload):
            raise MalformedRequestHeaderException("Missing message in POST request")

        self.client_connection_service.post(payload['token'], payload['message'])

    @validate_token_exists
    def _handle_forward_ack(self):
        pass

    @validate_token_exists
    def _handle_retrieve(self):
        if( not 'num_messages' in payload):
            raise MalformedRequestHeaderException("Missing number of message in RETRIEVE request")

        self.client_connection_service.retrieve(payload['token'], payload['num_messages'])

    @validate_token_exists
    def _handle_logout(self):
        self.client_connection_service.logout(payload['token'])