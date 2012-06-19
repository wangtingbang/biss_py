class PubVO(object):
	'''
+------------------+-------------+------+-----+---------+-------+
| Field            | Type        | Null | Key | Default | Extra |
+------------------+-------------+------+-----+---------+-------+
| pmid             | varchar(16) | YES  |     | NULL    |       |
| pubdate          | datetime    | YES  |     | NULL    |       |
| iso_abbreviation | text        | YES  |     | NULL    |       |
| medline_pgn      | text        | YES  |     | NULL    |       |
| article_title    | text        | YES  |     | NULL    |       |
| authors          | text        | YES  |     | NULL    |       |
| abstracts        | text        | YES  |     | NULL    |       |
| pub_types        | text        | YES  |     | NULL    |       |
| mesh_items       | text        | YES  |     | NULL    |       |
| substances       | text        | YES  |     | NULL    |       |
| link_out         | text        | YES  |     | NULL    |       |
+------------------+-------------+------+-----+---------+-------+
	'''
	pmid = ''		# pmid
	p_date = ''		# pubdate
	iso_abbr = ''		# iso_abbreviation
	mdl_pgn = ''		# medline_pgn
	atl_ttl = ''			# article_title
	aths = ''		# authors
	abstr = ''		# abstracts
	p_type = ''		# pub_types
	msh_itm = ''		# mesh_items
	subs = ''		# substances
	lnk_out = ''		# link_out
	##########  setter  ###########
	def setId(object, para ):
		PubVO.pmid = para
	
	def setPd(object, para ):
		PubVO.p_date = para
		
	def setIa(object, para ):
		PubVO.iso_abbr = para
	
	def setMp(object, para ):
		PubVO.mdl_pgn = para
	
	def setAt(object, para ):
		PubVO.atl_ttl = para
	
	def setAth(object, para ):
		PubVO.aths = para
	
	def setAbs(object, para ):
		PubVO.abstr = para

	def setPt(object, para ):
		PubVO.p_type = para
	
	def setMi(object, para ):
		PubVO.msh_itm = para
	
	def setSb(object, para ):
		PubVO.subs = para

	def setLo(object, para ):
		PubVO.lnk_out = para
	
	###########  gettter  ###########
	def getId(object):
		return PubVO.pmid
	
	def getPd(object):
		return PubVO.p_date
		
	def getIa(object):
		return PubVO.iso_abbr
	
	def getMp(object):
		return PubVO.mdl_pgn
	
	def getAt(object):
		return PubVO.atl_ttl
	
	def getAth(object):
		return PubVO.aths
	
	def getAbs(object):
		return PubVO.abstr

	def getPt(object):
		return PubVO.p_type
	
	def getMi(object):
		return PubVO.msh_itm
	
	def getSb(object):
		return PubVO.subs

	def getLo(object):
		return PubVO.lnk_out
