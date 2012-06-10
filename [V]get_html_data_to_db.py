import re

def process_html_data_to_db( br, url ):
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
	print 'item id:\n' + con_id[0].lstrip()
	con_locus = prog_locus.findall(f_data)
	print 'locus:\n' + con_locus[0].lstrip()
	con_def = prog_def.findall(f_data)
	print 'definition:\n' + con_def[0].lstrip()
	con_acc = prog_acc.findall(f_data)
	print 'accession:\n' + con_acc[0].lstrip()
	con_kw = prog_kw.findall(f_data)
	print 'keywords:\n' + con_kw[0].lstrip()
	con_ver = prog_ver.findall(f_data)
	print 'version:\n' + con_ver[0].lstrip()
	con_dbs = prog_dbs.findall(f_data)
	con_org = prog_org.findall(f_data)
#	print 'organism:' + con_org[0]
	con_cmt =prog_cmt.findall(f_data)
#	print 'comment: '  + con_cmt[0]
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
	print 'dbsource:\n'
	print dbs_txt
# dbsource data item process completed

# process organism data item
	org_txt = con_org[0]
	times_rpl = org_txt.count( '</a>' )
	org_txt = org_txt.replace( '</a>', '', times_rpl)
	org_rpl = prog_rpl.findall( org_txt )
	for rpl in org_rpl:
		org_txt = org_txt.replace( '<a' + rpl + '">', '' )
	print 'organsim:\n' + org_txt
# organism data item process completed

# process comments data item
	cmt_txt = con_cmt[0]
	times_rpl = cmt_txt.count( '</a>' )
	cmt_txt = cmt_txt.replace( '</a>', '', times_rpl)
	cmt_rpl = prog_rpl.findall( cmt_txt )
	for rpl in cmt_rpl:
		cmt_txt = cmt_txt.replace( '<a' + rpl + '">', '' )
	print 'commtens:\n' + cmt_txt

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
	print 'origin:\n' + org_txt
# origin data item processe completed
	
	return

if __name__ == '__main__':
	process_html_data_to_db('', '')
