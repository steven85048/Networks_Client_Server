import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from messaging_system.server.client_account_service_postgres import ClientAccountService
from messaging_system.server.db_model import Base, ClientAccount, Subscriptions, Messages, drop_all, create_all

class ClientAccountTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine('postgresql+psycopg2://root:12345@3.136.156.128/networks-messaging-server')
        connection = engine.connect()

        drop_all(engine)
        create_all(engine)

        Base.metadata.bind = engine
        self.db_session = sessionmaker(bind=engine)
        self.session = self.db_session()

        self.add_account('ac1', 'pass1')
        self.add_account('ac2', 'pass2')
        self.add_account('ac3', 'pass3')

        self.client_account_service = ClientAccountService('ac1', self.session)

    def test_add_subscription_successful(self):
        rc = self.client_account_service.add_subscription('ac2')
        self.assertTrue( rc is True )

        num_subscriptions = self.session.query(Subscriptions).count()
        self.assertTrue(num_subscriptions == 1)

    def test_unsubscribe_successful(self):
        self.client_account_service.add_subscription('ac2')
        rc = self.client_account_service.remove_subscription('ac2')
        self.assertTrue( rc is True )

        num_subscriptions = self.session.query(Subscriptions).count()
        self.assertTrue(num_subscriptions == 0)

    # TODO: Move to client accounts service
    def add_account(self, username, password):
        new_account = ClientAccount(username=username, password=password)
        self.session.add(new_account)
        self.session.commit()

if __name__ == '__main__':
    unittest.main()