import socket, ssl, pprint, time

class sslClient:
    def __init__(self, ip, port, ca_certs):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_ssl = ssl.wrap_socket(self.client, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
        print self.client_ssl.connect(('localhost', 10000))
        time.sleep(0.5)
        pprint.pprint(self.client_ssl.getpeercert())

    def send(self,data):
        return self.client_ssl.send(data)

    def recv(self):
        return self.client_ssl.recv(1024)

    def close(self):
        self.client_ssl.close()


