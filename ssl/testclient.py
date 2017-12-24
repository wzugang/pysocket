from sslclient import sslClient

client=sslClient("47.100.22.213",10000,"cert.pem")

client.send("hello world")
print client.recv()
client.close()
