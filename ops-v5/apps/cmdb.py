#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,session,redirect
from . import app,session_check,role_check
import mysql_init
from datetime import *
import json

@app.route("/cmdb/server_add",methods=['GET','POST'])
@session_check
@role_check
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

def app_ip_detail(mysql_table):
	app_ip_fields = ['app_ip']
	app_ip_select = mysql_init.select_sql('%s' %(mysql_table),app_ip_fields)
	if app_ip_select:
		app_ip_list_pre = [i[0].split(' ; ') for i in app_ip_select]
		app_ip_list = []
		for i in app_ip_list_pre:
			app_ip_list = app_ip_list + i
		app_ip_list = list(set(app_ip_list))
		print "**** app_ip_list ****"
		print app_ip_list
		return app_ip_list

@app.route("/cmdb/server_update",methods=['GET','POST'])
@session_check
def server_update():
	if request.method == 'GET':
		select_condition = {}
		select_condition['id'] = request.args.get('id')
		print "**** server_select_condition ***"
                print select_condition
		fields_1 = ['id','HostName','PrivateIP','PublicIP','ENV','ServerBrand','ServerModel','OS','Kernel']
		fields_2 = ['CpuType','CpuCount','RAM_GB','PhyDiskSize','IDC','status','OnlineTime','OfflineTime']
		fields = fields_1 + fields_2	
		server_info = mysql_init.select_sql('serverinfo',fields,select_condition)
		server_info_dict = [dict(zip(fields,i)) for i in server_info][0]
		print "**** server_info_dict ***"
		print server_info_dict
		return json.dumps(server_info_dict)
	if request.method == 'POST':
                server_update_dict = dict((i,j[0]) for i,j in dict(request.form).items())
                if not server_update_dict['HostName'].strip() or not server_update_dict['ENV'].strip() or not server_update_dict['OS']:
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
                if  not server_update_dict['Kernel'] or not server_update_dict['CpuType'] or not server_update_dict['CpuCount']:
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
                if not server_update_dict['RAM_GB'] or not server_update_dict['PhyDiskSize'] or not server_update_dict['IDC']:
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
		if server_update_dict['status'] == '1' or server_update_dict['IDC'] != 'online':
			app_ip_list = app_ip_detail('cmdb_online')
			if server_update_dict['PrivateIP'] in app_ip_list:
				return json.dumps({'result':1,'msg':'ip is in cmdb_online ; please delete if from cmdb first!'})
			
		update_conditions = {}
		update_conditions['id'] = server_update_dict['id'].strip('')
		update_conditions['PrivateIP'] = server_update_dict['PrivateIP'].strip('')
		if server_update_dict['status'].strip('') == '1':
			server_update_dict['OfflineTime'] = datetime.now().strftime("%Y-%m-%d %X")
		else:
			server_update_dict['OfflineTime'] = ''
                print "**** server_update_dict ****"
                print server_update_dict
		del server_update_dict['id']
		del server_update_dict['PrivateIP']
                mysql_init.update_sql('serverinfo',server_update_dict,update_conditions)
                return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/server_list",methods=['GET'])
@session_check
def server_list():
	fields_1 = ['id','HostName','PrivateIP','PublicIP','ENV','OS','Kernel']
	fields_2 = ['CpuCount','RAM_GB','PhyDiskSize','IDC','status']
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

@app.route("/cmdb/server_delete",methods=["GET"])
@session_check
def server_delete():
	delete_condition = {}
	delete_condition['id'] = request.args.get('id')
	mysql_init.delete_sql('serverinfo',delete_condition)
	return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/cmdb_online_add",methods=['GET','POST'])
@session_check
@role_check
def cmdb_online_add():
        if request.method == 'GET':
		fields = ['PrivateIP']
		ip_list_condition = {}
                ip_list_condition['ENV'] = 'online'
                ip_list_condition['status'] = 0
		server_ip_list = [dict(zip(fields,i)) for i in mysql_init.select_sql('serverinfo',fields,ip_list_condition)]
		print '**** select_PrivateIP_list ****'
		print server_ip_list
		return render_template("cmdb_online_add.html",server_ip_info=server_ip_list)
        if request.method == 'POST':
		print "**** cmdb_online_add_request.form ****"
		print request.form
		print dict(request.form)
		cmdb_add_dict = dict((i,' ; '.join(j)) for i,j in dict(request.form).items())
                if not cmdb_add_dict['app_name'].strip() or not cmdb_add_dict['app_ip'].strip():
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
                if not cmdb_add_dict['app_path'] or not cmdb_add_dict['app_shell'] or not cmdb_add_dict['status']:
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
                cmdb_add_dict['online_time'] = datetime.now().strftime("%Y-%m-%d %X")
                print "**** cmdb_online_add_dict ****"
                print cmdb_add_dict
                insert_fields = [x for x in cmdb_add_dict.keys()]
                mysql_init.insert_sql('cmdb_online',insert_fields,cmdb_add_dict)
                return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/cmdb_online_update",methods=['GET','POST'])
@session_check
def cmdb_online_update():
        if request.method == 'GET':
                select_condition = {}
                select_condition['id'] = request.args.get('id')
                print "**** cmdb_online_select_condition ***"
                print select_condition
		fields_1 = ['id','app_name','app_ip','app_describe','app_way','domain','cdn_domain']
        	fields_2 = ['app_path','app_shell','app_log','app_ports','status','online_time','offline_time']
                fields = fields_1 + fields_2
		ip_list_fields = ['PrivateIP']
		ip_list_condition = {}
		ip_list_condition['ENV'] = 'online'
		ip_list_condition['status'] = 0
                server_ip_list = [i[0] for i in mysql_init.select_sql('serverinfo',ip_list_fields,ip_list_condition)]
                cmdb_info = mysql_init.select_sql('cmdb_online',fields,select_condition)
                cmdb_info_dict = [dict(zip(fields,i)) for i in cmdb_info][0]
		server_ip_select_list = cmdb_info_dict['app_ip'].split(' ; ')
		del cmdb_info_dict['app_ip']
                print "**** cmdb_online_update_server_ip_list ***"
                print server_ip_list
                print "**** cmdb_online_update_server_ip_select_list ***"
                print server_ip_select_list
                print "**** cmdb_online_info_dict ***"
                print cmdb_info_dict
                return json.dumps({'cmdb_info':cmdb_info_dict,'server_ip_list':server_ip_list,'server_ip_select':server_ip_select_list})
        if request.method == 'POST':
                cmdb_update_dict = dict((i,' ; '.join(j)) for i,j in dict(request.form).items())
		if not cmdb_update_dict['app_name'].strip() or not cmdb_update_dict['app_ip'].strip():
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
                if not cmdb_update_dict['app_path'] or not cmdb_update_dict['app_shell'] or not cmdb_update_dict['status']:
                        msg = "input not null"
                        return json.dumps({'result':1,'msg':msg})
                print "**** cmdb_online_update_dict ****"
                print cmdb_update_dict
		if cmdb_update_dict['status'].strip('') == '1':
                        cmdb_update_dict['offline_time'] = datetime.now().strftime("%Y-%m-%d %X")
                else:
                        cmdb_update_dict['offline_time'] = ''
                update_conditions = {}
                update_conditions['id'] = cmdb_update_dict['id'].strip('')
                update_conditions['app_name'] = cmdb_update_dict['app_name'].strip('')
                del cmdb_update_dict['id']
                del cmdb_update_dict['app_name']
                mysql_init.update_sql('cmdb_online',cmdb_update_dict,update_conditions)
                return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/cmdb_online_list",methods=['GET','POST'])
@session_check
def cmdb_online_list():
	fields_1 = ['id','app_name','app_ip','app_describe','app_way','domain','cdn_domain']
	fields_2 = ['app_path','app_shell','app_log','app_ports','status']
	fields = fields_1 + fields_2
        print "**** cmdb_online_fields ****"
        print fields
        cmdb_online = mysql_init.select_sql('cmdb_online',fields)
        print "***** cmdb_online *****"
        print cmdb_online
        cmdb_online_list = [dict(zip(fields,i)) for i in cmdb_online]
        print "***** cmdb_online_list *****"
        print cmdb_online_list
	return render_template("cmdb_online_list.html",cmdb_online_list=cmdb_online_list)

@app.route("/cmdb/cmdb_online_delete",methods=["GET"])
@session_check
def cmdb_online_delete():
        delete_condition = {}
        delete_condition['id'] = request.args.get('id')
        mysql_init.delete_sql('cmdb_online',delete_condition)
        return json.dumps({'result':0,'msg':'ok'})
