import re
from mechanize import Browser

webroot = '.'
kw_file_pro = './keywords/pro_kw.txt'	# keyword list file of protein
ul_file_pro = './logs/pro_ul.txt'	# url list file of protein
ul_err_file_pro = './logs/pro_ul_error.txt'	# url error log file of protein
local_html_dir = './local_html/web/protein'
base_dir = webroot + '/html/protein/'
base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'

def get_url_list( kw ): # function same as url_list_init
	print 'Get url list by query keywords from NCBI website...'
	br = Browser()
#	f = open( './html/af.html', 'r' )
	kw_url = 'http://www.ncbi.nlm.nih.gov/protein?term=' + kw
	print '\tOpenning url: '+ kw_url + ' with browser tool, plz wait...'
	web = None
	try:
		web = br.open(kw_url)
	except urllib2.URLError, e:
		print '\tURL open error, ', e
	except urllib2.HTTPError, e:
		print '\tHTTP error, ', e

	if not web:
		print '\tCannot open url: ' + kw_url
		return
	web_cont = web.get_data()
#	cont = f.read()
	cont = web_cont
	print '\tWeb contents gotten, url: ' + kw_url
#	print cont

	patt_r = '<p class="title"(.*?)</p>'	# rough re pattern
	patt_d = 'href="/protein/(.*?)">'		# detail re pattern
#	print patt_r
	print '\tStarting get url list from web content...'
	print '\tCompiling ragular expression....'
	prog_r = re.compile(patt_r)
	rough = prog_r.findall(cont)			# rough keywords
	if len(rough) == 0:
		print rough
		print '\tNone of result by keyword:' + kw
		return None
	idx = 1 
	url_list = []
	for r in rough:
#		print 'kw is: \t' + r
		prog_d = re.compile(patt_d)
		d_url_kws = prog_d.findall(r)
		for d_kws in d_url_kws:
			kw = d_kws.split('"')[0]
			nice_url = base_url_pro + '/' + kw
			url_list.append(nice_url)
			print '\t%d\tnice url: %s' % ( idx, nice_url )
		idx = idx + 1
#	patt_np = '<input class="num" type="text"(.*?)">'
	patt_np = 'Next &gt;</a>'
	prog_np = re.compile(patt_np, re.DOTALL)
	np = prog_np.findall(web_cont)
	if np is not None:
		print '\tNexp page...'
		print np

	br.close()
	return url_list

if __name__ == '__main__':
	get_url_list('af')
