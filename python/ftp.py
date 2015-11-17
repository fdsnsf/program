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
			print self.f.login(user, passwd)
		except Exception, e:
			self.quit()
			raise e
	def  quit(self):
		return self.f.quit()

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

	def dir(self):
		return self.f.dir()
	def pwd(self):
		print self.f.pwd()



		
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
		os._exit(0)
	ftp = Ftp(sys.argv[1], sys.argv[2], sys.argv[3])
	while True:
		try:
			cmd = raw_input('>:')
			parms = cmd.split()
			if parms[0] == 'quit' or parms[0] == 'q':
				print ftp.quit()
				break
			elif parms[0] == 'cd' or parms[0] == 'cwd':
				ftp.cwd(parms[1])
			elif parms[0] == 'dir' or parms[0] == 'ls':
				ftp.dir()
			elif parms[0] == 'd' or parms[0] == 'download':
				ftp.download(parms[1])
			elif parms[0] == 'pwd':
				ftp.pwd()
			elif parms[0] == 'u' or parms[0] == 'upload':
				ftp.upload(parms[1])
			elif parms[0] == 'r' or parms[0] == 'rename':
				ftp.rename(parms[1], parms[2])
			else:
				print ('---- q or quit 退出      ---- cd or cwd 切换目录\n'
				       '---- d or download 下载  ---- pwd  获取当前目录\n'
				       '---- u or upload 上传    ---- ls or dir 获取当前目录内容\n'
				       '---- r or rename 修改文件名\n')

		except Exception, e:
			print 'ERROR: ',e 
		


	
