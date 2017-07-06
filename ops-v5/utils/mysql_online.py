#!/usr/bin/env python
#coding=utf8

import MySQLdb as mysql
from DBUtils.PooledDB import PooledDB
import traceback
import woops_log

pool = PooledDB(mysql,
	host='rm-bp10bh7gc24147f4y.mysql.rds.aliyuncs.com',
	port=3306,
	user='watsons_watch',
	passwd='hhKOm5AgdYYv6x62XHOF',
	db='information_schema',
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

## 通用SQL ##=
def general_sql(sql_str):
        general_sql_str = sql_str 
        try:
                db_connect()
                cur.execute(general_sql_str)
                general_fetch_all = cur.fetchall()
                return {'result':0,'msg':general_fetch_all}
        except:
		woops_log.log_write('DB_mysql').error('general_sql_str : "%s",error: %s' %(general_sql_str,traceback.format_exc()))
                return {'result':1,'msg':'mysql operation faild,please check log'}
        finally:
                close_db()

