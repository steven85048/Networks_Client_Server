# Multiplexes the user_input into the correct sublogic

class InputHandler:
    def __init__(self):
        pass

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

        print("{} {}".format(username, password))

    def _handle_subscribe(self, user_input):
        pass