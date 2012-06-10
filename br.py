import mechanize
import time

br = mechanize.Browser()
url = 'http://www.ncbi.nlm.nih.gov/protein/P45796.1'

def open_url(url):
	resp = mechanize.urlopen(url)
	req = mechanize.Request(url)
	print resp.read()
	print '**********************************'
#	print req

# no use
def get_web_by_mch(url):
	print 'open url....'
	web = br.open(url)
	print 'sleep for 5.5....'
	time.sleep(5.5)
	print 'getting web data...'
	data = web.get_data()
	f_name = 'f:/r.html'
	f = open(f_name, 'w')
	print 'write data to: ' + f_name
	f.write(data)
	f.close()
	print 'finished...'

def get_web_url2(url):


if __name__ == '__main__':
#	open_url(url)
	get_web(url)
