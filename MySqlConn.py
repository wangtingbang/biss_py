'''
Created on 2012-5-26

@author: sigh.differ
'''
import MySQLdb

hostname = 'localhost'
dbuser = 'root'
dbpwd = 'mysql'
dbname = 'biss'

def query_by_sql(sql):
	conn = MySQLdb.Connect(host=hostname, user=dbuser, passwd=dbpwd, db=dbname)
	cursor = conn.cursor()
	cursor.execute(sql)
	cds = cursor.fetchall()
	#print cds
	return cds
'''
def query_by_proc(proc_sql):
    conn = MySQLdb.Connect(host=hostname, user=dbuser, passwd=dbpwd, db=dbname)
    cursor = conn.cursor()
    cursor.callproc(proc_sql)
    cds = cursor.fetchall()
    #print cds
    return cds
'''
def query_by_proc(proc_name, val):
	conn = MySQLdb.Connect(host=hostname, user=dbuser, passwd=dbpwd, db=dbname)
	cursor = conn.cursor()
	print val
	cursor.callproc(proc_name,  val )
	cds = cursor.fetchall()
    #print cds
	return cds

def insert_one_by_sql(sql):
	conn = MySQLdb.Connect(host=hostname, user=dbuser, passwd=dbpwd, db=dbname)
	cursor = conn.cursor()
	result = cursor.execute(sql)
	conn.commit()
	return result

def insert_many_by_sql(sql,para):
	conn = MySQLdb.Connect(host=hostname, user=dbuser, passwd=dbpwd, db=dbname)
	cursor = conn.cursor()
	result = cursor.executemany(sql,para)
	conn.commit()
	cursor.close()
	conn.close()
	return result

def insert_one_by_data(data, dbtalbe):
	return

def insert_all_by_data(data, dbtable):    
	return

if __name__ == '__main__':
#	sql = 'insert into user (name) values (%s);'
#	para = (('wang'),('ting'), ('bang'))
#	n = insert_many_by_sql(sql, para)
#	print n
	parse
