import socket
import sys

host,port = "localhost",9999

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect((host,port))

while 1:
	cmd = raw_input("Imput An command:").strip()
	if len(cmd) == 0:continue
	sock.sendall(cmd)
	
	if cmd.split()[0] == 'get':
		with open(cmd.split()[1],'wb') as f
			while 1:
				data = f.recv(1024)
				if data == "FileTransferDone":break
				#if not data:break
				f.write(data)		
		continue
	else:	
		print sock.recv(8096)

sock.close()


#not data s.close()


