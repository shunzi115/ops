#!/usr/bin/env python
#coding=utf8

import mysql_exec,mysql_online
import woops_log
from datetime import *
import sys
#from apscheduler.schedulers.background import BackgroundScheduler

def cron_job():
	time_now_str = datetime.now().strftime("%Y-%m-%d %X")
	insert_column = ['TABLE_SCHEMA', 'TABLE_NAME', 'TABLE_ROWS', 'UpdateTime']
	select_online_sql = 'SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA != "performance_schema" AND TABLE_SCHEMA != "information_schema" AND TABLE_SCHEMA != "mysql" ORDER BY TABLE_SCHEMA;'
	select_online_result = mysql_online.general_sql(select_online_sql)
	if select_online_result['result'] != 0:
		sys.exit()

	select_online_result_list = [list(i)+[time_now_str] for i in select_online_result['msg']]
	select_online_result_dict = [dict(zip(insert_column,i)) for i in select_online_result_list]

	time_exist = list(set([i[0] for i in mysql_exec.select_sql('online_table_rows',['UpdateTime'])]))

	if datetime.now().strftime("%Y-%m-%d") in time_exist:
		sys.exit()

	for i in select_online_result_dict:
		if i['TABLE_ROWS'] == None:
			i['TABLE_ROWS'] = 0
		mysql_exec.insert_sql('online_table_rows',insert_column,i)

cron_job()

#scheduler = BackgroundScheduler(daemonic = False)
#scheduler.add_job(cron_job,'cron',minute=59,hour=6, day='*',month='*',week='*')
#scheduler.start()
