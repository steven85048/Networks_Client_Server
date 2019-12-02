# This class handles miscellaneous requests from clients and calls various more specific handlers

import json

from messaging_system.resources import opcodes, MAGIC_NUMBER_1, MAGIC_NUMBER_2, header_keys
from messaging_system.server.exceptions import MalformedRequestHeaderException, InvalidTokenException, MalformedRequestIdentityException
from messaging_system.server.server_message_factory import ServerMessageFactory
from messaging_system.packet_sender_utilities import send_packet

class RequestHandler:
    def __init__(self, client_connection_service):
        self.client_connection_service = client_connection_service

    def handle_request(self, data, addr):
        # The input comes in as a json string encoded as bytes, so we decode it and deserialize the json from a string
        decoded_payload = json.loads( data.decode() )
        print("")
        print("Received payload: {}".format(decoded_payload))

        self.curr_response = []
        self.curr_addr = addr

        try: 
            self._multiplex_request(decoded_payload)
        except MalformedRequestIdentityException as err:
            self.curr_response.append((ServerMessageFactory.invalid_header_identity(str(err)), self.curr_addr))
            send_packet(self.curr_response)
        except InvalidTokenException as err: 
            # Send must-login-first-error
            self.curr_response.append((ServerMessageFactory.must_login_first_error(str(err)), self.curr_addr))
            send_packet(self.curr_response)

    # Depending on the opcode, handle the request in a different manner
    def _multiplex_request(self, payload):
        if( not header_keys['MAGIC_NUM_1'] in payload 
            or not header_keys['MAGIC_NUM_2'] in payload 
            or payload[header_keys['MAGIC_NUM_1']] != MAGIC_NUMBER_1
            or payload[header_keys['MAGIC_NUM_2']] != MAGIC_NUMBER_2 ):
            raise MalformedRequestIdentityException("Invalid Magic Numbers in Request")

        if( not header_keys['OPCODE'] in payload ):
            raise MalformedRequestIdentityException("Missing Opcode in request")

        if( payload[header_keys['OPCODE']] == opcodes['LOGIN'] ):
            try:
                user_token = self._handle_login(payload, self.curr_addr)       
                self.curr_response.append((ServerMessageFactory.successful_login_ack(user_token['token_val']), self.curr_addr))
            except MalformedRequestHeaderException as err:
                self.curr_response.append((ServerMessageFactory.failed_login_ack(str(err)), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['SUBSCRIBE']):
            try: 
                self._handle_subscribe(payload)
                self.curr_response.append((ServerMessageFactory.successful_subscribe_ack(), self.curr_addr))
            except MalformedRequestHeaderException as err: 
                self.curr_response.append((ServerMessageFactory.failed_subscribe_ack(str(err)), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['UNSUBSCRIBE']):
            try:
                self._handle_unsubscribe(payload)
                self.curr_response.append((ServerMessageFactory.successful_unsubscribe_ack(), self.curr_addr))
            except MalformedRequestHeaderException as err:
                self.curr_response.append((ServerMessageFactory.failed_unsubscribe_ack(str(err)), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['POST']):
            try: 
                message_details = self._handle_post(payload)
                self.curr_response.append((ServerMessageFactory.successful_post_ack(), self.curr_addr))

                for subscriber_token in message_details['SUBSCRIBER_TOKENS']:
                    self.curr_response.append((ServerMessageFactory.forward(message_details['FROM_USERNAME'], 
                                                                            message_details['FORWARD_MESSAGE']), 
                                              (subscriber_token['client_addr']['ip_addr'], subscriber_token['client_addr']['port'])))
            
            except MalformedRequestHeaderException as err:
                self.curr_response.append((ServerMessageFactory.failed_post_ack(str(err)), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['FORWARD_ACK']):
            try: 
                self._handle_forward_ack(payload)
            except MalformedRequestHeaderException as err:
                self.curr_response.append((ServerMessageFactory.session_reset(), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['RETRIEVE']):
            try: 
                messages_to_send = self._handle_retrieve(payload)
                for message_to_send in messages_to_send:
                    message = message_to_send[0]
                    from_username = message_to_send[1]
                    self.curr_response.append((ServerMessageFactory.retrieve_ack(from_username, message), self.curr_addr))
            
                # Send by end of retrieve ACK after sending all messages
                self.curr_response.append((ServerMessageFactory.end_of_retrieve_ack(), self.curr_addr))

            except MalformedRequestHeaderException as err:
                self.curr_response.append((ServerMessageFactory.session_reset(), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['LOGOUT'] ):
            try: 
                self._handle_logout(payload)
                self.curr_response.append((ServerMessageFactory.logout_ack(), self.curr_addr))
            except MalformedRequestHeaderException as err:   
                self.curr_response.append((ServerMessageFactory.session_reset(), self.curr_addr))
        elif( payload[header_keys['OPCODE']] == opcodes['SESSION_RESET']):
            try:
                self._handle_session_reset(payload)
            except MalformedRequestHeaderException as err:
                self.curr_response.append((ServerMessageFactory.session_reset(), self.curr_addr))
        else:
            raise MalformedRequestIdentityException("Opcode is invalid")
        
        send_packet(self.curr_response)

    def validate_token_exists(func):
        def validate(self, payload):
            # Special case for login, since token is not set of course
            if( not header_keys["TOKEN"] in payload):
                raise MalformedRequestHeaderException("Token missing from request")

            return func(self, payload)

        return validate

    def _handle_login(self, payload, addr):
        if( not( header_keys['USERNAME'] in payload or header_keys['PASSWORD'] in payload ) ):
            raise MalformedRequestHeaderException("Missing login information in LOGIN request")

        token = self.client_connection_service.login(payload[header_keys['USERNAME']], payload[header_keys['PASSWORD']], addr)
        if token is None:
            raise MalformedRequestHeaderException("Login credentials invalid")
        
        return token

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

    #@return message_details - dict of three elements
    # SUBSCRIBER_TOKENS - array of tokens corresponding to who the message should be forwarded to
    # FROM_USERNAME - the username from which the message was sent
    # FORWARD_MESSAGE - the message to be forwarded
    @validate_token_exists
    def _handle_post(self, payload):
        if( not header_keys['MESSAGE'] in payload):
            raise MalformedRequestHeaderException("Missing message in POST request")

        subscriber_tokens, from_username = self.client_connection_service.post(payload[header_keys['TOKEN']], payload[header_keys['MESSAGE']])
        forward_message = payload[header_keys['MESSAGE']]

        message_details = dict( SUBSCRIBER_TOKENS = subscriber_tokens, FROM_USERNAME = from_username, FORWARD_MESSAGE = forward_message )
        return message_details

    @validate_token_exists
    def _handle_forward_ack(self, payload):
        pass

    #@return messages_to_send - array of a two tuple with ( message, from_username )
    # Essentially returns the set of messages retrieved
    @validate_token_exists
    def _handle_retrieve(self, payload):
        if( not header_keys['NUM_MESSAGES'] in payload):
            raise MalformedRequestHeaderException("Missing number of message in RETRIEVE request")

        messages_to_send = self.client_connection_service.retrieve(payload[header_keys['TOKEN']], payload[header_keys['NUM_MESSAGES']])
        return messages_to_send

    @validate_token_exists
    def _handle_logout(self, payload):
        self.client_connection_service.logout(payload[header_keys['TOKEN']])

    # Session reset is essentially the same state as logged out in this use case
    def _handle_session_reset(self, payload):
        if( header_keys['TOKEN'] in payload ):
            self.client_connection_service.logout(payload[header_keys['TOKEN']])