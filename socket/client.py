import socket

host = ''		#remot host
port = 5007
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.conn(host,port)
s.sendall("hello world!")
data = s.recv(1024)
s.close()
print 'received',repr(data)









