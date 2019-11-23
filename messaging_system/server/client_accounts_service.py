# Data Class for all Client - Handles all higher level operations that interact with 1+ client accounts
# Class mainly exists for cohesion for eventual SQL operations

from messaging_system.server.client_account import ClientAccount

class ClientAccountsService:
    def __init__(self):
        self.client_accounts = []
        pass

    def add_account(self, username, password):
        new_account = ClientAccount(username, password)
        self.client_accounts.append(new_account)

    def get_user_from_token(self, token):
        for account in self.client_accounts:
            account_token = account.get_token()
            if( not account_token is None and account_token['token_val'] == token ):
                return account
                
        return None

    def get_user_from_username(self, username):
        for account in self.client_accounts:
            if( account.username == username ):
                return account

        return None

    def username_exists(self, username):
        for account in self.client_accounts:
            if( account.username == username ):
                return True

        return False

    def login(self, username, password, addr):
        for account in self.client_accounts:
            if( account.username == username and account.password == password ):
                account.generate_token(addr)
                return account.token
        return None

    # @return - array of tokens of subscribers of the message
    def add_message_to_subscribers(self, sender_username, message):
        subscriber_tokens = []
        for account in self.client_accounts:
            if sender_username in account.subscriptions:
                account.add_message(message)
                if( account.is_token_valid() ):
                    subscriber_tokens.append( account.get_token() )

        return subscriber_tokens