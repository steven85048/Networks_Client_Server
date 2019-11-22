
# If a token does not exist in the database
class InvalidTokenException(Exception):
    def __init__(self, token):
        Exception.__init__(self, "Token cannot be found in list of users; token: {token}")

# If a token does not have the correct structure
class MalformedTokenException(Exception):
    def __init__(self, token):
        Exception.__init__(self, "Token provided in a malformed format: {token}")

# If a request does not have valid parameters
class MalformedRequestHeaderException(Exception):
    def __init__(self, err_messsage):
        Exception.__init__(self, "Request provided is malformed -- Error is: {err_message}")