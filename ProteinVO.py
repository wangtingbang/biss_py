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


if __name__ == '__main__':
	mc = MyClass()
	print mc.myval
	mc.mysetter( 12, 'sigh.differ')
	mc.print_val()
	print 'my val: %d ' % mc.get_val()

	pro = ProteinVO()
	pro.setDef( 'definition' )
	print pro.getDef()
