from messaging_system.server.client_connection_service import ClientConnectionService
from messaging_system.server.exceptions import MalformedTokenException, InvalidTokenException

import unittest

class ClientConnectionServiceTests(unittest.TestCase):
    def setUp(self):
        self.connection_service = ClientConnectionService()

        #Add two dummy accounts
        self.connection_service.add_account('ac1', 'pass1')
        self.connection_service.add_account('ac2', 'pass2')

    def test_login(self):
        token = self.connection_service.login('ac1', 'pass1')
        self.assertTrue(not token is None)

    def test_invalid_login(self):
        token = self.connection_service.login('ac1', 'wrong_pass')
        self.assertTrue(token is None)

    def test_malformed_token_1(self):
        token = 'bad-token'

        with self.assertRaises(MalformedTokenException):
            self.connection_service.retrieve(token)

    def test_malformed_token_2(self):
        token = {'token_val' : 'asdf', 'testt' : 'sup'}

        with self.assertRaises(MalformedTokenException):
            self.connection_service.retrieve(token)

    def test_get_user_from_token(self):
        token = self.connection_service.login('ac2', 'pass2')
        account = self.connection_service._get_user_from_token(token)
        self.assertTrue(not account is None)
        self.assertEqual(account.get_username(), 'ac2')
        self.assertTrue(account.is_token_valid())

    def test_subscribe(self):
        token = self.connection_service.login('ac1', 'pass1')
        self.connection_service.subscribe(token, 'ac2')

if __name__ == '__main__':
    unittest.main()