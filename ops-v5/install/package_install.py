#!/usr/bin/env python
#coding=utf8
#OS: CentOS7.2

1. ##### 安装数据库 #####

   yum -y remove mariadb-libs.x86_64 1:5.5.52-1.el7

   wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm

   rpm -ivh mysql57-community-release-el7-11.noarch.rpm

   yum -y install mysql-community-server.x86_64 mysql-community-devel.x86_64 mysql-community-client.x86_64 mysql-connector-python.x86_64

2. ##### 安装 mysqlDB 模块 #####

   yum -y install MySQL-python python-devel

3. ##### 安装定时任务包: apscheduler #####

   pip install apscheduler

4. ##### 安装 flask #####

   pip  install  flask

5. ##### 安装数据库连接池:DBUtils #####

   wget https://pypi.python.org/packages/source/D/DBUtils/DBUtils-1.1.tar.gz
   tar zxvf DBUtils-1.1.tar.gz
   cd DBUtils-1.1
   python setup.py install

6. ##### 安装 ansi2html:方便在shell中定义的颜色能在前端html中显示相应的颜色

   pip install ansi2html
