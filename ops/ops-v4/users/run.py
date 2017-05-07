#!/usr/bin/env python
#coding=utf8

from flask import Flask

app=Flask(__name__)

app.secret_key = "Abcd1234!"

from users_login import *

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8888,debug=True)
