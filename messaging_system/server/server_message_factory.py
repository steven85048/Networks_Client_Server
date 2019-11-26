# Utility functions for creating the payloads for server->client messages

from messaging_system.resources import opcodes, MAGIC_NUMBER_1, MAGIC_NUMBER_2, header_keys

class ServerMessageFactory:

    @staticmethod
    def invalid_header_identity(error_message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['HEADER_IDENTITY_INVALID']
        header[header_keys['ERROR_MESSAGE']] = error_message
        return header

    @staticmethod
    def must_login_first_error(error_message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['MUST_LOGIN_FIRST_ERROR'] 
        header[header_keys['ERROR_MESSAGE']] = error_message
        return header

    @staticmethod
    def successful_login_ack(token_val):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['SUCCESSFUL_LOGIN_ACK']
        header[header_keys['TOKEN']] = token_val
        return header

    @staticmethod
    def failed_login_ack(error_message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['FAILED_LOGIN_ACK']
        header[header_keys['ERROR_MESSAGE']] = error_message
        return header

    @staticmethod
    def successful_subscribe_ack():
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['SUCCESSFUL_SUBSCRIBE_ACK']
        return header

    @staticmethod
    def failed_subscribe_ack(error_message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['FAILED_SUBSCRIBE_ACK']
        header[header_keys['ERROR_MESSAGE']] = error_message
        return header

    @staticmethod
    def successful_unsubscribe_ack():
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['SUCCESSFUL_UNSUBSCRIBE_ACK']
        return header

    @staticmethod
    def failed_unsubscribe_ack(error_message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['FAILED_UNSUBSCRIBE_ACK']
        header[header_keys['ERROR_MESSAGE']] = error_message
        return header

    @staticmethod
    def successful_post_ack():
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['SUCCESSFUL_POST_ACK']
        return header

    @staticmethod
    def failed_post_ack(error_message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['FAILED_POST_ACK']
        header[header_keys['ERROR_MESSAGE']] = error_message
        return header

    @staticmethod
    def forward(source_username, message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['FORWARD']
        header[header_keys['FROM_USERNAME']] = source_username
        header[header_keys['MESSAGE']] = message
        return header

    @staticmethod
    def retrieve_ack(source_username, message):
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['RETRIEVE_ACK']
        header[header_keys['FROM_USERNAME']] = source_username
        header[header_keys['MESSAGE']] = message
        return header

    @staticmethod
    def end_of_retrieve_ack():
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['END_OF_RETRIEVE_ACK']
        return header

    @staticmethod
    def logout_ack():
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['LOGOUT_ACK']
        return header

    @staticmethod
    def session_reset():
        header = ServerMessageFactory.create_base_request()
        header[header_keys['OPCODE']] = opcodes['SESSION_RESET']
        return header

    @staticmethod
    def create_base_request():
        header = {}

        header[header_keys['MAGIC_NUM_1']] = MAGIC_NUMBER_1
        header[header_keys['MAGIC_NUM_2']] = MAGIC_NUMBER_2

        return header
        
