from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.client.state_handler.client_state import ClientState
from messaging_system.resources import opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException
import messaging_system.client.token_holder

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
        if( response[header_keys['OPCODE']] == opcodes['FAILED_LOGIN_ACK'] ):
            print("login_ack#failed")

            if( header_keys['ERROR_MESSAGE'] in response ):
                err_message = response[header_keys['ERROR_MESSAGE']]
            raise MalformedRequestException("Login Failed from Server: {}".format(err_message))

        if( response[header_keys['OPCODE']] != opcodes['SUCCESSFUL_LOGIN_ACK'] ):
            raise MalformedRequestException("LOGIN_ACK expected in response")

        if( not header_keys['TOKEN'] in response ):
            raise MalformedRequestException("TOKEN expected in response")

        # Get and store token in global module
        token = response[header_keys['TOKEN']]
        messaging_system.client.token_holder.token = token

        print("login_ack#successful")

        self.state_completed = True