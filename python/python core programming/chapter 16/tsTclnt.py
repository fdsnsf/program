
from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
	data = raw_input('>')
	if not data:
		break
	tcpCliSock.send('%s\r\n' % data)
	data = tcpCliSock.recv(BUFSIZE)
	if not data:
		break
	print data

tcpCliSock.close()