'''
csvm.py - simple delete rows and cols from a csv, and extra build a json document

'''

import sys
import os.path
import re
import shutil

TESTING = 1

#--------------------------------------------------------------------
# Get backup file name

def get_bakname(fname):

	cnt = 0
	foo = True
	
	# make backup filename to start with
	bname = fname + '.bak'
	# try backup file names until an unused one
	while(foo):
		if os.path.isfile(bname):
			cnt += 1
			bname = fname + '.bak' + str(cnt) 
		else:
			foo = False
	
	return bname

#--------------------------------------------------------------------
# Copy data to a backup file

def create_backup(fname, delimiter):
	
	bname = get_bakname(fname)
	shutil.copyfile(fname, bname)

#--------------------------------------------------------------------
# Get data from csv file and append it to a list
	
def get_data(fname, delimiter):
	data = []
	
	create_backup(fname, delimiter)
	
	try:
		ip = open(fname)
	except:
		print 'Could not open input file in get_data()'
		sys.exit(15)
	
	line = ip.readline()	
	while(line):
		data.append(line.split(delimiter))
		line = ip.readline()
	
	ip.close()
	return data
		
# ------------------------------------------------------------------	
#Deletes columns (row[column]) from list of col numbers

def delete_cols(fname, cols, header, delimiter): 	
	
	# get list of file data
	data = get_data(fname, delimiter)
		
	# Make sure input file had data in it
	if not len(data):
		print 'No data to process in delete_cols()'
		sys.exit(2)
	
	# Make sure number of columns does not exceed the data cols
	if len(cols) > len(data):
		print 'cols is greater than columns in data.'
		sys.exit(12)
			
	# Open csv file and truncate it	
	try:
		of = open(fname, 'w+')
	except:
		print 'Could not open input file in delete_cols().'
		sys.exit(15)
	
	count = 0
	
	# if there is a header, save it
	if header:
		head = data[count]
	
	for row in data:
		# Delete rows provided in cols list
		for idx, column in enumerate(cols):
			column -= idx
			del row[column]		
			
			# if header delete column name of delete column
			if header:
				del head[column]
		
		# write header if there is one
		if header and count == 0:
			of.write(delimeter.join(head))
			
		# write the row with elimnated cols
		of.write(delimiter.join(row))
		
		# increment row index
		count += 1
	
	of.close()				

	return count

# -----------------------------------------------------------------	
# Deletes rows (skips them) if regex do not match cells

def delete_rows(fname, mdict, header, delimiter):
	
	# Get data
	data = get_data(fname, delimiter)
	
	if not len(data):
		print 'No data to process in delete_rows()'
		sys.exit(2)
			
	# Open the csv file	and truncate it 	
	try:
		of = open(fname,'w+')
	except:
		print 'Could not open file in delete_rows()'
		sys.exit(10)

			
	count = 0			
	is_match = False
	
	# Save header and increment count
	if header:
		head = data[0]
	
	for row in data:
		
		# iterate through key:value pairs {column number:regex}
		for key, value in mdict.iteritems():
			# if cell *does not* match against regex, delete row (skip it)
			p = re.compile(value)				
			if not p.match(row[key]):
				is_match = False
				break
			else:
				is_match = True
			
		# if all matches are good, write the row
		if is_match == True:	
			# put the header back
			if header and count == 0:
				of.write(delimeter.join(head))
			# write the row
			of.write(delimiter.join(row))
			
			count += 1
			
		is_match = False
	
	of.close()

	return count

# -------------------------------------------------------------------
# Inserts a header. Only useful if there never was one

def insert_header(ifile, hlist, delimiter):

	if not os.path.isfile(ifile):
		print 'Input file ' + ifile + ' does not exist'
		sys.exit(5)
	
		
# --------------------------------------------------------------------	
# Make a json document from csv

def to_json(ifile, ofile, header, delimiter):
	# Create utf-8 json from csv

	print

# --------------------------------------------------------------------	
# Make a json document from csv	
			
def main():
	
	if TESTING:
		cols = [2,3, 7, 8, 9, 10, 13, 14]
		cn = delete_cols('csvm-test.csv' , cols, False, ',')
	
		print '\nProcessed ' + str(cn) + ' records'
	
		dict = {3:'^(SP|NP|NF)$'}
		rn = delete_rows('csvm-test.csv' , dict, False, ',')

		print 'Deleted ' + str(cn-rn) + ' rows'

if __name__ == '__main__':
	
	main()
	sys.exit(0)
			
