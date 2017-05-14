#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,session,redirect
from . import app
import mysql_init
from datetime import *
import json


@app.route("/cmdb/server_list",methods=['GET'])
def server_list():
	fields_1 = ['id','HostName','PrivateIP','PublicIP','ENV','ServerBrand','ServerModel','OS','Kernel']
	fields_2 = ['CpuType','CpuCount','RAM_GB','PhyDiskSize','IDC','status','OnlineTime','OfflineTime']
	fields = fields_1 + fields_2	
	print "**** fields ****"
	print fields
	server_list = mysql_init.select_sql('serverinfo',fields)
	print "***** server_list *****"
        print server_list
	server_list_list = [dict(zip(fields,i)) for i in server_list]
	print "***** server_list_list *****"
        print server_list_list
	return render_template("server_list.html",server_list=server_list_list)

@app.route("/cmdb/server_add",methods=['GET','POST'])
def server_add():
	if request.method == 'GET':
		return render_template("server_add.html")
	if request.method == 'POST':
		server_add_dict = dict((i,j[0]) for i,j in dict(request.form).items())
		if not server_add_dict['HostName'].strip() or not server_add_dict['ENV'].strip() or not server_add_dict['PrivateIP']:
			msg = "input not null"
			return json.dumps({'result':1,'msg':msg})
		if not server_add_dict['OS'] or not server_add_dict['Kernel'] or not server_add_dict['CpuType']:
			msg = "input not null"
			return json.dumps({'result':1,'msg':msg})
		if not server_add_dict['CpuCount'] or not server_add_dict['RAM_GB'] or not server_add_dict['PhyDiskSize'] or not server_add_dict['IDC']:
			msg = "input not null"
			return json.dumps({'result':1,'msg':msg})
		server_add_dict['OnlineTime'] = datetime.now().strftime("%Y-%m-%d %X")
		print "**** server_add_dict ****"
		print server_add_dict
		insert_fields = [x for x in server_add_dict.keys()]
		mysql_init.insert_sql('serverinfo',insert_fields,server_add_dict)
		return json.dumps({'result':0,'msg':'ok'})
