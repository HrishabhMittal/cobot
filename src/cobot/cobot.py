from enum import Enum
from socket import AF_INET, SOCK_STREAM, socket


# felt cleaner
class Dirn(Enum):
    POSITIVE='+'
    NEGATIVE='-'



# main controlling class
class Cobot:

    def __init__(self,host: str,password: str):
        self.host=host
        self.port=5000
        self.sock=None
        self.password=password
    def __del__(self):
        self.disconnect()
    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # it is better to use `with` instead of these for proper socket operations
    def connect(self):
        self.sock=socket(AF_INET,SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        self.sock.recv(1) # 'a'
        self.sock.send(self.password.encode())
    def disconnect(self):
        if self.sock!=None:
            self.sock.close()
        self.sock=None
    def ping(self):
        if self.sock!=None:
            self.sock.send(b"p")
            self.sock.recv(1)
            return True
        return False
    # for jogging the cobot around
    def setVelocity(self,velocity):
        if self.sock!=None:
            self.sock.sendall(b"v"+str(velocity).encode())
    def jogJoint(self,dirn: Dirn,jointNo: int):
        if self.sock!=None:
            self.sock.sendall(b"j"+dirn.value.encode()+str(jointNo).encode())
    def jogCartesian(self,dirn: Dirn,jointNo: int):
        if self.sock!=None:
            self.sock.sendall(b"c"+dirn.value.encode()+str(jointNo).encode())

    # stop cobot
    def stopJogging(self):
        if self.sock!=None:
            self.sock.sendall(b"f")


    # grippers are now blocking to make sure the code syncs with cobot nicely
    def gripperOpen(self):
        if self.sock!=None:
            self.sock.sendall(b"go")
            self.ping()
    def gripperClose(self):
        if self.sock!=None:
            self.sock.sendall(b"gc")
            self.ping()

    # query operations: all return list[] with 6 decimal values
    def queryPos(self):
        if self.sock!=None:
            self.sock.sendall(b"qp")
            return eval(self.sock.recv(1024).decode())
        return []
    def queryJointVel(self):
        if self.sock!=None:
            self.sock.sendall(b"qjv")
            return eval(self.sock.recv(1024).decode())
        return []
    def queryJointRot(self):
        if self.sock!=None:
            self.sock.sendall(b"qjp")
            return eval(self.sock.recv(1024).decode())
        return []
    def queryJointTorque(self):
        if self.sock!=None:
            self.sock.sendall(b"qjt")
            return eval(self.sock.recv(1024).decode())
        return []
    def queryJointAccn(self):
        if self.sock!=None:
            self.sock.sendall(b"qja")
            return eval(self.sock.recv(1024).decode())
        return []
    

    # for recovery in case of failure, blocking function ~10s
    def baseRigid(self):
        if self.sock!=None:
            self.sock.sendall(b"b")
            self.ping()

    # stop the server (not only closes connection, but also terminates server on cobot)
    def stopServer(self):
        if self.sock!=None:
            self.sock.sendall(b"e")
