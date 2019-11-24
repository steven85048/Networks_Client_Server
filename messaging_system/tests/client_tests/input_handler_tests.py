
import unittest

from messaging_system.client.input_handler import InputHandler

class InputHandlerTests(unittest.TestCase):
    def setUp(self):
        self.input_handler = InputHandler()

    def test_login(self):
        input = "login#ac1&pass1"
        self.input_handler.handle_input(input)

if __name__ == '__main__':
    unittest.main()