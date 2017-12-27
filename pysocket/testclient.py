import pysocket

client=pysocket.pyclient("47.100.22.213",10000,"cert.pem","key.pem")
client.setwork(client.defaultwork())
client.working()
