'''
Created on 2012-5-26

@author: sigh.differ
'''
import re
import os.path
import mechanize
import MySQLdb
import MySqlConn
import ProteinVO

webroot = '.'
kw_file_pro = './pro_kw.txt'
base_dir = webroot + '/html/protein/'
base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'

def read_kw(fdir):
	if not os.path.isfile( fdir ):
		print 'file read fail. can not read keyword from file...'
		return None
	f = open( fdir, 'r')
	print 'keyword file open, getting keywords and generating keyword list...'
	words = f.read().split('\n')
	print 'keyword list processed...'
	return words

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
	sql = 'call query_protein_by_id_proc ( \'' + pid + '\');';
	proc_name = 'query_protein_by_id_proc'
	cds = MySqlConn.query_by_sql(sql)
	print cds
	return

def save_html_file( html, name ):
    f = file(base_dir + name, 'w')
    f.write(html)
    return

def get_html_data( br, url, vo ):
	patt_id = 'UniProtKB/Swiss-Prot:(.*?)</p>'	# item id
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
	f_name = './Q45071.2.htm'
	print 'open file ' + f_name + '....'
	f_html = open(f_name, 'r')
	f_data = f_html.read()
	print 'ragular expression compiling...'
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
	
	print 'find all content by RE....'	
	con_id = prog_id.findall(f_data)
	con_locus = prog_locus.findall(f_data)
	con_def = prog_def.findall(f_data)
	con_acc = prog_acc.findall(f_data)
	con_kw = prog_kw.findall(f_data)
	con_ver = prog_ver.findall(f_data)
	con_dbs = prog_dbs.findall(f_data)
	con_org = prog_org.findall(f_data)
	con_cmt =prog_cmt.findall(f_data)
	con_ori = prog_ori.findall(f_data)

# processe dbsource data item
	dbs_txt = con_dbs[0]
	patt_rpl = '<a(.*?)">'
	times_rpl = dbs_txt.count( '</a>' )
	dbs_txt = dbs_txt.replace( '</a>', '', times_rpl)
#	print times_rpl
	prog_rpl = re.compile(patt_rpl, re.DOTALL)
	dbs_rpl = prog_rpl.findall(dbs_txt)
	for rpl in dbs_rpl:
		dbs_txt = dbs_txt.replace( '<a' + rpl + '">', '' )
#	print 'dbsource:\n'
#	print dbs_txt
# dbsource data item process completed

# process organism data item
	org_txt = con_org[0]
	times_rpl = org_txt.count( '</a>' )
	org_txt = org_txt.replace( '</a>', '', times_rpl)
	org_rpl = prog_rpl.findall( org_txt )
	for rpl in org_rpl:
		org_txt = org_txt.replace( '<a' + rpl + '">', '' )
#	print 'organsim:\n' + org_txt
# organism data item process completed

# process comments data item
	cmt_txt = con_cmt[0]
	times_rpl = cmt_txt.count( '</a>' )
	cmt_txt = cmt_txt.replace( '</a>', '', times_rpl)
	cmt_rpl = prog_rpl.findall( cmt_txt )
	for rpl in cmt_rpl:
		cmt_txt = cmt_txt.replace( '<a' + rpl + '">', '' )
#	print 'commtens:\n' + cmt_txt

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
#	print 'origin:\n' + org_txt
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
	return vo

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

if __name__ == '__main__':
	kws = read_kw( kw_file_pro )
	for kw in kws:
		print kw
	br = mechanize.Browser()
	url_lst = get_url_list( br, 'afd')
	idx = 1
	for url in url_lst:
		print '%d: %s' %( idx, url)
		idx = idx + 1
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
	'''
