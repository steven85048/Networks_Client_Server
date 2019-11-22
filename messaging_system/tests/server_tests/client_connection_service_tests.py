from messaging_system.server.client_connection_service import ClientConnectionService
from messaging_system.server.exceptions import MalformedTokenException, InvalidTokenException

import unittest

class ClientConnectionServiceTests(unittest.TestCase):
    def setUp(self):
        self.connection_service = ClientConnectionService()

        #Add dummy accounts
        self.connection_service.add_account('ac1', 'pass1')
        self.connection_service.add_account('ac2', 'pass2')
        self.connection_service.add_account('ac3', 'pass3')

    def test_login(self):
        token = self.connection_service.login('ac1', 'pass1')
        self.assertTrue(not token is None)

    def test_invalid_login(self):
        token = self.connection_service.login('ac1', 'wrong_pass')
        self.assertTrue(token is None)

    def test_malformed_token_1(self):
        token = 'bad-token'

        with self.assertRaises(MalformedTokenException):
            self.connection_service.retrieve(token, 2)

    def test_malformed_token_2(self):
        token = {'token_val' : 'asdf', 'testt' : 'sup'}

        with self.assertRaises(MalformedTokenException):
            self.connection_service.retrieve(token, 3)

    def test_get_user_from_token(self):
        token = self.connection_service.login('ac2', 'pass2')
        account = self.connection_service._get_user_from_token(token)
        self.assertTrue(not account is None)
        self.assertEqual(account.get_username(), 'ac2')
        self.assertTrue(account.is_token_valid())

    def test_subscribe(self):
        token1 = self.connection_service.login('ac1', 'pass1')
        token2 = self.connection_service.login('ac2', 'pass2')
        token3 = self.connection_service.login('ac3', 'pass3')

        self.connection_service.subscribe(token1, 'ac3')
        self.connection_service.subscribe(token2, 'ac3')

        post_message = 'testing_hello'
        self.connection_service.post(token3, post_message)
        
        ac1_messages = self.connection_service.retrieve(token1, 3)
        self.assertTrue( post_message in ac1_messages )

        ac2_messages = self.connection_service.retrieve(token2, 2)
        self.assertTrue( post_message in ac2_messages )


if __name__ == '__main__':
    unittest.main()