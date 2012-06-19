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

class NucRefVO(object):
	n_id = ''		# item id
	r_no = ''		# residues_no
	ath = ''		# authors
	ttl = ''		# title
	jur = ''		# journal

	##########  setter  ###########
	def setNid(object, para ):
		NucRefVO.n_id = para

	def setRno(object, para ):
		NucRefVO.r_no = para

	def setAth(object, para ):
		NucRefVO.ath = para

	def setTtl(object, para ):
		NucRefVO.ttl = para

	def setJur(object, para ):
		NucRefVO.jur = para

	###########  gettter  ###########
	def getNid(object):
		return NucRefVO.n_id

	def getRno(object):
		return NucRefVO.r_no

	def getAth(object):
		return NucRefVO.ath 

	def getTtl(object):
		return NucRefVO.ttl

	def getJur(object):
		return NucRefVO.jur
