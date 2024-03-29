# Multiplexes the user_input into the correct sublogic

from messaging_system.client.state_handler.login_state import LoginState
from messaging_system.client.state_handler.logout_state import LogoutState
from messaging_system.client.state_handler.subscribe_state import SubscribeState
from messaging_system.client.state_handler.unsubscribe_state import UnsubscribeState
from messaging_system.client.state_handler.post_state import PostState
from messaging_system.client.state_handler.retrieve_state import RetrieveState
from messaging_system.client.exceptions import MalformedUserInputException

class InputHandler:
    def __init__(self, state_transition_manager):
        self.state_transition_manager = state_transition_manager

    def handle_input(self, user_input):
        try:
            self._multiplex_input(user_input)
        except MalformedUserInputException as err:
            raise

    def _multiplex_input(self, user_input):
        if "login" in user_input:
            self._handle_login(user_input)
        if "logout" in user_input:
            self._handle_logout(user_input)
        # order matters ((un)subscribe)
        elif "unsubscribe" in user_input:
            self._handle_unsubscribe(user_input)
        elif "subscribe" in user_input:
            self._handle_subscribe(user_input)
        elif "post" in user_input:
            self._handle_post(user_input)
        elif "retrieve" in user_input:
            self._handle_retrieve(user_input)

    def _handle_login(self, user_input):
        op_split_arr = user_input.split('#')
        if(len(op_split_arr) != 2):
            raise MalformedUserInputException("Login missing or contains an extra #")
        
        auth_split = op_split_arr[1].split('&')
        if(len(auth_split) != 2):
            raise MalformedUserInputException("Login missing or contains an extra &")

        username = auth_split[0]
        password = auth_split[1]

        login_state = LoginState(username, password)
        self.state_transition_manager.transition_to_state(login_state)
        
    def _handle_logout(self, user_input):
        logout_state = LogoutState()
        self.state_transition_manager.transition_to_state(logout_state)

    def _handle_subscribe(self, user_input):
        subscribe_name_arr = user_input.split('#')
        if( len(subscribe_name_arr) != 2 ):
            raise MalformedUserInputException("Subscribe missing or contains an extra #")
        
        subscribe_state = SubscribeState(subscribe_name_arr[1])
        self.state_transition_manager.transition_to_state(subscribe_state)

    def _handle_unsubscribe(self, user_input):
        unsubscribe_name_arr = user_input.split('#')
        if( len(unsubscribe_name_arr) != 2 ):
            raise MalformedUserInputException("Unsubscribe missing or contains an extra #")

        unsubscribe_state = UnsubscribeState(unsubscribe_name_arr[1])
        self.state_transition_manager.transition_to_state(unsubscribe_state)

    def _handle_post(self, user_input):
        message_arr = user_input.split('#')
        if( len(message_arr) != 2 ):
            raise MalformedUserInputException("Post missing or contains an extra #")

        post_state = PostState(message_arr[1])
        self.state_transition_manager.transition_to_state(post_state)

    def _handle_retrieve(self, user_input):
        num_messages_arr = user_input.split("#")
        if( len(num_messages_arr) != 2 ):
            raise MalformedUserInputException("Retrieve missing or contains an extra #")

        post_state = RetrieveState(num_messages_arr[1])
        self.state_transition_manager.transition_to_state(post_state)