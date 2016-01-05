# Retrieve all the .tar files from an NRAO VLA archive folder
# ian.heywood@csiro.au

import urllib2
import base64
import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u','--user',dest='myuser',help='Archive username')
parser.add_option('-p','--password',dest='mypass',help='Archive password')
(options,args) = parser.parse_args()

myuser = options.myuser
mypass = options.mypass

archiveurl = 'https://archive.nrao.edu/secured/'
request = urllib2.Request(archiveurl+myuser)
request.add_header('Authorization',b'Basic '+base64.b64encode(myuser+b':'+mypass))
result = urllib2.urlopen(request)

pagesrc = result.readlines()

for item in pagesrc:
	cols = item.split()
	if cols[0] == '<a':
		target = cols[1].split('">')[0].replace('href="','')
		fcomps = target.split('.')
		if (fcomps[-1] == 'tar') and (fcomps[-2] == 'ms'):
			if not os.path.isfile(target):
				syscall = 'wget --user='+myuser+' --password='+mypass+' '+archiveurl+myuser+'/'+target
				print syscall
				os.system(syscall)
			else:
				print target,'already exists locally, skipping'
