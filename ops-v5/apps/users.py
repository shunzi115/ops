#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,redirect,session
from . import app
from common_func import session_check,role_check
from datetime import *
import json,hashlib
from utils import woops_log,mysql_exec

salt="Watsons_OPS@163.com"

@app.route('/users/register',methods=['GET','POST'])
def user_register():
	woops_log.log_write('hello').error('hello')
	select_fields = ['login_name']
	user_list = [x[0] for x in mysql_exec.select_sql('users',select_fields)]
	woops_log.log_write('users').debug('user_list:%s' % user_list)
	if request.method == 'GET':
		return render_template('/register.html')
	if request.method == 'POST':
		user_register = dict((i,j[0]) for i,j in dict(request.form).items())
		woops_log.log_write('users').debug('user_register:%s' % user_register)
		user_register['status'] = 0
		user_register['update_time'] = datetime.now().strftime("%Y-%m-%d %X") 
		user_register['last_login_time'] = user_register['update_time'] 
		if not user_register['login_name'].strip('') or not user_register['name_cn'].strip('') or not user_register['password'].strip(''):
			woops_log.log_write('users').error('Input can not be empty')
			return json.dumps({'result':1,'msg':'Input can not be empty'})
		if not user_register['mobile'].strip('') or not user_register['email'].strip('') or not user_register['role'].strip(''):
			woops_log.log_write('users').error('Input can not be empty')
			return json.dumps({'result':1,'msg':'Input can not be empty'})
		if user_register['login_name'] in user_list:
			woops_log.log_write('users').error('user "%s" already exists' % user_register['login_name'])
			return json.dumps({'result':1,'msg':'User already exists'})
		if user_register['password'] != user_register['password_again']:
			woops_log.log_write('users').error('Input two password is not consistent')
			return json.dumps({'result':1,'msg':'Input two password is not consistent'})
		del user_register['password_again']
		insert_fields = [x for x in user_register.keys()]
		user_register['password'] = hashlib.md5(user_register['password'] + salt).hexdigest()
		mysql_exec.insert_sql('users',insert_fields,user_register)
		woops_log.log_write('users').info('User "%s" registration successful' % user_register['login_name'])
		return json.dumps({'result':0,'msg':'ok'})

@app.route("/")
@session_check
def base():
	return render_template("base.html")

@app.route("/users/login",methods=["GET","POST"])
def user_login():
	if request.method == 'POST':
		login_info = {}
		login_info = dict((i,j[0]) for i,j in dict(request.form).items())
		if not login_info.get('login_name',None) or not login_info.get('password',None):
			woops_log.log_write('users').error('Input can not be empty')
			return json.dumps({'result':1,'msg':'Input can not be empty'}) 
		fields = ['id','login_name','name_cn','password','mobile','email','role','status','last_login_time']
		password = hashlib.md5(login_info['password']+salt).hexdigest()
		del login_info['password']
		select_login_info = mysql_exec.select_sql('users',fields,login_info)
		woops_log.log_write('users').debug('select_login_info:%s' % select_login_info)
		if not select_login_info:
			woops_log.log_write('users').error('user "%s" does not exists' % login_info['login_name'])
			return json.dumps({'result':1,'msg':'user does not exists'}) 
		select_login_info_dict = [dict(zip(fields,x)) for x in select_login_info][0]
		woops_log.log_write('users').debug('select_login_info_dict:%s' % select_login_info_dict)
		if select_login_info_dict['password'] != password:
			woops_log.log_write('users').error('User "%s" input password is not correct' % login_info['login_name'])
                        return json.dumps({'result':1,'msg':'Input password is not correct'}) 
		if select_login_info_dict['status'] == 1:
			woops_log.log_write('users').error('The state of the user "%s" has locked, please contact OPS' % login_info['login_name'])
                        return json.dumps({'result':1,'msg':'User has locked,please contact OPS'}) 
		session['login_name'] = select_login_info_dict['login_name']
		session['role'] = select_login_info_dict['role']
		session['status'] = select_login_info_dict['status']
		mysql_exec.update_sql('users',{'last_login_time':"%s" %(datetime.now().strftime("%Y-%m-%d %X"))},login_info)
		woops_log.log_write('users').info('"%s" login success' % login_info['login_name'])
		return json.dumps({'result':0,'msg':'ok'})
	if request.method == 'GET':
		return render_template("user_login.html")

@app.route("/users/user_info")
@session_check
def user_info():
	select_conditon = {}
	select_conditon['login_name']=session.get('login_name',None)
	fields = ['id','login_name','name_cn','mobile','email','role','status','update_time','last_login_time']
	user_info_dict=[dict(zip(fields,i)) for i in mysql_exec.select_sql('users',fields,select_conditon)][0]
	woops_log.log_write('users').debug('user_info_dict : %s' % user_info_dict)
        return render_template("user_personal_info.html",user_info=user_info_dict)

@app.route("/users/user_list",methods=['GET'])
@session_check
@role_check
def user_list():
	fields = ['id','login_name','name_cn','password','mobile','email','role','status','update_time','last_login_time']
	users_info_tuple = mysql_exec.select_sql('users',fields)
	user_info_list = [dict(zip(fields,i)) for i in users_info_tuple]
	woops_log.log_write('users').debug('user_info_list : %s' % user_info_list)
	return render_template("/user_list.html",users_info=user_info_list)

@app.route("/users/update",methods=["GET","POST"])
@session_check
def user_update():
	if request.method == 'GET':
		select_condition = {}
		select_condition['id'] = request.args.get('id')
		select_fields = ['id','login_name','name_cn','mobile','email','role','status']
		select_results_pre = mysql_exec.select_sql('users',select_fields,select_condition)
		select_result_dict = [dict(zip(select_fields,x)) for x in select_results_pre][0]
		woops_log.log_write('users').debug('select_result_dict : %s' % select_result_dict)
		return json.dumps(select_result_dict)
	if request.method == "POST":
		update_conditions = {}
		update_user = dict((i,j[0]) for i,j in dict(request.form).items())
		update_conditions['id'] = update_user['id'].strip('')
		update_conditions['login_name'] = update_user['login_name'].strip('')
		update_user['update_time'] = "%s" %(datetime.now().strftime("%Y-%m-%d %X"))
		woops_log.log_write('users').debug('update_user : %s' % update_user)
		if not update_user['name_cn'].strip('') or not update_user['mobile'].strip('') or not update_user['email'].strip(''):
			woops_log.log_write('users').error('User information input can not be empty')
			return json.dumps({'result':1,'msg':'User information input can not be empty'})
		del update_user['id']
		del update_user['login_name']
		mysql_exec.update_sql('users',update_user,update_conditions)
		woops_log.log_write('users').info('User information change success')
		return json.dumps({'result':0,'msg':'ok'}) 

@app.route("/users/update_password",methods=['GET','POST'])
@session_check
def user_update_password():
	fields = ['id','login_name','password']
	if request.method == 'POST':
		select_password_condition = {}
		update_password_info = {}
		select_password_condition['login_name'] = request.form.get('login_name').strip('')
		update_password_info['password'] = request.form.get('password_new').strip('')
		password_again = hashlib.md5(request.form.get('password_new_again').strip('') + salt).hexdigest()
		if session.get('role',2) != 0 and session.get('role',2) != 1:
			password_old_input = request.form.get('password_old_input',None).strip('')
			select_password_pre = mysql_exec.select_sql('users',fields,select_password_condition)
			select_password_info = [dict(zip(fields,x)) for x in select_password_pre]
			woops_log.log_write('users').debug('select_password_info : %s' % select_password_info)
			password_old = select_password_info[0]['password']
			if not password_old_input:
				woops_log.log_write('users').error('The old password input can not be empty')
				return json.dumps({'result':1,'msg':'The old password input can not be empty'})
			password_old_input = hashlib.md5(password_old_input + salt).hexdigest()
			if password_old_input != password_old:
				woops_log.log_write('users').error('The old password input can not be correctly')
				return json.dumps({'result':1,'msg':'The old password input can not be correctly'}) 
		if not update_password_info['password']:
			woops_log.log_write('users').error('The update password input can not be empty')
			return json.dumps({'result':1,'msg':'The update password input can not be empty'}) 
		update_password_info['password'] = hashlib.md5(update_password_info['password'] + salt).hexdigest()
		if update_password_info['password'] != password_again: 
			woops_log.log_write('users').error('Input two password is not consistent')
			return json.dumps({'result':1,'msg':'Input two password is not consistent'}) 

		update_password_info['update_time']="%s" %(datetime.now().strftime("%Y-%m-%d %X"))
		mysql_exec.update_sql('users',update_password_info,select_password_condition)
		woops_log.log_write('users').info('User password change success')
		return json.dumps({'result':0,'msg':'ok'})

@app.route("/users/delete",methods=['GET'])
@session_check
@role_check
def user_delete():
	delete_condition = {}
	delete_user = {}
	delete_condition['id'] = request.args.get('id')
	delete_user = [dict(zip(['login_name'],i)) for i in mysql_exec.select_sql('users',['login_name'],delete_condition)][0]
	woops_log.log_write('users').debug('delete_user : %s' % delete_user['login_name'])
	mysql_exec.delete_sql('users',delete_condition)
	woops_log.log_write('users').info('Delete user "%s" success' % delete_user['login_name'] )
	return json.dumps({'result':0,'msg':'ok'})

@app.route("/users/logout",methods=['GET'])
def user_logout():
	woops_log.log_write('users').info('User "%s" logout success' % session['login_name'])
	del session['login_name']
	return redirect("/users/login")

