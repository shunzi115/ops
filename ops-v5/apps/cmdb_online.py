#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,session,redirect
from . import app
from common_func import session_check,role_check,online_app_list
from datetime import *
import json
from utils import woops_log,mysql_exec

apps=[i['app_name'] for i in online_app_list()]

@app.route("/cmdb/cmdb_online_add",methods=['GET','POST'])
@session_check
@role_check
def cmdb_online_add():
        if request.method == 'GET':
                fields = ['PrivateIP']
                ip_list_condition = {}
                ip_list_condition['ENV'] = 'online'
                ip_list_condition['status'] = 0
                server_ip_list = [dict(zip(fields,i)) for i in mysql_exec.select_sql('serverinfo',fields,ip_list_condition)]
                woops_log.log_write('cmdb_online').debug('server_ip_list: %s' % server_ip_list)
                return render_template("cmdb_online_add.html",server_ip_info=server_ip_list)
        if request.method == 'POST':
                cmdb_add_dict = dict((i,'<br>'.join(j)) for i,j in dict(request.form).items())
		print "**** cmdb_add_dict *****"
		print cmdb_add_dict
                if not cmdb_add_dict['app_name'].strip() or not cmdb_add_dict.get('app_ip',None):
                        woops_log.log_write('cmdb_online').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
                if not cmdb_add_dict['app_path'] or not cmdb_add_dict['app_shell'] or not cmdb_add_dict['status']:
                        woops_log.log_write('cmdb_online').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
		if cmdb_add_dict['app_name'].strip() in apps:
			woops_log.log_write('server').error('APP "%s" already exists' % cmdb_add_dict['app_name'])
                        return json.dumps({'result':1,'msg':'APP already exists'})
                cmdb_add_dict['online_time'] = datetime.now().strftime("%Y-%m-%d %X")
                woops_log.log_write('cmdb_online').debug('cmdb_add_dict: %s' % cmdb_add_dict)
                insert_fields = [x for x in cmdb_add_dict.keys()]
                mysql_exec.insert_sql('cmdb_online',insert_fields,cmdb_add_dict)
                woops_log.log_write('cmdb_online').info('The app "%s" add successfully' % cmdb_add_dict['app_name'])
                return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/cmdb_online_update",methods=['GET','POST'])
@session_check
def cmdb_online_update():
        if request.method == 'GET':
                select_condition = {}
                select_condition['id'] = request.args.get('id')
                fields_1 = ['id','app_name','app_ip','app_describe','app_way','domain','cdn_domain']
                fields_2 = ['app_path','app_shell','app_log','app_ports','status','online_time','offline_time']
                fields = fields_1 + fields_2
                ip_list_fields = ['PrivateIP']
                ip_list_condition = {}
                ip_list_condition['ENV'] = 'online'
                ip_list_condition['status'] = 0
                server_ip_list = [i[0] for i in mysql_exec.select_sql('serverinfo',ip_list_fields,ip_list_condition)]
                cmdb_info = mysql_exec.select_sql('cmdb_online',fields,select_condition)
                cmdb_info_dict = [dict(zip(fields,i)) for i in cmdb_info][0]
                server_ip_select_list = cmdb_info_dict['app_ip'].split('<br>')
                del cmdb_info_dict['app_ip']
                woops_log.log_write('cmdb_online').debug('server_ip_list: %s' % server_ip_list)
                woops_log.log_write('cmdb_online').debug('server_ip_select_list: %s' % server_ip_select_list)
                woops_log.log_write('cmdb_online').debug('cmdb_info_dict: %s' % cmdb_info_dict)
                return json.dumps({'cmdb_info':cmdb_info_dict,'server_ip_list':server_ip_list,'server_ip_select':server_ip_select_list})
        if request.method == 'POST':
                cmdb_update_dict = dict((i,'<br>'.join(j)) for i,j in dict(request.form).items())
                if not cmdb_update_dict['app_name'].strip() or not cmdb_update_dict['app_ip'].strip():
                        woops_log.log_write('cmdb_online').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
                if not cmdb_update_dict['app_path'] or not cmdb_update_dict['app_shell'] or not cmdb_update_dict['status']:
                        woops_log.log_write('cmdb_online').error('The * symbol part of the input cannot be empty')
                        msg = "The * symbol part of the input cannot be empty"
                        return json.dumps({'result':1,'msg':msg})
                woops_log.log_write('cmdb_online').debug('cmdb_update_dict: %s' % cmdb_update_dict)
                if cmdb_update_dict['status'].strip('') == '1':
                        cmdb_update_dict['offline_time'] = datetime.now().strftime("%Y-%m-%d %X")
                else:
                        cmdb_update_dict['offline_time'] = ''
                update_conditions = {}
                update_conditions['id'] = cmdb_update_dict['id'].strip('')
                update_conditions['app_name'] = cmdb_update_dict['app_name'].strip('')
                del cmdb_update_dict['id']
                del cmdb_update_dict['app_name']
                mysql_exec.update_sql('cmdb_online',cmdb_update_dict,update_conditions)
                woops_log.log_write('cmdb_online').info('The app "%s" update successfully' % update_conditions['app_name'])
                return json.dumps({'result':0,'msg':'ok'})

@app.route("/cmdb/cmdb_online_list",methods=['GET','POST'])
@session_check
def cmdb_online_list():
        fields_1 = ['id','app_name','app_ip','app_describe','app_way','domain','cdn_domain']
        fields_2 = ['app_path','app_shell','app_log','app_ports','status']
        fields = fields_1 + fields_2
        cmdb_online = mysql_exec.select_sql('cmdb_online',fields)
        cmdb_online_list = [dict(zip(fields,i)) for i in cmdb_online]
        woops_log.log_write('cmdb_online').debug('cmdb_online_list: %s' % cmdb_online_list)
        return render_template("cmdb_online_list.html",cmdb_online_list=cmdb_online_list)

@app.route("/cmdb/cmdb_online_delete",methods=["GET"])
@session_check
def cmdb_online_delete():
        delete_condition = {}
        delete_app = {}
        delete_condition['id'] = request.args.get('id')
        delete_app = [dict(zip(['app_name'],i)) for i in mysql_exec.select_sql('cmdb_online',['app_name'],delete_condition)][0]
        mysql_exec.delete_sql('cmdb_online',delete_condition)
        woops_log.log_write('cmdb_online').info('Delete app "%s" success' % delete_app['app_name'])
        return json.dumps({'result':0,'msg':'ok'})
