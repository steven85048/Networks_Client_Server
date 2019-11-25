from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.client.state_handler.client_state import ClientState
from messaging_system.resources import opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException
import messaging_system.client.token_holder

class SubscribeState(ClientState):
    def __init__(self, subscribe_name):
        self.subscribe_name = subscribe_name
        super().__init__()

    def start_state(self):
        payload = ClientMessageFactory.subscribe(messaging_system.client.token_holder.token, self.subscribe_name)
        self.curr_request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
        super().start_state()

    def process_response(self, response):
        super().process_response(response)

        if( response[header_keys['OPCODE']] == opcodes['FAILED_SUBSCRIBE_ACK'] ):
            if( header_keys['ERROR_MESSAGE'] in response ):
                err_message = response[header_keys['ERROR_MESSAGE']]
            raise MalformedRequestException("Subscribe Failed from Server: {}".format(err_message))

        if( response[header_keys['OPCODE']] != opcodes['SUCCESSFUL_SUBSCRIBE_ACK'] ):
            raise MalformedRequestException("SUBSCRIBE_ACK expected in response")

        self.state_completed = True