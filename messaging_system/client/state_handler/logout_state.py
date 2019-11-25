from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.client.state_handler.client_state import ClientState
from messaging_system.resources import opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException
import messaging_system.client.token_holder

class LogoutState(ClientState):
    def __init__(self):
        super().__init__()

    def start_state(self):
        payload = ClientMessageFactory.logout()
        self.curr_request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
        super().start_state()

    def process_response(self, response):
        super().process_response(response)

        if( response[header_keys['OPCODE']] != opcodes['LOGOUT_ACK'] ):
            raise MalformedRequestException("LOGOUT_ACK expected in response")

        # Reset the token
        messaging_system.client.token_holder.token = None

        self.state_completed = True