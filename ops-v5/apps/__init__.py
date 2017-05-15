#!/usr/bin/env python
#coding=utf8

from flask import Flask

app=Flask(__name__)

app.secret_key = "Abcd1234!"

import users,cmdb
