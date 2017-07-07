#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,redirect,session
from . import app
from common_func import session_check,role_check,online_app_list
from datetime import *
import json
from utils import woops_log,mysql_exec

@app.route("/pub/operation",methods=['GET','POST'])
def pub_opera():
	online_apps = online_app_list()
	return render_template("/pub/pub_opera.html",online_apps=online_apps)

@app.route("/get/apps_ip",methods=['GET'])
def online_apps_ip():
	fields = ['app_ip']
	module_condition = {}
	module_condition['app_name'] = request.args.get('app_name').strip('')
	if not module_condition['app_name']:
		return json.dumps({'result':1,'msg':'The module name is not GET'})

        module_ips_list = list(mysql_exec.select_sql('cmdb_online',fields,module_condition)[0])
        if not module_ips_list:
		woops_log.log_write('pub_opera').error('The module %s has NO IP' % module_condition['app_name'])
		return json.dumps({'result':1,'msg':'The module has no IP'})		
	module_ips=module_ips_list[0].split('<br>')
	woops_log.log_write('pub_opera').debug('module_ips: %s' % module_ips)
	return json.dumps({'result':0,'msg':module_ips})
                
