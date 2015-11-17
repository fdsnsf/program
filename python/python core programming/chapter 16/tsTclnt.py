
from socket import *
from time import ctime
import threading

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

def sendData(socket):
	while True:
		data = raw_input('>')
		if data == 'q':
			break
		socket.send('[%s] %s' % (ctime(), data))

def recvData(socket):
	while True:
		data = socket.recv(BUFSIZE)
		if not data:
			break
		print '\n', data

try:
	tcpCliSock = socket(AF_INET, SOCK_STREAM)
	tcpCliSock.connect(ADDR)

	sendthr = threading.Thread(target=sendData, args=(tcpCliSock,))
	#sendthr.daemon = True
	sendthr.start()
	recvthr = threading.Thread(target=recvData, args=(tcpCliSock,))
	recvData.daemon = True
	recvthr.start()

except KeyboardInterrupt, e:
	tcpCliSock.close()
	print 'client close...'
