# This class defines all the operations to be performed on a single user

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_model import Base, ClientAccount, Messages, Subscriptions

class ClientAccountService:
    def __init__(self, account_id):
        self.account_id = account_id

        engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
        connection = engine.connect()

        Base.metadata.bind = engine
        self.db_session = sessionmaker(bind=engine)
        self.session = self.db_session()

    def get_username(self):
        res = self.session.query(ClientAccount).filter(ClientAccount.id==self.account_id).one()
        return res.username

    def get_password(self):
        res = self.session.query(ClientAccount).filter(ClientAccount.id==self.account_id).one()
        return res.password

    def get_token(self):
        res = self.session.query(ClientAccount).filter(ClientAccount.id==self.account_id).one()
        return res.token

    def add_subscription(self, subscription_username):
        if(self._is_username_valid(subscription_username)):
            return False

    def remove_subscription(self, subscription_username):
        if(self._is_username_valid(subscription_username)):
            return False

    def _is_username_valid(self, username):
        res = self.session.query(ClientAccount).filter(ClientAccount.username==username).all()
        return not res is None


account = ClientAccountService(1)
account.get_password()

#session = DBSession()

#new_account = ClientAccount(username='ac1', password='pass1')
#session.add(new_account)
#session.commit()