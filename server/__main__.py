from server.server_setup import ServerSetup

if __name__ == '__main__':
    server = ServerSetup()
    server.initiate_listening_thread()
    #server.initiate_writing_thread()