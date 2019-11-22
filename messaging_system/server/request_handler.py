# This class handles miscellaneous requests from clients and calls various more specific handlers

import json

from messaging_system.resources import opcodes

class RequestHandler:
    def __init__(self):
        pass

    def handle_request(self, data, addr):
        print("Read thread processing request")

        # The input comes in as a json string encoded as bytes, so we decode it and deserialize the json from a string
        decoded_payload = json.loads( data.decode() )
        print(decoded_payload)

        self._multiplex_request(decoded_payload)

    # Depending on the opcode, handle the request in a different manner
    def _multiplex_request(self, payload):
        if( not payload.opcode ):
            print("Faulty Request -- Missing opcode")
            return

        if( payload.opcode == opcodes['LOGIN'] ):
            pass
        elif( payload.opcode == opcodes['SUBSCRIBE']):
            pass
        elif( payload.opcode == opcodes['UNSUBSCRIBE']):
            pass
        elif( payload.opcode == opcodes['POST']):
            pass
        elif( payload.opcode == opcodes['FORWARD_ACK']):
            pass
        elif( payload.opcode == opcodes['RETRIEVE']):
            pass
        elif( payload.opcode == opcodes['LOGOUT'] ):
            pass
        
