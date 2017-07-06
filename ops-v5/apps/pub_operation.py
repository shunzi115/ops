#!/usr/bin/env python
#coding=utf8

from flask import request,render_template,redirect,session
from . import app
from common_func import session_check,role_check
from datetime import *
import json
from utils import woops_log,mysql_exec

@app.route("/pub/operation",methods=['GET','POST'])
def pub_opera():
	return render_template("/pub/pub_opera.html")
