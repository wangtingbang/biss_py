class NucVO(object):
	'''
+------------+---------------+------+-----+---------+-------+
| Field      | Type          | Null | Key | Default | Extra |
+------------+---------------+------+-----+---------+-------+
| nrsid      | varchar(32)   | YES  |     | NULL    |       |
| locus      | varchar(256)  | YES  |     | NULL    |       |
| definition | varchar(256)  | YES  |     | NULL    |       |
| accession  | varchar(128)  | YES  |     | NULL    |       |
| version    | varchar(128)  | YES  |     | NULL    |       |
| dblink     | varchar(128)  | YES  |     | NULL    |       |
| keyword    | varchar(32)   | YES  |     | NULL    |       |
| source     | varchar(32)   | YES  |     | NULL    |       |
| organism   | varchar(512)  | YES  |     | NULL    |       |
| comments   | varchar(1024) | YES  |     | NULL    |       |
| contig     | varchar(128)  | YES  |     | NULL    |       |
+------------+---------------+------+-----+---------+-------+
	'''
	nid = ''		# item id
	locus = ''		# locus
	defi = ''		# definition
	acc = ''		# accession
	kw = ''			# keywords
	ver = ''		# version
	dbl = ''		# dblink
	src = ''		# source
	org = ''		# organism
	cmt = ''		# comment
	ctg = ''		# contig
	##########  setter  ###########
	def setId(object, para ):
		NucVO.nid = para

	def setLocus(object, para ):
		NucVO.locus = para

	def setDef(object, para ):
		NucVO.defi = para

	def setAcc(object, para ):
		NucVO.acc = para

	def setKw(object, para ):
		NucVO.kw = para

	def setVer(object, para ):
		NucVO.ver = para

	def setDbl(object, para ):
		NucVO.dbl = para

	def setOrg(object, para ):
		NucVO.org = para

	def setCmt(object, para ):
		NucVO.cmt = para

	def setCtg(object, para ):
		NucVO.ctg = para

	def setSrc(object, para ):
		NucVO.src = para

	###########  gettter  ###########
	def getId(object):
		return NucVO.nid

	def getLocus(object):
		return NucVO.locus

	def getDef(object):
		return NucVO.defi

	def getAcc(object):
		return NucVO.acc

	def getKw(object):
		return NucVO.kw

	def getVer(object ):
		return NucVO.ver

	def getDbl(object ):
		return NucVO.dbl

	def getOrg(object):
		return NucVO.org

	def getCmt(object ):
		return NucVO.cmt

	def getCtg(object ):
		return NucVO.ctg

	def getSrc(object):
		return NucVO.src
