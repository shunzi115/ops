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
		table_row_info[i]=table_info
	return table_row_info


@app.route("/",methods=['GET','POST'])
@session_check
def dashboard():
	time_today_str = datetime.now().strftime("%Y-%m-%d")
	oneday_str = timedelta(days=1)
	time_yesterday_str = (datetime.now()-oneday_str).strftime("%Y-%m-%d")
	aa = haha(time_yesterday_str)
	bb = haha(time_today_str)

	### aa 和 bb 是{库1:{表1:行数1,表2:行数2,表3:行数3},库2:{表1:行数1,表2:行数2,表3:行数3}}; k 是 库名，v 是{表名:行数};ki 是表名,vi 是表对应的行数

	for k,v in bb.items():
		if k in aa:
			for ki,vi in v.items():
				if ki in aa[k]:
					aa[k][ki].append(vi[0])
					aa[k][ki].append(aa[k][ki][1]-aa[k][ki][0])
					if aa[k][ki][0] != 0:
						aa[k][ki].append('%.2f%%' %((aa[k][ki][2]+0.0)/aa[k][ki][0]*100))
					elif aa[k][ki][0] == 0 and aa[k][ki][1] == 0:
						aa[k][ki].append('0.00%')
					else:
						aa[k][ki].append('100.00%')
				else:
					aa[k][ki] = []
					aa[k][ki].insert(0,0)
					aa[k][ki].insert(1,vi[0])
					aa[k][ki].insert(2,vi[0])
					if aa[k][ki][2] == 0:
						aa[k][ki].append('0.00%')
					else:
						aa[k][ki].append('100.00%')
		else:
			aa[k]=v
			for kj,vj in aa[k].items():
				vj.insert(0,0)
				vj.append(vj[1])
				if vj[2] == 0:
					vj.append('0.00%')
				else:
					vj.append('100.00%')

	return render_template("/dashboard.html",time_1=time_yesterday_str,time_2=time_today_str,table_rows_result=aa)
