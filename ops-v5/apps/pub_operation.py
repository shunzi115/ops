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
		select_condition = {}
		select_condition['app_name'] = request.args.get('pub_app_name')
		select_version_condition = request.args.get('opera_type')
        	select_ips_list = list(mysql_exec.select_sql('cmdb_online',ip_fields,select_condition)[0])
        	if not select_ips_list:
			woops_log.log_write('pub_opera').error('The module %s has NO IP' % select_condition['app_name'])
			return json.dumps({'result':1,'msg':'The module has no IP'})		
		select_ips=select_ips_list[0].split('<br>')
		woops_log.log_write('pub_opera').debug('select_ips: %s' % select_ips)
		sql_str = 'select pub_app_version from pub_version_status where pub_app_name="%s" ' %(select_condition['app_name'])
		if select_version_condition == 'publish':	
			select_version_sql = sql_str + 'and pub_app_version_status in ("packaged","publishing") order by package_time DESC limit 5;'
		else:
			select_version_sql = sql_str + 'and pub_app_version_status in ("used","rollbacking") order by pub_time DESC limit 10;'
		select_version_list = [i[0] for i in mysql_exec.general_sql(select_version_sql)]
		if not select_version_list:
                        woops_log.log_write('pub_opera').error('The module %s has not select its version' % select_condition['app_name'])
                        return json.dumps({'result':1,'msg':'The module has not select version'})
                woops_log.log_write('pub_opera').debug('select_version: %s' % select_version_list)
		return json.dumps({'result':0,'msg_ip':select_ips,'msg_version':select_version_list})
                
@app.route("/pub/opera_shell",methods=['GET','POST'])
@session_check
def pub_opera_shell():
	shell_dir = os.path.dirname(os.path.realpath(__file__)) + '/../scripts/'
	history_dir = os.path.dirname(os.path.realpath(__file__)) + '/../history/'
	if request.method == 'GET':
		file_name_get = request.args.get('file_name_get')
		history_file = history_dir + file_name_get
		with open(history_file,'r') as f1:
			lines_str = "".join(f1.read())
			return json.dumps({'msg':conv.convert(lines_str)})
	if request.method == 'POST':
		opera_shell_args = dict((i,j[0]) for i,j in dict(request.form).items())
		if opera_shell_args['opera_type'] == 'no_select' or opera_shell_args['pub_app_name'] == 'no_select':
			woops_log.log_write('pub_opera').error('The "opera_type" and "pub_app_name" part of the selector must select one')
			return json.dumps({'result':1,'msg':'The * symbol part of the selector must select one'})
		if opera_shell_args['pub_app_version'] == 'no_select' or opera_shell_args['pub_app_addr'] == 'no_select':
			woops_log.log_write('pub_opera').error('The "pub_app_version" and "pub_app_addr" part of the selector must select one')
			return json.dumps({'result':1,'msg':'The * symbol part of the selector must select one'})
		pub_time = datetime.now().strftime("%Y-%m-%d %X")
		file_name_3 = datetime.strptime(pub_time,"%Y-%m-%d %X").strftime("%Y%m%d%H%M%S")
		file_name_1 = opera_shell_args['pub_app_version'].split('.')[0]
		file_name_2 = opera_shell_args['pub_app_addr']
		file_name = file_name_1 + file_name_2 + file_name_2 + '.txt'
		shell_file_dir = shell_dir + 'pub.sh'
		pub_command = '%s %s %s %s' %(shell_file_dir,opera_shell_args['pub_app_name'],opera_shell_args['pub_app_addr'],opera_shell_args['pub_app_version'])
		print "***** pub_command *****"
		print pub_command
		woops_log.log_write('pub_opera').debug('pub command: %s' % pub_command)
		history_dir_file = history_dir + file_name
		try:
			with open(history_dir_file,'a+') as f_history:
				shell_subprocess = subprocess.Popen(pub_command,shell=True,stdout=f_history,stderr=f_history)
				return json.dumps({'result':0,'msg':"正在执行发布脚本,稍后打印执行过程......",'history_file_name':file_name})
		except:
#			woops_log.log_write('pub_opera').error('%s : "%s"' %(shell_subprocess,traceback.format_exc()))
			return json.dumps({'result':1,'msg':'The shell subprocess exec failed,please check log'})
