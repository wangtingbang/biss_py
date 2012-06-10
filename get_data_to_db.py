import re

def process_html_data_to_db( br, url ):
	patt_id = 'UniProtKB/Swiss-Prot:(.*?)</p>'# item id
	patt_locus = 'LOCUS(.*?)DEFINITION'	# locus
	patt_def = 'DEFINITION(.*?)ACCESSION'	#definition
	patt_acc = 'ACCESSION(.*?)VERSION'	#accession
	patt_kw = 'KEYWORDS(.*?)SOURCE'	#keywords
	patt_ver = 'VERSION(.*?)DBSOURCE'	#version
	patt_dbs = 'DBSOURCE(.*?)KEYWORDS'	#dbsource
	patt_org = 'ORGANISM(.*?)REFERENCE'	#organism
	patt_cmt = 'COMMENT(.*?)FEATURES'	#comment
	patt_ori = 'ORIGIN(.*?)//'	#origin
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
#	print f_data
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
	print 'item id:' + con_id[0].lstrip()
	con_locus = prog_locus.findall(f_data)
	print 'locus:' + con_locus[0].lstrip()
	con_def = prog_def.findall(f_data)
	print 'def:' + con_def[0].lstrip()
	con_acc = prog_acc.findall(f_data)
	print 'acc:' + con_acc[0].lstrip()
	con_kw = prog_kw.findall(f_data)
	print 'keywords:' + con_kw[0].lstrip()
	con_ver = prog_ver.findall(f_data)
	print 'version:' + con_ver[0].lstrip()
	con_dbs = prog_dbs.findall(f_data)
	print '-----------------------------------------------------'
	print 'dbsource:' + con_dbs[0].lstrip()
	print '-------------------------------------------------------'
	con_org = prog_org.findall(f_data)
	con_cmt =prog_cmt.findall(f_data)
	con_ori = prog_ori.findall(f_data)

	dbs_txt = con_dbs[0]
	patt_rpl = '<a(.*?)">'
	times_rpl = dbs_txt.count( '</a>' )
	dbs_txt = dbs_txt.replace( '</a>', '', times_rpl)
	print times_rpl
	prog_rpl = re.compile(patt_rpl, re.DOTALL)
	dbs_rpl = prog_rpl.findall(dbs_txt)
	for rpl in dbs_rpl:
		dbs_txt = dbs_txt.replace( '<a' + rpl + '">', '' )
	print 'dbs:======================================================='
	print dbs_txt
	print 'dbs end======================================================'
	'''
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
	'''
	'''
	print 'id:\t' + con_id[0]
	print 'locus:\t' + con_locus[0]
	print 'definition:\t' + con_def[0]
	print 'accession:\t' + con_acc[0]
	print 'keywords:\t' + con_kw[0]
	
	print 'locus|' + con_locus[0].lstrip()
	print 'version|' + con_ver[0].lstrip()
#	print 'dbsource|' + con_dbs[0]
	print 'organism|' + con_org[0].lstrip()
	print 'comment|' + con_cmt[0].lstrip()
	'''
	
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

#	print 'origin|' + ori_txt + '||'
	return

if __name__ == '__main__':
	process_html_data_to_db('', '')
