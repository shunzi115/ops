#!/usr/bin/env python
#coding=utf8
import sys
sys.path.append('..')
print "*** sys.path ***"
print sys.path

from flask import Flask,request,render_template,redirect

from db_mysql import mysql_init

app = Flask(__name__)

@app.route('/users/register',methods=['GET','POST'])
def user_register():
	select_fields = ['login_name']
	user_list = [x[0] for x in mysql_init.select_sql('users',select_fields)]
	print "**** user_list ****"
	print user_list
	user_register = {}
	if request.method == 'GET':
		return render_template('/register.html')
	if request.method == 'POST':
		user_register['login_name'] = request.form.get('login_name').strip('')
		user_register['name_cn'] = request.form.get('name_cn').strip('')
		user_register['password'] = request.form.get('password').strip('')
		password_again = request.form.get('password_again').strip('')
		user_register['mobile'] = request.form.get('mobile').strip('')
		user_register['email'] = request.form.get('email').strip('')
		user_register['role'] = request.form.get('role').strip('')
		user_register['status'] = 0
		user_register['update_time'] = "2017-04-15 14:05:05" 
		user_register['last_login_time'] = "2017-04-15 14:05:05" 
		print "***** user_register *****"
		print user_register
		if not user_register['login_name'] or not user_register['name_cn'] or not user_register['password'] or not user_register['mobile'] or not user_register['email'] or not user_register['role']:
			err_info = "input not null"
			return render_template("/register.html",err_info=err_info)
		if user_register['login_name'] in user_list:
			err_info = "user has exists"
			return render_template("/register.html",err_info=err_info)
		if user_register['password'] != password_again:
			err_info = "two password is not same"
                        return render_template("/register.html",err_info=err_info)
		insert_fields = [x for x in user_register.keys()]
		mysql_init.insert_sql('users',insert_fields,user_register)
		return redirect("/users/user_list")

@app.route("/")
@app.route("/users/login",methods=["GET","POST"])
def user_login():
	if request.method == 'GET':
		return render_template("/user_login.html")
	if request.method == 'POST':
		login_info = {}
		login_info['login_name'] = request.form.get('login_name').strip('')
		password = request.form.get('password').strip('')
		if not login_info['login_name'] or not password:
			err_info = "input not null"
			return render_template("/user_login.html",err_info=err_info)
		fields = ['id','login_name','name_cn','password','mobile','email','role','status','last_login_time']
		select_login_info = mysql_init.select_sql('users',fields,login_info)
		print "***** select_login_info *****"
		print select_login_info
		if not select_login_info:
			err_info = "login_name in not exist"
			return render_template("/user_login.html",err_info=err_info)
		select_login_info_list = [dict(zip(fields,x)) for x in select_login_info]
		print "***** select_login_info_list *****"
		print select_login_info_list
		if select_login_info_list[0]['password'] != password:
			err_info = "password is not right"
                        return render_template("/user_login.html",err_info=err_info)
		return render_template("/user_personal_info.html",login_user_info=select_login_info_list[0])

@app.route("/users/user_list",methods=['GET'])
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
		select_result_list = [dict(zip(select_fields,x)) for x in select_results_pre]
		print "**** select_result_list ***"
		print select_result_list
		return render_template("/user_update.html",user_info=select_result_list)
	if request.method == "POST":
		print "**** request.form ****"
		print request.form
		print dict(request.form)
		update_conditions = {}
		update_user = {}
		update_conditions['id'] = request.form.get('id').strip('')
		update_user['login_name'] = request.form.get('login_name').strip('')
		update_user['name_cn'] = request.form.get('name_cn').strip('')
		update_user['mobile'] = request.form.get('mobile').strip('')
		update_user['email'] = request.form.get('email').strip('')
		update_user['role'] = request.form.get('role').strip('')
		update_user['status'] = request.form.get('status').strip('')
		update_user['update_time'] = '2017-04-16 14:41:52'
		print "**** update_user ****"
		print update_user
		if not update_user['name_cn'] or not update_user['mobile'] or not update_user['email']:
			err_info = "input not null"
			return render_template("/user_update.html",err_info=err_info)
		mysql_init.update_sql('users',update_user,update_conditions)
		if update_user['role'] == '0':
			return redirect("/users/user_list")
		else:
			update_user_personal_info = dict(update_conditions.items() + update_user.items())
			print "**** update_user_personal_info ****"
			print update_user_personal_info
			return render_template("/user_personal_info.html",login_user_info=update_user_personal_info)

@app.route("/users/update_password",methods=['GET','POST'])
def user_update_password():
	fields = ['id','login_name','password']
	if request.method == 'GET':
		select_password_condition = {}
		select_password_condition['id'] = request.args.get('id') 
		select_password_pre = mysql_init.select_sql('users',fields,select_password_condition)
		print "***** select_password_pre ****"
                print select_password_pre
		select_password_info = [dict(zip(fields,x)) for x in select_password_pre]
		print "***** select_password_info ****"
		print select_password_info
		password_info = select_password_info[0]
		return render_template("/user_update_password.html",password_info=password_info)
	if request.method == 'POST':
		update_info = {}
		update_password_info = {}
		update_info['login_name'] = request.form.get('login_name').strip('')
		password_old = request.form.get('password_old').strip('')
		password_old_input = request.form.get('password_old_input').strip('')
		update_password_info['password'] = request.form.get('password_new').strip('')
		password_again = request.form.get('password_new_again').strip('')
		if not password_old_input or not update_password_info['password']:
			err_info = "input not null"
			return render_template("/user_update_password.html",err_info=err_info)
		if password_old_input != password_old:
			err_info = "old_password is not right"
                        return render_template("/user_update_password.html",err_info=err_info)		
		if update_password_info['password'] != password_again: 
			err_info = "two password is not same "
                        return render_template("/user_update_password.html",err_info=err_info)		

		mysql_init.update_sql('users',update_password_info,update_info)
		return redirect("/users/user_list")

@app.route("/users/delete",methods=['GET'])
def user_delete():
	delete_condition = {}
	delete_condition['id'] = request.args.get('id')
	mysql_init.delete_sql('users',delete_condition)
	return redirect("/users/user_list")



if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8888,debug=True)
