
from socket import *
from time import ctime

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)
try:
	while True:
		print 'waiting for connection...'
		tcpCliSock, addr = tcpSerSock.accept()
		print '...connected from:', addr
		while True:
			data = tcpCliSock.recv(BUFSIZE)
			if not data:
				break
			print data
			data = raw_input('>')
			tcpCliSock.send('[%s] %s' % (ctime(), data))
		tcpCliSock.close()
except KeyboardInterrupt, e:
	tcpSerSock.close()
	print 'server close...'
