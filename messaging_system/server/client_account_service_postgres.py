# This class defines all the operations to be performed on a single user

from numpy.random import randint
from datetime import datetime
from sqlalchemy import update

from messaging_system.server.db_model import Base, ClientAccount, Messages, Subscriptions
from messaging_system.server.config import MAX_RANDOM_TOKEN, TOKEN_EXPIRATION_INTERVAL

class ClientAccountService:
    def __init__(self, account_username, session):
        self.account_username = account_username
        self.session = session

    def get_username(self):
        return self.account_username

    def get_password(self):
        res = self.session.query(ClientAccount).filter(ClientAccount.username==self.account_username).one()
        return res.password

    def get_token(self):
        res = self.session.query(ClientAccount).filter(ClientAccount.username==self.account_username).one()
        return res.token

    # Assumes subscription_username is valid
    def add_subscription(self, subscription_username):
        if( self._is_subscription_active(subscription_username) ):
            return False

        new_subscription = Subscriptions(subscriber_username = self.account_username, subscription_username = subscription_username)
        self.session.add(new_subscription)
        self.session.commit()
        return True

    # Assumes subscription_username is valid
    def remove_subscription(self, subscription_username):        
        if( not self._is_subscription_active(subscription_username) ):
            return False

        self.session.query(Subscriptions)\
                    .filter(Subscriptions.subscription_username == subscription_username)\
                    .filter(Subscriptions.subscriber_username == self.account_username).delete()
        self.session.commit()
        return True

    def logout(self):
        account = self.session.query(ClientAccount)\
            .filter(ClientAccount.username == self.account_username)\
            .first()
        account.token = None

        self.session.commit()

    def generate_token(self, addr):
        token = {   'token_val' : self._generate_token(), 
                    'time' : str( datetime.utcnow() ),
                    'client_addr' : { 'ip_addr' : addr[0], 'port' : addr[1] } }
        account = self.session.query(ClientAccount)\
            .filter(ClientAccount.username == self.account_username)\
            .first()
        account.token = token

        self.session.commit()

    def _is_subscription_active(self, subscription_username):
        res = self.session.query(Subscriptions)\
                          .filter(Subscriptions.subscription_username == subscription_username)\
                          .filter(Subscriptions.subscriber_username == self.account_username).first()
        return not res is None

    def _generate_token(self):
        return randint(0, MAX_RANDOM_TOKEN)