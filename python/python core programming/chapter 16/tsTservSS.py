
from SocketServer import (TCPServer as TCP,
	StreamRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 21567
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
	"""docstring for MyRequestHandler"""
	def handle(self):
		print '...connected from', self.client_address
		self.wfile.write('[%s] %s' % (ctime(), self.rfile.readline()))

tcpServ = TCP(ADDR, MyRequestHandler)
print 'waiting for connection...'
try:
	tcpServ.serve_forever()
except KeyboardInterrupt, e:
	tcpServ.server_close()
	print 'server close...'

		