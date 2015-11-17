
from socket import *
from time import ctime
import threading

HOST = 'localhost'
PORT = 21569
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)

def sendData(socket, serSock):
	while True:
		data = raw_input('>')
		if data == '' or data.isspace():
			print 'message can not be empty ...'
			continue
		if data == 'q':
			socket.close()
			serSock.close()
			print 'close ... '
			break
		socket.send('[%s] %s' % (ctime(), data))

def recvData(socket):
	while True:
		data = socket.recv(BUFSIZE)
		if not data or data=='q':
			print 'client close ...'
			socket.close()
			break
		print '\n', data
	

try:
	print 'waiting for connection...'
	tcpCliSock, addr = tcpSerSock.accept()
	print '...connected from:', addr
	sendthr = threading.Thread(target=sendData, args=(tcpCliSock, tcpSerSock))
	#sendthr.daemon = True
	sendthr.start()
	recvthr = threading.Thread(target=recvData, args=(tcpCliSock,))
	recvthr.daemon = True
	recvthr.start()
	#tcpCliSock.close()
except KeyboardInterrupt, e:
	tcpSerSock.close()
	tcpCliSock.close()
	print 'server close...'
