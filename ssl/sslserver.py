import socket, ssl, time

class sslServer:
    def __init__(self, ip, port, certFile, keyFile):
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain(certfile=certFile, keyfile=keyFile)
        self.bindsocket = socket.socket()
        self.bindsocket.bind(('localhost', 10000))

    def listen(self):
        self.bindsocket.listen(5)
        while True:
            self.newsocket, self.fromaddr = self.bindsocket.accept()
            self.server_ssl = self.context.wrap_socket(self.newsocket, server_side=True)
            self.work()

    def work(self):
        try:
            data=self.recv()
            print "%s" %(data)
            print self.send("OK")
        finally:
            self.server_ssl.shutdown(socket.SHUT_RDWR)
            self.server_ssl.close()

    def send(self,data):
        return self.server_ssl.send(data)

    def recv(self):
        return self.server_ssl.recv(1024)






