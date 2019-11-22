import socket
import json

def run(): 
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    MESSAGE = json.dumps({'test' : 'test1', 'opcode' : 'code'}).encode()

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind(('127.0.0.1', 5006))
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)
    print(data)

run()