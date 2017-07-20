#!/usr/bin/env python
#coding=utf8


from flask import request,render_template,session,redirect
from . import app
from common_func import session_check,role_check
from datetime import *
import json,traceback
from utils import woops_log,mysql_exec
from api.ansible_exec import ansible_exec
import os
from werkzeug import secure_filename

file_dir = os.path.dirname(os.path.realpath(__file__))
upload_dir = file_dir + '/../upload/'

@app.route("/test",methods=['GET','POST'])
@session_check
def test():
        if request.method == 'GET':
                return render_template("test.html")
	if request.method == 'POST':
		file = request.files['files']
		print "***** file *****"
		print file
            	filename = secure_filename(file.filename)
		filetype = file.content_type
		print "**** filetype ****"
		print filetype
            	file.save(os.path.join(upload_dir, filename))
            	return json.dumps({"files": [{"name": filename, "minetype": filetype}]})
