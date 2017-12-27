import ssl

class pyssl:

    def __init__(self,certfile,keyfile,ca_sert_file=None,password=None):
        self.ctx=ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.ctx.load_cert_chain(certfile,keyfile,password=password)
        if(None !=ca_sert_file):
            self.ctx.load_verify_locations(ca_sert_file)
        self.ctx.verify_mode=ssl.CERT_REQUIRED
        #self.ctx.set_default_verify_paths()

    def wrap_server(self,socket):
        method=type.MethodType(self.ctx.wrap_socket(socket,server_side=True,do_handshake_on_connect=True),None,pyssl)
        setattr(pyssl,"ssl_socket",method)

    def wrap_client(self,socket):
        setattr(pyssl,"ssl_socket",self.ctx.wrap_socket(socket,do_handshake_on_connect=True))
        #self.ssl_socket=self.ctx.wrap_socket(socket,server_side=True,do_handshake_on_connect=True)

    def connect(self,addr):
        self.ssl_socket.connect(addr)

    def recv(self):
        return self.ssl_socket.read()

    def send(self,buffer):
        self.ssl_socket.send(buffer)

    def close(self):
        self.ssl_socket.shutdown(1)
