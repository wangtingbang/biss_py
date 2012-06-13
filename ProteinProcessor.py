'''
Created on 2012-5-26

@author: sigh.differ
'''
import re
import os.path
import time
import mechanize
import urllib2
import sys
import MySQLdb
import MySqlConn
import ProteinVO

webroot = '.'
kw_file_pro = './keywords/pro_kw.txt'	# keyword list file of protein
ul_file_pro = './logs/pro_ul.txt'	# url list file of protein
ul_err_file_pro = './logs/pro_ul_error.txt'	# url error log file of protein
local_html_dir = './local_html/web/protein'
base_dir = webroot + '/html/protein/'
base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'

def read_kw(fdir):
	print 'Reading keywords from file, plase wait...'
	try:
		if not os.path.isfile( fdir ):
			print '\tFile read fail. can not read keyword from file...'
			return None
		f = open( fdir, 'r')
		print '\tKeyword file open, getting keywords and generating keyword list...'
		words = f.read().split('\n')
		print '\tKeyword list processed...'
		print '\tKeywords:'
		wds = []
		for k in words:
			if len(k) != 0:
				print '\t\t\t' + k
				wds.append(k)
		return wds
	except IOError:
		print '\tKeyword file ' + f_dir + 'read error'
		return None

def save_to_db(vo):
	'''
|item_id          | varchar(16)  | NO   | PRI |         |       |
| locus            | text         | YES  |     | NULL    |       |
| definition       | text         | YES  |     | NULL    |       |
| accession        | varchar(16)  | YES  |     | NULL    |       |
| keywords         | varchar(16)  | YES  |     | NULL    |       |
| version          | varchar(32)  | YES  |     | NULL    |       |
| dbsource         | varchar(32)  | YES  |     | NULL    |       |
| source           | varchar(256) | YES  |     | NULL    |       |
| organism         | text         | YES  |     | NULL    |       |
| comment          | text         | YES  |     | NULL    |       |
| features         | varchar(32)  | YES  |     | NULL    |       |
| features_source  | text         | YES  |     | NULL    |       |
| features_protein | text         | YES  |     | NULL    |       |
| features_cds     | text         | YES  |     | NULL    |       |
| origin      
	
	'''
	'''
	sql = 'insert into biss_protein values (' + vo.getId() + '\', \'' 
		+ vo.getLocus() + '\', \''
		+ vo.getDef() + '\', \'' 
		+ vo.getAcc() + '\', \'' 
		+ vo.getKw() + '\', \'' 
		+ vo.getVer() + '\', \'' 
		+ vo.getDbs() + '\', \'' 
		+ '' + '\', \'' 
		+ vo.getOrg() + '\', \'' 
		+ vo.getCmt() + '\', \'' 
		+ '' + '\', \'' 
		+ '' + '\', \'' 
		+ '' + '\', \'' 
		+ '' + '\', \''	
		+ vo.getOri() + '\');'
	'''
	sql = 'insert into biss_protein values (\'' + vo.getId() + '\', \'' + vo.getLocus() + '\', \'' + vo.getDef() + '\', \'' + vo.getAcc() + '\', \'' + vo.getKw() + '\', \'' + vo.getVer() + '\', \'' + vo.getDbs() + '\', \'' + '' + '\', \'' + vo.getOrg() + '\', \'' + vo.getCmt() + '\', \'' + '' + '\', \'' + '' + '\', \'' + '' + '\', \'' + '' + '\', \'' + vo.getOri() + '\');'
	f_open = open( 'f:/sql.sql', 'w')
	f_open.write(sql)
	print sql
	res = MySqlConn.insert_one_by_sql(sql)
	print 'result: '
	print res
	return

def query_from_db( pid):
	print 'query from database, item id: ' + pid
	sql = 'call query_protein_by_id_proc ( \'' + pid + '\');';
	proc_name = 'query_protein_by_id_proc'
	cds = MySqlConn.query_by_sql(sql)
	if len(cds) == 0:
		print '\tquery result is None'
#	print cds
	return	cds

def save_html_file( html, name ):
    f = file(base_dir + name, 'w')
    f.write(html)
    return

def get_html_data( url, vo ):
	print 'Getting html data from url: ' + url
#	patt_id = 'UniProtKB/Swiss-Prot:(.*?)</p>'	# item id
	patt_id = '<p class="itemid">(.*?)</p>'
	patt_locus = 'LOCUS(.*?)DEFINITION'		# locus
	patt_def = 'DEFINITION(.*?)ACCESSION'		# definition
	patt_acc = 'ACCESSION(.*?)VERSION'		# accession
	patt_kw = 'KEYWORDS(.*?)SOURCE'			# keywords
	patt_ver = 'VERSION(.*?)DBSOURCE'		# version
	patt_dbs = 'DBSOURCE(.*?)KEYWORDS'		# dbsource
	patt_org = 'ORGANISM(.*?)REFERENCE'		# organism
	patt_cmt = 'COMMENT(.*?)FEATURES'		# comment
	patt_ori = 'ORIGIN(.*?)//'			# origin
	'''
	patt_ftr	#features
	patt_ftrs	#feature_source
	patt_ftrp	#feature_protein
	patt_ftrc	#feature_cds
	'''
	'''
	f_name = './Q45071.2.htm'
	print 'open file ' + f_name + '....'
	f_html = open(f_name, 'r')
	f_data = f_html.read()
	f_html.close()
	'''
	try:
		br = mechanize.Browser()
		f_url = br.open(url)
		f_data = f_url.get_data()
		br.close()
	except urllib2.URLError, e:
		print '\tURL open error, url is: ' + url, e

	print '\tRagular expressions compiling...'
	prog_id = re.compile( patt_id, re.DOTALL )
	prog_locus = re.compile( patt_locus, re.DOTALL )
	prog_def = re.compile( patt_def, re.DOTALL )
	prog_acc = re.compile( patt_acc, re.DOTALL )
	prog_kw = re.compile( patt_kw, re.DOTALL )
	prog_ver = re.compile( patt_ver, re.DOTALL )
	prog_dbs = re.compile( patt_dbs, re.DOTALL )
	prog_org = re.compile( patt_org, re.DOTALL )
	prog_cmt = re.compile( patt_cmt, re.DOTALL )
	prog_ori = re.compile( patt_ori, re.DOTALL )
	
	print '\tFind all content by RE....'	
	con_id = prog_id.findall(f_data)

	if len(con_id) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	con_id = con_id[0].split(':')[1].lstrip()
	print '\tItem id: ' + con_id[0]
	con_locus = prog_locus.findall(f_data)
	con_def = prog_def.findall(f_data)
	con_acc = prog_acc.findall(f_data)
	con_kw = prog_kw.findall(f_data)
	con_ver = prog_ver.findall(f_data)
	con_dbs = prog_dbs.findall(f_data)
	con_org = prog_org.findall(f_data)
	con_cmt =prog_cmt.findall(f_data)
	con_ori = prog_ori.findall(f_data)
	'''
	print url
	print con_id
	print con_def
	print con_acc
	print con_kw
	print con_ver
	print con_dbs
	print con_org
	print con_cmt
	print con_ori
	'''
	# processe dbsource data item
	if len(con_dbs) == 0:
		dbs_txt = ''
	else:
		dbs_txt = con_dbs[0]
		patt_rpl = '<a(.*?)">'
		times_rpl = dbs_txt.count( '</a>' )
		dbs_txt = dbs_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		dbs_rpl = prog_rpl.findall(dbs_txt)
		for rpl in dbs_rpl:
			dbs_txt = dbs_txt.replace( '<a' + rpl + '">', '' )
	# dbsource data item process completed

	# process organism data item
	if len(con_org) == 0:
		org_txt = ''
	else:
		org_txt = con_org[0]
		times_rpl = org_txt.count( '</a>' )
		org_txt = org_txt.replace( '</a>', '', times_rpl)
		org_rpl = prog_rpl.findall( org_txt )
		for rpl in org_rpl:
			org_txt = org_txt.replace( '<a' + rpl + '">', '' )
	# organism data item process completed

	# process comments data item
	if len(con_cmt) == 0:
		cmt_txt = ''
	else:
		cmt_txt = con_cmt[0]
		times_rpl = cmt_txt.count( '</a>' )
		cmt_txt = cmt_txt.replace( '</a>', '', times_rpl)
		cmt_rpl = prog_rpl.findall( cmt_txt )
		for rpl in cmt_rpl:
			cmt_txt = cmt_txt.replace( '<a' + rpl + '">', '' )
	# comments data item process completed

	# process origin data item
	if len(con_ori) == 0:
		ori_txt = ''
	else:
		ori_txt = con_ori[0]
		patt_rpl = '<span(.*?)">'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ori_rpl = prog_rpl.findall(ori_txt)
		times = ori_txt.count('</span>')
		ori_txt = ori_txt.replace( '</span>', '', times)
		for rep in ori_rpl:
			rep_txt = '<span' + rep + '">'
			ori_txt = ori_txt.replace( rep_txt, '')
	
		patt_rpl = '<a(.*?)a>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ori_rpl = prog_rpl.findall(ori_txt)
		for rep in ori_rpl:
			rep_txt = '<a' + rep + 'a>'
			ori_txt = ori_txt.replace( rep_txt, '')
	# origin data item processe completed

	# save data to vo
	print '\tSaving data to vo...'
	vo.setId(con_id[0].lstrip())
	vo.setLocus(con_locus[0].lstrip())
	vo.setDef(con_def[0].lstrip())
	vo.setAcc(con_acc[0].lstrip())
	vo.setKw(con_kw[0].lstrip())
	vo.setDbs(dbs_txt)
	vo.setOrg(org_txt)
	vo.setCmt(cmt_txt)
	vo.setOri(ori_txt)
	print '\tvo size is: %d' % getsizeof(vo)
	print '\tSaving url to log file...'
	f_ul = open(ul_file_pro, 'a')	# append a url to url list log file
	f_ul.write( vo.getId() + ':' + url + '\n' )
	f_ul.close()
	print '\tHTML data gotten, url saved, next processing...'
	return vo

def get_data_from_local( f_path, vo ):
	print 'Getting html data from local html file: ' + f_path
#	patt_id = 'UniProtKB/Swiss-Prot:(.*?)</p>'	# item id
	patt_id = '<p class="itemid">(.*?)</p>'
	patt_locus = 'LOCUS(.*?)DEFINITION'		# locus
	patt_def = 'DEFINITION(.*?)ACCESSION'		# definition
	patt_acc = 'ACCESSION(.*?)VERSION'		# accession
	patt_kw = 'KEYWORDS(.*?)SOURCE'			# keywords
	patt_ver = 'VERSION(.*?)DBSOURCE'		# version
	patt_dbs = 'DBSOURCE(.*?)KEYWORDS'		# dbsource
	patt_org = 'ORGANISM(.*?)REFERENCE'		# organism
	patt_cmt = 'COMMENT(.*?)FEATURES'		# comment
	patt_ori = 'ORIGIN(.*?)//'			# origin
	'''
	patt_ftr	#features
	patt_ftrs	#feature_source
	patt_ftrp	#feature_protein
	patt_ftrc	#feature_cds
	'''
	print '\tOpen file ' + f_path + ' ...'
	f_html = open(f_name, 'r')
	f_data = f_html.read()
	f_html.close()
	'''
	br = mechanize.Browser()
	f_url = br.open(url)
	f_data = f_url.get_data()
	br.close()
	'''
	print '\tRagular expressions compiling...'
	prog_id = re.compile( patt_id, re.DOTALL )
	prog_locus = re.compile( patt_locus, re.DOTALL )
	prog_def = re.compile( patt_def, re.DOTALL )
	prog_acc = re.compile( patt_acc, re.DOTALL )
	prog_kw = re.compile( patt_kw, re.DOTALL )
	prog_ver = re.compile( patt_ver, re.DOTALL )
	prog_dbs = re.compile( patt_dbs, re.DOTALL )
	prog_org = re.compile( patt_org, re.DOTALL )
	prog_cmt = re.compile( patt_cmt, re.DOTALL )
	prog_ori = re.compile( patt_ori, re.DOTALL )
	
	print '\tFind all content by RE....'	
	con_id = prog_id.findall(f_data)
	con_id = con_id[0].split(':')[1].lstrip()
	if len(con_id) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	print '\tItem id: ' + con_id[0]
	con_locus = prog_locus.findall(f_data)
	con_def = prog_def.findall(f_data)
	con_acc = prog_acc.findall(f_data)
	con_kw = prog_kw.findall(f_data)
	con_ver = prog_ver.findall(f_data)
	con_dbs = prog_dbs.findall(f_data)
	con_org = prog_org.findall(f_data)
	con_cmt =prog_cmt.findall(f_data)
	con_ori = prog_ori.findall(f_data)
	print '\tAll data found....'
	print url
	print con_id
	print con_def
	print con_acc
	print con_kw
	print con_ver
	print con_dbs
	print con_org
	print con_cmt
	print con_ori

	# processe dbsource data item
	dbs_txt = con_dbs[0]
	patt_rpl = '<a(.*?)">'
	times_rpl = dbs_txt.count( '</a>' )
	dbs_txt = dbs_txt.replace( '</a>', '', times_rpl)
	#print times_rpl
	prog_rpl = re.compile(patt_rpl, re.DOTALL)
	dbs_rpl = prog_rpl.findall(dbs_txt)
	for rpl in dbs_rpl:
		dbs_txt = dbs_txt.replace( '<a' + rpl + '">', '' )
	# dbsource data item process completed

	# process organism data item
	org_txt = con_org[0]
	times_rpl = org_txt.count( '</a>' )
	org_txt = org_txt.replace( '</a>', '', times_rpl)
	org_rpl = prog_rpl.findall( org_txt )
	for rpl in org_rpl:
		org_txt = org_txt.replace( '<a' + rpl + '">', '' )
	# organism data item process completed

	# process comments data item
	cmt_txt = con_cmt[0]
	times_rpl = cmt_txt.count( '</a>' )
	cmt_txt = cmt_txt.replace( '</a>', '', times_rpl)
	cmt_rpl = prog_rpl.findall( cmt_txt )
	for rpl in cmt_rpl:
		cmt_txt = cmt_txt.replace( '<a' + rpl + '">', '' )
	# comments data item process completed

	# process origin data item
	ori_txt = con_ori[0]
	patt_rpl = '<span(.*?)">'
	prog_rpl = re.compile(patt_rpl, re.DOTALL)
	ori_rpl = prog_rpl.findall(ori_txt)
	times = ori_txt.count('</span>')
	ori_txt = ori_txt.replace( '</span>', '', times)
	for rep in ori_rpl:
		rep_txt = '<span' + rep + '">'
		ori_txt = ori_txt.replace( rep_txt, '')

	patt_rpl = '<a(.*?)a>'
	prog_rpl = re.compile(patt_rpl, re.DOTALL)
	ori_rpl = prog_rpl.findall(ori_txt)
	for rep in ori_rpl:
		rep_txt = '<a' + rep + 'a>'
		ori_txt = ori_txt.replace( rep_txt, '')
	# origin data item processe completed

	# save data to vo
	print 'saving data to vo...'
	vo.setId(con_id[0].lstrip())
	vo.setLocus(con_locus[0].lstrip())
	vo.setDef(con_def[0].lstrip())
	vo.setAcc(con_acc[0].lstrip())
	vo.setKw(con_kw[0].lstrip())
	vo.setDbs(dbs_txt)
	vo.setOrg(org_txt)
	vo.setCmt(cmt_txt)
	vo.setOri(ori_txt)

	print '\tHtml data gotten, next processing...'
	return vo

def get_url_list( kw ): # function same as url_list_init
	print 'Get url list by query keywords from NCBI website...'
	br = mechanize.Browser()
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
	br.close()
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
	return url_list

def protein_grab():
	'''
	# read keywords for quering from file
	kws = read_kw( kw_file_pro )
	if kws is None:
		print 'Keywords is None, plz check you keywords file:\n\t' + kw_file_pro
		print 'Programming will exit....'
		exit()

	#for kw in kws:
	#	print 'Keyword is: ' + kw
	
	# get url list
	#		input is keyword
	#		output: list of url
	#		process: open NBCI websitea, query keyword, get url list
	url_list = []
	for kw in kws:
		print '\nStarting get url list by keyword: ' + kw + ' ...'
		urls = get_url_list(kw)
		if urls is None:
			continue
		for url in urls:
			url_list.append(url)
	'''
	url_list = ['http://www.ncbi.nlm.nih.gov/protein/AAN15854.1', 'http://www.ncbi.nlm.nih.gov/protein/AAN15855.1']
	if len(url_list) == 0:
		print 'None of URL generated by keywords, cannot grab web from NCBI...'
		print 'Programming will exit....'
		exit()
	idx = 1
	for url in url_list:
		print '\tURL from url list:\t%d\t%s'%(idx, url)
		idx = idx + 1
	# get data from html doc
	#		input: url, vo( which type is ProteinVO )
	#		output: vo, which is data stored
	#		process: get data by ragular expression, save data item to protein vo
	vo = ProteinVO.ProteinVO()
	for url in url_list:
		get_html_data(url, vo)
#	print 'in main: vo: id: ' + vo.getId()
#	print query_from_db('234')
	'''
	'''
	vo = ProteinVO.ProteinVO()
	get_html_data('', '', vo)
	#save_to_db( vo )
	cds = query_from_db( vo.getId())
	if cds is None:
		save_to_db( vo )
		print 'none'

	else:
		print 'existed data...'
	
if __name__ == '__main__':
	protein_grab()
