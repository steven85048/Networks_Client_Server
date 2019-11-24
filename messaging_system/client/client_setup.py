import socket

from messaging_system.server.config import server_config
from messaging_system.client.input_handler import InputHandler

class ClientSetup:
    def __init__(self):
        self.udp_ip = server_config['SERVER_IP_ADDR']
        self.port = server_config['UDP_PORT']

        self.input_handler = InputHandler()

        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.port))

    def start_client(self):
        while( True ):
            user_input = input()
            self.input_handler.handle_input(user_input)

    def recv_from_server(self):
        while( True ):
            