from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.client.state_handler.client_state import ClientState
from messaging_system.resources import opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException
import messaging_system.client.token_holder

class RetrieveState(ClientState):
    def __init__(self, num_messages):
        self.num_messages = num_messages
        super().__init__()

    def start_state(self):
        payload = ClientMessageFactory.retrieve(messaging_system.client.token_holder.token, self.num_messages)
        self.curr_request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
        super().start_state()

    def process_response(self, response):
        if( response[header_keys['OPCODE']] == opcodes['RETRIEVE_ACK'] ):
            retrieved_message = response[header_keys['MESSAGE']]
            from_username = response[header_keys['FROM_USERNAME']]

            print("{from_username} : {retrieved_message}".format(from_username = from_username, retrieved_message = retrieved_message))
        elif( response[header_keys['OPCODE']] == opcodes['END_OF_RETRIEVE_ACK'] ):
            self.state_completed = True
        else:
            raise MalformedRequestException("RETRIEVE_ACK expected in response")