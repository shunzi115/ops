#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,session,redirect
from . import app
import mysql_init

@app.route("/cmdb/server_list",methods=['GET'])
def server_list():
	fields = ['id','HostName','PrivateIP','PublicIP','ENV','ServerBrand','ServerModel','OS','Kernel','CpuType','CpuCount','RAM_GB','PhyDiskSize','IDC','status','OnlineTime','OfflineTime']	
	server_list = mysql_init.select_sql('serverinfo',fields)
	print "***** server_list *****"
        print server_list
	server_list_dict = dict(zip(fields,i) for i in server_list)
	return render_template("server_list.html",server_list=server_list_dict)

@app.route("/cmdb/server_add",methods=['GET','POST'])
def server_add():
	if request.method == 'GET':
		return render_template("server_add.html")
'''
	if request.method == 'POST':
'''		
