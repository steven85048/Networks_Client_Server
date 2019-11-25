# Multiplexes the user_input into the correct sublogic

from messaging_system.client.state_handler.login_state import LoginState
from messaging_system.client.state_handler.subscribe_state import SubscribeState
from messaging_system.client.exceptions import MalformedUserInputException

class InputHandler:
    def __init__(self, state_transition_manager):
        self.state_transition_manager = state_transition_manager

    def handle_input(self, user_input):
        self._multiplex_input(user_input)

    def _multiplex_input(self, user_input):
        if "login" in user_input:
            self._handle_login(user_input)
        elif "subscribe" in user_input:
            self._handle_subscribe(user_input)
        elif "unsubscribe" in user_input:
            pass
        elif "post" in user_input:
            pass
        elif "retrieve" in user_input:
            pass

    def _handle_login(self, user_input):
        op_split = user_input.split('#')[1]
        auth_split = op_split.split('&')

        username = auth_split[0]
        password = auth_split[1]

        login_state = LoginState(username, password)

        try:
            self.state_transition_manager.transition_to_state(login_state)
        except MalformedUserInputException as err:
            print(err)

    def _handle_subscribe(self, user_input):
        subscribe_name = user_input.split('#')[1]

        subscribe_state = SubscribeState(subscribe_name)

        try:
            self.state_transition_manager.transition_to_state(subscribe_state)
        except MalformedUserInputException as err:
            print(err)