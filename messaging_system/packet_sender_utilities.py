# Just contains the basic utilities to send a packet

import json
import socket

import messaging_system.socket_holder

# Each element in payloads is a tuple that contains
# (a) The json object with the payload
# (b) The two-tuple with (ip_addr, port)
def send_packet(payloads):
    print("Sending packets: {}".format(str(payloads)))

    for payload in payloads:
        # Convert string if json type
        if type(payload[0]) is dict:
            temp_payload = json.dumps(payload[0])

        ip_addr = payload[1][0]
        port = payload[1][1]

        if( not messaging_system.socket_holder.socket is None ):
            messaging_system.socket_holder.socket.sendto(temp_payload.encode(), (ip_addr, port))
