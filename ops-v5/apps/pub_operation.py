#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,redirect,session
from . import app
from common_func import session_check,role_check,online_app_list
from datetime import *
import json,os,traceback
from utils import woops_log,mysql_exec
import subprocess
from ansi2html import Ansi2HTMLConverter
import sys

reload(sys)
sys.setdefaultencoding('utf8')

conv = Ansi2HTMLConverter()

@app.route("/pub/operation",methods=['GET','POST'])
@session_check
def pub_opera():
	online_apps = online_app_list()
	return render_template("/pub/pub_opera.html",online_apps=online_apps)

@app.route("/get/apps_ip_version",methods=['GET'])
@session_check
def apps_ip_version():
	if request.method == 'GET':
		ip_fields = ['app_ip']
		version_fields = ['pub_app_version']
		select_version_condition = request.args.get('opera_type')
		sql_str = 'select pub_app_version,pub_app_addr from pub_version_status where pub_app_name="%s" ' %(request.args.get('pub_app_name'))
		if select_version_condition == 'publish':	
			select_version_sql = sql_str + 'and pub_app_version_status in ("packaged","publishing") order by id DESC limit 5;'
			select_condition = {}
			select_condition['app_name'] = request.args.get('pub_app_name')
        		select_ips_list = list(mysql_exec.select_sql('cmdb_online',ip_fields,select_condition)[0])
        		if not select_ips_list:
				woops_log.log_write('pub_opera').error('The module %s has NO IP' % select_condition['app_name'])
				return json.dumps({'result':1,'msg':'The module has no IP'})		
			select_ips=select_ips_list[0].split('<br>')
		else:
			select_version_sql = sql_str + 'and pub_app_version_status in ("used","rollbacking") order by id DESC limit 10;'
			select_ips_sql = sql_str + 'and pub_app_version_status in ("using","publishing") order by id DESC limit 1'
			select_ips_tuple = mysql_exec.general_sql(select_ips_sql)[0]
			select_ips = select_ips_tuple[1].split(';')

		select_version_list = [i[0] for i in mysql_exec.general_sql(select_version_sql)]
		if not select_version_list:
                        woops_log.log_write('pub_opera').error('The module %s has not select its version' % select_condition['app_name'])
                        return json.dumps({'result':1,'msg':'The module has not select version'})
                woops_log.log_write('pub_opera').debug('select_version: %s' % select_version_list)
		woops_log.log_write('pub_opera').debug('select_ips: %s' % select_ips)
		return json.dumps({'result':0,'msg_ip':select_ips,'msg_version':select_version_list})
                
@app.route("/pub/opera_shell",methods=['GET','POST'])
@session_check
def pub_opera_shell():
	shell_dir = os.path.dirname(os.path.realpath(__file__)) + '/../scripts/'
	history_dir = os.path.dirname(os.path.realpath(__file__)) + '/../history/'
	if request.method == 'GET':
		file_name_get = request.args.get('file_name_get')
		history_file = history_dir + file_name_get
		shell_pid_str = request.args.get('shell_pid_str')
		history_id_str = request.args.get('history_id_str')
		with open(history_file,'r') as f1:
			lines_str = "".join(f1.read())
		process_filter_str = 'ps -p %s' %(shell_pid_str)
		shell_returncode = subprocess.call(process_filter_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		print " %s ".center(100,"*") %("shell_returncode")
		print shell_returncode
		history_end_status = {}
		if shell_returncode != 0:
			if '_*_ERROR_*_:' not in lines_str:
				history_end_status['app_opera_status'] = 'Success'
			else:
				history_end_status['app_opera_status'] = 'Fail'
			history_end_status['opera_end_time'] = datetime.now().strftime("%Y-%m-%d %X")
			mysql_exec.update_sql('pub_history_detail',history_end_status,{'id':history_id_str})
		return json.dumps({'shell_returncode':shell_returncode,'msg':conv.convert(lines_str)})
	if request.method == 'POST':
		opera_shell_args = dict((i,j[0]) for i,j in dict(request.form).items())
		if opera_shell_args['opera_type'] == 'no_select' or opera_shell_args['pub_app_name'] == 'no_select':
			woops_log.log_write('pub_opera').error('The "opera_type" and "pub_app_name" part of the selector must select one')
			return json.dumps({'result':1,'msg':'The * symbol part of the selector must select one'})
		if opera_shell_args['pub_app_version'] == 'no_select' or opera_shell_args['pub_app_addr'] == 'no_select':
			woops_log.log_write('pub_opera').error('The "pub_app_version" and "pub_app_addr" part of the selector must select one')
			return json.dumps({'result':1,'msg':'The * symbol part of the selector must select one'})
		pub_already_ip_select = dict((k,v) for k,v in opera_shell_args.items() if k == 'pub_app_name' or k == 'pub_app_version')
		pub_already = mysql_exec.select_sql('pub_version_status',['pub_app_addr'],pub_already_ip_select)[0][0]
		if pub_already:
			pub_already_ips = pub_already.split(';')
		else:
			pub_already_ips = []
		print " %s ".center(100,"*") %("pub_already_ips")
		print pub_already_ips
		file_name_1 = opera_shell_args['pub_app_version'].split('.')[0]
		file_name_2 = opera_shell_args['pub_app_addr']
		pub_status_update = {}
		opera_history_detail = {}
		opera_history_detail['app_name_detail'] = opera_shell_args['pub_app_name']
		opera_history_detail['app_version_detail'] = opera_shell_args['pub_app_version']
		opera_history_detail['app_opera_type'] = opera_shell_args['opera_type']
		opera_history_detail['app_ip_detail'] = opera_shell_args['pub_app_addr']
		opera_history_detail['opera_start_time'] = datetime.now().strftime("%Y-%m-%d %X")
		file_name_3 = datetime.strptime(opera_history_detail['opera_start_time'],"%Y-%m-%d %X").strftime("%Y%m%d%H%M%S")
		current_version_sql_str = 'select pub_app_name,pub_app_version,pub_app_addr from pub_version_status where pub_app_name="%s"' %(opera_shell_args['pub_app_name'])
		if opera_shell_args['opera_type'] == 'publish':
			current_version_select_sql = current_version_sql_str + ' and pub_app_version_status in ("publishing","using") order by id DESC limit 1;'
		else:
			current_version_select_sql = current_version_sql_str + ' and pub_app_version_status in ("rollbacking","using","publishing") order by id DESC limit 1;'
		app_current_using_select = mysql_exec.general_sql(current_version_select_sql)
		print " %s ".center(100,"*") %("app_current_using_select")
		print app_current_using_select
		if app_current_using_select:
			app_current_using = dict(zip(('pub_app_name','pub_app_version','pub_app_addr'),app_current_using_select[0]))
			print " %s ".center(100,"*") %("app_current_using")
			print app_current_using
			status_update_condition = {'pub_app_name':opera_shell_args['pub_app_name'],'pub_app_version':app_current_using['pub_app_version']}
		else:
			status_update_condition = {}
		pre_version_status = {}
		update_pre_version_condition = {}

		if opera_shell_args['opera_type'] == 'publish':
			app_ips_list = mysql_exec.select_sql('cmdb_online',['app_ip'],{'app_name':opera_shell_args['pub_app_name']})[0][0].split('<br>')
			print " %s ".center(100,"*") %("status_update_condition")
			print status_update_condition
			print pub_already_ips
			if status_update_condition and not pub_already_ips:
				pre_version_ips = app_current_using['pub_app_addr'].split(';')
				if len(pre_version_ips) != len(app_ips_list):
					pre_version_status['pub_app_version_status'] = 'part_used'
				else:
					pre_version_status['pub_app_version_status'] = 'used'	
				update_pre_version_condition = status_update_condition

			if opera_shell_args['pub_app_addr'] in pub_already_ips:
				woops_log.log_write('pub_opera').error('The IP %s and version %s already Published' % (opera_shell_args['pub_app_addr'],opera_shell_args['pub_app_version']))
				return json.dumps({'result':1,'msg':'The IP and version had already Published'})

			file_name = 'publish_' + file_name_1 + '_' + file_name_2 + '_' + file_name_3 + '.txt'
			shell_file_dir = shell_dir + 'pub.sh'
			pub_already_ips.append(opera_shell_args['pub_app_addr'])
			if len(pub_already_ips) != len(app_ips_list):
				pub_status_update['pub_app_version_status'] = 'publishing'
			else:
				pub_status_update['pub_app_version_status'] = 'using'
			pub_status_update['pub_app_addr'] = ';'.join(pub_already_ips)
			pub_status_update_condition = pub_already_ip_select
			opera_history_detail['app_opera_status'] = 'publishing'

		elif opera_shell_args['opera_type'] == 'rollback':
			file_name = 'rollback_' + file_name_1 + '_' + file_name_2 + '_' + file_name_3 + '.txt'
                        shell_file_dir = shell_dir + 'rollback.sh'
			rollback_already = mysql_exec.select_sql('pub_version_status',['rollback_addr'],status_update_condition)[0][0]
			print " %s ".center(100,"*") %("rollback_already")
			print rollback_already
                	if rollback_already:
                        	rollback_already_ips = rollback_already.split(';')
                	else:
                        	rollback_already_ips = []

			if not rollback_already_ips:
				pre_version_status['pub_app_version_status'] = 'using'
				update_pre_version_condition = {'pub_app_name':opera_shell_args['pub_app_name'],'pub_app_version':opera_shell_args['pub_app_version']}

			if opera_shell_args['pub_app_addr'] in rollback_already_ips:
                                woops_log.log_write('pub_opera').error('The IP %s and version %s already rollbackd' % (opera_shell_args['pub_app_addr'],opera_shell_args['pub_app_version']))
                                return json.dumps({'result':1,'msg':'The IP and version had already Rollbackd'})
			rollback_already_ips.append(opera_shell_args['pub_app_addr'])
			app_current_using_ips=app_current_using['pub_app_addr'].split(';')
			print " %s ".center(100,"*") %("app_current_using_ips")
			print app_current_using_ips
			if len(rollback_already_ips) != len(app_current_using_ips):
                                pub_status_update['pub_app_version_status'] = 'rollbacking'
                        else:
                                pub_status_update['pub_app_version_status'] = 'rollbacked'
                        pub_status_update['rollback_addr'] = ';'.join(rollback_already_ips)
			pub_status_update['rollback_to_version'] = opera_shell_args['pub_app_version']
			pub_status_update_condition = status_update_condition
			opera_history_detail['app_opera_status'] = 'rollbacking'

		pub_command = '%s %s %s %s' %(shell_file_dir,opera_shell_args['pub_app_name'],opera_shell_args['pub_app_addr'],opera_shell_args['pub_app_version'])
		woops_log.log_write('pub_opera').debug('pub command: %s' % pub_command)
		history_dir_file = history_dir + file_name
		opera_history_detail['app_opera_detail'] = history_dir_file
		try:
			with open(history_dir_file,'a+') as f_history:
				shell_subprocess = subprocess.Popen(pub_command,shell=True,stdout=f_history,stderr=f_history)
				shell_pid = shell_subprocess.pid
		except:
			return json.dumps({'result':1,'msg':'The shell subprocess exec failed,please check log'})
		print " %s ".center(100,"*") %("update_pre_version_condition")
		print update_pre_version_condition
		if update_pre_version_condition:	
			mysql_exec.update_sql('pub_version_status',pre_version_status,update_pre_version_condition)
		mysql_exec.update_sql('pub_version_status',pub_status_update,pub_status_update_condition)
		mysql_exec.insert_sql('pub_history_detail',[k for k,v in opera_history_detail.items()],opera_history_detail)
		del opera_history_detail['app_opera_status']
		del opera_history_detail['app_opera_detail']
		del opera_history_detail['opera_start_time']
		history_id = mysql_exec.select_sql('pub_history_detail',['id'],opera_history_detail)[0][0]
		print " %s ".center(100,"*") %("history_id")
		print history_id
		return json.dumps({'result':0,'msg':"正在执行发布脚本,稍后打印执行过程......",'history_file_name':file_name,'shell_pid':shell_pid,'history_id':history_id})

@app.route("/pub/history",methods=['GET','POST'])
@session_check
def history_list():
	if request.method == 'GET':
		fields_1 = ['id','app_name_detail','app_version_detail','app_opera_type','app_ip_detail']
                fields_2 = ['app_opera_detail','app_opera_status','opera_start_time','opera_end_time']
                fields = fields_1 + fields_2
		oneday_str = timedelta(days=30)
		time_30days_ago = (datetime.now()-oneday_str).strftime("%Y-%m-%d %X")
		history_sql_str = 'select %s from pub_history_detail where opera_start_time >= "%s" order by id DESC;' %(','.join(fields),time_30days_ago) 
                history_list = mysql_exec.general_sql(history_sql_str)
                history_list_dict = [dict(zip(fields,i)) for i in history_list]
                return render_template("/pub/pub_history_list.html",history_list_dict=history_list_dict)
	
	if request.method == 'POST':
		history_file_name = request.form.get('id',None)
		if not history_file_name or not os.path.exists(history_file_name):
			return json.dumps({'result':1,'msg':'The history file is not exist'})
		with open(history_file_name,'r') as f2:
                        history_strs = "".join(f2.read())
		return json.dumps({'result':0,'msg':conv.convert(history_strs)})
		
