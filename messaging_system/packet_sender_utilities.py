# Just contains the basic utilities to send a packet

import json
import socket

# Each element in payloads is a tuple that contains
# (a) The json object with the payload
# (b) The two-tuple with (ip_addr, port)
def send_packet(payloads):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for payload in payloads:
        # Convert string if json type
        if type(payload[0]) is dict:
            temp_payload = json.dumps(payload[0])

        ip_addr = payload[1][0]
        port = payload[1][1]

        sock.sendto(temp_payload.encode(), (ip_addr, port))

    sock.close()
