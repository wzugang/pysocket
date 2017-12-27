import socket
import pyssl

class pyserver:
    def __init__(self,port,certfile,keyfile,ca_certfile=None,password=None):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.ctx = pyssl.pyssl(certfile,keyfile,ca_certfile,password)
        self.server_socket.bind(("",port))
    def working(self):
        self.server_socket.listen(socket.SOMAXCONN)
        while True:
            client_socket,client_addr = self.server_socket.accept()
            self.ctx.wrap_server(self.client_socket)
            self.work()

    def setwork(self,work):
        self.work = work

    def send(self,buffer):
        self.ctx.send(buffer)

    def recv(self):
        return self.ctx.recv()

    def defaultwork(self):
        print self.recv()
        self.send("OK")

class pyclient:
    def __init__(self,ip,port,certfile,keyfile,ca_certfile=None,password=None):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ctx = pyssl.pyssl(certfile,keyfile,ca_certfile,password)
        self.ctx.wrap_client(self.client_socket)
        self.ctx.connect((ip,port))

    def working(self):
        self.work()

    def setwork(self,work):
        self.work = work

    def send(self,buffer):
        self.ctx.send(buffer)

    def recv(self):
        return self.ctx.recv()

    def defaultwork(self):
        self.send("hello world")
        print self.recv()