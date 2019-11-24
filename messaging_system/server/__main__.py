from messaging_system.server.server_setup import ServerSetup

if __name__ == '__main__':
    server = ServerSetup()
    server.initiate_listening_thread()