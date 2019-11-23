
# If a token does not exist in the database
class InvalidTokenException(Exception):
    def __init__(self, token):
        Exception.__init__(self, "Token cannot be found in list of users; token: {token}".format(token=token))

# Malformed header but with magic number or opcode
class MalformedRequestIdentityException(Exception):
    def __init__(self, err_message):
        Exception.__init__(self, "Request Header Identity Incorrect: {err_message}".format(err_message=err_message))

# If a request does not have valid parameters
class MalformedRequestHeaderException(Exception):
    def __init__(self, err_message):
        Exception.__init__(self, "Request provided is malformed -- Error is: {err_message}".format(err_message=err_message))