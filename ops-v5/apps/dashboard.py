#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,session,redirect
from . import app
from common_func import session_check,role_check
from datetime import *
from utils import woops_log,mysql_exec
import json

def haha(time_str):
	fields = ['TABLE_SCHEMA','TABLE_NAME','TABLE_ROWS']
#	sql = "SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA != 'performance_schema' AND TABLE_SCHEMA != 'information_schema' ORDER BY TABLE_SCHEMA;"
	sql = "SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_ROWS FROM online_table_rows where UpdateTime like '%s';" %(time_str+'%')
	print sql
	table_row = mysql_exec.general_sql(sql)
	db_name = sorted(list(set([i[0] for i in table_row])))
	table_row_dict = [dict(zip(fields,i)) for i in table_row]
	table_row_info = {}
	for i in db_name:
		table_info = {}
		for j in table_row_dict:
			if j['TABLE_SCHEMA'] == i:
				table_rows = []
				table_rows.append(int(j['TABLE_ROWS']))
				table_info[j['TABLE_NAME']]=table_rows
		print "***** table_info *****"
		print table_info
		table_row_info[i]=table_info
	print "***** table_row_info *****"
	print table_row_info
	table_row_info_json = json.dumps(table_row_info)
	print "***** table_row_info_json *****"	
	print table_row_info_json
	return table_row_info


@app.route("/",methods=['GET','POST'])
def dashboard():
	time_today_str = datetime.now().strftime("%Y-%m-%d")
	oneday_str = timedelta(days=1)
	time_yesterday_str = (datetime.now()-oneday_str).strftime("%Y-%m-%d")
	aa = haha(time_yesterday_str)
	bb = haha(time_today_str)
	for k,v in bb.items():
		if k in aa:
			for ki,vi in v.items():
				if ki in aa[k]:
					aa[k][ki].append(vi[0])
					aa[k][ki].append(aa[k][ki][1]-aa[k][ki][0])
					if aa[k][ki][0] != 0:
						aa[k][ki].append('%.2f%%' %((aa[k][ki][2]+0.0)/aa[k][ki][0]*100))
						print type(aa[k][ki][0])
					else:
						aa[k][ki].append('100%')
				else:
					aa[k][ki].insert(0,'null')
					aa[k][ki].append('100%')
		else:
			aa[k]=v
			for kj,vj in aa[k].items():
				vj.insert(0,'null')
				vj.append(vj[1])
				vj.append('100%')

	return render_template("/dashboard.html",table_rows_result=aa)
