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

class ProteinRefVO(object):
	p_id = ''		# item id
	r_no = ''		# residues_no
	ath = ''		# authors
	ttl = ''		# title
	jur = ''		# journal

	##########  setter  ###########
	def setPid(object, para ):
		ProteinRefVO.p_id = para

	def setRno(object, para ):
		ProteinRefVO.r_no = para

	def setAth(object, para ):
		ProteinRefVO.ath = para

	def setTtl(object, para ):
		ProteinRefVO.ttl = para

	def setJur(object, para ):
		ProteinRefVO.jur = para

	###########  gettter  ###########
	def getPid(object):
		return ProteinRefVO.p_id

	def getRno(object):
		return ProteinRefVO.r_no

	def getAth(object):
		return ProteinRefVO.ath 

	def getTtl(object):
		return ProteinRefVO.ttl

	def getJur(object):
		return ProteinRefVO.jur
