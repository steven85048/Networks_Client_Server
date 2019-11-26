# ABC containing the interface methods that all client states should have
# These methods are important for the state_transition_manager

from abc import ABC, abstractmethod

from messaging_system.packet_sender_utilities import send_packet
from messaging_system.resources import header_keys, MAGIC_NUMBER_1, MAGIC_NUMBER_2
from messaging_system.client.exceptions import MalformedRequestException, MalformedUserInputException

import messaging_system.client.state_handler.login_state
import messaging_system.client.token_holder

class ClientState(ABC):

    def __init__(self):
        if( not isinstance(self, messaging_system.client.state_handler.login_state.LoginState) ):
            if( messaging_system.client.token_holder.token is None ):
                raise MalformedUserInputException("Cannot make that type of request until logged in")

        self.curr_request = []
        self.state_completed = False

    def state_transition_permitted(self):
        return self.state_completed

    # Child classes should set the curr_requests that need to be sent to the server
    @abstractmethod
    def start_state(self):
        send_packet(self.curr_request)

    @abstractmethod
    def process_response(self, response):
        pass