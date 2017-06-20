#!/usr/bin/env python
#!coding=utf8

from flask import request,render_template,redirect,session
from . import app
from common_func import session_check,role_check
from datetime import *
import json
from utils import woops_log,mysql_exec


@app.route("/workform/publish",methods=['GET'])
def publish():
	return render_template("/workform/publist_index.html")

@app.route("/workform/pub_add",methods=['POST'])
def pub_add():
	if request.method == 'POST':
		pub_info = dict((i,j[0]) for i,j in dict(request.form).items())
		print "**** pub_info ****"
		print pub_info
		woops_log.log_write('publish').debug('pub_info:%s' % pub_info)
		if not pub_info['pub_title'].strip('') or not pub_info['pub_module'].strip('') or not pub_info['pub_content'].strip(''):
			msg = 'Input can not be empty'
			woops_log.log_write('publish').error(msg)
			return json.dumps({'result':1,'msg':msg})
		if pub_info['pub_SQL'].strip('') == 'YES' and not pub_info['pub_SQL_detail'].strip(''):
			msg = 'Please choose correct if there were any SQL'
			woops_log.log_write('publish').error(msg)
                        return json.dumps({'result':1,'msg':msg})
		if pub_info['pub_SQL'].strip('') == 'NO' and pub_info['pub_SQL_detail'].strip(''):
			msg = 'Please choose correct if there were any SQL'
                        woops_log.log_write('publish').error(msg)
                        return json.dumps({'result':1,'msg':msg})
		if pub_info['pub_level'].strip('') == 'emergency':
			pub_info['pub_status'] = '0'
		else:
			pub_info['pub_status'] = '3'
		pub_info['pub_submit_time'] = datetime.now().strftime("%Y-%m-%d %X")
		pub_info['pub_application_people'] = session.get('login_name',None)
		print '**** pub_info ****'
		print pub_info
		insert_fields = [x for x in pub_info.keys()]
		mysql_exec.insert_sql('publish_online',insert_fields,pub_info)
		woops_log.log_write('publish').info('"%s" submit successful' % pub_info['pub_title'])
		return json.dumps({'result':0,'msg':'ok'})

@app.route("/workform/pub_list",methods=['GET'])
def pub_list():
	fields_1 = ['id','pub_title','pub_level','pub_module','pub_content','pub_SQL','pub_SQL_detail']
	fields_2 = ['pub_application_people','pub_status','pub_audit_people','pub_submit_time','pub_done_time','pub_operation_people']
	fields = fields_1 + fields_2
	pub_info_tuple = mysql_exec.select_sql('publish_online',fields)
        pub_info_list = [dict(zip(fields,i)) for i in pub_info_tuple]
        woops_log.log_write('publish').debug('pub_info_list : %s' % pub_info_list)
	print "**** pub_info_list ****"
	print pub_info_list
        return json.dumps({'pub_info':pub_info_list})

@app.route("/workform/pub_my",methods=['GET','POST'])
def pub_my():
	if request.method == 'GET':
       		fields_1 = ['id','pub_title','pub_level','pub_module','pub_content','pub_SQL','pub_SQL_detail']
        	fields_2 = ['pub_application_people','pub_status','pub_audit_people','pub_submit_time','pub_done_time','pub_operation_people']
        	fields = fields_1 + fields_2
		my_conditon = {}
		my_conditon['pub_application_people'] = session.get('login_name',None)
        	pub_my_tuple = mysql_exec.select_sql('publish_online',fields,my_conditon)
        	pub_my_list = [dict(zip(fields,i)) for i in pub_my_tuple]
        	woops_log.log_write('publish').debug('pub_my_list : %s' % pub_my_list)
        	print "**** pub_my_list ****"
        	print pub_my_list
        	return json.dumps({'pub_my':pub_my_list})

@app.route("/workform/pub_audit",methods=['GET','POST'])
def pub_audit():
        if request.method == 'GET':
                fields_1 = ['id','pub_title','pub_level','pub_module','pub_SQL']
                fields_2 = ['pub_application_people','pub_status','pub_submit_time']
                fields = fields_1 + fields_2
		audit_conditon = {}
		audit_conditon['pub_status'] = session.get('role',None)
        	pub_audit_tuple = mysql_exec.select_sql('publish_online',fields,audit_conditon)
                pub_audit_list = [dict(zip(fields,i)) for i in pub_audit_tuple]
                woops_log.log_write('publish').debug('pub_audit_list : %s' % pub_audit_list)
                print "**** pub_my_audit ****"
                print pub_audit_list
                return json.dumps({'pub_audit':pub_audit_list})
	if request.method == 'POST':
		audit_msg_condation = {}
		audit_msg =  dict((i,j[0]) for i,j in dict(request.form).items())
		audit_msg['pub_audit_people'] = session.get('login_name',None)
		if not audit_msg['pub_audit_people']:
			return json.dumps({'result':1,'msg':'Please log in again...'})
		print "**** audit_msg ****"
		print audit_msg
		audit_msg_condation['id'] = audit_msg.get('id',None)
		if not audit_msg_condation['id']:
                        return json.dumps({'result':1,'msg':'Please contact the OPS...'})
		del audit_msg['id']
		if audit_msg['QA_audit_result'] == 'YES':
			audit_msg['pub_status'] = '1'
			audit_msg['audit_time'] = datetime.now().strftime("%Y-%m-%d %X")
		else:
			audit_msg['pub_status'] = '6'
			audit_msg['pub_done_time'] = datetime.now().strftime("%Y-%m-%d %X")
		mysql_exec.update_sql('publish_online',audit_msg,audit_msg_condation)
		return json.dumps({'result':0,'msg':'ok'})

@app.route("/workform/pub_info",methods=['GET','POST'])
def pub_info():
        if request.method == 'GET':
                fields_1 = ['id','pub_title','pub_level','pub_module','pub_content','pub_SQL','pub_SQL_detail']
                fields_2 = ['pub_application_people','pub_status','pub_submit_time']
                fields = fields_1 + fields_2
                pub_info_conditon = {}
                pub_info_conditon['id'] = request.args.get('id',None)
                pub_info_tuple = mysql_exec.select_sql('publish_online',fields,pub_info_conditon)
                pub_info_dict = [dict(zip(fields,i)) for i in pub_info_tuple][0]
                woops_log.log_write('publish').debug('pub_info_dict : %s' % pub_info_dict)
                print "**** pub_info_dict ****"
                print pub_info_dict
                return json.dumps(pub_info_dict)

@app.route("/test",methods=['GET','POST'])
def test():
        if request.method == 'GET':
                return render_template("test.html")
