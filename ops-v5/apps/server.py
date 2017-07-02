#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,session,redirect
from . import app
from common_func import session_check,role_check
from datetime import *
import json
from utils import woops_log,mysql_exec
from api.ansible_exec import ansible_exec

def server_list():
	select_fields = ['PrivateIP']
        svr_list = [x[0] for x in mysql_exec.select_sql('serverinfo',select_fields)]
        woops_log.log_write('server').debug('server_list:%s' % svr_list)
	return svr_list

@app.route("/cmdb/server_add",methods=['GET','POST'])
@session_check
@role_check
def server_add():
        if request.method == 'GET':
                return render_template("server_add.html")
        if request.method == 'POST':
                server_add_dict = dict((i,j[0]) for i,j in dict(request.form).items())
                if not server_add_dict['ENV'].strip() or not server_add_dict['PrivateIP'] or not server_add_dict['IDC']:
                        woops_log.log_write('server').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
                if not server_add_dict['SSH_port'].strip() or not server_add_dict['status']:
                        woops_log.log_write('server').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
		if server_add_dict['PrivateIP'] in server_list():
			woops_log.log_write('server').error('IP "%s" already exists' % server_add_dict['PrivateIP'])
			return json.dumps({'result':1,'msg':'IP already exists'})
                server_add_dict['OnlineTime'] = datetime.now().strftime("%Y-%m-%d %X")
                woops_log.log_write('server').debug('server_add_dict: %s' % server_add_dict)
                insert_fields = [x for x in server_add_dict.keys()]
                mysql_exec.insert_sql('serverinfo',insert_fields,server_add_dict)
                woops_log.log_write('server').info('The server "%s" added successfully' % server_add_dict['PrivateIP'])
                return json.dumps({'result':0,'msg':'ok'})

## 在修改 服务器 状态时 先查询这个 IP 是否在 cmdb 中使用,如果在使用则禁止修改该状态 ##
def app_ip_detail(mysql_table):
        app_ip_fields = ['app_ip']
        app_ip_select = mysql_exec.select_sql('%s' %(mysql_table),app_ip_fields)
        if app_ip_select:
                app_ip_list_pre = [i[0].split(' ; ') for i in app_ip_select]
                app_ip_list = []
                for i in app_ip_list_pre:
                        app_ip_list = app_ip_list + i
                app_ip_list = list(set(app_ip_list))
                woops_log.log_write('server').debug('app_ip_list: %s' % app_ip_list)
                return app_ip_list

@app.route("/cmdb/server_update",methods=['GET','POST'])
@session_check
def server_update():
        if request.method == 'GET':
                select_condition = {}
                select_condition['id'] = request.args.get('id')
                fields_1 = ['id','HostName','PrivateIP','PublicIP','ENV','ServerBrand','ServerModel','OS','Kernel','SSH_port']
                fields_2 = ['CpuType','CpuCount','RAM_GB','SWAP_size','PhyDiskSize','Part_mount','IDC','status','OnlineTime','OfflineTime']
                fields = fields_1 + fields_2
                server_info = mysql_exec.select_sql('serverinfo',fields,select_condition)
                server_info_dict = [dict(zip(fields,i)) for i in server_info][0]
                woops_log.log_write('server').debug('server_info_dict: %s' % server_info_dict)
                return json.dumps(server_info_dict)
        if request.method == 'POST':
                server_update_dict = dict((i,j[0]) for i,j in dict(request.form).items())
                if not server_update_dict['ENV'].strip() or not server_update_dict['IDC'] or not server_update_dict['SSH_port']:
                        woops_log.log_write('server').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
                if server_update_dict['status'] == '1' or server_update_dict['ENV'] != 'online':
                        app_ip_list = app_ip_detail('cmdb_online')
                        if server_update_dict['PrivateIP'] in app_ip_list:
                                woops_log.log_write('server').error('Server update failure,because of he ip has been in cmdb_online ; Please delete if from cmdb_online first!')
                                msg = 'The ip has been in cmdb_online ; Please delete if from cmdb_online first!'
                                return json.dumps({'result':1,'msg':msg})

                update_conditions = {}
                update_conditions['id'] = server_update_dict['id'].strip('')
                update_conditions['PrivateIP'] = server_update_dict['PrivateIP'].strip('')
                if server_update_dict['status'].strip('') == '1':
                        server_update_dict['OfflineTime'] = datetime.now().strftime("%Y-%m-%d %X")
                else:
                        server_update_dict['OfflineTime'] = ''
                woops_log.log_write('server').debug('server_update_dict: %s' % server_update_dict)
                del server_update_dict['id']
                del server_update_dict['PrivateIP']
                mysql_exec.update_sql('serverinfo',server_update_dict,update_conditions)
                woops_log.log_write('server').info('The server "%s" update successfully' % update_conditions['PrivateIP'])
                return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/server_list",methods=['GET','POST'])
@session_check
def server_list():
	if request.method == 'GET':
        	fields_1 = ['id','HostName','PrivateIP','PublicIP','ENV','OS','Kernel','SSH_port']
        	fields_2 = ['CpuCount','RAM_GB','SWAP_size','PhyDiskSize','Part_mount','IDC','status']
        	fields = fields_1 + fields_2
        	server_list = mysql_exec.select_sql('serverinfo',fields)
        	server_list_list = [dict(zip(fields,i)) for i in server_list]
        	woops_log.log_write('server').debug('server_list_list: %s' % server_list_list)
        	return render_template("server_list.html",server_list=server_list_list)
	if request.method == 'POST':
		res_PrivateIP = request.form.get('PrivateIP')
		res_SSH_port = request.form.get('SSH_port')
		print "**** res_PrivateIP ****"
		print res_PrivateIP
		server_info_data = ansible_exec('setup','gather_subset=hardware',res_PrivateIP)[res_PrivateIP]['ansible_facts']
		woops_log.log_write('server').info('server_info_data: %s' % server_info_data)
		print "***** server_info_data *****"
		print server_info_data
		server_refresh_info = {}
		server_refresh_info['HostName'] = server_info_data['ansible_hostname']
		server_refresh_info['OS'] = ' '.join((server_info_data['ansible_distribution'],server_info_data['ansible_distribution_version']))
		server_refresh_info['ServerBrand'] = server_info_data['ansible_system_vendor']
		server_refresh_info['ServerModel'] = server_info_data['ansible_product_name']
		server_refresh_info['Kernel'] = server_info_data['ansible_kernel']
		server_refresh_info['CpuCount'] = server_info_data['ansible_processor_vcpus']
		server_refresh_info['CpuType'] = server_info_data["ansible_processor"][1]
		server_refresh_info['RAM_GB'] = '%.2f GB' %(server_info_data['ansible_memtotal_mb']/1024.0) 
		server_refresh_info['SWAP_size'] = '%.2f GB' %(server_info_data['ansible_swaptotal_mb']/1024.0) 
		server_refresh_info['PhyDiskSize'] = '\n'.join(['['+i+']'+':'+server_info_data['ansible_devices'][i]['size'] for i in server_info_data['ansible_devices'] if 'ss' in i or 'sd' in i]) 
		server_refresh_info['Part_mount'] = '\n'.join(['['+i['mount']+']'+': %.2f GB' %(i['size_total']/1024.0/1024.0/1024.0) for i in server_info_data['ansible_mounts']])
		woops_log.log_write('server').info('server_refresh_info: %s' % server_refresh_info)
		print "***** server_refresh_info *****"
                print server_refresh_info
                refresh_condition = {}
		refresh_condition['PrivateIP'] = res_PrivateIP
		mysql_exec.update_sql('serverinfo',server_refresh_info,refresh_condition)
		return json.dumps({'result':0,'msg':'ok'})
		
@app.route("/cmdb/server_delete",methods=["GET"])
@session_check
def server_delete():
        delete_condition = {}
        delete_server = {}
        delete_condition['id'] = request.args.get('id')
        delete_server = [dict(zip(['PrivateIP'],i)) for i in mysql_exec.select_sql('serverinfo',['PrivateIP'],delete_condition)][0]
        mysql_exec.delete_sql('serverinfo',delete_condition)
        woops_log.log_write('server').info('Delete server "%s" success' % delete_server)
        return json.dumps({'result':0,'msg':'ok'})

