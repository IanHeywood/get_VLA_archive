# Retrieve all the .tar files from an NRAO VLA archive folder
# ian.heywood@csiro.au

import urllib2
import base64
import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u','--user',dest='myuser',help='Archive username')
parser.add_option('-p','--password',dest='mypass',help='Archive password')
parser.add_option('-r','--resume',dest='resume',action='store_true',help='Resume broken downloads (default = False, which skips existing files)')
(options,args) = parser.parse_args()

myuser = options.myuser
mypass = options.mypass
resume = options.resume

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
				# No local file present, proceed to download
				syscall = 'wget --user='+myuser+' --password='+mypass+' '+archiveurl+myuser+'/'+target
				print syscall
				os.system(syscall)
			elif os.path.isfile(target) and resume:
				# Local file is present and we're resuming it
				syscall = 'wget --user='+myuser+' --password='+mypass+' --continue '+archiveurl+myuser+'/'+target
				print syscall
				os.system(syscall)
			elif os.path.isfile(target) and not resume:
				# Local file is present but we're not resuming
				print target,'already exists locally, skipping'
