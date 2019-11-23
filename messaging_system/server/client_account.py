# Data Class for a Client Account - This class handles the CRUD for a SINGLE account;
# The client_accounts_service will have a method that returns this object, allowing easy
# management of the associated account.
# TODO: move to postgresql

from numpy.random import randint
from datetime import datetime

from messaging_system.server.config import MAX_RANDOM_TOKEN, TOKEN_EXPIRATION_INTERVAL

class ClientAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.messages = []
        self.subscriptions = []
        self.token = None

    def add_message(self, message):
        self.messages.append(message)

    def add_subscription(self, subscription):
        if subscription in self.subscriptions:
            return False

        self.subscriptions.append(subscription)
        return True

    def remove_subscription(self, subscription):
        if not subscription in self.subscriptions:
            return False

        self.subscriptions.remove(subscription)
        return True

    def get_token(self):
        return self.token

    def get_username(self):
        return self.username

    def get_messages(self, num_messages):
        num_messages = min(len(self.messages), num_messages)
        return self.messages[-num_messages:]

    def generate_token(self, addr):
        self.token = {  'token_val' : self._generate_token(), 
                        'time' : self._generate_current_time(),
                        'client_addr' : { 'ip_addr' : addr[0], 'port' : addr[1] } }

    def is_token_valid(self):
        if( self.token == None ):
            return False

        current_time = datetime.now()
        if( self.token['time'] + TOKEN_EXPIRATION_INTERVAL < current_time ):
            self.token = None
            return False

        return True  

    def _generate_current_time(self):
        current_time = datetime.now()
        return current_time

    def _generate_token(self):
        return randint(0, MAX_RANDOM_TOKEN)