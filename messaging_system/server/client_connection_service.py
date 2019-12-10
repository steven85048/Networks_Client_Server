# Works on top of client_account_service and client_accounts_service to provide the encompassing
# API for all the backend operations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from messaging_system.server.db_model import Base
from messaging_system.server.client_account_service_postgres import ClientAccount
from messaging_system.server.exceptions import InvalidTokenException, MalformedRequestHeaderException
from messaging_system.server.client_accounts_service_postgres import ClientAccountsService
from messaging_system.server.config import DB_URL

class ClientConnectionService:
    def __init__(self):
        self.curr_session = None
        self.curr_account = None
        self.client_accounts_service = ClientAccountsService()
        self._create_psql_session_maker( DB_URL )

    # ============================ DECORATORS ===============================

    # NOTE that the first parameter of each method with this decorator MUST have the token
    # This decorator also associates the account with the token
    def user_logged_in(func):
        def validate_token(self, user_token, *args):
            self.curr_account = None

            account = self._get_user_from_token(user_token)

            if( account is None or not account.is_token_valid() ):
                raise InvalidTokenException(user_token)

            self.curr_account = account
            return func(self, user_token, *args)

        return validate_token

    def session_reset(func):
        def session_reset(self, *args):
            self.curr_session = self.db_session()
            self.client_accounts_service.reset_session( self.curr_session )

            return func(self, *args)

        return session_reset

    # ======================= PUBLIC METHODS ================================

    @session_reset
    def add_account(self, username, password):
        self.client_accounts_service.add_account(username, password)

    @session_reset
    def login(self, username, password, addr):
        return self.client_accounts_service.login(username, password, addr)

    @session_reset
    @user_logged_in
    def logout(self, token):
        self.curr_account.logout()

    @session_reset
    @user_logged_in
    def subscribe(self, token, to_subscribe_username):

        # Test subscribe username correct
        if not self.client_accounts_service.username_exists(to_subscribe_username):
            raise MalformedRequestHeaderException("Subscription error - The provided username does not exist")

        if to_subscribe_username == self.curr_account.get_username():
            raise MalformedRequestHeaderException("Subscription error - Cannot subscribe to yourself")

        self.curr_account.add_subscription(to_subscribe_username)

    @session_reset
    @user_logged_in
    def unsubscribe(self, token, to_unsubscribe_username):
        # Test unsubscribe username correct
        if not self.client_accounts_service.username_exists(to_unsubscribe_username):
            raise MalformedRequestHeaderException("Unsubscription error - The provided username does not exist")

        self.curr_account.remove_subscription(to_unsubscribe_username)

    @session_reset
    @user_logged_in
    def post(self, token, message): 
        # Relay all messages back to the subscribers
        from_username = self.curr_account.get_username()
        subscriber_tokens = self.client_accounts_service.add_message_to_subscribers(message, from_username)

        return subscriber_tokens, from_username

    # @return array of messages
    @session_reset
    @user_logged_in
    def retrieve(self, token, num_messages):
        return self.curr_account.get_messages( num_messages )

    # =========================== PRIVATE/TEST METHODS =============================

    def _get_user_from_token(self, token):
        return self.client_accounts_service.get_user_from_token(token)

    def _create_psql_session_maker( self, db_url ):
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()

        Base.metadata.bind = self.engine
        self.db_session = sessionmaker(bind=self.engine)

    # For testing; need to reset session before clearing database
    def reset_session(self):
        self.db_session.close_all()

        if( not self.curr_session is None ):
            self.curr_session.close()