import socket
import sys
import threading
import traceback

from messaging_system.client.config import client_config
from messaging_system.client.input_handler import InputHandler
from messaging_system.client.response_handler import ResponseHandler
from messaging_system.client.state_transition_manager import StateTransitionManager
from messaging_system.client.exceptions import MalformedRequestException, MalformedUserInputException
import messaging_system.socket_holder

class ClientSetup:
    def __init__(self):
        self.udp_ip = client_config['SERVER_IP_ADDR']
        self.port = client_config['UDP_PORT']

        self.state_transition_manager = StateTransitionManager()

        self.input_handler = InputHandler(self.state_transition_manager)
        self.response_handler = ResponseHandler(self.state_transition_manager)

        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.settimeout(client_config['SOCKET_TIMEOUT'])
        self.sock.bind((self.udp_ip, self.port))

        messaging_system.socket_holder.socket = self.sock

    # Starts two threads:
    # (a) User_input_thread continually listens for user input and handles
    # (b) Server_response_thread continually listens for messages from server and handles
    def start_client(self):
        self.user_input_thread = threading.Thread(name = 'user_input_thread', target =  self._user_input_thread, args = ( ) )
        self.user_input_thread.start()

        self.server_response_thread = threading.Thread(name = 'server_response_thread', target =  self._server_response_thread, args = ( ) )
        self.server_response_thread.start()

        self.user_input_thread.join()
        self.server_response_thread.join()

    def _user_input_thread(self):
        while( True ):
            try: 
                exc_info = None
                user_input = input()
                self.input_handler.handle_input(user_input)
            except MalformedUserInputException as err:
                print("Malformed input: {}".format(str(err)))
                print("Enter another input")
            except MalformedRequestException as err:
                print("Error in processing request: {}".format(str(err)))
                self.state_transition_manager.reset()
            except Exception as err:
                exc_info = sys.exc_info()
            finally:
                if( not exc_info is None ):
                    traceback.print_exception(*exc_info)
                
    def _server_response_thread(self):
        while( True ):
            
            try:
                exc_info = None
                data, addr = self.sock.recvfrom(client_config['BUFFER_MAX_SIZE'])
                self.response_handler.handle_response(data)
            except MalformedRequestException as err:
                print("Error in processing request: {}".format(str(err)))
                self.state_transition_manager.reset()
            except Exception as err:
                exc_info = sys.exc_info()
            finally:
                if( not exc_info is None ):
                    traceback.print_exception(*exc_info)