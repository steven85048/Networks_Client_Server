opcodes = dict(
    SESSION_RESET = 0x00,
    MUST_LOGIN_FIRST_ERROR = 0xF0,
    LOGIN = 0x10,
    SUCCESSFUL_LOGIN_ACK = 0x80,
    FAILED_LOGIN_ACK = 0x81,
    SUBSCRIBE = 0x20,
    SUCCESSFUL_SUBSCRIBE_ACK = 0x90,
    FAILED_SUBSCRIBE_ACK = 0x91,
    UNSUBSCRIBE = 0x21,
    SUCCESSFUL_UNSUBSCRIBE_ACK = 0xA0,
    FAILED_UNSUBSCRIBE_ACK = 0xA1,
    POST = 0x30,
    SUCCESSFUL_POST_ACK = 0xB0,
    FAILED_POST_ACK = 0xB1,
    FORWARD = 0xB1,
    FORWARD_ACK = 0x31,
    RETRIEVE = 0x40,
    RETRIEVE_ACK = 0xC0,
    END_OF_RETRIEVE_ACK = 0xC1,
    LOGOUT = 0x1F,
    LOGOUT_ACK = 0x8F,
    HEADER_IDENTITY_INVALID = 0x50
)

MAGIC_NUMBER_1 = 'S'
MAGIC_NUMBER_2 = 'T'

header_keys = dict(
    OPCODE = 'opcode',
    MAGIC_NUM_1 = 'magic_num_1',
    MAGIC_NUM_2 = 'magic_num_2',
    ERROR_MESSAGE = 'error_message',
    SUBSCRIBE_USERNAME = 'subscribe_username',
    UNSUBSCRIBE_USERNAME = 'unsubscribe_username',
    MESSAGE = 'message',
    USERNAME = 'username',
    PASSWORD = 'password',
    FROM_USERNAME = 'from_username',
    TOKEN = 'token',
    NUM_MESSAGES = 'num_messages'
)