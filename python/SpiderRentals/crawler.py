#encoding=utf-8
import urllib
import urllib2
import re
import threading
from time import ctime, sleep
from datetime import datetime

def get(url):
	"""
	"""
	req = urllib2.Request(url)
	req.add_header('Cookie','sessionid=e0qxvm90qtf1n4cqpdpoxmycuapzjg95; csrftoken=U91tKA1T5M0uA9pUfUThQd0kVnVyYQOi; Hm_lvt_74e694103cf02b31b28db0a346da0b6b=1456282705; Hm_lpvt_74e694103cf02b31b28db0a346da0b6b=1457857531')
	
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	#header
	#print res_data.info()
	return res

def post(url, values):

	data = urllib.urlencode(values)
	#print data
	req = urllib2.Request(url, data)
	req.add_header('Cookie','sessionid=e0qxvm90qtf1n4cqpdpoxmycuapzjg95; csrftoken=U91tKA1T5M0uA9pUfUThQd0kVnVyYQOi; Hm_lvt_74e694103cf02b31b28db0a346da0b6b=1456282705; Hm_lpvt_74e694103cf02b31b28db0a346da0b6b=1457857531')
	res_data = urllib2.urlopen(req)
	res = res_data.read()

	return res

def crawler01():
	#ziru
	url = 'http://www.ziroom.com/z/nl/z3.html?p=1'
	url2 = 'http://www.heibanke.com/lesson/crawler_ex00/'
	nextUrl = '62816'

	p = re.compile(r'<h3>[^\d]*(?P<result>\d+).</h3>')

	print url2+nextUrl
	#print res
	while True:	
		res = get(url2+nextUrl)
		match = p.search(res)
		if match:
			nextUrl = match.group(1)
			print url2+nextUrl
		else:
			print 'not search any'
			break	

def crawler02():

	url = 'http://www.heibanke.com/lesson/crawler_ex01/'
	values = {'csrfmiddlewaretoken':'E6vAOR1M5YbqnnSuNcjRlSQtMNocmLEw',
	'username':'t','password':3}
	p = re.compile(r'<h3>您输入的密码错误, 请重新输入</h3>')

	for i in range(30):
		print values['password']
		res = post(url, values)
		match = p.search(res)
		if match:
			values['password'] = i
		else:
			print 'pass'
			break

def crawler03():

	url = 'http://www.heibanke.com/lesson/crawler_ex02/'
	values = {'csrfmiddlewaretoken':'pJXuIuN8XvDO7gyKus1XKFaYzGIU1NtO',
	'username':'t','password':3}
	p = re.compile(r'<h3>您输入的密码错误, 请重新输入</h3>')

	res = post(url, values)
	#print res

	
	for i in range(30):
		print values['password']
		res = post(url, values)
		match = p.search(res)
		if match:
			values['password'] = i
		else:
			print 'pass'
			break
	
def crawler04():

	try:
		start = datetime.now()
		print 'start at', ctime()
		password = {}
		isRun = True

		for i in range(3):
			t = threading.Thread(target=loop, args=(password, i, isRun))
			t.start()
			sleep(1)

		while len(password) != 100:
			pass

		result = ''
		for i in range(100):
			result += password[str(i+1)]
		print result

		end = datetime.now()
		print 'end at', ctime()
		print 'cost ', end - start
		#3265314901636687745662881736185382536752649723381830867445135357748950695244329548946136479903948743
	except (Exception,KeyboardInterrupt), e:
		isRun = False
		print 'exitting...'
		sleep(15)
		print 'exited...'
		
	
def loop(password, index, isRun):

	print 'threading %s start at %s' % (index, ctime())
	
	try:
		dataurl = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page='
		page = 1
		p = re.compile(r'password_\w{3}">(\d+)')
		totalCount = 0
	
		while isRun and len(password) != 100:
			res = get(dataurl+str(page))
			match = p.findall(res)
			if match:
				count = 0
				for i in range(0, len(match), 2):
					if match[i] in password:
						continue
					password[match[i]] = match[i+1]
					count += 1
				print 'threading_%s now match %s password has %s' % (index, count, len(password)) 
				totalCount += count
	except Exception, e:
		print 'threading %s is game over, reason %s' % (index, e)
	print 'threading %s end at %s total match %s' % (index, ctime(), totalCount)


if __name__ == '__main__':
	crawler04()
	#loop({}, 1)


