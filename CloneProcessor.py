'''
Created on 2012-5-31

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
import CloneVO

webroot = '.'
kw_file_clo = './keywords/clo_kw.txt'	# keyword list file of nuccore
ul_file_clo = './logs/clo_ul.txt'	# url list file of nuccore
ul_err_file_clo = './logs/clo_ul_error.txt'	# url error log file of nuccore
lh_err_file_clo = './logs/clo_lh_error.txt' # local html file error log file of nuccore
local_html_dir = './local_html/web/clone'
base_dir = webroot + '/html/clone/'
#base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'
base_url_clo = 'http://localhost/biss/clone'

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
+--------------+---------------+------+-----+---------+-------+
| Field        | Type          | Null | Key | Default | Extra |
+--------------+---------------+------+-----+---------+-------+
| cid          | varchar(16)   | YES  |     | NULL    |       |
| lib_name     | varchar(128)  | YES  |     | NULL    |       |
| lib_abbr     | varchar(16)   | YES  |     | NULL    |       |
| organism     | varchar(32)   | YES  |     | NULL    |       |
| destributors | varchar(1024) | YES  |     | NULL    |       |
| vetor_type   | varchar(16)   | YES  |     | NULL    |       |
| clones_db    | varchar(64)   | YES  |     | NULL    |       |
| end_seq_cdb  | int(11)       | YES  |     | NULL    |       |
| isrt_seq_cdb | int(11)       | YES  |     | NULL    |       |
| c_end_seq    | int(11)       | YES  |     | NULL    |       |
+--------------+---------------+------+-----+---------+-------+
	'''

	sql = 'insert into biss_clone values (\'' + vo.getId() + '\', \'' + vo.getLn() + '\', \'' + vo.getLa() + '\', \'' + vo.getOrg() + '\', \'' + vo.getDstr() + '\', \'' + vo.getVt() + '\', \'' + vo.getCdb() + '\', \'' + vo.getEsc() + '\', \'' + vo.getIsc() + '\', \'' + vo.getCes() + '\');'
	f_open = open( './logs/clone_sql.sql', 'a')
	f_open.write(sql + '\n')
	print 'Now inserting data into database...'
	print 'SQL:\n', sql
	try:
		res = MySqlConn.insert_one_by_sql(sql)
		print '\tData inserted into database...'
	except MySQLdb.DataError:
		print '\tData error, cannot save data...'
	return

def query_from_db( cid):
	print 'Query from database, item id: ' + cid
	sql = 'select cid from biss_clone where cid = ( \'' + cid + '\');';
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
	patt_id = '<smfont>(.*?)</smfont>'
	patt_ln = '<dt>Library name: (.*?)</dd>'				# lib name
	patt_la = '<dt>Clone name aliases: (.*?)</dd>'			# lib abbr
	patt_org = '<dt>Organism: (.*?)</dd>'			# organsim
	patt_dstr = ''			# destributors
	patt_vt = '<dt>Library type:(.*?)</dd>'			# version
	patt_cdb = '<dt>Clone DB name: (.*?)</dd>'			# version
	patt_esc = '<td><td>(.*?)</td><td>(.*?)</td>'		# dbsource
	patt_isc = ''		# organism
	patt_ces = ''			# comment
	f_data = None
	try:
		br = mechanize.Browser()
		f_url = br.open(url)
		f_data = f_url.get_data()
		br.close()
	except urllib2.URLError, e:
		print '\tURL open error, url is: ' + url, e
		print '\tSaving error url to log file: ' + ul_err_file_clo
		f_err = open(ul_err_file_clo, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return

	print '\tRagular expressions compiling...'
	prog_id = re.compile( patt_id, re.DOTALL )
	prog_ln = re.compile( patt_ln, re.DOTALL )
	prog_la = re.compile( patt_la, re.DOTALL )
	prog_org = re.compile( patt_org, re.DOTALL )
	prog_dstr = re.compile( patt_dstr, re.DOTALL )
	prog_vt = re.compile( patt_vt, re.DOTALL )
	prog_cdb = re.compile( patt_cdb, re.DOTALL )
	prog_esc = re.compile( patt_esc, re.DOTALL )
	prog_isc = re.compile( patt_isc, re.DOTALL )
	prog_ces = re.compile( patt_ces, re.DOTALL )
	
	print '\tFind all content by RE....'	
	con_id = prog_id.findall(f_data)

	if len(con_id) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_clo
		f_err = open(ul_err_file_clo, 'a')
		t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
		f_err.write( '====================================\n' + t + '\n\t' + url + '\n')
		f_err.close()
		return None

	id_txt = con_id[0].split(':')[1].lstrip()
	id_txt = id_txt.split(')')[0]

	con_ln = prog_ln.findall(f_data)
	con_la = prog_la.findall(f_data)
	con_org = prog_org.findall(f_data)
	con_dstr = prog_dstr.findall(f_data)
	con_vt = prog_vt.findall(f_data)
	con_cdb = prog_cdb.findall(f_data)
	con_esc = prog_esc.findall(f_data)
	con_isc = prog_isc.findall(f_data)
	con_ces =prog_ces.findall(f_data)

	# processe lib name data item
	if len(con_ln) == 0:
		ln_txt = ''
	else:
		ln_txt = con_ln[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = ln_txt.count( '</a>' )
		ln_txt = ln_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ln_rpl = prog_rpl.findall(ln_txt)
		times_rpl = ln_txt.count( '\n' )
		ln_txt.replace( '\n', '\t', times_rpl)
		for rpl in ln_rpl:
			ln_txt = ln_txt.replace( '<a' + rpl + '">', '' )
		ln_txt = ln_txt.lstrip()
	# lib name data item process completed

	# process definition data item
	if len(con_la) == 0:
		la_txt = ''
	else:
		la_txt = con_la[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = la_txt.count( '</a>' )
		la_txt = la_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		la_rpl = prog_rpl.findall(la_txt)
		la_txt.replace( '\n', '\t')
		for rpl in la_rpl:
			la_txt = la_txt.replace( '<a' + rpl + '">', '' )
		la_txt = la_txt.lstrip()
	# lib abbr data item process completed

	# process organsim data item
	if len(con_org) == 0:
		org_txt = ''
	else:
		org_txt = con_org[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = org_txt.count( '</a>' )
		org_txt = org_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		org_rpl = prog_rpl.findall(org_txt)
		org_txt.replace( '\n', '\t')
		for rpl in org_rpl:
			org_txt = org_txt.replace( '<a' + rpl + '">', '' )
		org_txt = org_txt.lstrip()
	# organism data item process completed

	# process destributors data item
	dstr_txt = ''
	'''
	if len(con_dstr) == 0:
		dstr_txt = ''
	else:
		print 'DSTR con:', con_dstr
		dstr_txt = con_dstr[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = dstr_txt.count( '</a>' )
		dstr_txt = dstr_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		dstr_rpl = prog_rpl.findall(dstr_txt)
		dstr_txt.replace( '\n', '\t')
		for rpl in dstr_rpl:
			dstr_txt = dstr_txt.replace( '<a' + rpl + '">', '' )
		dstr_txt = dstr_txt.lstrip()
		'''
	# destributors data item process completed

	# process vetor type data item
	if len(con_vt) == 0:
		vt_txt = ''
	else:
		vt_txt = con_vt[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = vt_txt.count( '</a>' )
		vt_txt = vt_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		vt_rpl = prog_rpl.findall(vt_txt)
		vt_txt.replace( '\n', '\t')
		for rpl in vt_rpl:
			vt_txt = vt_txt.replace( '<a' + rpl + '">', '' )
		vt_txt = vt_txt.lstrip()
	# vetor type data item process completed

	# process cdb data item
	if len(con_cdb) == 0:
		cdb_txt = ''
	else:
		cdb_txt = con_cdb[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = cdb_txt.count( '</a>' )
		cdb_txt = cdb_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		cdb_rpl = prog_rpl.findall(cdb_txt)
		cdb_txt.replace( '\n', '\t')
		for rpl in cdb_rpl:
			cdb_txt = cdb_txt.replace( '<a' + rpl + '">', '' )
		cdb_txt = cdb_txt.lstrip()
	# cdb data item process completed

	# process esc data item
	if len(con_esc) == 0:
		esc_txt = ''
	else:
		esc_txt = con_esc[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = esc_txt.count( '</a>' )
		esc_txt = esc_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		esc_rpl = prog_rpl.findall(esc_txt)
		esc_txt.replace( '\n', '\t')
		for rpl in cdb_rpl:
			esc_txt = esc_txt.replace( '<a' + rpl + '">', '' )
		esc_txt = esc_txt.lstrip()
	# cdb esc item process completed

	# process isc data item
	con_isc = []
	if len(con_isc) == 0:
		isc_txt = ''
	else:
		isc_txt = con_isc[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = isc_txt.count( '</a>' )
		isc_txt = isc_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		isc_rpl = prog_rpl.findall(isc_txt)
		isc_txt.replace( '\n', '\t')
		for rpl in cdb_rpl:
			isc_txt = isc_txt.replace( '<a' + rpl + '">', '' )
		isc_txt = isc_txt.lstrip()
	# cdb isc item process completed

	# process ces data item
	con_ces = []
	if len(con_ces) == 0:
		ces_txt = ''
	else:
		ces_txt = con_ces[0].split('<dd>')[1]
		patt_rpl = '<a(.*?)">'
		times_rpl = ces_txt.count( '</a>' )
		ces_txt = ces_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		ces_rpl = prog_rpl.findall(ces_txt)
		ces_txt.replace( '\n', '\t')
		for rpl in cdb_rpl:
			ces_txt = ces_txt.replace( '<a' + rpl + '">', '' )
		ces_txt = ces_txt.lstrip()
	# cdb ces item process completed


	'''
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
		print 'ftrc_txt = con_ftrc[0][1]\n\t', ftrc_txt
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
		print '\n\nPlaced:\t$$$$$$$$$$$$$$$$\n',ftrc_txt, '\n****************'
	# CDS protein data item process completed
	'''
	# save data to vo
	print '\tSaving data to vo...'
	vo.setId(id_txt)
	vo.setLn(ln_txt)
	vo.setLa(la_txt)
	vo.setOrg(org_txt)
	vo.setDstr(dstr_txt)
	vo.setVt(vt_txt)
	vo.setCdb(cdb_txt)
	vo.setEsc(esc_txt)
	vo.setIsc(isc_txt)
	vo.setCes(ces_txt)
#	print '\tvo size is: ', sys.getsizeof(vo)
	print '\tSaving url to log file...'
	f_ul = open(ul_file_clo, 'a')	# append a url to url list log file
	f_ul.write( vo.getId() + ':' + url + '\n' )
	f_ul.close()
	print '\tHTML data gotten, url saved, next processing...'
	return vo

def get_data_from_local( f_path, vo ):
	print 'Getting html data from local html file: ' + f_path
	patt_id = '<p class="itemid">(.*?)</p>'
	patt_locus = 'LOCUS(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z]'				# locus
	patt_def = 'DEFINITION(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z]'			# definition
	patt_acc = 'ACCESSION(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z]'			# accession
	patt_kw = 'KEYWORDS(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'			# keywords
	patt_ver = 'VERSION(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'			# version
	patt_src = 'SOURCE(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'			# version
	patt_dbl = 'DBLINK(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'		# dbsource
	patt_org = 'ORGANISM(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'		# organism
	patt_cmt = 'COMMENT(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'			# comment
	patt_ori = 'ORIGIN(.*?)//'										# origin
	patt_ori_2 = 'ORIGIN(.*?)[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]'
#	patt_ftr = ''
#	patt_ftrs = '<span id="feature_(.*?)_source(.*?)</span>'	#feature_source
#	patt_ftrp = '<span id="feature_(.*?)_Protein_(.*?)</span>'	#feature_protein
#	patt_ftrc = 'CDS</a>(.*?)</span>'	#feature_cds
	'''
	f_name = './Q45071.2.htm'
	print 'open file ' + f_name + '....'
	f_html = open(f_name, 'r')
	f_data = f_html.read()
	f_html.close()
	'''
	f_data = None
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
	prog_src = re.compile( patt_src, re.DOTALL )
	prog_dbl = re.compile( patt_dbl, re.DOTALL )
	prog_org = re.compile( patt_org, re.DOTALL )
	prog_cmt = re.compile( patt_cmt, re.DOTALL )
	prog_ori = re.compile( patt_ori, re.DOTALL )
	prog_ori_2 = re.compile( patt_ori_2, re.DOTALL )
#	prog_ftrs = re.compile( patt_ftrs, re.DOTALL )
#	prog_ftrp = re.compile( patt_ftrp, re.DOTALL )
#	prog_ftrc = re.compile( patt_ftrc, re.DOTALL )
	
	print '\tFind all content by RE....'	
	con_id = prog_id.findall(f_data)

	if len(con_id) == 0:
		print '\tCannot get item id from html doc, maybe url is error...'
		print '\tSaving error url to log file: ' + ul_err_file_clo
		f_err = open(ul_err_file_clo, 'a')
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
	con_src = prog_src.findall(f_data)
	con_dbl = prog_dbl.findall(f_data)
	con_org = prog_org.findall(f_data)
	con_cmt =prog_cmt.findall(f_data)
	con_ori = prog_ori.findall(f_data)
	con_ori_2 = prog_ori_2.findall(f_data)

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

	# process source data item
	if len(con_src) == 0:
		src_txt = ''
	else:
		src_txt = con_src[0].lstrip()
		src_txt.replace( '\n', '\t')
	# source data item process completed

	# processe dblink data item
	if len(con_dbl) == 0:
		dbl_txt = ''
	else:
		dbl_txt = con_dbs[0]
		patt_rpl = '<a(.*?)">'
		times_rpl = dbl_txt.count( '</a>' )
		dbl_txt = dbl_txt.replace( '</a>', '', times_rpl)
		#print times_rpl
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
		dbl_rpl = prog_rpl.findall(dbl_txt)
		dbl_txt.replace( '\n', '\t')
		for rpl in dbl_rpl:
			dbl_txt = dbl_txt.replace( '<a' + rpl + '">', '' )
	# dblink data item process completed

	# process organism data item
	if len(con_org) == 0:
		org_txt = ''
	else:
		org_txt = con_org[0]
		times_rpl = org_txt.count( '</a>' )
		org_txt = org_txt.replace( '</a>', '', times_rpl)
		patt_rpl = '<a(.*?)">'
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
		patt_rpl = '<a(.*?)">'
		prog_rpl = re.compile(patt_rpl, re.DOTALL)
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

	if len(con_ori)==0:
		if len(con_ori_2) == 0:
			ori_txt = ''
		else:
			ori_txt = con_ori_2[0]
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
	'''
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
		print 'ftrc_txt = con_ftrc[0][1]\n\t', ftrc_txt
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
		print '\n\nPlaced:\t$$$$$$$$$$$$$$$$\n',ftrc_txt, '\n****************'
	# CDS protein data item process completed
	'''
	# save data to vo
	print '\tSaving data to vo...'
	vo.setId(id_txt)
	vo.setLocus(lcs_txt)
	vo.setDef(def_txt)
	vo.setAcc(acc_txt)
	vo.setKw(kw_txt)
	vo.setVer(ver_txt)
	vo.setSrc(src_txt)
	vo.setDbl(dbl_txt)
	vo.setOrg(org_txt)
	vo.setCmt(cmt_txt)
	vo.setCtg(ori_txt)

#	print '\tvo size is: ', sys.getsizeof(vo)

	print '\tHtml data gotten, next processing...'
	return vo

def get_html_ref_data( nid, url, vo ):
	print 'Getting references from html doc...'
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
		print '\tSaving error url to log file: ' + ul_err_file_clo
		f_err = open(ul_err_file_clo, 'a')
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
		print '\tSaving error url to log file: ' + ul_err_file_clo
		f_err = open(ul_err_file_clo, 'a')
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
		times = ath_txt.count('            ')
		ath_txt = ath_txt.replace('            ', ' ',times)
		times = ath_txt.count('\'')
		ath_txt = ath_txt.replace('\'', '-',times)
		times = ath_txt.count('\n')
		ath_txt = ath_txt.replace('\n', ' ',times)

		ttl_txt = con_ttl[idx]
		ttl_txt = ttl_txt.lstrip()
		times = ttl_txt.count('\'')
		ttl_txt = ttl_txt.replace('\'', '-',times)
		times = ttl_txt.count('            ')
		ttl_txt = ttl_txt.replace('            ', ' ',times)
		times = ttl_txt.count('\n')
		ttl_txt = ttl_txt.replace('\n', ' ',times)

		jur_txt = con_jur[idx]
		jur_txt = jur_txt.lstrip()
		times = jur_txt.count('\'')
		jur_txt = jur_txt.replace('\'', '-',times)
		times = jur_txt.count('            ')
		jur_txt = jur_txt.replace('            ', ' ',times)
		times = jur_txt.count('\n')
		jur_txt = jur_txt.replace('\n', ' ', times)
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

		vo.setNid(nid)
		vo.setRno(rno_txt)
		vo.setAth(ath_txt)
		vo.setTtl(ttl_txt)
		vo.setJur(jur_txt)
		save_ref_to_db(vo)
		idx = idx + 1

def get_local_ref_data( nid, f_name, vo ):
	print 'Getting references from html doc...'
	patt_rno = 'REFERENCE(.*?)[A-Z][A-Z][A-Z][A-Z]'	# residues no
	patt_ath = 'AUTHORS(.*?)[A-Z][A-Z][A-Z]'	#authors
	patt_ttl = 'TITLE(.*?)[A-Z][A-Z][A-Z][A-Z]'	#title
	patt_jur = 'JOURNAL(.*?)[A-Z][A-Z][A-Z][A-Z]'		# journal

	f_data = None
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
		print '\tSaving error url to log file: ' + ul_err_file_clo
		f_err = open(ul_err_file_clo, 'a')
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
		times = ath_txt.count('            ')
		ath_txt = ath_txt.replace('            ', ' ',times)
		times = ath_txt.count('\'')
		ath_txt = ath_txt.replace('\'', '-',times)
		times = ath_txt.count('\n')
		ath_txt = ath_txt.replace('\n', ' ',times)

		ttl_txt = con_ttl[idx]
		ttl_txt = ttl_txt.lstrip()
		times = ttl_txt.count('\'')
		ttl_txt = ttl_txt.replace('\'', '-',times)
		times = ttl_txt.count('            ')
		ttl_txt = ttl_txt.replace('            ', ' ',times)
		times = ttl_txt.count('\n')
		ttl_txt = ttl_txt.replace('\n', ' ',times)

		jur_txt = con_jur[idx]
		jur_txt = jur_txt.lstrip()
		times = jur_txt.count('\'')
		jur_txt = jur_txt.replace('\'', '-',times)
		times = jur_txt.count('            ')
		jur_txt = jur_txt.replace('            ', ' ',times)
		times = jur_txt.count('\n')
		jur_txt = jur_txt.replace('\n', ' ', times)
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

		vo.setNid(nid)
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
	sql = 'insert into biss_nuc_ref values (\'' + vo.getNid() + '\', \'' + vo.getRno() + '\', \'' + vo.getAth() + '\', \'' + vo.getTtl() + '\', \'' + vo.getJur() + '\');'
	f_open = open( './logs/clo_ref.sql', 'w')
	f_open.write(sql)
	print 'Now inserting data into database...'
	try:
		print 'SQL:\n',sql
		res = MySqlConn.insert_one_by_sql(sql)
		print '\tData inserted into database...'
	except MySQLdb.DataError:
		print '\tData error, cannot save data...'
	return


def get_url_list( kw ): # function same as url_list_init
	print 'Get url list by query keywords( ' + kw + ' )from NCBI website...'
	br = mechanize.Browser()
	idx_pg = 1
	web = None
	f = None
	is_np = True
	url_list = []
	while is_np == True:
		kw_url = 'http://localhost/biss/clone_af_' + str(idx_pg) + '.htm'
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

		patt_r = '<a href="http://www.ncbi.nlm.nih.gov/clone/(.*?)"'	# rough re pattern
		patt_d = '/clone/(.*?)">'		# detail re pattern
	#	print patt_r
		print '\tStarting get url list from web content...'
		print '\tCompiling ragular expression....'
		prog_r = re.compile(patt_r)
		rough = prog_r.findall(cont)			# rough keywords
		print 'ROUGH:\n\t',rough
		if len(rough) == 0:
			print rough
			print '\tNone of result by keyword:' + kw
			return None
		idx = 0
		for r in rough:
#			kw = d_kws.split('"')[0]
#			nice_url = base_url_pro + '/' + kw
			nice_url = base_url_clo + '/' + r + '.htm'
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

def clone_grab():
	# read keywords for quering from file
	kws = read_kw( kw_file_clo )
	if kws is None:
		print 'Keywords is None, plz check you keywords file:\n\t' + kw_file_clo
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
	if len(url_list) == 0:
		print '\t\tNone of URL generated by keywords, cannot grab web from NCBI...'
		print '\t\tProgramming will exit....'
		exit()
	idx = 1
	# get data from html doc
	#		input: url, vo( which type is ProteinVO )
	#		output: vo, which is data stored
	#		process: get data by ragular expression, save data item to protein vo
	vo = CloneVO.CloneVO()
	for url in url_list:
		get_html_data(url, vo)
#		print query_from_db(vo.getId())
		cds = query_from_db( vo.getId())
		if len(cds) == 0:
			print '\t\tNone of this data item existed in database, now saving to database...'
			save_to_db( vo )
		else:
			print '\t\tExisted data in database, no data saved into database...'
	
def clone_get_from_local():
	if os.listdir(local_html_dir) is None:
		print 'No local html file...'
		return
	files = os.listdir(local_html_dir)
	vo = NucVO.NucVO()
	vo_r = NucRefVO.NucRefVO()
	for f_path in files:
		if not os.path.isfile(local_html_dir + '/' + f_path):
			continue
		get_data_from_local( local_html_dir + '/' + f_path, vo )
		cds = query_from_db( vo.getId())
		if len(cds) == 0:
			print '\tNone of this data item existed in database, now saving to database...'
			save_to_db( vo )
			get_local_ref_data( vo.getId(), local_html_dir + '/' + f_path, vo_r )
		else:
			print '\t\tExisted data in database, no data saved into database...'

if __name__ == '__main__':
	clone_grab()
	#clone_get_from_local()


