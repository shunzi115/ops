#!/usr/bin/env python
#coding=utf8

import mysql_init

fields_pre = ['id','login_name','name_cn','password','mobile','email','role','status','update_time','last_login_time']
fields = ['password','mobile','email','role']

value_list_pre = ['xz','xiaozhang','1234567','13700001112','hehe@163.com',0,0,'2017-04-15 13:16:26','2017-04-15 13:16:26']
value_list = ['3456879','18600001112','123@163.com',1]

value_dict = dict(zip(fields,value_list))

conditions = {'id':3,'login_name':'xh'}

print "value_dict: %s" %(value_dict)

#mysql_init.delete_sql('users',conditions)

haha = mysql_init.select_sql('users',fields_pre)
print "*" * 100 
print haha
print "#" * 100 
user_info_list = [dict(zip(fields_pre,i)) for i in haha]
print user_info_list
