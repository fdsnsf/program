# encoding=utf-8

import urllib2
import re
import sys
import pickle
import string

import draw

class LocationType(object):
	"""docstring for Urls"""

	type_name =  ''
	urls = list()
	areas = dict()
	url_count = 0

	def __init__(self, type_name):
		
		self.type_name = type_name
		self.areas = dict()
		self.urls = list()

	def add_area(self, area_name, area):
		if area_name not in self.areas:
			self.areas[area_name] = area
			self.url_count += 1

	def get_area_by_name(self, area_name):
		return self.areas[area_name]

	def add_other_url(self, location):
		self.urls.append(location)


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
	rooms = list()

	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.rooms = list()

class Room(object):
	"""docstring for Room"""
	price = 0
	url = ''
	name = ''
	style = ''
	subway = ''
	address = ''
	# 面积
	area = ''
	# 楼层
	floor = ''	
	# 格局
	pattern = ''
	# 合租类型
	roommate_type = ''
	#
	region = ''
	#
	subway_station = ''
	#
	sub_region = ''

	def __init__(self, name, price, url,style, subway, address, area,
		floor, pattern, roommate_type):
		self.name = name
		self.price = price
		self.url = url
		self.style = style
		self.subway = subway
		self.address = address
		self.area = area
		self.floor = floor
		self.pattern = pattern
		self.roommate_type = roommate_type

	def print_room(self):
		return ('%s -- %s -- %s -- %s -- %s -- %s -- %s -- %s -- %s -- %s -- %s -- %s -- %s' 
			% (self.name, self.price, self.url, self.style, self.subway, self.address, 
				self.area, self.floor, self.pattern, self.roommate_type, self.region, 
				self.subway_station, self.sub_region))


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


def analyze_url(datas):
	
	type_p = re.compile(r'<dt>(?P<type_name>.*)：</dt>')
	area_p = re.compile(r'<span class="tag"><a href="(?P<url>.*)">(?P<area>.*)</a') 
	location_p = re.compile(r'<a.*href="(?P<url>.*)"\s?>(?P<location>.*)</a>')
	search_type = dict()
	type_name = ''
	area_name = ''
	
	urls = dict()

	for data in datas:
		type_match = type_p.search(data)
		area_match = area_p.search(data)
		location_match = location_p.search(data)

		if type_match:
			type_name = type_match.group('type_name')
			if type_name == '更多':
				type_name = ''
				area_name = ''
			else:
				urls[type_name] = LocationType(type_name)

		elif area_match:
			area_name = area_match.group('area')
			urls[type_name].add_area(area_name, Area(area_name))

		elif location_match:
			l_name = location_match.group('location')
			l_url = location_match.group('url')
			l = Location(l_name, l_url)
			if type_name in urls:
				if area_name in urls[type_name].areas:
					urls[type_name].get_area_by_name(area_name).add_location(l)
				else:
					urls[type_name].add_other_url(l)

	return urls


def analyze_room(datas):

	start_p = re.compile(r'<li  class="clearfix">')
	end_p = re.compile(r'</li>')
	name_p = re.compile(r'<h3>.*href="(?P<url>.*)" class.*>(?P<name>.*)</a>')
	address_p = re.compile(r'<h4>')
	style_p = re.compile(r'class="style">(?P<style>.*)</span>')
	subway_p = re.compile(r'class="subway">(?P<subway>.*)</span>')
	price_p = re.compile(r'class="price">￥(?P<price>.*)<span')
	area_p = re.compile(r'<span>(?P<area>.*)㎡</span>')
	floor_p = re.compile(r'  <span>(?P<floor>.*层)</span>')	
	pattern_p = re.compile(r' <span>(?P<pattern>\d室\d厅)</span>')
	roommate_type_p = re.compile(r'class="icons">(?P<type>.*)</span>')

	name = ''
	price = 0
	url = ''
	style = ''
	subway = ''
	address = ''
	area = ''
	floor = ''	
	pattern = ''
	roommate_type = ''

	result = list()
	is_start = False
	address_start = -1

	for data in datas:
		start_m = start_p.search(data)

		if start_m:
			is_start = True
			name, price, url, style, subway, address, area, floor, pattern, roommate_type = ('', 0, '', '', '', 
				'', '', '', '', '')
			continue
		if is_start:
			end_m = end_p.search(data)
			name_m = name_p.search(data)
			address_m = address_p.search(data)
			style_m = style_p.search(data)
			subway_m = subway_p.search(data)
			price_m = price_p.search(data)
			area_m = area_p.search(data)
			floor_m = floor_p.search(data)
			pattern_m = pattern_p.search(data)
			roommate_type_m = roommate_type_p.search(data)

			if address_start > -1 and address_start<2:
				data = string.strip(data)
				d = data.split()
				address += d[0]
				address_start += 1
			if address_start>= 2:
				address_start = -1

			if name_m:
				name = name_m.group('name')
				url = name_m.group('url')
				continue
			if area_m:
				area = area_m.group('area')
			if floor_m:
				floor = floor_m.group('floor')
			if pattern_m:
				pattern = pattern_m.group('pattern')
			if roommate_type_m:
				roommate_type = roommate_type_m.group('type')
			elif address_m:
				address_start = 0
				continue
			elif style_m:
				style = style_m.group('style')
			elif subway_m:
				subway = subway_m.group('subway')
			elif price_m:
				price = price_m.group('price')
			elif end_m:
				result.append(Room(name, int(price), url, style, subway, address, area,
					floor, pattern, roommate_type))
				is_start = False

	return result

	#output = open('ziru/data', 'w')
	#pickle.dump(result, output)
	#for r in result:
	#	output.write(r.print_room() + '\n')
	#output.close()


def url_test(datas):
	#catch() 
	result = analyze_url(datas)
	#print search_type
	#s.decode('utf-8')
	interval = '----*****----\n'
	url_result = open('ziru/url', 'w')
	for s in result:
		url_result.write(interval)
		url_result.write(s+'\n')
		url_result.write(interval)

		for k in result[s].urls:
			url_result.write(k.name+' '+k.url+'\n')

		for p in result[s].areas:
			url_result.write(interval)
			url_result.write(p+'\n')
			url_result.write(interval)
			for l in result[s].areas[p].get_location():
				url_result.write(l.name+' '+l.url+'\n')

	url_result.close()

def down_data():

	url_template = 'http://www.ziroom.com/z/nl/z3.html?p='
	data_dump = open('ziru/data_dump', 'a')
	data_json = open("ziru/data_json", 'a')
	#data_temp = open("ziru/data_temp", 'w+')
	result = list()

	for page in range(1,250):
		url = url_template + str(page)
		print 'start down ...  '+url
		datas = get(url)
		print 'analyze ...'
		data_temp = open("ziru/data_temp", 'w+')
		data_temp.write(datas)
		data_temp.close()
		data_temp = open("ziru/data_temp")
		dd = analyze_room(data_temp.readlines())
		result.extend(dd)
		for r in dd:
			data_json.write(r.print_room() + '\n')

	pickle.dump(result, data_dump)
	data_dump.close()
	data_temp.close()
	data_json.close()



def analy_test():

	data_file = open('ziru/data_dump') 
	datas = pickle.load(data_file)
	data_file.close()

	#result_file = open('ziru/data', 'w')
	count = 0
	#region_p = re.compile(r'\[(?P<region>.*)\]')
	region = ''
	#datas.sort(key=lambda x:x.price)
	x = list()
	y = list()
	x_name = dict()
	for data in datas:
		count += 1
		#if data.address.find('东城') != -1 and int(data.price) < 2000:
		if count < 5:
			print data.print_room()
			#region_m = region_p.search(data.address)
			#if region_m:
			#	region = region_m.group('region')
				#print region
				#if region not in x_name:
				#	count += 1
				#	x_name[region] = count
				#x.append(x_name[region])
				#y.append(int(data.price))

			#result_file.write(data.print_room() + '\n')
			#print data.name, data.area, data.price, data.address
		#print data.price
	#print count
	#s = sorted(x_name.iteritems(), key=lambda x_name:x_name[1])
	#for name in s:
	#	result_file.write(str(name[1]) + " " +name[0]+ " ")
	#result_file.close()
	
	#draw.scatterplot(x,y,'priceDistributed')

def set_other_info():
	data_file = open('ziru/data_dump') 
	datas = pickle.load(data_file)
	data_file.close()

	region_p = re.compile(r'\[(?P<region>.*)\]')
	subway_p = re.compile(r'\](?P<subway>.*线)')
	sub_region_p = re.compile(r'线(?P<subre>.*)')
	for data in datas:
		region_m = region_p.search(data.address)
		subway_m = subway_p.search(data.address)
		sub_region_m = sub_region_p.search(data.address)
		if region_m:
			region = region_m.group('region')
			data.region = region
		if subway_m:
			data.subway_station = subway_m.group('subway')
		if sub_region_m:
			data.sub_region = sub_region_m.group('subre')
	data_dump = open('ziru/data_dump1', 'w')
	pickle.dump(datas, data_dump)
	data_dump.close()

def analy_data():

	data_file = open('ziru/data_dump') 
	datas = pickle.load(data_file)
	data_file.close()

	x = list()
	y = list()
	x_name_dic = dict()
	count = 0
	file_name = 'result/10_sub_region_price'
	x_name_file = open(file_name, 'w')

	for data in datas:
		if data.subway_station == '10号线':
			x_name = data.sub_region
			if x_name not in x_name_dic:
				count += 1
				x_name_dic[x_name] = count

			x.append(x_name_dic[x_name])
			y.append(int(data.price))

	s = sorted(x_name_dic.iteritems(), key=lambda x_name_dic:x_name_dic[1])
	for n in s:
		x_name_file.write(str(n[1]) + " " +n[0]+ " ")
	x_name_file.close()
	draw.scatterplot(x, y, file_name)


if __name__ == '__main__':

	#page = open('ziru/z3.html')
	#datas = page.readlines()
	#page.close()

	#analyze_room(datas)
	#url_test(datas)
	try:
		#down_data()	
		#set_other_info()
		#analy_test()
		analy_data()
	except BaseException, e:
		print e
	

