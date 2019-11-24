# Multiplexes the user_input into the correct sublogic

from messaging_system.client.state_handler.login_state import LoginState

class InputHandler:
    def __init__(self, state_transition_manager):
        self.state_transition_manager = state_transition_manager

    def handle_input(self, user_input):
        self._multiplex_input(user_input)

    def _multiplex_input(self, user_input):
        if "login" in user_input:
            self._handle_login(user_input)
        elif "subscribe" in user_input:
            pass
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
        self.state_transition_manager.transition_to_state(login_state)

    def _handle_subscribe(self, user_input):
        pass