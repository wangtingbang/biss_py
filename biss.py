'''
Created on 2012-4-26

@author: sigh.differ
'''

#if __name__ == '__main__':
#   pass

#import MySQLdb

#conn = MySQLdb.Connect(host='localhost', user='root', passwd='mysql', db='test')
#cursor = conn.cursor()
#cursor.execute( "select * from user")
#cds = cursor.fetchall()

import CloneProcessor, NucCoreProcessor, ProteinProcessor, PubmedProcessor

if __name__ == '__main__':
	print 'Welcome to BISS....'
	print 'Start grabing Protein data item from NCBI....\n'
	ProteinProcessor.protein_grab()
	print '\nProtein data item grab completed...\n'

	print 'Start grabing Protein data item from NCBI....\n'
	NucCoreProcessor.nuccore_grab()
	print '\nNuccore data item grab completed...\n'

	print 'Start grabing Protein data item from NCBI....\n'
	CloneProcessor.clone_grab()
	print '\nClone data item grab completed...\n'

	print 'Start grabing Protein data item from NCBI....\n'
	PubmedProcessor.pubmed_grab()
	print '\nPubmed data item grab completed...\n'
