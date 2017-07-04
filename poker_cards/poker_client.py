import socket, json, sys
class Player_Socket():
    """
    Handles information transfer between Game() and players
    """
    def _init__(self):
        """"""
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

    def _bind(self, HOST = socket.gethostbyname(socket.gethostname()),
        PORT = 8901):
        """"""
        try:
            self.serv_sock.bind((HOST, PORT))
        except OSError as err:
            print("Bind failed. Error Code : {0}".format(err))
            sys.exit()

        print('Socket{0},{1} bind complete'.format(HOST, PORT))
        self.serv_sock.listen(10)
        print('socket listening at {}'.format(PORT))

    def client_query(self):
        """"""

    def client_receive(self):
        """"""

    def client_query(self):
        """"""
    # TODO Add client query, client_receive and server ip verification methods
    # How to handle user requests async/when user needs it?