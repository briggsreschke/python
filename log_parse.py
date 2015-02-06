'''
File: plog.py - (Apache log file parser) - GNU Public License
reschke.briggs@gmail.com

Parse Apache log file. regex pattern may need be altered to suit specfic log format
Includes optional user adaptable routines for further parsing of each field.
'''

import sys
import re

# Constants; Index values into logfile record
_VERBOSE_ = True 

_LOG_REGEX_ = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'

#Field index values into each logfile record
_HOST_ = 0
_DATE_ = 1
_TIME_ = 1
_TZ_ = 1
_METHOD_ = 2
_PATH_ = 2
_PROTOCOL_ = 2
_STATUS_ = 3
_BYTES_ = 4
_REFERER_ = 5
_AGENT_ = 6
		
# ----------------------------------------------------------------------------------
# Optional routines for  error checking or further parsing of individual log records

def log_host(arr):
	host = arr[_HOST_]
	
	if not host: 
		return 'none'
	return host

# Still need to do date and time parsing
def log_date(arr):
	regex = '^(\d+\/\w+\/\d+)'
	
	pattern = re.compile(regex)
	match = pattern.match(arr[_DATE_])
	
	if not match:
		return 'unknown'
	return match.group()
			
def log_time(arr):
	regex =  '^(\d+\/\w+\/\d+)((:\d\d)+)\s'
	
	pattern = re.compile(regex)
	match = pattern.match(arr[_TIME_])
	
	if not match:
		return 'unknown'
	return match.group(2)[1:]
	
def log_tz(arr):
	#regex =  '^(\d+\/\w+\/\d+)((:\d\d)+)(\s\S\d+)'
	regex =  '^(.+)(.+)(\s\S\d+)'
	
	pattern = re.compile(regex)
	match = pattern.match(arr[_TIME_])
	
	if not match:
		return 'unknown'
	return match.group(3)
	
	
def log_method(arr):
	method_list = ['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE', 'TRACE', 'CONNECT']
	
	tmp = arr[_METHOD_]
	method = tmp.split(' ')[0]

	if method not in method_list:
		return 'unknown'
	return method	


def log_path(arr):
	tmp = arr[_PATH_]
	regex = '[\/(\S*)]+'
	
	pattern = re.compile(regex)
	match = pattern.match(tmp.split(' ')[1])
	
	if not match:
		return 'none'
	return match.group()
	

def log_protocol(arr):
	tmp = arr[_PROTOCOL_]
	protocol = tmp.split(' ')[2]
	return protocol


def log_status(arr):
	# Could check against a list of all status codes
	status = arr[_STATUS_]
	
	if not status:
		return 'none'
	return status
	

def log_bytes(arr):	
	bytes = arr[_BYTES_]
	
	if not long(bytes):
		return '0'
	return bytes


def log_referer(arr):	
	referer = arr[_REFERER_]
	
	if referer == '-':
		return 'none'
	return referer


def log_agent(arr):
	# Much more to possibly do here
	agent = arr[_AGENT_]
	
	if agent == '-':
		return 'none'
	return agent


# ---------------------------------------------------------------------
	
# Entry point. Main loop

def log_parse(fname):	
	arr = []
	dicts = []
	
	try:
		# Read in records and parse them against regex 
		with open(fname, 'r') as f:
			line = f.readline().replace('\n', '')
			while (line):
				result = list(re.match(_LOG_REGEX_, line).groups())
				arr.append(result)
				line = f.readline().replace('\n', '')
			f.close()
	
		return arr
	except:
		if _VERBOSE_:
			print 'Error processing log file: ' + fname
		sys.exit(2)
	

#--------------------------------- main() -----------------------------

_TESTING_ = True

if __name__ == '__main__':
	
	if _TESTING_:
		try:
			records = log_parse('access.log')
		except:
			print 'Unable to proccess log file'
			sys.exit(1)
		
		for r in records:
			#print line
			print log_host(r) + ' ' + \
			log_date(r) + ' ' + \
			log_time(r) + ' ' + \
			log_tz(r) + ' ' + \
			log_method(r) + ' ' + \
			log_path(r) + ' ' + \
			log_protocol(r) + ' ' 
			log_status(r) + ' ' + \
			log_bytes(r) + ' ' + \
			log_referer(r) + ' ' + \
			log_agent(r)
			
		print 'processed ' + str(len(records)) + ' records' 
	
	sys.exit(0)
