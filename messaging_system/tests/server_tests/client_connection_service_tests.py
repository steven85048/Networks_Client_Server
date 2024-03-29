import unittest

from messaging_system.server.client_connection_service import ClientConnectionService
from messaging_system.server.exceptions import InvalidTokenException
from messaging_system.server.db_model import drop_all, create_all

class ClientConnectionServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection_service = ClientConnectionService()

    def setUp(self):
        self.connection_service.reset_session()
        drop_all(self.connection_service.engine)
        create_all(self.connection_service.engine)
        self._add_test_accounts()

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
        subscriber_tokens, from_username = self.connection_service.post(token3, post_message)

        self.assertTrue(self._token_val_exists_in_list( token1, subscriber_tokens))
        self.assertTrue(self._token_val_exists_in_list( token2, subscriber_tokens))
        self.assertFalse(self._token_val_exists_in_list( token3, subscriber_tokens))
        self.assertFalse(self._token_val_exists_in_list( token4, subscriber_tokens))

        ac1_messages = self.connection_service.retrieve(token1, 3)
        self.assertTrue( self._message_exists_in_list( post_message, ac1_messages) )

        ac2_messages = self.connection_service.retrieve(token2, 2)
        self.assertTrue( self._message_exists_in_list( post_message, ac2_messages) )

        ac3_messages = self.connection_service.retrieve(token3, 3)
        self.assertTrue( not self._message_exists_in_list( post_message, ac3_messages) )

        ac4_messages = self.connection_service.retrieve(token4, 3)
        self.assertTrue( not self._message_exists_in_list( post_message, ac4_messages) )

    def test_unsubscribe(self):
        addr = ('127.0.0.1', 2000) 
    
        token1 = self.connection_service.login('ac1', 'pass1', addr)
        token2 = self.connection_service.login('ac2', 'pass2', addr)

        self.connection_service.subscribe(token1, 'ac2')

        post_message = 'testing2'
        subscriber_tokens, from_username = self.connection_service.post(token2, post_message)
        self.assertTrue(self._token_val_exists_in_list( token1, subscriber_tokens))
        ac1_messages = self.connection_service.retrieve(token1, 2)
        self.assertTrue( self._message_exists_in_list( post_message, ac1_messages) )

        self.connection_service.unsubscribe(token1, 'ac2')
        
        post_message_2 = 'testing3'
        subscriber_tokens, from_username = self.connection_service.post(token2, post_message_2)
        self.assertFalse(self._token_val_exists_in_list( token1, subscriber_tokens))
        ac1_messages_2 = self.connection_service.retrieve(token1, 2)
        self.assertTrue( not self._message_exists_in_list( post_message_2, ac1_messages_2) )

    def _add_test_accounts(self):
        self.connection_service.add_account('ac1', 'pass1')
        self.connection_service.add_account('ac2', 'pass2')
        self.connection_service.add_account('ac3', 'pass3')
        self.connection_service.add_account('ac4', 'pass4')

    def _message_exists_in_list( self, message, full_message_list):
        for full_message in full_message_list:
            if( full_message.message == message ):
                return True

        return False

    def _token_val_exists_in_list( self, token_val, full_token_list):
        for full_token in full_token_list:
            if( full_token['token_val'] == token_val ):
                return True

        return False

if __name__ == '__main__':
    unittest.main()