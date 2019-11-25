import socket
import json

from messaging_system.server.server_message_factory import ServerMessageFactory

def run(): 
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5007

    token_number = 123
    response = ServerMessageFactory.logout_ack()
    response = json.dumps(response).encode()

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind(('127.0.0.1', 5008))
    sock.sendto(response, (UDP_IP, UDP_PORT))
    #data, addr = sock.recvfrom(1024)
    #print(data)

run()