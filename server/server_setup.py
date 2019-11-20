# This class handles the high level server initialization

import socket
import threading

import server.config

class ServerSetup:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind((server.config.server_config['SERVER_IP_ADDR'], server.config.server_config['UDP_PORT']))

    def initiate_listening_thread(self):
        self.listen_thread = threading.Thread(name = 'listen_thread', target =  self.__listen_receive, args = ( ) )
        self.listen_thread.start()

    def initiate_writing_thread(self):
        self.writer_thread = threading.Thread(name = 'writing_thread', target = self.__listen_writing, args = ( ) )
        self.writer_thread.start()

    # Is run on a worker thread; constantly listens for new packets from clients in the background
    def __listen_receive(self):
        while True:
            data, addr = self.sock.recvfrom(server.config.server_config['BUFFER_MAX_SIZE'])
            print( data.decode() )
            print( addr )

    def __listen_writing(self):
        while True:
            pass
        