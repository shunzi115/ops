#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append('..')
print "*** sys.path ***"
print sys.path

from flask import request,render_template,redirect,session

from db_mysql import mysql_init

from run import app
import json

from functools import wraps

##定义装饰器做session 校验##
def session_check(func):
	@wraps(func)
	def session_if(*args,**kwargs):
		if not session.get('login_name',None):
			return redirect("/users/login")
		else:
			return func(*args,**kwargs)
	return session_if

@app.route('/users/register',methods=['GET','POST'])
def user_register():
	select_fields = ['login_name']
	user_list = [x[0] for x in mysql_init.select_sql('users',select_fields)]
	print "**** user_list ****"
	print user_list
	if request.method == 'GET':
		return render_template('/register.html')
	if request.method == 'POST':
		user_register = dict((i,j[0]) for i,j in dict(request.form).items())
		print "**** user_register ****"
		print user_register
		user_register['status'] = 0
		user_register['update_time'] = "2017-04-15 14:05:05" 
		user_register['last_login_time'] = "2017-04-15 14:05:05" 
		if not user_register['login_name'].strip('') or not user_register['name_cn'].strip('') or not user_register['password'].strip(''):
			return json.dumps({'result':1,'msg':'input not null'})
		if not user_register['mobile'].strip('') or not user_register['email'].strip('') or not user_register['role'].strip(''):
			return json.dumps({'result':1,'msg':'input not null'})
		if user_register['login_name'] in user_list:
			return json.dumps({'result':1,'msg':'user has exists'})
		if user_register['password'] != user_register['password_again']:
			return json.dumps({'result':1,'msg':'two password is not same'})
		del user_register['password_again']
		insert_fields = [x for x in user_register.keys()]
		mysql_init.insert_sql('users',insert_fields,user_register)
		return json.dumps({'result':0,'msg':'ok'})

@app.route("/")
@session_check
def base():
	return render_template("base.html")

@app.route("/users/login",methods=["GET","POST"])
def user_login():
	if request.method == 'POST':
		login_info = {}
		print "**** request.form ****"
		print request.form
		print dict(request.form)
		login_info = dict((i,j[0]) for i,j in dict(request.form).items())
		if not login_info.get('login_name',None) or not login_info.get('password',None):
			return json.dumps({'result':1,'msg':'input not null'}) 
		fields = ['id','login_name','name_cn','password','mobile','email','role','status','last_login_time']
		password = login_info['password']
		del login_info['password']
		select_login_info = mysql_init.select_sql('users',fields,login_info)
		print "***** select_login_info *****"
		print select_login_info
		if not select_login_info:
			return json.dumps({'result':1,'msg':'login_name in not exist'}) 
		select_login_info_dict = [dict(zip(fields,x)) for x in select_login_info][0]
		print "***** select_login_info_dict *****"
		print select_login_info_dict
		if select_login_info_dict['password'] != password:
                        return json.dumps({'result':1,'msg':'password is not right'}) 
		session['login_name'] = select_login_info_dict['login_name']
		session['role'] = select_login_info_dict['role']
		session['status'] = select_login_info_dict['status']	
		return json.dumps({'result':0,'msg':'ok'})
	if request.method == 'GET':
		return render_template("user_login.html")

@app.route("/users/user_info")
@session_check
def user_info():
	select_conditon = {}
	select_conditon['login_name']=session.get('login_name',None)
	fields = ['id','login_name','name_cn','mobile','email','role','status','update_time','last_login_time']
	user_info_dict=[dict(zip(fields,i)) for i in mysql_init.select_sql('users',fields,select_conditon)][0]
	print "**** user_info_dict ****"
	print user_info_dict
        return render_template("user_personal_info.html",user_info=user_info_dict)

@app.route("/users/user_list",methods=['GET'])
@session_check
def user_list():
	fields = ['id','login_name','name_cn','password','mobile','email','role','status','update_time','last_login_time']
	users_info_tuple = mysql_init.select_sql('users',fields)
	print "***** users_info_tuple *****"
	print users_info_tuple
	user_info_list = [dict(zip(fields,i)) for i in users_info_tuple]
	print "***** user_info_list *****"
	print user_info_list
	return render_template("/user_list.html",users_info=user_info_list)

@app.route("/users/update",methods=["GET","POST"])
@session_check
def user_update():
	if request.method == 'GET':
		select_condition = {}
		select_condition['id'] = request.args.get('id')
		print "**** select_condition ***"
		print select_condition
		select_fields = ['id','login_name','name_cn','mobile','email','role','status']
		select_results_pre = mysql_init.select_sql('users',select_fields,select_condition)
		print "**** select_results_pre ***"
		print select_results_pre
		select_result_dict = [dict(zip(select_fields,x)) for x in select_results_pre][0]
		print "**** select_result_dict ***"
		print select_result_dict
		return render_template("/user_update.html",user_info=select_result_dict)
	if request.method == "POST":
		print "**** request.form ****"
		print request.form
		print dict(request.form)
		update_conditions = {}
		update_user = dict((i,j[0]) for i,j in dict(request.form).items())
		update_conditions['id'] = update_user['id'].strip('')
		update_conditions['login_name'] = update_user['login_name'].strip('')
		update_user['update_time'] = '2017-04-16 14:41:52'
		print "**** update_user ****"
		print update_user
		if not update_user['name_cn'].strip('') or not update_user['mobile'].strip('') or not update_user['email'].strip(''):
			return json.dumps({'result':1,'msg':'input not null'})
		del update_user['id']
		del update_user['login_name']
		mysql_init.update_sql('users',update_user,update_conditions)
		return json.dumps({'result':0,'msg':'ok'}) 

@app.route("/users/update_password",methods=['GET','POST'])
@session_check
def user_update_password():
	fields = ['id','login_name','password']
	if request.method == 'POST':
		select_password_condition = {}
		update_password_info = {}
		select_password_condition['login_name'] = request.form.get('login_name').strip('')
		password_old_input = request.form.get('password_old_input').strip('')
		update_password_info['password'] = request.form.get('password_new').strip('')
		password_again = request.form.get('password_new_again').strip('')
		select_password_pre = mysql_init.select_sql('users',fields,select_password_condition)
		print "***** select_password_pre ****"
                print select_password_pre
		select_password_info = [dict(zip(fields,x)) for x in select_password_pre]
		print "***** select_password_info ****"
		print select_password_info
		password_old = select_password_info[0]['password']
		if not password_old_input or not update_password_info['password']:
			return json.dumps({'result':1,'msg':'input not null'}) 
		if password_old_input != password_old:
			return json.dumps({'result':1,'msg':'old_password is not right'}) 
		if update_password_info['password'] != password_again: 
			return json.dumps({'result':1,'msg':'two password is not same'}) 

		mysql_init.update_sql('users',update_password_info,select_password_condition)
		return json.dumps({'result':0,'msg':'ok'})

@app.route("/users/delete",methods=['GET'])
@session_check
def user_delete():
	delete_condition = {}
	delete_condition['id'] = request.args.get('id')
	mysql_init.delete_sql('users',delete_condition)
	return json.dumps({'result':0,'msg':'ok'})

@app.route("/users/logout",methods=['GET'])
def user_logout():
	print "**** session ****"
	print session
	del session['login_name']
	return redirect("/users/login")

