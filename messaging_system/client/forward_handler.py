# Forwarding is a slightly different set of operations, so we just separate out a separate case for it

from messaging_system.resources import opcodes, header_keys
from messaging_system.client.exceptions import MalformedRequestException

class ForwardHandler():
    def handle_forwarding(self, response):
        if( response[header_keys['OPCODE']] != opcodes['FORWARD'] ):
            return False

        if( not header_keys['FROM_USERNAME'] in response or
            not header_keys['MESSAGE'] in response):
            raise MalformedRequestException("Missing FROM_USERNAME or MESSAGE in forward packet")

        from_username = response[header_keys['FROM_USERNAME']]
        message = response[header_keys['MESSAGE']]
        print("{from_username} : {message}".format(from_username = from_username, message = message))

        return True
