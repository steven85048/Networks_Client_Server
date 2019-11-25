class MalformedUserInputException(Exception):
    def __init__(self, err_message):
        Exception.__init__(self, "Malformed User Input: {err_message}".format(err_message=err_message))

class MalformedRequestException(Exception):
    def __init__(self, err_message):
        Exception.__init__(self, "Malformed Request Header: {err_message}".format(err_message=err_message))
