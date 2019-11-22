# This class handles miscellaneous requests from clients and calls various more specific handlers

import json

from messaging_system.resources import opcodes, MAGIC_NUMBER_1, MAGIC_NUMBER_2
from messaging_system.server.exceptions import MalformedRequestHeaderException, InvalidTokenException, MalformedRequestIdentityException

class RequestHandler:
    def __init__(self, client_connection_service):
        self.client_connection_service = client_connection_service

    def handle_request(self, data, addr):
        print("Read thread processing request")

        # The input comes in as a json string encoded as bytes, so we decode it and deserialize the json from a string
        decoded_payload = json.loads( data.decode() )
        print(decoded_payload)

        self.curr_addr = addr

        try: 
            self._multiplex_request(decoded_payload)
        except MalformedRequestIdentityException as err:
            # Send back invalid header packet
            pass

    # Depending on the opcode, handle the request in a different manner
    def _multiplex_request(self, payload):
        if( not 'opcode' in payload ):
            raise MalformedRequestIdentityException("Missing Opcode in request")

        if( not 'magic_num_1' in payload 
            or not 'magic_num_2' in payload 
            or not payload['magic_num_1'] != MAGIC_NUMBER_1
            or not payload['magic_num_2'] != MAGIC_NUMBER_2 ):
            raise MalformedRequestIdentityException("Invalid Magic Numbers in Request")

        if( payload['opcode'] == opcodes['LOGIN'] ):
            try:
                self._handle_login(payload)
            except Exception as err:
                # Send 
                pass
        elif( payload.opcode == opcodes['SUBSCRIBE']):
            try: 
                self._handle_subscribe(payload)
            except Exception as err:
                pass

        elif( payload.opcode == opcodes['UNSUBSCRIBE']):
            try:
                self._handle_unsubscribe(payload)
            except Exception as err:
                pass
        elif( payload.opcode == opcodes['POST']):
            try: 
                self._handle_post(payload)
            except Exception as err:
                pass
        elif( payload.opcode == opcodes['FORWARD_ACK']):
            try: 
                self._handle_forward_ack(payload)
            except Exception as err:
                pass
        elif( payload.opcode == opcodes['RETRIEVE']):
            try: 
                self._handle_retrieve(payload)
            except Exception as err:
                pass
        elif( payload.opcode == opcodes['LOGOUT'] ):
            try: 
                self._handle_logout(payload)
            except Exception as err:
                pass                
        else:
            raise MalformedRequestIdentityException("Opcode {payload.opcode} is invalid")
        
    def validate_token_exists(func):
        def validate(self, payload):
            try: 
                # Special case for login, since token is not set of course
                if( not func.__name__ == '_handle_login' and not 'token' in payload):
                    raise MalformedRequestHeaderException("Token missing from request")
                func(self, payload)
            except InvalidTokenException as err:
                # Send must-login-first-error
                pass
            except Exception as err:
                print(err)
                raise

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
    def _handle_forward_ack(self, payload):
        pass

    @validate_token_exists
    def _handle_retrieve(self, payload):
        if( not 'num_messages' in payload):
            raise MalformedRequestHeaderException("Missing number of message in RETRIEVE request")

        self.client_connection_service.retrieve(payload['token'], payload['num_messages'])

    @validate_token_exists
    def _handle_logout(self, payload):
        self.client_connection_service.logout(payload['token'])