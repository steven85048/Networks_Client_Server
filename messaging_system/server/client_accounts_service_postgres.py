# Data Class for all Clients - Handles all higher level operations that interact with 1+ client accounts
# Class mainly exists for cohesion for eventual SQL operations

from messaging_system.server.db_model import Base, ClientAccount, Messages, Subscriptions
from messaging_system.server.client_account_service_postgres import ClientAccountService

class ClientAccountsService:
    def __init__(self, session = None):
        self.session = session

    def add_account(self, username, password):
        new_account = ClientAccount(username=username, password=password)
        self.session.add(new_account)
        self.session.commit()

    def get_user_from_token(self, token_number):
        account = self.session.query(ClientAccount)\
                      .filter( not ClientAccount.token is None )\
                      .filter( ClientAccount.token['token_val'].astext == str(token_number) )\
                      .first()

        account_service = None
        if( not account is None ):
            account_service = ClientAccountService( account.username, self.session )
        
        return account_service

    # Creates a ClientAccountService for interacting with a single account
    def get_user_from_username(self, username):
        account = self.session.query(ClientAccount)\
                      .filter( ClientAccount.username == username )\
                      .first()

        account_service = None
        if( not account is None ):
            account_service = ClientAccountService( username, self.session )
        
        return account_service

    def get_user_from_credentials(self, username, password):
        account = self.session.query(ClientAccount)\
                      .filter( ClientAccount.username == username )\
                      .filter( ClientAccount.password == password )\
                      .first()

        account_service = None
        if( not account is None ):
            account_service = ClientAccountService( username, self.session )
        
        return account_service

    def username_exists(self, username):
        account_num = self.session.query(ClientAccount)\
                          .filter( ClientAccount.username == username )\
                          .count()

        return account_num == 1

    # @return - Numerical value of the token
    def login(self, username, password, addr):
        account_service = self.get_user_from_credentials(username, password)

        user_token = None
        if( not account_service is None ):
            account_service.generate_token(addr)
            user_token = account_service.get_token()['token_val']

        return user_token

    # @return - array of JSON tokens of subscribers of the message
    def add_message_to_subscribers(self, sender_username, message, from_username ):
        subscriber_tokens = []
        subscriber_accounts = self.session.query(Subscriptions)\
                                 .filter( Subscriptions.subscription == sender_username )\
                                 .all()
        
        for subscriber_account in subscriber_accounts:
            subscriber_account_service = ClientAccountService( subscriber_account.subscriber )
            subscriber_account_service.add_message( message, from_username )
            if( subscriber_account_service.is_token_valid() ):
                subscriber_tokens.append( subscriber_account_service.get_token() )

        return subscriber_tokens

    def reset_session(self, new_session):
        if( not self.session is None ):
            self.session.commit()
    
        self.session = new_session