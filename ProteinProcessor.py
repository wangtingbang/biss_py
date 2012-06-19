'''
Created on 2012-5-26

@author: sigh.differ
'''
import re
import os
import os.path
import time
import mechanize
import urllib2
import sys
import MySQLdb
import MySqlConn
import ProteinVO
import ProteinRefVO

webroot = '.'
kw_file_pro = './keywords/pro_kw.txt'	# keyword list file of protein
ul_file_pro = './logs/pro_ul.txt'	# url list file of protein
ul_err_file_pro = './logs/pro_ul_error.txt'	# url error log file of protein
lh_err_file_pro = './logs/pro_lh_error.txt' # local html file error log file of protein
local_html_dir = './local_html/web/protein'
base_dir = webroot + '/html/protein/'
#base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'
base_url_pro = 'http://localhost/biss/protein'

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
	sql = 'insert into biss_protein values (\'' + vo.getId() + '\', \'' + vo.getLocus() + '\', \'' + vo.getDef() + '\', \'' + vo.getAcc() + '\', \'' + vo.getKw() + '\', \'' + vo.getVer() + '\', \'' + vo.getDbs() + '\', \'' + '' + '\', \'' + vo.getOrg() + '\', \'' + vo.getCmt() + '\', \'' + vo.getFtr() + '\', \'' + vo.getFtrs() + '\', \'' + vo.getFtrp() + '\', \'' + vo.getFtrc() + '\', \'' + vo.getOri() + '\');'
	f_open = open( './logs/protein_sql.sql', 'a')
	f_open.write(sql)
	print 'Now inserting data into database...'
	res = MySqlConn.insert_one_by_sql(sql)
	print '\tData inserted into database...'
	return

def query_from_db( pid):
	print 'Query from database, item id: ' + pid
	sql = '\tCall query_protein_by_id_proc ( \'' + pid + '\');';
	proc_name = 'query_protein_by_id_proc'
	cds = MySqlConn.query_by_sql(sql)
	if len(cds) == 0:
		print '\tQuery result is None'
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
	patt_ftr = ''
	patt_ftrs = '<span id="feature_(.*?)_source(.*?)</span>'	#feature_source
	patt_ftrp = '<span id="feature_(.*?)_Protein_(.*?)</span>'	#feature_protein
	patt_ftrc = 'CDS</a>(.*?)</span>'	#feature_cds
	'''
	f_name = './Q45071.2.htm'
	print 'open file ' + f_name + '....'
	f_html = open(f_name, 'r')
	f_data = f_html.read()
	f_html.close()
	'''
	f_data = None
	try:
		br = mechanize.Browser()
		f_url = br.open(url)
		f_data = f_url.get_data()
		br.close()
	except urllib2.URLError, e:
		print '\tURL open error, url is: ' + url, e
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return

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
	prog_ftrs = re.compile( patt_ftrs, re.DOTALL )
	prog_ftrp = re.compile( patt_ftrp, re.DOTALL )
	prog_ftrc = re.compile( patt_ftrc, re.DOTALL )
	
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
	id_txt = con_id[0].split(':')[1].lstrip()
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

	# processe locus data item
	if len(con_locus) == 0:
		lcs_txt = ''
	else:
		lcs_txt = con_locus[0].lstrip()
		lcs_txt.replace( '\n', '\t')
	# locus data item process completed

	# process definition data item
	if len(con_def) == 0:
		def_txt = ''
	else:
		def_txt = con_def[0].lstrip()
		def_txt.replace( '\n', '\t')
	# definition data item process completed

	# process accession data item
	if len(con_acc) == 0:
		acc_txt = ''
	else:
		acc_txt = con_acc[0].lstrip()
		acc_txt.replace( '\n', '\t')
	# accession data item process completed

	# process keyword data item
	if len(con_kw) == 0:
		kw_txt = ''
	else:
		kw_txt = con_kw[0].lstrip()
		kw_txt.replace( '\n', '\t')
	# keyword data item process completed

	# process version data item
	if len(con_ver) == 0:
		ver_txt = ''
	else:
		ver_txt = con_ver[0].lstrip()
		ver_txt.replace( '\n', '\t')
	# version data item process completed

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
		dbs_txt.replace( '\n', '\t')
		for rpl in dbs_rpl:
			dbs_txt = dbs_txt.replace( '<a' + rpl + '">', '' )
	# dbsource data item process completed

	# process organism data item
	if len(con_org) == 0:
		org_txt = ''
	else:
		org_txt = con_org[0]
		times_rpl = org_txt.count( '</a>' )
		patt_rpl = '<a(.*?)">'
		org_txt = org_txt.replace( '</a>', '', times_rpl)
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		org_rpl = prog_rpl.findall( org_txt )
		org_txt.replace( '\n', '\t')
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
		cmt_txt.replace( '\n', '\t')
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
		ori_txt.replace( '\n', '\t')
		for rep in ori_rpl:
			rep_txt = '<a' + rep + 'a>'
			ori_txt = ori_txt.replace( rep_txt, '')
	# origin data item processe completed

	ftr_txt = 'Location/Qualifiers'

	# process feature source data item
	con_ftrs = prog_ftrs.findall(f_data)
	if len(con_ftrs) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	else:
		ftrs_txt = con_ftrs[0][1]
		times_rpl = ftrs_txt.count( '</a>' )
		ftrs_txt = ftrs_txt.replace( '</a>', '', times_rpl)
		patt_rpl = '<script(.*?)/script>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrs_rpl = prog_rpl.findall(ftrs_txt)
		for rpl in ftrs_rpl:
			ftrs_txt = ftrs_txt.replace( '<script' + rpl + '/script>', '' )
			ftrs_txt = ftrs_txt.replace('                     ', ' ')
			ftrs_txt = ftrs_txt.replace('\n', ' ')
		patt_rpl = '<a(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrs_rpl = prog_rpl.findall(ftrs_txt)
		for rpl in ftrs_rpl:
			ftrs_txt = ftrs_txt.replace( '<a' + rpl + '>', '' )
		ftrs_txt = ftrs_txt.split('>')[1]
	# feature source data item process completed

	# process feature protein data item
	prog_ftrp = re.compile( patt_ftrp, re.DOTALL )
	con_ftrp = prog_ftrp.findall(f_data)
	if len(con_ftrp) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	else:
		ftrp_txt = con_ftrp[0][1]
		times_rpl = ftrp_txt.count( '</a>' )
		ftrp_txt = ftrp_txt.replace( '</a>', '', times_rpl)
		patt_rpl = '<script(.*?)/script>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrp_rpl = prog_rpl.findall(ftrp_txt)
		idx = 1
		for rpl in ftrp_rpl:
			ftrp_txt = ftrp_txt.replace( '<script' + rpl + '/script>', '' )
			ftrp_txt = ftrp_txt.replace('                     ', ' ')
			ftrp_txt = ftrp_txt.replace('"\n', ' ')
			idx = idx +1
		patt_rpl = '<a(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrs_rpl = prog_rpl.findall(ftrp_txt)
		for rpl in ftrs_rpl:
			ftrp_txt = ftrp_txt.replace( '<a' + rpl + '>', '' )
		ftrp_txt = ftrp_txt.split('>')[1].lstrip()
	# feature protein data item process completed

	# process feature CDS data item
	prog_ftrc = re.compile( patt_ftrc, re.DOTALL )
	con_ftrc = prog_ftrc.findall(f_data)
#	print '\n@@\n', con_ftrc, '\n@@\n'
	if len(con_ftrc) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	else:
		ftrc_txt = con_ftrc[0]
#		print 'ftrc_txt = con_ftrc[0][1]\n\t', ftrc_txt
		times_rpl = ftrc_txt.count( '</a>' )
		ftrc_txt = ftrc_txt.replace( '</a>', '', times_rpl)
		times_rpl = ftrc_txt.count( '                     ' )
		ftrc_txt = ftrc_txt.replace('                     ', ' ', times_rpl)
		times_rpl = ftrc_txt.count( '\n' )
		ftrc_txt = ftrc_txt.replace('\n', ' ', times_rpl)
		patt_rpl = '<a href(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrc_rpl = prog_rpl.findall(ftrc_txt)
#		print 'After place:\t@@@@@@@@@@@@@@@\n', ftrc_txt
		idx = 1
		for rpl in ftrc_rpl:
			ftrc_txt = ftrc_txt.replace( '<a href' + rpl + '>', '' )
			idx = idx +1
#			print '\n\nIn placing\t%%%%%%%%%%%%%%%%%%%%\nRPL:',rpl, '\nREED\n', ftrc_txt
		patt_rpl = '<a(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrc_rpl = prog_rpl.findall(ftrp_txt)
#		ftrc_txt = ftrc_txt.split('>')[1].lstrip()
	# CDS protein data item process completed

	# save data to vo
	print '\tSaving data to vo...'
	vo.setId(id_txt)
	vo.setLocus(lcs_txt)
	vo.setDef(def_txt)
	vo.setAcc(acc_txt)
	vo.setKw(kw_txt)
	vo.setVer(ver_txt)
	vo.setDbs(dbs_txt)
	vo.setOrg(org_txt)
	vo.setCmt(cmt_txt)
	vo.setOri(ori_txt)
	vo.setFtr(ftr_txt)
	vo.setFtrs(ftrs_txt)
	vo.setFtrp(ftrp_txt)
	vo.setFtrc(ftrc_txt)
#	print '\tvo size is: ', sys.getsizeof(vo)
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
	patt_ftr = ''
	patt_ftrs = '<span id="feature_(.*?)_source(.*?)</span>'	#feature_source
	patt_ftrp = '<span id="feature_(.*?)_Protein_(.*?)</span>'	#feature_protein
	patt_ftrc = 'CDS</a>(.*?)</span>'	#feature_cds

	print '\tOpen file ' + f_path + ' ...'
	f_html = None
	try:
		f_html = open(f_path, 'r')
	except IOError, e:
		print '\tLocal html file open error, ', e
		return

	f_data = f_html.read()
	f_html.close()

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
	prog_ftrs = re.compile( patt_ftrs, re.DOTALL )
	prog_ftrp = re.compile( patt_ftrp, re.DOTALL )
	prog_ftrc = re.compile( patt_ftrc, re.DOTALL )
	
	print '\tFind all content by RE....'	
	con_id = prog_id.findall(f_data)

	if len(con_id) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error html file path to log file: ' + lh_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + f_path + '\n')
		f_err.close()
		return None
	id_txt = con_id[0].split(':')[1].lstrip()
	con_locus = prog_locus.findall(f_data)
	con_def = prog_def.findall(f_data)
	con_acc = prog_acc.findall(f_data)
	con_kw = prog_kw.findall(f_data)
	con_ver = prog_ver.findall(f_data)
	con_dbs = prog_dbs.findall(f_data)
	con_org = prog_org.findall(f_data)
	con_cmt =prog_cmt.findall(f_data)
	con_ori = prog_ori.findall(f_data)

	# processe locus data item
	if len(con_locus) == 0:
		lcs_txt = ''
	else:
		lcs_txt = con_locus[0].lstrip()
		lcs_txt.replace( '\n', '\t')
	# locus data item process completed

	# process definition data item
	if len(con_def) == 0:
		def_txt = ''
	else:
		def_txt = con_def[0].lstrip()
		def_txt.replace( '\n', '\t')
	# definition data item process completed

	# process accession data item
	if len(con_acc) == 0:
		acc_txt = ''
	else:
		acc_txt = con_acc[0].lstrip()
		acc_txt.replace( '\n', '\t')
	# accession data item process completed

	# process keyword data item
	if len(con_kw) == 0:
		kw_txt = ''
	else:
		kw_txt = con_kw[0].lstrip()
		kw_txt.replace( '\n', '\t')
	# keyword data item process completed

	# process version data item
	if len(con_ver) == 0:
		ver_txt = ''
	else:
		ver_txt = con_ver[0].lstrip()
		ver_txt.replace( '\n', '\t')
	# version data item process completed

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
		dbs_txt.replace( '\n', '\t')
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
		org_txt.replace( '\n', '\t')
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
		cmt_txt.replace( '\n', '\t')
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
		ori_txt.replace( '\n', '\t')
		for rep in ori_rpl:
			rep_txt = '<a' + rep + 'a>'
			ori_txt = ori_txt.replace( rep_txt, '')
	# origin data item processe completed

	ftr_txt = 'Location/Qualifiers'

	# process feature source data item
	con_ftrs = prog_ftrs.findall(f_data)
	if len(con_ftrs) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + f_path + '\n')
		f_err.close()
		ftrs_txt = ''
#		return None
	else:
		ftrs_txt = con_ftrs[0][1]
		times_rpl = ftrs_txt.count( '</a>' )
		ftrs_txt = ftrs_txt.replace( '</a>', '', times_rpl)
		patt_rpl = '<script(.*?)/script>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrs_rpl = prog_rpl.findall(ftrs_txt)
		for rpl in ftrs_rpl:
			ftrs_txt = ftrs_txt.replace( '<script' + rpl + '/script>', '' )
			ftrs_txt = ftrs_txt.replace('                     ', ' ')
			ftrs_txt = ftrs_txt.replace('\n', ' ')
		patt_rpl = '<a(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrs_rpl = prog_rpl.findall(ftrs_txt)
		for rpl in ftrs_rpl:
			ftrs_txt = ftrs_txt.replace( '<a' + rpl + '>', '' )
		ftrs_txt = ftrs_txt.split('>')[1]
	# feature source data item process completed

	# process feature protein data item
	prog_ftrp = re.compile( patt_ftrp, re.DOTALL )
	con_ftrp = prog_ftrp.findall(f_data)
	if len(con_ftrp) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + f_path + '\n')
		f_err.close()
		ftrp_txt = ''
#		return None
	else:
		ftrp_txt = con_ftrp[0][1]
		times_rpl = ftrp_txt.count( '</a>' )
		ftrp_txt = ftrp_txt.replace( '</a>', '', times_rpl)
		patt_rpl = '<script(.*?)/script>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrp_rpl = prog_rpl.findall(ftrp_txt)
		idx = 1
		for rpl in ftrp_rpl:
			ftrp_txt = ftrp_txt.replace( '<script' + rpl + '/script>', '' )
			ftrp_txt = ftrp_txt.replace('                     ', ' ')
			ftrp_txt = ftrp_txt.replace('"\n', ' ')
			idx = idx +1
		patt_rpl = '<a(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrs_rpl = prog_rpl.findall(ftrp_txt)
		for rpl in ftrs_rpl:
			ftrp_txt = ftrp_txt.replace( '<a' + rpl + '>', '' )
		ftrp_txt = ftrp_txt.split('>')[1].lstrip()
	# feature protein data item process completed

	# process feature CDS data item
	prog_ftrc = re.compile( patt_ftrc, re.DOTALL )
	con_ftrc = prog_ftrc.findall(f_data)

#	print '\n@@\n', con_ftrc, '\n@@\n'
	if len(con_ftrc) == 0:
		print '\tCannot get feature cds from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + f_path + '\n')
		f_err.close()
		ftrc_txt = ''
#		return None
	else:
		ftrc_txt = con_ftrc[0]
		times_rpl = ftrc_txt.count( '</a>' )
		ftrc_txt = ftrc_txt.replace( '</a>', '', times_rpl)
		times_rpl = ftrc_txt.count( '                     ' )
		ftrc_txt = ftrc_txt.replace('                     ', ' ', times_rpl)
		times_rpl = ftrc_txt.count( '\n' )
		ftrc_txt = ftrc_txt.replace('\n', ' ', times_rpl)
		patt_rpl = '<a href(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrc_rpl = prog_rpl.findall(ftrc_txt)
#		print 'After place:\t@@@@@@@@@@@@@@@\n', ftrc_txt
		idx = 1
		for rpl in ftrc_rpl:
			ftrc_txt = ftrc_txt.replace( '<a href' + rpl + '>', '' )
			idx = idx +1
#			print '\n\nIn placing\t%%%%%%%%%%%%%%%%%%%%\nRPL:',rpl, '\nREED\n', ftrc_txt
		patt_rpl = '<a(.*?)>'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ftrc_rpl = prog_rpl.findall(ftrp_txt)
#		ftrc_txt = ftrc_txt.split('>')[1].lstrip()
#		print '\n\nPlaced:\t$$$$$$$$$$$$$$$$\n',ftrc_txt, '\n****************'
	# CDS protein data item process completed

	# save data to vo
	print '\tSaving data to vo...'
	vo.setId(id_txt)
	vo.setLocus(lcs_txt)
	vo.setDef(def_txt)
	vo.setAcc(acc_txt)
	vo.setKw(kw_txt)
	vo.setVer(ver_txt)
	vo.setDbs(dbs_txt)
	vo.setOrg(org_txt)
	vo.setCmt(cmt_txt)
	vo.setOri(ori_txt)
	vo.setFtr(ftr_txt)
	vo.setFtrs(ftrs_txt)
	vo.setFtrp(ftrp_txt)
	vo.setFtrc(ftrc_txt)

#	print '\tvo size is: ', sys.getsizeof(vo)

	print '\tHtml data gotten, next processing...'
	return vo

def get_html_ref_data( pid, url, vo ):
	patt_rno = 'REFERENCE(.*?)[A-Z][A-Z][A-Z][A-Z]'	# residues no
	patt_ath = 'AUTHORS(.*?)[A-Z][A-Z][A-Z]'	#authors
	patt_ttl = 'TITLE(.*?)[A-Z][A-Z][A-Z][A-Z]'	#title
	patt_jur = 'JOURNAL(.*?)[A-Z][A-Z][A-Z][A-Z]'		# journal

	f_data = None
	try:
		br = mechanize.Browser()
		f_url = br.open(url)
		f_data = f_url.get_data()
		br.close()
	except urllib2.URLError, e:
		print '\tURL open error, url is: ' + url, e
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return

	print '\tRagular expressions compiling...'

	prog_rno = re.compile( patt_rno, re.DOTALL )
	prog_ath = re.compile( patt_ath, re.DOTALL )
	prog_ttl = re.compile( patt_ttl, re.DOTALL )
	prog_jur = re.compile( patt_jur, re.DOTALL )
	print '\tFind all content by RE....\n'

	# process feature source data item
	con_rno = prog_rno.findall(f_data)
	con_ath = prog_ath.findall(f_data)
	con_ttl = prog_ttl.findall(f_data)
	con_jur = prog_jur.findall(f_data)
#	print 'A:\n', con_ath, '\n\n', patt_ath
	ref_num = len(con_rno)
	valid = True
	if ref_num == 0:
		print '\tNo reference found in this web page, now will quit getting reference...'
		valid = False
		return None
	err_txt = ''
	if len(con_ath) != ref_num:
		err_txt = '\t\tAuthors data item error...'
		valid = False
	if len(con_ttl) != ref_num:
		err_txt = '\t\tTitle data item error...'
		valid = False
	if len(con_jur) != ref_num:
		err_txt = '\t\tJournal data item error...'
		valid = False

	if valid == False:
		print '\tReference cannot get correctly, now will quit getting reference...'
		print err_txt
		t = '\tReference cannot get correctly, now will quit getting reference...\n' + err_txt
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	idx = 0
	while idx < ref_num:
		rno_txt = con_rno[idx].split('(')[0]
		rno_txt = rno_txt.lstrip()
		rno_txt = rno_txt.rstrip()

		ath_txt = con_ath[idx]
		ath_txt = ath_txt.lstrip()
		ath_txt = ath_txt.replace('            ', ' ')
		ath_txt = ath_txt.replace('"\n', ' ')

		ttl_txt = con_ttl[idx]
		ttl_txt = ttl_txt.lstrip()
		ttl_txt = ttl_txt.replace('            ', ' ')
		ttl_txt = ttl_txt.replace('"\n', ' ')

		jur_txt = con_jur[idx]
		jur_txt = jur_txt.lstrip()
		jur_txt = jur_txt.replace('            ', ' ')
		jur_txt = jur_txt.replace('"\n', ' ')
		jur_txt = jur_txt.replace( '</a>', '', jur_txt.count('</a>'))
		patt_jur_a = '<a(.*?)>'
		prog_jur_a = re.compile(patt_jur_a, re.DOTALL)
		jur_rpl = prog_jur_a.findall(jur_txt)
		for rpl in jur_rpl:
			jur_txt = jur_txt.replace( '<a'+rpl+'>', '')
#		print jur_rpl

#		print idx + 1
#		print '\tRe#:\t\n##', rno_txt, '##'
#		print 'Authors:\t\n',  ath_txt
#		print '\tTitle:\t\n',  ttl_txt
#		print '\tJournal:\t\n', jur_txt 
#		print jur_rpl

		vo.setPid(pid)
		vo.setRno(rno_txt)
		vo.setAth(ath_txt)
		vo.setTtl(ttl_txt)
		vo.setJur(jur_txt)
		save_ref_to_db(vo)
		idx = idx + 1

def get_local_ref_data( pid, f_name, vo ):
	patt_rno = 'REFERENCE(.*?)[A-Z][A-Z][A-Z][A-Z]'	# residues no
	patt_ath = 'AUTHORS(.*?)[A-Z][A-Z][A-Z]'	#authors
	patt_ttl = 'TITLE(.*?)[A-Z][A-Z][A-Z][A-Z]'	#title
	patt_jur = 'JOURNAL(.*?)[A-Z][A-Z][A-Z][A-Z]'		# journal

	f_data = None
	try:
		f = open(f_name)
		f_data = f.read()
		f.close()
	except urllib2.URLError, e:
		print '\tFile open error, file name is: ' + f_name, e
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + f_name + '\n')
		f_err.close()
		return

	print '\tRagular expressions compiling...'

	prog_rno = re.compile( patt_rno, re.DOTALL )
	prog_ath = re.compile( patt_ath, re.DOTALL )
	prog_ttl = re.compile( patt_ttl, re.DOTALL )
	prog_jur = re.compile( patt_jur, re.DOTALL )
	print '\tFind all content by RE....\n'

	# process feature source data item
	con_rno = prog_rno.findall(f_data)
	con_ath = prog_ath.findall(f_data)
	con_ttl = prog_ttl.findall(f_data)
	con_jur = prog_jur.findall(f_data)
#	print 'A:\n', con_ath, '\n\n', patt_ath
	ref_num = len(con_rno)
	valid = True
	if ref_num == 0:
		print '\tNo reference found in this web page, now will quit getting reference...'
		valid = False
		return None
	err_txt = ''
	if len(con_ath) != ref_num:
		err_txt = '\t\tAuthors data item error...'
		valid = False
	if len(con_ttl) != ref_num:
		err_txt = '\t\tTitle data item error...'
		valid = False
	if len(con_jur) != ref_num:
		err_txt = '\t\tJournal data item error...'
		valid = False

	if valid == False:
		print '\tReference cannot get correctly, now will quit getting reference...'
		print err_txt
		t = '\tReference cannot get correctly, now will quit getting reference...\n' + err_txt
		print '\tSaving error url to log file: ' + ul_err_file_pro
		f_err = open(ul_err_file_pro, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None
	idx = 0
	while idx < ref_num:
		rno_txt = con_rno[idx].split('(')[0]
		rno_txt = rno_txt.lstrip()
		rno_txt = rno_txt.rstrip()

		ath_txt = con_ath[idx]
		ath_txt = ath_txt.lstrip()
		ath_txt = ath_txt.replace('            ', ' ')
		ath_txt = ath_txt.replace('\n', ' ')

		ttl_txt = con_ttl[idx]
		ttl_txt = ttl_txt.lstrip()
		ttl_txt = ttl_txt.replace('            ', ' ')
		ttl_txt = ttl_txt.replace('\n', ' ')

		jur_txt = con_jur[idx]
		jur_txt = jur_txt.lstrip()
		jur_txt = jur_txt.replace('            ', ' ')
		jur_txt = jur_txt.replace('\n', ' ')
		jur_txt = jur_txt.replace( '</a>', '', jur_txt.count('</a>'))
		patt_jur_a = '<a(.*?)>'
		prog_jur_a = re.compile(patt_jur_a, re.DOTALL)
		jur_rpl = prog_jur_a.findall(jur_txt)
		for rpl in jur_rpl:
			jur_txt = jur_txt.replace( '<a'+rpl+'>', '')
#		print jur_rpl

#		print idx + 1
#		print '\tRe#:\t\n##', rno_txt, '##'
#		print 'Authors:\t\n',  ath_txt
#		print '\tTitle:\t\n',  ttl_txt
#		print '\tJournal:\t\n', jur_txt 
#		print jur_rpl

		vo.setPid(pid)
		vo.setRno(rno_txt)
		vo.setAth(ath_txt)
		vo.setTtl(ttl_txt)
		vo.setJur(jur_txt)
		save_ref_to_db(vo)
		idx = idx + 1

def save_ref_to_db(vo):
	'''
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| protein_id  | varchar(16)  | YES  |     | NULL    |       |
| residues_no | int(11)      | YES  |     | NULL    |       |
| authors     | varchar(128) | YES  |     | NULL    |       |
| title       | varchar(256) | YES  |     | NULL    |       |
| journal     | varchar(256) | YES  |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+
	'''
	sql = 'insert into biss_protein_reference values (\'' + vo.getPid() + '\', \'' + vo.getRno() + '\', \'' + vo.getAth() + '\', \'' + vo.getTtl() + '\', \'' + vo.getJur() + '\');'
	f_open = open( './logs/protein_sql.sql', 'a')
	f_open.write(sql)
	print 'Now inserting data into database...\n\t\SQL:\n', sql
	res = MySqlConn.insert_one_by_sql(sql)
	print '\tData inserted into database...'
	return


def get_url_list( kw ): # function same as url_list_init
	print 'Get url list by query keywords( ' + kw + ' )from NCBI website...'
	br = mechanize.Browser()
	idx_pg = 1
#	kw_url = 'http://localhost/biss/protein_af_' + idx + '.htm'
#	f = open( './html/af.html', 'r' )
#	kw_url = 'http://www.ncbi.nlm.nih.gov/protein?term=' + kw
	web = None
	f = None
	is_np = True
	url_list = []
	while is_np == True:
		kw_url = 'http://localhost/biss/protein_af_' + str(idx_pg) + '.htm'
		print '\tOpenning url: '+ kw_url + ' with browser tool, plz wait...'
		try:
			web = br.open(kw_url)
		#	f = open(kw_url, 'r')
		#	web = f.get_data()
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
		patt_d = '/protein/(.*?)">'		# detail re pattern
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
		for r in rough:
	#		print 'kw is: \t' + r
			prog_d = re.compile(patt_d)
			d_url_kws = prog_d.findall(r)
			for d_kws in d_url_kws:
	#			kw = d_kws.split('"')[0]
	#			nice_url = base_url_pro + '/' + kw
				nice_url = base_url_pro + '/' + d_kws.split('"')[0] + '.htm'
				url_list.append(nice_url)
				print '\t%d\tnice url: %s' % ( idx, nice_url )
			idx = idx + 1
		
		patt_np = 'Next &gt;</a>'
		prog_np = re.compile(patt_np, re.DOTALL)
		np = prog_np.findall(web_cont)
		if len(np) != 0:
			print '\tNexp page...\t',np
			is_np = True
			np = None
			web = None
			web_cont = None
			idx_pg = idx_pg + 1
			'''
		    br.select_form(name="login")  # Find the login form
		    br[np] = idx_pg     # Set the form values
		    resp = br.submit()            # Submit the form

		    # Automatic redirect sometimes fails, follow manually when needed
		    if 'Redirecting' in br.title():
				resp = br.follow_link(text_regex='click here')

		    # Loop through the searches, keeping fixed query parameters
		    for actor in in VARIABLE_QUERY:
				# I like to watch what's happening in the console
		        print >> sys.stderr, '***', actor
				# Lets do the actual query now
		        br.open(kw_url)
		        # The query actually gives us links to the content pages we like,
		        # but there are some other links on the page that we ignore
		        nice_links = [l for l in br.links()
                        if 'good_path' in l.url
                        and 'credential' in l.url]
				if not nice_links:        # Maybe the relevant results are empty
		            break
		        for link in nice_links:
					try:
						response = br.follow_link(link)
		                # More console reporting on title of followed link page
		                print >> sys.stderr, br.title()
		                # Increment output filenames, open and write the file
				        result_no += 1
		                out = open(result_%04d' % result_no, 'w')
				        print >> out, response.read()
		                out.close()
					# Nothing ever goes perfectly, ignore if we do not get page
				    except mechanize._response.httperror_seek_wrapper:
					print >> sys.stderr, "Response error (probably 404)"
		            # Let s not hammer the site too much between fetches
					time.sleep(1)
				'''
		else:
			is_np = False

	br.close()
	#	f.close()
	return url_list

def protein_grab():
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
#	url_list = ['http://www.ncbi.nlm.nih.gov/protein/AAN15854.1', 'http://www.ncbi.nlm.nih.gov/protein/AAN15855.1']
	if len(url_list) == 0:
		print '\t\tNone of URL generated by keywords, cannot grab web from NCBI...'
		print '\t\tProgramming will exit....'
		exit()
	idx = 1
	'''
	for url in url_list:
		print '\t\tURL from url list:\t%d\t%s'%(idx, url)
		idx = idx + 1
	'''
	# get data from html doc
	#		input: url, vo( which type is ProteinVO )
	#		output: vo, which is data stored
	#		process: get data by ragular expression, save data item to protein vo
	vo = ProteinVO.ProteinVO()
	vo_r = ProteinRefVO.ProteinRefVO()
	for url in url_list:
		get_html_data(url, vo)
#		print query_from_db(vo.getId())
		cds = query_from_db( vo.getId())
		if len(cds) == 0:
			print '\t\tNone of this data item existed in database, now saving to database...'
			save_to_db( vo )
			get_html_ref_data( vo.getId(), url, vo_r )
		else:
			print '\t\tExisted data in database, no data saved into database...'
	
def protein_get_from_local():
	files = os.listdir(local_html_dir)
	vo = ProteinVO.ProteinVO()
	vo_r = ProteinRefVO.ProteinRefVO()
	for f_path in files:
		if not os.path.isfile(local_html_dir + '/' + f_path):
			continue
		vo = get_data_from_local( local_html_dir + '/' + f_path, vo )
		if vo is None:
			print '\tNone of data gotten from local html file...'
			return
		cds = query_from_db( vo.getId())
		if len(cds) == 0:
			print '\tNone of this data item existed in database, now saving to database...'
			save_to_db( vo )
			get_local_ref_data( vo.getId(), local_html_dir + '/' + f_path, vo_r )
		else:
			print '\t\tExisted data in database, no data saved into database...'

if __name__ == '__main__':
#	protein_grab()
	protein_get_from_local()
