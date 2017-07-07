#!/usr/bin/env python
#coding:utf8

from flask import session,render_template,redirect
from . import app
from functools import wraps
from utils import woops_log,mysql_exec
import json




app.secret_key = "Abcd1234!"

### 定义装饰器做session 校验 ##
def session_check(func):
        @wraps(func)
        def session_if(*args,**kwargs):
                if not session.get('login_name',None):
                        return redirect("/users/login")
                else:
                        return func(*args,**kwargs)
        return session_if

### 定义装饰器,用来判断用户角色是否是 管理员或者是ops ###
def role_check(func):
        @wraps(func)
        def role_if(*args,**kwargs):
                if session.get('role',None) != 0 and session.get('role',None) != 1:
                        return render_template("error_role.html",errmsg="You have no permission !!!")
                else:
                        return func(*args,**kwargs)
        return role_if


### 查询线上有哪些模块 ###
def online_app_list():
	fields = ['app_name']
	module_name_tuple = mysql_exec.select_sql('cmdb_online',fields)
	module_name_list = [dict(zip(fields,i)) for i in module_name_tuple]
	woops_log.log_write('common_func').debug('module_name_list : %s' % module_name_list)
	return module_name_list


### 查询线上有哪些 IP 地址 ###
