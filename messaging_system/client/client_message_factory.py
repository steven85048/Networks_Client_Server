from messaging_system.resources import opcodes, MAGIC_NUMBER_1, MAGIC_NUMBER_2, header_keys

class ClientMessageFactory():
    @staticmethod
    def login(username, password):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['LOGIN']
        header[header_keys['USERNAME']] = username
        header[header_keys['PASSWORD']] = password
        return header

    @staticmethod
    def logout(token):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['LOGOUT']
        header[header_keys['TOKEN']] = token
        return header

    @staticmethod
    def session_reset(token):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['SESSION_RESET']
        if( not token is None ):
            header[header_keys['TOKEN']] = token
        return header

    @staticmethod
    def subscribe(token, from_username):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['SUBSCRIBE']
        header[header_keys['TOKEN']] = token
        header[header_keys['SUBSCRIBE_USERNAME']] = from_username
        return header

    @staticmethod
    def unsubscribe(token, from_username):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['UNSUBSCRIBE']
        header[header_keys['TOKEN']] = token
        header[header_keys['UNSUBSCRIBE_USERNAME']] = from_username
        return header

    @staticmethod
    def post(token, message):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['POST']
        header[header_keys['TOKEN']] = token
        header[header_keys['MESSAGE']] = message
        return header

    @staticmethod
    def retrieve(token, num_messages):
        header = ClientMessageFactory._create_base_request()
        header[header_keys['OPCODE']] = opcodes['RETRIEVE']
        header[header_keys['TOKEN']] = token
        header[header_keys['NUM_MESSAGES']] = num_messages
        return header

    @staticmethod
    def _create_base_request():
        header = {}

        header[header_keys['MAGIC_NUM_1']] = MAGIC_NUMBER_1
        header[header_keys['MAGIC_NUM_2']] = MAGIC_NUMBER_2

        return header