#coding=utf-8

from socket import *
from time import ctime
import threading

class ChatRoomServer(object):

	def __init__(self, host='localhost', port=21569, bufsize=1024):
		self.bufsize = bufsize
		self.addr = (host, port)
		self.serSocket = socket(AF_INET, SOCK_STREAM)
		self.serSocket.bind(self.addr)
		self.serSocket.listen(5)
		self.cliSocket = []

	def forever(self):
		try:
			print 'waiting for connection...'
			while True:
				cliSocket, addr = self.serSocket.accept()
				print 'connect from ', addr
				self.cliSocket.append(cliSocket)
				sendthr = threading.Thread(target=self.sendData, args=(cliSocket,))
				#sendthr.daemon = True
				sendthr.start()
				recvthr = threading.Thread(target=self.recvData, args=(cliSocket,))
				recvthr.daemon = True
				recvthr.start()
		except KeyboardInterrupt, e:
			self.close()
			print 'server close ...'

	def close(self):
		for socket in self.cliSocket:
			socket.close()
		self.serSocket.close()

	def sendData(self, cliSocket):
		while True:
			data = raw_input()
			if len(data) == 0 or data.isspace():
				print 'message can not be empty ...'
				continue
			cliSocket.send('[%s] %s' % (ctime(), data))

	def recvData(self, cliSocket):
		while True:
			data = cliSocket.recv(self.bufsize)
			if not data or data=='q':
				print 'client close ...'
				for i in range(len(self.cliSocket)):
					if self.cliSocket[i] == cliSocket:
						self.cliSocket[i].close()
						del self.cliSocket[i]
				break
			print '\n', data
			
if __name__ == '__main__':
	s = ChatRoomServer()
	s.forever()