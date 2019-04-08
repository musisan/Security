#!/usr/bin/python
#-*- coding:utf-8 -*-
import base64,time
import threading,Queue
import sys
import ipaddr
import argparse
import subprocess


def decoLog(level):
	def deco(func):
		def logFunc(msg):
			sys.stdout.write(color.get(level) + """\
				\r[%s] [%s]: %s\
			""" % (time.strftime("%X"), level.upper(), msg) + \
				color.get('Normal')+'\n')
			if level.upper() == 'ERROR':
				sys.exit(1)
		return logFunc
	return deco

class LOG(object):
	@staticmethod
	@decoLog('Error')
	def LogError(msg):
		pass

	@staticmethod
	@decoLog('Debug')
	def LogDebug(msg):
		pass

	@staticmethod
	@decoLog('Info')
	def LogInfo(msg):
		pass

class PortScan(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self._queue = queue
		self.portlist = {
				'FTP': 21, 
				'SSH': 22,
				'SSH_ME': 20190,
				'Telnet': 23, 
				'SMTP': 25,
				'POP3': 110,
				'LDAP': 389,
				'Rsync': 873, 
				'SQL Server': 1433,
				'Oracle': 1521,
				'Squid': 3128,
				'MySQL': 3306,
				'RDP': 3389,
				'PostgreSQL': 5432,
				'Redis': 6379,
				'MongoDB': 27017
			}
	
	def run(self):
		while True:
			if self._queue.empty():
				break
			ip = str(self._queue.get(timeout=0.6))
			for port in self.portlist.values():
				#if int(port) == 6379:
				#	try:
				#		s.send('ping\n')
				#		r = s.recv(1024)
				#		if "+PONG" in r:
				#			sys.stdout.write('%s: %d is vul!\n' % (ip, port))
				#	except:
				#		continue
				cmd = 'cat</dev/null>/dev/tcp/'+str(ip)+'/'+str(port)
				status = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
				if status == 0:
					LOG.LogInfo(ip+': '+str(port))
				else:
					pass

def main():
	#figlet Asen -f smslant.flf
	logo_code = 'ICAgX19fICAgICAgICAgICAgICAKICAvIF8gfCBfX18gX19fIF9fXyAKIC8gX18gfChfLTwvIC1fKSBfIFwKL18vIHxfL19fXy9cX18vXy8vXy8KICAgICAgICAgICAgICAgICAgICAK'
	logo = base64.b64decode(logo_code)

	parser = argparse.ArgumentParser(description='Port Scan Vul')
	parser.add_argument("-i", "--cidr-ip", default=None, type=str, help="The CIDR IP LIKE 24")
	parser.add_argument("-c", "--thread-count", default=None, type=int, help="The THREAD NUMBER")
	args = parser.parse_args()
	if args.cidr_ip == None or args.thread_count == None:
		parser.print_help()
		exit(1)

	sys.stdout.write("\033[32m"+logo+"\033[0m")
	threads = []
	queue = Queue.Queue()
	if ',' not in args.cidr_ip:
		IPs = ipaddr.IPNetwork(args.cidr_ip)
	else:
		IPs = args.cidr_ip.split(',')
	thread_count = args.thread_count

	for ip in IPs:
		queue.put(ip)
	for i in xrange(thread_count):
		threads.append(PortScan(queue))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

if __name__ == '__main__':

	color = {
		'Error': '\033[31m',
		'Debug': '\033[33m',
		'Info': '\033[32m',
		'Normal': '\033[0m'
	}
	main()
