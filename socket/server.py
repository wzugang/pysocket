import socket

host = ''
port = 5007
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(host,port)
s.listen(1)
conn,addr = s.accept()

print 'connected by ',addr
while 1:
	data = conn.recv(1024)
	if not data:break
	conn.sendall(data)
conn.close()







