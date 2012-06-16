import re
import os
import os.path
import time
import mechanize
import urllib2
import sys
import MySQLdb
import MySqlConn
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

		print idx + 1
		print '\tRe#:\t\n##', rno_txt, '##'
		print 'Authors:\t\n',  ath_txt
		print '\tTitle:\t\n',  ttl_txt
		print '\tJournal:\t\n', jur_txt 
		print jur_rpl

		vo.setPid(pid)
		vo.setRno(rno_txt)
		vo.setAth(ath_txt)
		vo.setTtl(ttl_txt)
		vo.setJur(jur_txt)
		save_ref_to_db(vo)
		idx = idx + 1
	'''

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

	vo.setFtr(ftr_txt)
	vo.setFtrs(ftrs_txt)
	vo.setFtrp(ftrp_txt)
	vo.setFtrc(ftrc_txt)
	print 'End **************************************End'
	return vo
'''

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
	f_open = open( './logs/sql.sql', 'w')
	f_open.write(sql)
	print 'Now inserting data into database...'
	res = MySqlConn.insert_one_by_sql(sql)
	print '\tData inserted into database...'
	return


if __name__ == '__main__':
	vo = ProteinRefVO.ProteinRefVO()
	url = 'http://localhost/biss/protein/ADI01203.1.htm'
#	url = 'http://localhost/biss/protein/AAH02365.1.htm'
	get_html_ref_data( 'AAH02365.1', url, vo )
