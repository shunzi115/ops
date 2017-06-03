#!/usr/bin/env python
#coding=utf8

import MySQLdb as mysql
import woops_conf,woops_log
import traceback
from DBUtils.PooledDB import PooledDB


mysql_conf = woops_conf.conf_read('woops.conf',section='DB_mysql')

pool = PooledDB(mysql,
		host=mysql_conf['db_host'],
		port=int(mysql_conf['db_port']),
		user=mysql_conf['db_user'],
		passwd=mysql_conf['db_password'],
		db=mysql_conf['db_database'],
		mincached=5,
		maxcached=20,
		maxshared=20,
		maxconnections=50,
		blocking=False,
		maxusage=10,
		setsession=['set autocommit = 1'],
		charset="utf8"
		)

def db_connect():
	global db,cur
	db = pool.connection()
	cur = db.cursor()

## 关闭数据库连接 ##
def close_db():
	cur.close()
        db.close()

## fields 是列表存储列名,values 是字典(列名:值) ##
def insert_sql(table,fields,values):
	insert_sql = "insert into %s (%s) values(%s);" %(table,','.join(fields),','.join(['"%s"' % values[x] for x in fields]))
	woops_log.log_write('DB_mysql').debug('insert_sql : "%s"' % insert_sql)
	try:
		db_connect()
		cur.execute(insert_sql)
	except:
		woops_log.log_write('DB_mysql').error('insert_sql : "%s",error: %s' %(insert_sql,traceback.format_exc()))
	finally:
		close_db()

## values 和 condition 都是字典 ##
def update_sql(table,values,condition):
	update_sql = "update %s set %s where %s;" %(table,','.join(["%s='%s'" % (i,j) for i,j in values.items()]),' AND '.join(["%s='%s'" % (i,j) for i,j in condition.items()]))
	woops_log.log_write('DB_mysql').debug('update_sql : "%s"' % update_sql)
	try:
		db_connect()
                cur.execute(update_sql)
        except:
                woops_log.log_write('DB_mysql').error('update_sql : "%s",error: %s' %(update_sql,traceback.format_exc()))
        finally:
                close_db()

## condition 是字典 ##
def delete_sql(table,condition):
	delete_sql = "delete from %s where %s;" %(table,' AND '.join(["%s='%s'" % (i,j) for i,j in condition.items()]))
	woops_log.log_write('DB_mysql').debug('delete_sql : "%s"' % delete_sql)
	try:
		db_connect()
                cur.execute(delete_sql)
        except:
                woops_log.log_write('DB_mysql').error('delete_sql : "%s",error: %s' %(delete_sql,traceback.format_exc()))
        finally:
                close_db()


## condition 是字典 ##
def select_sql(table,fields,condition=None):
	if condition:
		select_sql = "select %s from %s where %s;" %(','.join(fields),table,' AND '.join(['%s="%s"' % (i,j) for i,j in condition.items()]))
	else:
		select_sql = "select %s from %s ;" %(','.join(fields),table)
	woops_log.log_write('DB_mysql').debug('select_sql : "%s"' % select_sql)
	try:
		db_connect()
		cur.execute(select_sql)
		select_all = cur.fetchall()
		return select_all
	except:
                woops_log.log_write('DB_mysql').error('select_sql : "%s",error: %s' %(select_sql,traceback.format_exc()))
        finally:
                close_db()
