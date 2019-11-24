from messaging_system.server.config import server_config
from messaging_system.client.client_message_factory import ClientMessageFactory
from messaging_system.packet_sender_utilities import send_packet

class LoginState():
    def __init__(self):
        self.curr_request = []

    def start_state(self, username, password):
        payload = ClientMessageFactory.login(username, password)
        self.curr_request.append((payload, (server_config['SERVER_IP_ADDR'], server_config['UDP_PORT'])))
        send_packet(self.curr_request)

    def receive_response(self, response):
        pass