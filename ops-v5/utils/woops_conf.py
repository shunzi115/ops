#!/usr/bin/env python
#coding=utf8

import os
import ConfigParser,traceback

woops_conf = ConfigParser.ConfigParser()
def conf_read(config_file='woops.conf',section=''):
	work_dir = os.path.dirname(os.path.realpath(__file__))
	file_read = os.path.join(work_dir, '../conf/woops.conf')
	print file_read
	woops_conf.read(file_read)
	print woops_conf.items(section)
	try:
		conf_items_dict = dict(woops_conf.items(section))
		return conf_items_dict
	except Exception:
		traceback.print_exc()

if __name__ == '__main__':
	conf_read('woops.conf','DB_mysql')
