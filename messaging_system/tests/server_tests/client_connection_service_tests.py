from messaging_system.server.client_connection_service import ClientConnectionService

import unittest

class ClientConnectionServiceTests(unittest.TestCase):
    def test_login(self):
        connection_service = ClientConnectionService()

if __name__ == '__main__':
    unittest.main()