
# If a token does not exist in the database
class InvalidTokenException(Exception):
    def __init__(self, token):
        self.token = token

# If a token does not have the correct structure
class MalformedTokenException(Exception):
    def __init__(self, token):
        self.token = token