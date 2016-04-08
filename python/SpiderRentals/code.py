# encoding=utf-8

import urllib2
import re
import sys


class LocationType(object):
	"""docstring for Urls"""

	type_name =  ''
	url = ''
	areas = dict()
	url_count = 0

	def __init__(self, type_name):
		
		self.type_name = type_name
		self.areas = dict()

	def add_area(self, area_name, area):
		if area_name not in self.areas:
			self.areas[area_name] = area
			self.url_count += 1

	def get_area_by_name(self, area_name):
		return self.areas[area_name]


class Area(object):
	"""docstring for Area"""

	name = ''
	url = ''
	locations = list()
	location_count = 0

	def __init__(self, name):
		self.name = name
		self.locations = list()

	def add_location(self, location):

		self.locations.append(location)
		self.location_count += 1

	def get_location(self):
		return self.locations

class Location(object):

	name = ''
	url = ''

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
	location_p = re.compile(r'<a href="(?P<url>.*)" >(?P<location>.*)</a>')
	search_type = dict()
	type_name = ''
	area_name = ''
	location_name = ''
	
	urls = dict()

	for data in datas:
		type_match = type_p.search(data)
		area_match = area_p.search(data)
		location_match = location_p.search(data)

		if type_match:
			type_name = type_match.group('type_name')
			urls[type_name] = LocationType(type_name)

		elif area_match:
			area_name = area_match.group('area')
			urls[type_name].add_area(area_name, Area(area_name))

		elif location_match:
			l_name = location_match.group('location')
			l_url = location_match.group('url')
			if type_name in urls:
				urls[type_name].get_area_by_name(area_name).add_location(Location(l_name, l_url))

	return urls



if __name__ == '__main__':
	#catch() 
	result = analyze()
	#print search_type
	#s.decode('utf-8')
	interval = '----*****----\n'
	url_result = open('ziru/url', 'w')
	for s in result:
		url_result.write(interval)
		url_result.write(s+'\n')
		url_result.write(interval)
		for p in result[s].areas:
			url_result.write(interval)
			url_result.write(p+'\n')
			url_result.write(interval)
			for l in result[s].areas[p].get_location():
				url_result.write(l.name+' '+l.url+'\n')

	url_result.close()

