# This class handles the high level server initialization

import socket
import threading

from messaging_system.server.config import server_config
from messaging_system.server.request_handler import RequestHandler
from messaging_system.server.client_connection_service import ClientConnectionService
import messaging_system.socket_holder

class ServerSetup:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((server_config['SERVER_IP_ADDR'], server_config['UDP_PORT']))

        self.client_connection_service = ClientConnectionService()
        self.request_handler = RequestHandler( self.client_connection_service )
        messaging_system.socket_holder.socket = self.sock

    def initiate_listening_thread(self):
        self.listen_thread = threading.Thread(name = 'listen_thread', target =  self._listen_receive, args = ( ) )
        self.listen_thread.start()
        self.listen_thread.join()

    # Is run on a worker thread; constantly listens for new packets from clients in the background
    def _listen_receive(self):
        while True:
            data, addr = self.sock.recvfrom(server_config['BUFFER_MAX_SIZE'])
            self.request_handler.handle_request(data, addr)