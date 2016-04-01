#coding=utf-8

import os

host_file = ''
def input_command(script_dir, is_first):

	host_file_list = ['1', '2', '3']
	command_list = ['get', 'keys', 'del', 'quit', 'g','d', 'q', 'k']
	global host_file

	if is_first:
		host_file = raw_input("redis host 所在文件(1,2,3):")
		if 	host_file not in host_file_list:
			print '脚本终止。。。文件不对'
			exit()

	keys = raw_input("输入key值，支持模糊查询:")

	command = raw_input("command get,keys,del or quit:")
	if command.lower() not in command_list:
		print '脚本终止，你可能输入了非法命令'
		exit()

	os.chdir(script_dir)
	redis_file = open(host_file)
	redis_hosts = redis_file.readlines()
	redis_file.close()

	return redis_hosts,keys,command

def run_command(redis_hosts, command, key):

	redis_dir = '/home/work/redis/redis-2.8.6-6481/src'
	os.chdir(redis_dir)
	for host in redis_hosts:
		h = host.split(':')
                print h[0],h[1]
		c = command % (h[0], h[1],key)
		result = os.system(c) 

def main():

	script_dir = os.getcwd()	
	keys_command = './redis-cli -h %s -p %s keys %s'
	get_command = './redis-cli -h %s -p %s get %s'
	del_command = './redis-cli -h %s -p %s del %s'
	is_first = True
	while True:
		redis_hosts,keys,command = input_command(script_dir, is_first)
		is_first = False
		if command=='keys' or command=='k':
			keys = '*%s*' % keys
			run_command(redis_hosts, keys_command, keys)

		elif command=='del' or command=='d':
			run_command(redis_hosts, del_command, keys)
			
		elif command=='get' or command=='g':
			run_command(redis_hosts, get_command, keys)
		else:
			print 'quit...'
			break


if __name__ == '__main__':
	try:
		main()
	except BaseException, e:
		print 'error', e
	
