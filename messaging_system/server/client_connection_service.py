# This class owns the different client accounts and performs operations on them
# depending on the message

from messaging_system.server.client_account import ClientAccount

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
            account = self._get_user_from_token(user_token)

            if( account is None or not account.is_token_valid() ):
                print("Token " + str(user_token) + " is invalid")
                return None

            self.curr_account = account
            return function(self, user_token, *args)

        return validate_token

    def login(self, username, password):
        for account in self.client_accounts:
            if( account.username == username and account.password == password ):
                account.generate_token()

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
        pass

    @user_logged_in
    def retrieve(self, token):
        pass

    def _get_user_from_token(self, token):
        for account in self.client_accounts:
            if( account.token and account.token.token_val == token ):
                return 
                
        return None