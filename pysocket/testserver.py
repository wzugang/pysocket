import pysocket

server=pysocket.pyserver(10000,"cert.pem","key.pem")
server.setwork(server.defaultwork())
server.working()
