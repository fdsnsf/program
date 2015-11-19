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
		self.cliSocket = {}
		self.cliNo = 0

	def forever(self):
		try:
			print 'waiting for connection...'
			while True:
				cliSocket, addr = self.serSocket.accept()
				print '%d connect from %s' % (self.cliNo, addr)
				self.cliSocket[self.cliNo] = cliSocket
				
				sendthr = threading.Thread(target=self.sendData, args=(cliSocket, self.cliNo))
				sendthr.daemon = True
				sendthr.start()
				recvthr = threading.Thread(target=self.recvData, args=(cliSocket, self.cliNo))
				recvthr.daemon = True
				recvthr.start()
				self.cliNo += 1
		except KeyboardInterrupt, e:
			self.close()
			print 'server forever close ...'

	def close(self):
		for key in self.cliSocket.keys():
			self.cliSocket[key].close()
		self.serSocket.close()

	def sendData(self, cliSocket, no):
		print '%d send start ... ' % no
		while True:
			data = raw_input()
			if len(data) == 0 or data.isspace():
				print 'message can not be empty ...'
				continue
			if data == 'q':
				print 'server send close ...'
				#self.close()
				break
			cliSocket.send('[%s] %s' % (ctime(), data))
		print '%d send close ...' % no

	def recvData(self, cliSocket, no):
		print '%d recv start ...' % no
		while True:
			data = cliSocket.recv(self.bufsize)
			if not data or data=='q':
				print '%d client close ...' % no
				self.cliSocket[no].close()
				del self.cliSocket[no]
				break
			print '\n', data
		print '%d recv close ...' % no
			
if __name__ == '__main__':
	s = ChatRoomServer()
	s.forever()