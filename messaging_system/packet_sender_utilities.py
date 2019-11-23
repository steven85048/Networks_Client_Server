# Just contains the basic utilities to send a packet

import json
import socket

def send_packet(payloads, ip_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for payload in payloads:
        # Convert string if json type
        if type(payload) is dict:
            payload = json.dumps(payload)
        sock.sendto(payload.encode(), (ip_addr, port))

    sock.close()
