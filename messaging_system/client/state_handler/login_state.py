from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.client.state_handler.client_state import ClientState
from messaging_system.resources import opcodes, header_keys

class LoginState(ClientState):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        super().__init__()

    def start_state(self):
        payload = ClientMessageFactory.login(self.username, self.password)
        self.curr_request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
        super().start_state()

    def process_response(self, response):
        super().process_response(response)

        if( header_keys['OPCODE'] == opcodes['FAILED_LOGIN_ACK'] ):
            if( header_keys['ERROR_MESSAGE'] in response ):
                err_message = response[header_keys['ERROR_MESSAGE']]
            raise Exception("Login Failed from Server: {}".format(err_message))

        if( header_keys['OPCODE'] != opcodes['SUCCESSFUL_LOGIN_ACK'] ):
            raise Exception("LOGIN_ACK expected in response")

        if( not header_keys['TOKEN'] in response ):
            raise Exception("TOKEN expected in response")

        # Get the token and store it for future uses (TODO)
        token = header_keys['TOKEN']

        self.state_completed = True