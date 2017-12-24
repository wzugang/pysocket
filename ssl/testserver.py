from sslserver import sslServer

server=sslServer("47.100.22.213",10000,"cert.pem", "key.pem")
server.listen()

