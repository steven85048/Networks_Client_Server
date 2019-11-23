# This class handles miscellaneous requests from clients and calls various more specific handlers

import json

from messaging_system.resources import opcodes, MAGIC_NUMBER_1, MAGIC_NUMBER_2, header_keys
from messaging_system.server.exceptions import MalformedRequestHeaderException, InvalidTokenException, MalformedRequestIdentityException
from messaging_system.server.server_message_factory import ServerMessageFactory

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
            response = ServerMessageFactory.invalid_header_identity(str(err))

    # Depending on the opcode, handle the request in a different manner
    def _multiplex_request(self, payload):
        if( not header_keys['OPCODE'] in payload ):
            raise MalformedRequestIdentityException("Missing Opcode in request")

        if( not header_keys['MAGIC_NUM_1'] in payload 
            or not header_keys['MAGIC_NUM_2'] in payload 
            or not payload[header_keys['MAGIC_NUM_1']] != MAGIC_NUMBER_1
            or not payload[header_keys['MAGIC_NUM_2']] != MAGIC_NUMBER_2 ):
            raise MalformedRequestIdentityException("Invalid Magic Numbers in Request")

        # NOTE that some exceptions below are not relayed back to the user since
        # not mandated

        if( payload[header_keys['OPCODE']] == opcodes['LOGIN'] ):
            try:
                self._handle_login(payload)
            except Exception as err:
                print(err)
                response = ServerMessageFactory.failed_login_ack(str(err))
        elif( payload.opcode == opcodes['SUBSCRIBE']):
            try: 
                self._handle_subscribe(payload)
            except Exception as err:
                print(err)
                response = ServerMessageFactory.failed_subscribe_ack(str(err))
        elif( payload.opcode == opcodes['UNSUBSCRIBE']):
            try:
                self._handle_unsubscribe(payload)
            except Exception as err:
                print(err)
        elif( payload.opcode == opcodes['POST']):
            try: 
                self._handle_post(payload)
            except Exception as err:
                print(err)
                response = ServerMessageFactory.failed_post_ack(str(err))
        elif( payload.opcode == opcodes['FORWARD_ACK']):
            try: 
                self._handle_forward_ack(payload)
            except Exception as err:
                print(err)
        elif( payload.opcode == opcodes['RETRIEVE']):
            try: 
                self._handle_retrieve(payload)
            except Exception as err:
                print(err)
        elif( payload.opcode == opcodes['LOGOUT'] ):
            try: 
                self._handle_logout(payload)
            except Exception as err:
                print(err)
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
                print(err)
                response = ServerMessageFactory.must_login_first_error(str(err))
            except Exception as err:
                print(err)
                raise

        return validate

    def _handle_login(self, payload):
        if( not( header_keys['USERNAME'] in payload or header_keys['PASSWORD'] in payload ) ):
            raise MalformedRequestHeaderException("Missing login information in LOGIN request")

        self.client_connection_service.login(payload[header_keys['USERNAME']], payload[header_keys['PASSWORD']])
        

    @validate_token_exists
    def _handle_subscribe(self, payload):
        if( not header_keys['SUBSCRIBE_USERNAME'] in payload ):
            raise MalformedRequestHeaderException("Missing subscribe_username in SUBSCRIBE request")
    
        self.client_connection_service.subscribe(payload[header_keys['TOKEN']], payload[header_keys['SUBSCRIBE_USERNAME']])

    @validate_token_exists
    def _handle_unsubscribe(self, payload):
        if( not header_keys['UNSUBSCRIBE_USERNAME'] in payload ):
            raise MalformedRequestHeaderException("Missing unsubscribe_username in SUBSCRIBE request")

        self.client_connection_service.unsubscribe(payload[header_keys['TOKEN']], payload[header_keys['UNSUBSCRIBE_USERNAME']])

    @validate_token_exists
    def _handle_post(self, payload):
        if( not header_keys['MESSAGE'] in payload):
            raise MalformedRequestHeaderException("Missing message in POST request")

        self.client_connection_service.post(payload[header_keys['TOKEN']], payload[header_keys['MESSAGE']])

    @validate_token_exists
    def _handle_forward_ack(self, payload):
        pass

    @validate_token_exists
    def _handle_retrieve(self, payload):
        if( not header_keys['NUM_MESSAGES'] in payload):
            raise MalformedRequestHeaderException("Missing number of message in RETRIEVE request")

        self.client_connection_service.retrieve(payload[header_keys['TOKEN']], payload[header_keys['NUM_MESSAGES']])

    @validate_token_exists
    def _handle_logout(self, payload):
        self.client_connection_service.logout(payload[header_keys['TOKEN']])