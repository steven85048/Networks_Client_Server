from messaging_system.client.state_handler.client_state import ClientState

class SubscribeState(ClientState):
    def __init__(self, subscribe_name):
        self.subscribe_name = subscribe_name
        super().__init__()

    def start_state(self):
        pass

    def process_response(self, response):
        pass