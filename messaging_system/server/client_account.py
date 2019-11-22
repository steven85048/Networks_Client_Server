# Data Class for a Client Account
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
        self.subscriptions.append(subscription)

    def remove_subscription(self, subscription):
        self.subscriptions.remove(subscription)

    def generate_token(self):
        self.token = {'token_val' : self._generate_token(), 'time' : self._generate_current_time()}

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