config.cfg
[ssl]
#证书文件路径
path=./ssl
ca_cert_file=ca.crt
cert_file=server.cer
key_file=server_unsecure_key.pem
#ssl版本设置,有效值为:sslv3,sslv23,tlsv1_1,tlsv1_2
version=tlsv1_2
#连接超时时间
timeout=30

[endpoint]
#服务端IP,IP可以不进行设置
ip=
#服务端使用端口,必须要设置,默认10000,可以根据实际需要修改
port=10000

[scc]
#最多接收请求次数,必须要设置,为0表示没有限制
max=0
#请求处理延时时间,必须要设置,为0表示不进行延时
interval=0
#报文收发配置文件
cfgfile=config.csv

config.py
#!/usr/bin/env python
import ConfigParser as config

class sccConfig:
    def __init__(self, sslFilePath):
        self.cfg=config.ConfigParser()
        self.cfg.read(sslFilePath)
    def caCertFile(self):
        return "{0}/{1}".format(self.cfg.get("ssl","path"), self.cfg.get("ssl","ca_cert_file"))
    def certFile(self):
        return "{0}/{1}".format(self.cfg.get("ssl","path"), self.cfg.get("ssl","cert_file"))
    def keyFile(self):
        return "{0}/{1}".format(self.cfg.get("ssl","path"), self.cfg.get("ssl","key_file"))
    def timeout(self):
        return self.cfg.getint("ssl","timeout")
    def version(self):
        return self.cfg.get("ssl","version")
    def ip(self):
        return self.cfg.get("endpoint","ip")
    def port(self):
        return self.cfg.getint("endpoint","port")
    def max(self):
        return self.cfg.getint("scc","max")
    def interval(self):
        return self.cfg.getint("scc","interval")
    def cfgfile(self):
        return self.cfg.get("scc","cfgfile")

clientcore.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import ssl
from config import sccConfig

class sccClient:
    def __init__(self, cfg):
        self.cfg=sccConfig(cfg)
        self.ca_cert_file = self.cfg.caCertFile()
        self.cert_file = self.cfg.certFile()
        self.key_file = self.cfg.keyFile()
        self.ip = self.cfg.ip()
        print self.ip
        self.port = self.cfg.port()

        #self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(self.cert_file, self.key_file)
        self.context.load_verify_locations(self.ca_cert_file)
        self.context.verify_mode = ssl.CERT_REQUIRED
        #self.context.verify_mode = ssl.CERT_NONE

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_client = self.context.wrap_socket(client_socket)
        self.ssl_client.connect((self.ip, self.port))

    def send(self, str):
        self.ssl_client.send(str)
    def recv(self):
        return self.ssl_client.read()

servercore.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,socket,ssl,time
from config import sccConfig

class sccServer:
    def __init__(self, cfg):
        self.cfg=sccConfig(cfg)
        self.ca_cert_file = self.cfg.caCertFile()
        self.cert_file = self.cfg.certFile()
        self.key_file = self.cfg.keyFile()
        self.version = self.cfg.version()
        self.timeout = self.cfg.timeout()
        self.ip = self.cfg.ip()
        self.port = self.cfg.port()
        self.count = 0
        self.max = self.cfg.max()
        self.interval = self.cfg.interval()
        self.cfgfile = self.cfg.cfgfile()
        self.stream = open(self.cfgfile,"r")
        self.context = self.ssl_check_and_create(self.version)
        self.context.load_cert_chain(self.cert_file, self.key_file)
        self.context.load_verify_locations(self.ca_cert_file)
        self.context.verify_mode = ssl.CERT_REQUIRED
        #self.context.verify_mode = ssl.CERT_NONE
        #context.set_default_verify_paths()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        #self.server_socket.settimeout(1)
        self.server_socket.bind((self.ip, self.port))

    def ssl_check_and_create(self,version):
        if "sslv3" == version:
            return ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        elif "sslv23" == version:
            return ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        elif "tlsv1_1" == version:
            return ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        elif "tlsv1_2" == version:
            return ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        else:
            print "ssl version error."
            return None

    def running(self):
        self.server_socket.listen(socket.SOMAXCONN)
        while True:
            client_socket, addr = self.server_socket.accept()
            try:
                self.ssl_client_socket = self.context.wrap_socket(client_socket, server_side=True)
                self.ssl_client_socket.settimeout(self.timeout)
            except ssl.SSLError, e:
                print e
                continue
            except ssl.SSLEOFError, e:
                print e
                continue
            if not self.working(self.max, self.interval):
                break
        self.server_socket.shutdown(2)
        self.server_socket.close()
        self.stream.close()

    def send(self, str):
        self.ssl_client_socket.send(str)

    def recv(self):
        return self.ssl_client_socket.read()
    def close(self):
        self.ssl_client_socket.shutdown(2)
        self.ssl_client_socket.close()

    def working(self,max,interval):
        while True:
            try:
                data = self.recv()
            except ssl.SSLError:
                self.close()
                return True
            else:
                if 0 == len(data):
                    self.close()
                    return True
                print("%s" % (str(data)))
                #print "%d,%d" % (max,interval)
                if (0 != interval):
                    time.sleep(interval)
                try:
                    ret=self.response()
                except ssl.SSLError:
                    self.close()
                    return True
                #self.close()
                #配置文件中没有记录了
                if not ret:
                    self.close()
                    return False
                self.count = self.count + 1
                #超过设置的最大响应次数了
                if (0 != max):
                    if (self.count >= max):
                        self.close()
                        return False
                #return True

    def getline(self):
        line = self.stream.readline()
        while 0 == cmp("\r\n",line):
            line = self.stream.readline()
        #需要去掉csv文件行尾换行符
        return line.replace("\r\n","")

    def get_response(self):
        #获取响应码
        linetext= self.getline()
        if 0 == len(linetext):
            return False,0,""
        try:
            code=int(linetext[0:linetext.index(',')])
            body=linetext[linetext.index(',')+1:]
            return True,code,body
        except ValueError:
            code=int(linetext)
            body=""
            return True,code,body

    def response(self):
        ret,code,body=self.get_response()
        if 200 == code:
            self.response_ok(body)
        elif 400 == code:
            self.response_error(body)
        elif 500 == code:
            self.response_server_error(body)
        else:
            pass
        return ret

    def response_ok(self,body):
        bodyLen = len(str(body))
        if 0 == bodyLen:
            resMsg="""HTTP/1.1 200 OK\r\nContent-Type: application/json;charset=utf-8\r\nServer: SERVICECENTER/3.0.0\r\nDate: %s\r\nContent-Length: 0\r\n\r\n""" % (os.popen("date -u").read().replace("\n",""))
        else:
            resMsg="""HTTP/1.1 200 OK\r\nContent-Type: application/json;charset=utf-8\r\nServer: SERVICECENTER/3.0.0\r\nDate: %s\r\nContent-Length: %d\r\n\r\n%s""" % (os.popen("date -u").read().replace("\n",""),bodyLen,body)
        self.send(resMsg)
        
    def response_error(self,body):
        bodyLen = len(str(body))
        if 0 == bodyLen:
            resMsg="""HTTP/1.1 400 Bad Request\r\nContent-Type: application/json;charset=utf-8\r\nServer: SERVICECENTER/3.0.0\r\nDate: %s\r\nContent-Length: 0\r\n\r\n""" % (os.popen("date -u").read().replace("\n",""))
        else:
            resMsg="""HTTP/1.1 400 Bad Request\r\nContent-Type: application/json;charset=utf-8\r\nServer: SERVICECENTER/3.0.0\r\nDate: %s\r\nContent-Length: %d\r\n\r\n%s""" % (os.popen("date -u").read().replace("\n",""),bodyLen,body)
        self.send(resMsg)
        
    def response_server_error(self,body):
        bodyLen = len(str(body))
        if 0 == bodyLen:
            resMsg="""HTTP/1.1 500 server error\r\nContent-Type: application/json;charset=utf-8\r\nServer: SERVICECENTER/3.0.0\r\nDate: %s\r\nContent-Length: 0\r\n\r\n""" % (os.popen("date -u").read().replace("\n",""))
        else:
            resMsg="""HTTP/1.1 500 server error\r\nContent-Type: application/json;charset=utf-8\r\nServer: SERVICECENTER/3.0.0\r\nDate: %s\r\nContent-Length: %d\r\n\r\n%s""" % (os.popen("date -u").read().replace("\n",""),bodyLen,body)
        self.send(resMsg)

server.py
#!/usr/bin/env python
#coding=utf-8
from sccServer import sccServer

server = sccServer("./config.cfg")
try:
    server.running()
except KeyboardInterrupt:
    print "\b\b\b\r\ntest server is stoped."

client.py
#!/usr/bin/env python
import os
from config import sccConfig
from sccClient import sccClient
from sccServer import sccServer

#cfg=sccConfig("./config.cfg")
#print cfg.caCertFile()
#print cfg.certFile()
#print cfg.keyFile()

client = sccClient("./config.cfg")
client.send("hello world.")
print client.recv()
