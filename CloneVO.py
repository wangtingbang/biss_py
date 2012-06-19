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

class CloneVO(object):
	cid = ''
	lib_name = ''
	lib_abbr = ''
	organism = ''
	destributors = ''
	vetor_type = ''
	clones_db = ''
	end_seq_cdb = ''
	isrt_seq_cdb = ''
	c_end_seq = ''
	##########  setter  ###########
	def setId(object, para ):
		CloneVO.cid = para

	def setLn(object, para ):
		CloneVO.lib_name = para

	def setLa(object, para ):
		CloneVO.lib_abbr = para

	def setOrg(object, para ):
		CloneVO.organism = para

	def setDstr(object, para ):
		CloneVO.destributors = para

	def setVt(object, para ):
		CloneVO.vetor_type = para

	def setCdb(object, para ):
		CloneVO.clones_db = para

	def setEsc(object, para ):
		CloneVO.end_seq_cdb = para

	def setIsc(object, para ):
		CloneVO.isrt_seq_cdb = para

	def setCes(object, para ):
		CloneVO.c_end_seq = para

	###########  gettter  ###########
	def getId(object):
		return CloneVO.cid

	def getLn(object):
		return CloneVO.lib_name

	def getLa(object):
		return CloneVO.lib_abbr

	def getOrg(object):
		return CloneVO.organism

	def getDstr(object):
		return CloneVO.destributors

	def getVt(object):
		return CloneVO.vetor_type

	def getCdb(object):
		return CloneVO.clones_db

	def getEsc(object):
		return CloneVO.end_seq_cdb

	def getIsc(object):
		return CloneVO.isrt_seq_cdb

	def getCes(object):
		return CloneVO.c_end_seq

if __name__ == '__main__':
	mc = MyClass()
	print mc.myval
	mc.mysetter( 12, 'sigh.differ')
	mc.print_val()
	print 'my val: %d ' % mc.get_val()

	pro = CloneVO()
	pro.setDef( 'definition' )
	print pro.getDef()
