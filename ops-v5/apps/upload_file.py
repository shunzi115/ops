#!/usr/bin/env python
#coding=utf8


from flask import request,session,redirect,url_for
from . import app
from common_func import session_check,role_check
from datetime import *
import json,traceback
from utils import woops_log,mysql_exec
import os
from werkzeug import secure_filename
from unicodedata import normalize
from flask import send_from_directory


file_dir = os.path.dirname(os.path.realpath(__file__))
upload_dir = file_dir + '/../upload/'
allow_file_type=set(['txt','sql','pdf','docx'])


@app.route("/upload/files",methods=['GET','POST'])
@session_check
def upload_files():
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
			if '.' not in filename or  filename.rsplit('.',1)[1] not in allow_file_type:
				return json.dumps({"result":1,"msg":"The type %s of file %s is not allow" %(filetype,filename)})
			file_upload_time = datetime.now().strftime("%Y%m%d%H%M%S")
			file_store_name = filename.rsplit('.',1)[0] + '_' + file_upload_time + '.' + filename.rsplit('.',1)[1]
			file_url = url_for('uploaded_file',filename=file_store_name)
			print "**** file_url ****"
			print file_url
            		file.save(os.path.join(upload_dir, file_store_name))
            		return json.dumps({"result":0,"files": [{"name": file_store_name, "minetype": filetype}],"file_url":file_url})


@app.route('/uploads/<filename>')
@session_check
def uploaded_file(filename):
	return send_from_directory(upload_dir,filename)
