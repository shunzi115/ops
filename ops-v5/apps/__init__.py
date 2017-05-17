#!/usr/bin/env python
#coding=utf8

from flask import Flask,session,render_template,redirect

from functools import wraps

app=Flask(__name__)

app.secret_key = "Abcd1234!"

##定义装饰器做session 校验##
def session_check(func):
        @wraps(func)
        def session_if(*args,**kwargs):
                if not session.get('login_name',None):
                        return redirect("/users/login")
                else:
                        return func(*args,**kwargs)
        return session_if

###定义装饰器,用来判断用户角色是否是 管理员或者是ops###
def role_check(func):
        @wraps(func)
        def role_if(*args,**kwargs):
                if session.get('role',None) != 0 and session.get('role',None) != 1:
                        return render_template("error_role.html",errmsg="You have no permission !!!")
                else:
                        return func(*args,**kwargs)
        return role_if

import users,cmdb
