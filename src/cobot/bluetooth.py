from socket import AF_INET, SOCK_STREAM, socket
import serial
class BluetoothCobot:
    def __init__(self,host: str,comm: str,password: str):
        self.host=host
        self.port=5000
        self.sock=socket(AF_INET,SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        self.sock.recv(1) # 'a'
        self.sock.send(password.encode())
        self.ser=serial.Serial(comm,9600,timeout=0.1)
    def reroute(self):
        running=True
        while running:
            if self.ser.in_waiting>0:
                data=self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                self.sock.send(data.encode())
                for i in data:
                    if i=='e' or i=='d':
                        running=False
    def __del__(self):
        self.sock.close()
        self.ser.close()
