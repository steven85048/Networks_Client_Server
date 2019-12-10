# This class defines all the operations to be performed on a single user

from numpy.random import randint
from datetime import datetime
from sqlalchemy import update, desc
from dateutil import parser

from messaging_system.server.db_model import Base, ClientAccount, Messages, Subscriptions
from messaging_system.server.config import MAX_RANDOM_TOKEN, TOKEN_EXPIRATION_INTERVAL
from messaging_system.server.exceptions import MalformedRequestHeaderException

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
            raise MalformedRequestHeaderException("Subscription error - Already subscribed to this user")

        new_subscription = Subscriptions(subscriber_username = self.account_username, subscription_username = subscription_username)
        self.session.add(new_subscription)
        self.session.commit()

    # Assumes subscription_username is valid
    def remove_subscription(self, subscription_username):        
        if( not self._is_subscription_active(subscription_username) ):
            raise MalformedRequestHeaderException("Unsubscription error - Cannot unsubscribe from someone you are not already subscribed to")

        self.session.query(Subscriptions)\
                    .filter(Subscriptions.subscription_username == subscription_username)\
                    .filter(Subscriptions.subscriber_username == self.account_username).delete()
        self.session.commit()

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

    def is_token_valid(self):
        token = self.get_token()
        if( token is None ):
            return False

        current_time = datetime.utcnow()     
        token_time = parser.parse(token['time'])

        if( token_time + TOKEN_EXPIRATION_INTERVAL < current_time ):
            self.logout()
            return False

        return True

    def add_message(self, message, from_username):
        new_message = Messages(message=message, to_account_username=self.account_username, from_account_username=from_username)
        self.session.add(new_message)
        
        self.session.commit()

    def get_messages(self, num_messages):
        messages = self.session.query(Messages)\
                               .filter(Messages.to_account_username==self.account_username)\
                               .order_by(Messages.post_time.desc())\
                               .limit(num_messages)\
                               .all()
        return messages

    def _is_subscription_active(self, subscription_username):
        res = self.session.query(Subscriptions)\
                          .filter(Subscriptions.subscription_username == subscription_username)\
                          .filter(Subscriptions.subscriber_username == self.account_username).first()
        return not res is None

    def _generate_token(self):
        return randint(0, MAX_RANDOM_TOKEN)