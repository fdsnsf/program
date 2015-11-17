
from socket import *
from time import ctime

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

try:
	tcpCliSock = socket(AF_INET, SOCK_STREAM)
	tcpCliSock.connect(ADDR)

	while True:
		data = raw_input('>')
		if not data:
			break
		tcpCliSock.send('[%s]%s' % (ctime(), data))
		data = tcpCliSock.recv(BUFSIZE)
		if not data:
			break
		print data

except KeyboardInterrupt, e:
	tcpCliSock.close()
	print 'client close...'
