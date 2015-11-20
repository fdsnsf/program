#coding=utf-8

from socket import *
from time import ctime
import threading

class Client(object):
	def __init__(self, cliSocket, no, isOnline, name='client'):
		self.cliSocket = cliSocket
		self.no = no 
		self.name = name 
		self.isOnline = isOnline


class ChatRoomServer(object):

	def __init__(self, host='localhost', port=21569, bufsize=1024):
		self.bufsize = bufsize
		self.addr = (host, port)
		self.serSocket = socket(AF_INET, SOCK_STREAM)
		self.serSocket.bind(self.addr)
		self.serSocket.listen(5)
		self.client = {}
		self.cliNo = 0

	def forever(self):
		try:
			print 'waiting for connection...'
			while True:
				cliSocket, addr = self.serSocket.accept()
				print '%d connect from %s' % (self.cliNo, addr)
				client = Client(cliSocket, self.cliNo, 1, addr)
				self.client[self.cliNo] = client 
				
				sendthr = threading.Thread(target=self.sendData, args=(self.cliNo, ))
				sendthr.daemon = True
				sendthr.start()
				recvthr = threading.Thread(target=self.recvData, args=(self.cliNo, ))
				recvthr.daemon = True
				recvthr.start()
				self.cliNo += 1
		except KeyboardInterrupt, e:
			self.close()
			print 'server forever close ...'

	def close(self):
		for key in self.client.values():
			self.client[key].cliSocket.close()
		self.serSocket.close()

	def sendData(self,  no):
		print '%d send start ... ' % no
		while self.client[no].isOnline:
			data = raw_input()
			if len(data) == 0 or data.isspace():
				print 'message can not be empty ...'
				continue
			if data == 'q':
				print 'server send close ...'
				#self.close()
				break
			if self.client[no].isOnline:
				self.client[no].cliSocket.send('[%s] %s' % (ctime(), data))
			else:
				print 'client is quit, can not send message'
		del  self.client[no]
		print '%d send close ...' % no

	def recvData(self, no):
		print '%d recv start ...' % no
		while self.client[no].isOnline:
			data = self.client[no].cliSocket.recv(self.bufsize)
			if not data or data=='q':
				self.client[no].isOnline = 0
				print '%d client close ...' % no
				self.client[no].cliSocket.close()
				#del self.client[no]
				break
			print '\n', data
		print '%d recv close ...' % no
			
if __name__ == '__main__':
	s = ChatRoomServer()
	s.forever()