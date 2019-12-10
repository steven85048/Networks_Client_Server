# Data Class for all Clients - Handles all higher level operations that interact with 1+ client accounts
# Class mainly exists for cohesion for eventual SQL operations

from messaging_system.server.db_model import Base, ClientAccount, Messages, Subscriptions
from messaging_system.server.client_account_service_postgres import ClientAccountService

class ClientAccountsService:
    def __init__(self, session):
        self.session = session

    def add_account(self, username, password):
        new_account = ClientAccount(username=username, password=password)
        self.session.add(new_account)
        self.session.commit()

    def get_user_from_token(self, token_number):
        self.session.query(ClientAccount)\
            .filter( not ClientAccount.token is None and ClientAccount.token['token_val'] == token_number )\
            .first()

    # Creates a ClientAccountService for interacting with a single account
    def get_user_from_username(self, username):
        account = self.session.query(ClientAccount)\
                      .filter( ClientAccount.username == username )\
                      .first()

        account_service = ClientAccountService(self.session)
        return account_service

    def get_user_from_credentials(self, username, password):
        account = self.session.query(ClientAccount)\
                      .filter( ClientAccount.username == username )\
                      .filter( ClientAccount.password == password )\
                      .first()

        account_service = ClientAccountService(self.session)
        return account_service

    def username_exists(self, username):
        account_num = self.session.query(ClientAccount)\
                          .filter( ClientAccount.username == username )\
                          .count()

        return account_num == 1

    def login(self, username, password, addr):
        account_service = get_user_from_credentials(username, password)
        account_service.generate_token(addr)
        return account_service.get_token()

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