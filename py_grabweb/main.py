import mechanize
import os
import os.path
import re

base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'
kw_file_pro = './pro_kw.txt'


def main( kw ):
	# older
##	br = mechanize.Browser()
#	open_url = base_url
#	br.open(open_url)
#	br.select_form( name='EntrezForm')
#	br['search_term'] = kw
#	resp = br.submit()
#	print resp


	# 2012-Jun-7th
#	url = 'http://www.ncbi.nlm.nih.gov/protein/P45796.1'
#	main(kw)
	br = mechanize.Browser()
#	open_url(url, br)
	kw = read_kw(kw_file_pro)
	urls = get_url_list()
	for url_kw in urls:
		url = base_url + '?term=' + url_kw
		data = br.open(url).get_data()
		f = open( './html/' + url_kw + '.html', 'w' )
		f.write(data);
		print url
#	url_list_init(url, br)	

def read_kw(fdir):
	if not os.path.isfile( fdir ):
		print 'file read fail. can not read keyword from file...'
		return None
	f = open( fdir, 'r')
	print 'keyword file open, getting keywords and generating keyword list...'
	words = f.read().split('\n')
	print 'keyword list processed...'
	return words

	# url_list_init no use at present
'''
def url_list_init(url, br):
	data = br.open( url ).get_data()
	re_pattern = 'href="/protein/(.*?)">'
	prog = re.compile(re_pattern)
	print 'getting url list from keyword queried result...'
	nice = prog.match(data)
	print 'url list:'
	print nice
	print 'url: ' + url+ ' opened and data gotten'
	file_name = url.split( '=')[1] + '.html'
	f_base_dir = './html/'
	f_full_name = f_base_dir + file_name
	f = open( f_full_name, 'w')
	print 'saved html document: ' + f_full_name
	f.write(data)
'''
def get_url_list( br, kw ): # function same as url_list_init
#	f = open( './html/af.html', 'r' )
	kw_url = 'http://www.ncbi.nlm.nih.gov/protein?term=' + kw
	print 'open url: '+ kw_url + ' with browser tool, plz wait...'
	web_cont = br.open(kw_url).get_data()
#	cont = f.read()
	cont = web_cont
	print 'web contents gotten, url: ' + kw_url
#	print cont

	patt_r = '<p class="title"(.*?)</p>'	# rough re pattern
	patt_d = 'href="/protein/(.*?)">'		# detail re pattern
#	print patt_r
	print 'starting get data from web content...'
	print 'compiling ragular expression....'
	prog_r = re.compile(patt_r)
#	print prog_r
	rough = prog_r.findall(cont)			# rough keywords
	idx = 1 
	url_list = []
	for r in rough:
		print idx
#		print 'kw is: \t' + r
		prog_d = re.compile(patt_d)
		d_url_kws = prog_d.findall(r)
		for d_kws in d_url_kws:
			print d_kws
			kw = d_kws.split('"')[0]
			print kw
			nice_url = base_url_pro + '/' + kw
			url_list.append(nice_url)
			print 'nice url: ' + nice_url
		idx = idx + 1
	return url_list

def get_html_data(br, url):
	print 'in get_html_data, now open given url, ' + url + ', with browser tool...'
	web_cont = br.open(url).get_data()
	print 'web content gotten...'
	f = open( 'f:/af.html', 'w' )
	f.write(web_cont)

def process_html_data_to_db( br, url ):
	patt_r = '<pre class="genbank">(.*?)/pre>'
	patt_locus = 'LOCU(.*)DEFINITION'
	f_name = './html/Q45071.2.htm'
	print 'open file ' + f_name + '....'
	f_html = open(f_name)
	f_data = f_html.read()
#	print f_data
	print 'ragular expression ' + patt_r + ' compiling...'
	prog_r = re.compile( patt_r )
	prog_locus = re.compile( patt_locus )
	print 'find all content by RE....'
	cont = prog_r.findall(f_data)
	con_locus = prog_locus.findall(f_data)
	print 'result:'
	print cont
	print 'locus:'
	print con_locus


if __name__ == '__main__':
#	main()
#	kws = read_kw(kw_file_pro)
#	print 'init browser...'
#	br = mechanize.Browser()
#	print 'browser ok, now starting get url list....'
#	url_list = get_url_list(br, 'af')
#	url_list = ['http://www.ncbi.nlm.nih.gov/protein/P45796.1']
#	url_list = ['http://www.ncbi.nlm.nih.gov/protein/Q45071.2/b_files/contentLoader.js']
#	for url in url_list:
#		get_html_data( br, url )
#	print url_list
	process_html_data_to_db('', '')
