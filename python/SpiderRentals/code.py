# encoding=utf-8

import urllib2
import re
import sys

class Location:

	name = ''
	url = ''
	area = ''
	type_name = ''
	sub = ''

	def __init__(self, name, url):
		self.name = name
		self.url = url


def get(url):

	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	res = res_data.read()

	return res

    
def catch():

	ziru_url = 'http://www.ziroom.com/z/nl/z3.html?p=1'
	page = open('ziru/z3.html','w')
	page.write(get(ziru_url))
	page.close()


def analyze():

	page = open('ziru/z3.html')
	datas = page.readlines()
	page.close()
	
	type_p = re.compile(r'<dt>(?P<type_name>.*)：</dt>')
	area_p = re.compile(r'<span class="tag"><a href="(?P<url>.*)">(?P<area>.*)</a') 
	search_type = dict()
	type_name = ''
	for data in datas:
		type_match = type_p.search(data)
		area_match = area_p.search(data)
		if type_match:
			type_name = type_match.group('type_name')
			search_type[type_name] = dict()
		if area_match:
			area_name = area_match.group('area')
			search_type[type_name][area_name] = list()

	return search_type



if __name__ == '__main__':
	#catch() 
	search_type = analyze()
	print search_type
	for s in search_type:
		print s.decode('utf-8')
		for p in search_type[s]:
			print p.decode('utf-8')

