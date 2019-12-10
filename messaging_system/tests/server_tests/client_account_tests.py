import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from messaging_system.server.client_account_service_postgres import ClientAccountService
from messaging_system.server.db_model import Base, ClientAccount, Subscriptions, Messages, drop_all, create_all


class ClientAccountTests(unittest.TestCase):
    has_initialized = False
    
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
        cls.connection = cls.engine.connect()

        Base.metadata.bind = cls.engine
        cls.db_session = sessionmaker(bind=cls.engine)
        cls.session = cls.db_session()

    def setUp(self):
        self.client_account_service = ClientAccountService('ac1', self.session)
        self._reset_session()
        drop_all(self.engine)
        create_all(self.engine)
        self._add_test_accounts()

    def test_add_subscription_successful(self):
        rc = self.client_account_service.add_subscription('ac2')

        num_subscriptions = self.session.query(Subscriptions).count()
        self.assertTrue(num_subscriptions == 1)

    def test_unsubscribe_successful(self):
        self.client_account_service.add_subscription('ac2')
        rc = self.client_account_service.remove_subscription('ac2')

        num_subscriptions = self.session.query(Subscriptions).count()
        self.assertTrue(num_subscriptions == 0)
        
    def test_generate_token(self):
        self.client_account_service.generate_token(('127.0.0.1', 5006))
        token = self.client_account_service.get_token()

        is_token_valid = self.client_account_service.is_token_valid()
        self.assertTrue(is_token_valid is True)

    def test_add_and_get_messages(self):
        self.client_account_service.add_message('hello1', 'ac2')
        self.client_account_service.add_message('hello2', 'ac2')
        self.client_account_service.add_message('hello3', 'ac2')

        messages = self.client_account_service.get_messages(2)
        for message in messages:
            print(message.message)



    # For testing purposes, since this is a client_accounts_service method
    def _add_account(self, username, password):
        new_account = ClientAccount(username=username, password=password)
        self.session.add(new_account)
        self.session.commit()

    def _add_test_accounts(self):
        self._add_account('ac1', 'pass1')
        self._add_account('ac2', 'pass2')
        self._add_account('ac3', 'pass3')

    def _reset_session(self):
        self.db_session.close_all()
        self.session.close()
        self.session = self.db_session()

if __name__ == '__main__':
    unittest.main()