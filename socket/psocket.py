import SocketServer,commands,time
class psocket(SocketServer.BaseRequestHandler):
	def handle(self):
		while 1:
			self.data = self.request.recv(1024).strip()
			print "{} wrote:".format(self.client_address[0])
			if not self.data:
				print "client %s is exit !" %self.client_address
				break
			#user_input = self.data.split()
			#if user_input[0] == 'get':
			#	with open(user_input[1],'rb') as f
			#		self.request.sendall(f.read())
			#	time.sleep(0.5)
			#	self.request.send("FileTransferDone")
			#	continue
			#
			#cmd_status,result = commands.getstatusoutput(self.data)
			#if len(result.strip()) != 0:
			#	self.request.sendall(result)
			#else:
			#	self.request.sendall("Done")
			self.request.sendall(self.data.upper())
			
	
if __name__ == "__main__":
	host,port = "localhost",9999
	server = SocketServer.ThreadingTCPServer((host,port),psocket)
	server.serve_forever()
	
	
	