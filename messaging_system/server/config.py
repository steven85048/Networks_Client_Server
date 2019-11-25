from datetime import timedelta

server_config = dict(
    SERVER_IP_ADDR = "127.0.0.1",
    UDP_PORT = 5006,
    BUFFER_MAX_SIZE = 1024
)

MAX_RANDOM_TOKEN = 50000
TOKEN_EXPIRATION_INTERVAL = timedelta(hours = 1)