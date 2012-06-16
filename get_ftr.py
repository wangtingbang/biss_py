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

webroot = '.'
kw_file_pro = './keywords/pro_kw.txt'	# keyword list file of protein
ul_file_pro = './logs/pro_ul.txt'	# url list file of protein
ul_err_file_pro = './logs/pro_ul_error.txt'	# url error log file of protein
lh_err_file_pro = './logs/pro_lh_error.txt' # local html file error log file of protein
local_html_dir = './local_html/web/protein'
base_dir = webroot + '/html/protein/'
#base_url_pro = 'http://www.ncbi.nlm.nih.gov/protein'
base_url_pro = 'http://localhost/biss/protein'

def get_html_data( url, vo ):
	patt_ftr = ''	#features
	patt_ftrs = '<span id="feature_(.*?)_source(.*?)</span>'	#feature_source
#	patt_ftrs = 'class="feature">(.*?)</span>'
	patt_ftrp = '<span id="feature_(.*?)_Protein_(.*?)</span>'	#feature_protein
#	patt_ftrc = '<span id="feature_(.*?)_CDS_(.*?)</span>'	#feature_cds
	patt_ftrc = 'CDS</a>(.*?)</span>'	#feature_cds

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
	ftr_txt = 'Location/Qualifiers'


	prog_ftrs = re.compile( patt_ftrs, re.DOTALL )

	print '\tFind all content by RE....\n'

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

	vo.setFtr(ftr_txt)
	vo.setFtrs(ftrs_txt)
	vo.setFtrp(ftrp_txt)
	vo.setFtrc(ftrc_txt)
	print 'End **************************************End'
	return vo

if __name__ == '__main__':
	vo = ProteinVO.ProteinVO()
	url = 'http://localhost/biss/protein/AAH02365.1.htm'
	get_html_data( url, vo )
	print 'F:\t',vo.getFtr(), '\nF_S:\t', vo.getFtrs(), '\nF_P:\t', vo.getFtrp(), '\nF_CDS:\t', vo.getFtrc()
