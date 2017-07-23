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
from unicodedata import normalize

file_dir = os.path.dirname(os.path.realpath(__file__))
upload_dir = file_dir + '/../upload/'
allow_file_type=set(['txt','sql','docx'])


@app.route("/test",methods=['GET','POST'])
@session_check
def test():
        if request.method == 'GET':
                return render_template("test.html")
	if request.method == 'POST':
#		file = request.files['files[]']
		for file in request.files.getlist('files[]'):
			print "***** file *****"
			print file
#			app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
            		filename = file.filename
			filetype = file.content_type
			print "**** filetype ****"
			print filetype
			if '.' in filename and filename.rsplit('.',1)[1] in allow_file_type:
            			file.save(os.path.join(upload_dir, filename))
            			return json.dumps({"result":0,"files": [{"name": filename, "minetype": filetype}]})
			else:
				return json.dumps({"result":1,"msg":"haha nibeipianle","files": [{"name": filename, "minetype": filetype}]})
