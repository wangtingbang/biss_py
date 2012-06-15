import os

def read_dir( f_dir ):
	f = open(f_dir)
	print f
	lst = f.read()
	print lst
	return

if __name__ == '__main__':
	f_dir = './local_html/web/protein'
#	read_dir(f_dir)
	print os.listdir( f_dir )
