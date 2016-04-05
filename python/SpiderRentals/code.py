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

	def add_area(area_name, area):
		if area_name not in areas:
			areas[area_name] = area
			url_count += 1

	def get_area():
		return areas

class Area(object):
	"""docstring for Area"""

	name = ''
	url = ''
	locations = list()
	location_count = 0

	def __init__(self, name):
		self.name = name
		
	def add_location(location):

		locations.append(location)
		location_count += 1

	def get_location():
		return locations

class Location:

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
	LocationType locations = LocationType('')
	urls = list()

	for data in datas:
		type_match = type_p.search(data)
		area_match = area_p.search(data)
		location_match = location_p.search(data)
		if type_match:
			type_name = type_match.group('type_name')
		elif area_match:
			area_name = area_match.group('area')
		elif location_match:


	return search_type



if __name__ == '__main__':
	#catch() 
	search_type = analyze()
	print search_type
	for s in search_type:
		print s.decode('utf-8')
		for p in search_type[s]:
			print p.decode('utf-8')

