import socket


class Cobot:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.sock=None
    def __del__(self):
        self.disconnect()
    def __enter__(self):
        self.connect()
    def __exit__(self):
        self.disconnect()
    def connect(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
    def disconnect(self):
        if self.sock!=None:
            self.sock.close()
        self.sock=None
