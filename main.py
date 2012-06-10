'''
Created on 2012-5-26

@author: sigh.differ
'''

#if __name__ == '__main__':
#   pass

#import MySQLdb

#conn = MySQLdb.Connect(host='localhost', user='root', passwd='mysql', db='test')
#cursor = conn.cursor()
#cursor.execute( "select * from user")
#cds = cursor.fetchall()

import sys
import MySQLdb
import MySqlConn, URLGenerator, CloneProcessor, NucCoreProcessor, ProteinProcessor, PubmedProcessor

def getdata ():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='test', port=3306, charset='utf8')
    cur = conn.cursor()
    sql = 'select * from user'
    cur.execute(sql)
    alluser = cur.fetchall()
#    print 'good'
    for rec in alluser:
        print rec[0]
    cur.close()
    conn.close()

if __name__ == '__main__':
    sql = 'select * from user'
    cds = MySqlConn.query_by_sql(sql)
    print cds
#    file = 'f:\win-run-command.txt'
#    urls = URLGenerator.protein_url_generator(file)
#    print urls
#    cds = MySqlConn.query_by_sql('select * from user')
#    print cds
    
def get_clone(file):
    urls = URLGenerator.clone_url_generator(file)
    open(urls)
    return
    
def get_nuccore(file):
    return
    
def get_protein(file):
    return

def get_pubmed(file):
    return
