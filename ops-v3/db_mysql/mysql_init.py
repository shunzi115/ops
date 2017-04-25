#!/usr/bin/env python
#coding=utf8

import MySQLdb as mysql
db = mysql.connect(host='127.0.0.1',user='root',passwd='Abcd1234!',db='dev_ops',charset='utf8')
cur = db.cursor()

## fields 是列表存储列名,values 是字典(列名:值) ##
def insert_sql(table,fields,values):
	insert_sql = "insert into %s (%s) values(%s);" %(table,','.join(fields),','.join(['"%s"' % values[x] for x in fields]))
	print "**** insert_sql ****"
	print "insert_sql: %s" %(insert_sql)
	cur.execute(insert_sql)
	db.commit()

## values 和 condition 都是字典 ##
def update_sql(table,values,condition):
	update_sql = "update %s set %s where %s;" %(table,','.join(["%s='%s'" % (i,j) for i,j in values.items()]),' AND '.join(["%s='%s'" % (i,j) for i,j in condition.items()]))
	print "**** update_sql ****"
	print "update_sql: %s" %(update_sql)
	cur.execute(update_sql)
	db.commit()

## condition 是字典 ##
def delete_sql(table,condition):
	delete_sql = "delete from %s where %s;" %(table,' AND '.join(["%s='%s'" % (i,j) for i,j in condition.items()]))
	print "**** delete_sql ****"
	print "delete_sql: %s" %(delete_sql)
	cur.execute(delete_sql)
	db.commit()

## condition 是字典 ##
def select_sql(table,fields,condition=None):
	if condition:
		select_sql = "select %s from %s where %s;" %(','.join(fields),table,' AND '.join(['%s="%s"' % (i,j) for i,j in condition.items()]))
	else:
		select_sql = "select %s from %s ;" %(','.join(fields),table)
	print "**** select_sql ****"
	print "select_sql: %s" %(select_sql)
	cur.execute(select_sql)
	select_all = cur.fetchall()
	return select_all
