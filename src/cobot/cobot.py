import socket
from enum import Enum
class Dirn(Enum):
    POSITIVE='+'
    NEGATIVE='-'
class Cobot:
    def __init__(self,host):
        self.host=host
        self.port=5000
        self.sock=None
    def __del__(self):
        self.disconnect()
    def setVelocity(self,velocity):
        if self.sock!=None:
            self.sock.sendall(b"v"+str(velocity).encode())
    def jogJoint(self,dirn: Dirn,jointNo: int):
        if self.sock!=None:
            self.sock.sendall(b"j"+dirn.value.encode()+str(jointNo).encode())
    def jogCartesian(self,dirn: Dirn,jointNo: int):
        if self.sock!=None:
            self.sock.sendall(b"c"+dirn.value.encode()+str(jointNo).encode())
    def gripperOpen(self):
        if self.sock!=None:
            self.sock.sendall(b"go")
    def gripperClose(self):
        if self.sock!=None:
            self.sock.sendall(b"gc")
    def stopServer(self):
        if self.sock!=None:
            self.sock.sendall(b"q")
    def stopJogging(self):
        if self.sock!=None:
            self.sock.sendall(b"f")
    def baseRigid(self):
        if self.sock!=None:
            self.sock.sendall(b"b")
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
