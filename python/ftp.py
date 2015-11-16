#coding=utf-8

import ftplib
import os
import socket
import sys

HOST = 'ftp.org'
DIRN = '/home/test'
FILE = 'test.txt'

class Ftp(object):
	def __init__(self, host, user, passwd):
		self.f = ftplib.FTP(host)
		try:
			self.f.login(user, passwd)
		except Exception, e:
			self.quit()
			raise e
	def  quit(self):
		self.f.quit()

	def  cwd(self, dirn):
		print self.f.cwd(dirn)

	def download(self, filename):
		locfile = open(filename, 'wb')
		self.f.retrbinary('RETR %s' % filename, locfile.write)
		locfile.close()

	def upload(self, filename):
		f = open(filename, 'r')
		self.f.storlines('RETR %s' % filename,f)
		f.close()

	def rename(self, old, new):
		self.f.rename(old, new)



		
	 #os.unlink(FILE)
	 #loc.readlines()
	 #loc.close()
	 #f.delete('/home/test/test.py')
	 #f.mkd('/home/test')
	 #f.rmd('/home/test')
	 #f.rename(old,new)
	 #f.login(user='', paddwd='', acct='')
	 #f.storlines(cmd,f)
	 #f.storbinary(cmd,f,bs=8192)
	 #f.retrlines(cmd,cb)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print 'please input host, user, passwd'
	ftp = Ftp(sys.argv[1], sys.argv[2], sys.argv[3])
	while True:
		try:
			cmd = raw_imput('>:')
			parms = cmd.split(',')
			if cmd[0] == 'quit' or cmd[0] == 'q':
				ftp.quit()
				break
			elif cmd[0] == 'cwd':
				ftp.cwd(parms[1])
		except Exception, e:
			print 'ERROR ' 
		


	
