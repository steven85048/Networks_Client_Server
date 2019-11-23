import unittest

from messaging_system.server.client_connection_service import ClientConnectionService
from messaging_system.server.exceptions import InvalidTokenException

class ClientConnectionServiceTests(unittest.TestCase):
    def setUp(self):
        self.connection_service = ClientConnectionService()

        #Add dummy accounts
        self.connection_service.add_account('ac1', 'pass1')
        self.connection_service.add_account('ac2', 'pass2')
        self.connection_service.add_account('ac3', 'pass3')
        self.connection_service.add_account('ac4', 'pass4')

    def test_login(self):
        addr = ('127.0.0.1', 2000)

        token = self.connection_service.login('ac1', 'pass1', addr)
        self.assertTrue(not token is None)

    def test_invalid_login(self):
        addr = ('127.0.0.1', 2000)

        token = self.connection_service.login('ac1', 'wrong_pass', addr)
        self.assertTrue(token is None)

    def test_get_user_from_token(self):
        addr = ('127.0.0.1', 2000)

        token = self.connection_service.login('ac2', 'pass2', addr)
        account = self.connection_service._get_user_from_token(token)
        self.assertTrue(not account is None)
        self.assertEqual(account.get_username(), 'ac2')
        self.assertTrue(account.is_token_valid())

    def test_subscribe_and_retrieve(self):
        addr = ('127.0.0.1', 2000)

        token1 = self.connection_service.login('ac1', 'pass1', addr)
        token2 = self.connection_service.login('ac2', 'pass2', addr)
        token3 = self.connection_service.login('ac3', 'pass3', addr)
        token4 = self.connection_service.login('ac4', 'pass4', addr)

        self.connection_service.subscribe(token1, 'ac3')
        self.connection_service.subscribe(token2, 'ac3')

        post_message = 'testing_hello'
        subscriber_tokens = self.connection_service.post(token3, post_message)
        
        self.assertTrue( token1 in subscriber_tokens )
        self.assertTrue( token2 in subscriber_tokens )
        self.assertTrue( not token3 in subscriber_tokens )
        self.assertTrue( not token4 in subscriber_tokens )

        ac1_messages = self.connection_service.retrieve(token1, 3)
        self.assertTrue( post_message in ac1_messages )

        ac2_messages = self.connection_service.retrieve(token2, 2)
        self.assertTrue( post_message in ac2_messages )

        ac3_messages = self.connection_service.retrieve(token3, 3)
        self.assertTrue( not post_message in ac3_messages )

        ac4_messages = self.connection_service.retrieve(token4, 3)
        self.assertTrue( not post_message in ac4_messages )

    def test_unsubscribe(self):
        addr = ('127.0.0.1', 2000) 
    
        token1 = self.connection_service.login('ac1', 'pass1', addr)
        token2 = self.connection_service.login('ac2', 'pass2', addr)

        self.connection_service.subscribe(token1, 'ac2')

        post_message = 'testing2'
        subscriber_tokens = self.connection_service.post(token2, post_message)
        self.assertTrue( token1 in subscriber_tokens )
        ac1_messages = self.connection_service.retrieve(token1, 2)
        self.assertTrue( post_message in ac1_messages )

        self.connection_service.unsubscribe(token1, 'ac2')
        
        post_message_2 = 'testing3'
        subscriber_tokens = self.connection_service.post(token2, post_message_2)
        self.assertTrue( not token1 in subscriber_tokens )
        ac1_messages_2 = self.connection_service.retrieve(token1, 2)
        self.assertTrue( not post_message_2 in ac1_messages_2 )

if __name__ == '__main__':
    unittest.main()