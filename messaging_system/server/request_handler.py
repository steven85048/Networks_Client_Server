# This class handles miscellaneous requests from clients and calls various more specific handlers

import json

class RequestHandler:
    def __init__(self):
        pass

    def handle_request(self, data, addr):
        print("Read thread processing request")

        # The input comes in as a json string encoded as bytes, so we decode it and deserialize the json from a string
        decoded_payload = json.loads( data.decode() )

        print(decoded_payload)
        
