#!/usr/bin/env python
#coding=utf8

from flask import Flask

import sys

sys.path.append('../utils')
print "*** sys.path ***"
print sys.path

app=Flask(__name__)

import dashboard,users,cmdb_online,server,workform_pub
