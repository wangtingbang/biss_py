import re

def get_url_list():
	f = open( './html/af.html', 'r' )
	cont = f.read()
#	print cont

	patt_r = '<p class="title"(.*?)</p>' # rough re pattern
	patt_d = 'href="/protein/(.*?)">'  # detail re pattern
#	print patt_r
	prog_r = re.compile(patt_r)
#	print prog_r
	rough = prog_r.findall(cont) # rough keywords
	idx = 1 
	url_list = []
	for r in rough:
		print idx
#		print 'kw is: \t' + r
		prog_d = re.compile(patt_d)
		d_urls = prog_d.findall(r)
		for d in d_urls:
			print d
			kw = d.split('"')[0]
			print kw
			url_list.append(kw)
		idx = idx + 1
	return url_list

if __name__ == '__main__':
	urls = get_url_list()
	print '__main__:'
	for url in urls:
		print url
