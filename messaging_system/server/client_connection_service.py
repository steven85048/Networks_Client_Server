# This class owns the different client accounts and performs operations on them
# depending on the message

from messaging_system.server.client_account import ClientAccount
from messaging_system.server.exceptions import MalformedTokenException, InvalidTokenException

class ClientConnectionService:
    def __init__(self):
        self.client_accounts = []
        self.curr_account = None

        # Create accounts here for testing
        ac1 = ClientAccount('ac1', 'pass')
        ac2 = ClientAccount('ac2', 'pass')

        self.client_accounts.append(ac1)
        self.client_accounts.append(ac2)

    # NOTE that the first parameter of each method with this decorator MUST have the token
    # This decorator also associates the account with the token
    def user_logged_in(function):
        def validate_token(self, user_token, *args):
            self.curr_account = None

            if( not( type(user_token) is dict and 'token_val' in user_token and 'time' in user_token ) ):
                raise MalformedTokenException(user_token)

            account = self._get_user_from_token(user_token)

            if( account is None or not account.is_token_valid() ):
                raise InvalidTokenException(user_token)

            self.curr_account = account
            return function(self, user_token, *args)

        return validate_token

    def add_account(self, username, password):
        new_account = ClientAccount(username, password)
        self.client_accounts.append(new_account)

    def login(self, username, password):
        for account in self.client_accounts:
            if( account.username == username and account.password == password ):
                account.generate_token()
                return account.token
        return None

    @user_logged_in
    def logout(self, token):
        self.curr_account.token = None

    @user_logged_in
    def subscribe(self, token, to_subscribe_username):
        self.curr_account.add_subscription(to_subscribe_username)

    @user_logged_in
    def unsubscribe(self, token, to_unsubscribe_username):
        self.curr_account.remove_subscription(to_unsubscribe_username)

    @user_logged_in
    def post(self, token, message):
        self.curr_account.add_message(message)

        # Relay all messages back to the subscribers

    @user_logged_in
    def retrieve(self, token):
        pass

    def _get_user_from_token(self, token):
        for account in self.client_accounts:
            account_token = account.get_token()
            if( not account_token is None and account_token['token_val'] == token['token_val'] ):
                return account
                
        return None