# This class provides an asynchronous mechanism for other classes to change state
# It holds the current state, and allows multiple threads to interact with this state without deadlocking
# The threads that currently interact with this class are:
# (a) The user input thread
# (b) The response listener thread

from threading import Lock

from messaging_system.client.exceptions import MalformedRequestException
from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.packet_sender_utilities import send_packet
import messaging_system.client.token_holder

class StateTransitionManager:
    def __init__(self):
        self.curr_state = None
        self.state_lock = Lock()

    def transition_to_state(self, state ):
        with self.state_lock:
            if( not self.curr_state is None and not self.curr_state.state_transition_permitted() ):
                raise MalformedRequestException("Invalid state change")

            self.curr_state = state
            self.curr_state.start_state()

    def process_response(self, response):
        with self.state_lock:
            if( self.curr_state is None ):
                raise MalformedRequestException("Cannot process response from an empty state")

            self.curr_state.process_response(response)

    def reset(self):
        with self.state_lock:
            self.curr_state = None
            print("Client state reset!")

            # Send back a RESET
            request = []
            payload = ClientMessageFactory.session_reset(messaging_system.client.token_holder.token)
            request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
            send_packet(request)

            messaging_system.client.token_holder.token = None