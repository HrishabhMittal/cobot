import socket
import time
from enum import Enum


# felt cleaner
class Dirn(Enum):
    POSITIVE='+'
    NEGATIVE='-'



# main controlling class
class Cobot:

    def __init__(self,host):
        self.host=host
        self.port=5000
        self.sock=None
    def __del__(self):
        self.disconnect()

    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # it is better to use `with` instead of these for proper socket operations
    def connect(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
    def disconnect(self):
        if self.sock!=None:
            self.sock.close()
        self.sock=None

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
            time.sleep(5)
    def gripperClose(self):
        if self.sock!=None:
            self.sock.sendall(b"gc")
            time.sleep(5)

    
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
            time.sleep(10)

    # stop the server (not only closes connection, but also terminates server on cobot)
    def stopServer(self):
        if self.sock!=None:
            self.sock.sendall(b"e")
