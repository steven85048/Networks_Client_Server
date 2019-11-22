# This class owns the different client accounts and performs operations on them
# depending on the message

from messaging_system.server.client_account import ClientAccount
from messaging_system.server.exceptions import MalformedTokenException, InvalidTokenException
from messaging_system.server.client_accounts_service import ClientAccountsService

class ClientConnectionService:
    def __init__(self):
        self.curr_account = None
        self.client_accounts_service = ClientAccountsService()

    # NOTE that the first parameter of each method with this decorator MUST have the token
    # This decorator also associates the account with the token
    def user_logged_in(func):
        def validate_token(self, user_token, *args):
            self.curr_account = None

            if( not( type(user_token) is dict and 'token_val' in user_token and 'time' in user_token ) ):
                raise MalformedTokenException(user_token)

            account = self._get_user_from_token(user_token)

            if( account is None or not account.is_token_valid() ):
                raise InvalidTokenException(user_token)

            self.curr_account = account
            return func(self, user_token, *args)

        return validate_token

    def add_account(self, username, password):
        self.client_accounts_service.add_account(username, password)

    def login(self, username, password):
        return self.client_accounts_service.login(username, password)

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
        subscriber_tokens = self.client_accounts_service.add_message_to_subscribers(self.curr_account.get_username(), message)
        return subscriber_tokens

    @user_logged_in
    def retrieve(self, token, num_messages):
        return self.curr_account.get_messages( num_messages )

    def _get_user_from_token(self, token):
        return self.client_accounts_service.get_user_from_token(token)