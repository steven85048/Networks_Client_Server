from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.client.state_handler.client_state import ClientState
from messaging_system.resources import opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException
import messaging_system.client.token_holder

class UnsubscribeState(ClientState):
    def __init__(self, unsubscribe_name):
        self.unsubscribe_name = unsubscribe_name
        super().__init__()

    def start_state(self):
        payload = ClientMessageFactory.unsubscribe(messaging_system.client.token_holder.token, self.unsubscribe_name)
        self.curr_request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
        super().start_state()

    def process_response(self, response):
        super().process_response(response)

        if( response[header_keys['OPCODE']] == opcodes['FAILED_UNSUBSCRIBE_ACK'] ):
            print("unsubscribe_ack#failed")

            if( header_keys['ERROR_MESSAGE'] in response ):
                err_message = response[header_keys['ERROR_MESSAGE']]
            raise MalformedRequestException("Unsubscribe Failed from Server: {}".format(err_message))

        if( response[header_keys['OPCODE']] != opcodes['SUCCESSFUL_UNSUBSCRIBE_ACK'] ):
            raise MalformedRequestException("UNSUBSCRIBE_ACK expected in response")

        print("unsubscribe_ack#successful")

        self.state_completed = True