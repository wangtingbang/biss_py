class MyClass(object):
	myval = 0
	mystr = ''
	def mysetter( object, val, s ):
		MyClass.myval = val
		MyClass.mystr = s

	def print_val(object):
		print 'val:%d' % MyClass.myval
		print 'str:' + MyClass.mystr
	
	def get_val(object):
		return MyClass.myval

class ProteinVO(object):
	item_id = ''		# item id
	locus = ''		# locus
	defi = ''		# definition
	acc = ''		# accession
	kw = ''			# keywords
	ver = ''		# version
	dbs = ''		# dbsource
	org = ''		# organism
	cmt = ''		# comment
	ori = ''		# origin
	ftr = ''		# feature
	ftr_s = ''		# feature source
	ftr_p = ''		# feature protein
	ftr_c = ''		# feature cds
	##########  setter  ###########
	def setId(object, para ):
		ProteinVO.item_id = para

	def setLocus(object, para ):
		ProteinVO.locus = para

	def setDef(object, para ):
		ProteinVO.defi = para

	def setAcc(object, para ):
		ProteinVO.acc = para

	def setKw(object, para ):
		ProteinVO.kw = para

	def setVer(object, para ):
		ProteinVO.ver = para

	def setDbs(object, para ):
		ProteinVO.dbs = para

	def setOrg(object, para ):
		ProteinVO.org = para

	def setCmt(object, para ):
		ProteinVO.cmt = para

	def setOri(object, para ):
		ProteinVO.ori = para

	def setFtr(object, para ):
		ProteinVO.ftr = para

	def setFtrs(object, para ):
		ProteinVO.ftr_s = para

	def setFtrp(object, para ):
		ProteinVO.ftr_p = para

	def setFtrc(object, para ):
		ProteinVO.ftr_c = para

	###########  gettter  ###########
	def getId(object):
		return ProteinVO.item_id

	def getLocus(object):
		return ProteinVO.locus

	def getDef(object ):
		return ProteinVO.defi

	def getAcc(object ):
		return ProteinVO.acc

	def getKw(object):
		return ProteinVO.kw

	def getVer(object):
		return ProteinVO.ver

	def getDbs(object):
		return ProteinVO.dbs

	def getOrg(object ):
		return ProteinVO.org

	def getCmt(object):
		return ProteinVO.cmt

	def getOri(object):
		return ProteinVO.ori

	def getFtr(object):
		return ProteinVO.ftr

	def getFtrs(object):
		return ProteinVO.ftr_s

	def getFtrp(object):
		return ProteinVO.ftr_p

	def getFtrc(object):
		return ProteinVO.ftr_c

if __name__ == '__main__':
	mc = MyClass()
	print mc.myval
	mc.mysetter( 12, 'sigh.differ')
	mc.print_val()
	print 'my val: %d ' % mc.get_val()

	pro = ProteinVO()
	pro.setDef( 'definition' )
	print pro.getDef()
