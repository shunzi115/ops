#!/usr/bin/env python
#coding=utf8

import woops_conf
import logging,os
from logging.handlers import TimedRotatingFileHandler


log_conf = woops_conf.conf_read('woops.conf','log')

work_dir = os.path.dirname(os.path.realpath(__file__))
log_file = log_conf.get('log_path',work_dir + '/../logs') + '/' + log_conf['log_filename']
log_level = log_conf['log_level']
print log_level
print type(log_level)

if log_level == 'DEBUG':
	log_level = logging.DEBUG
elif log_level == 'INFO':
	log_level = logging.INFO
elif log_level == 'WARNING':
	log_level = logging.WARNING
elif log_level == 'ERROR':
	log_level = logging.ERROR
else:
	log_level = logging.CRITICAL

format = '%(asctime)s - %(name)s - %(filename)s[line:%(lineno)2d] - %(funcName)s - %(levelname)s - %(message)s'
log_format = logging.Formatter(format)

def log_write(log_name):
	log_handler = TimedRotatingFileHandler(log_file,when='midnight',backupCount=log_conf['log_backup'],encoding='utf8')
	log_handler.setFormatter(log_format)
	
	woops_logger = logging.getLogger(log_name)
	woops_logger.handlers = []
	woops_logger.addHandler(log_handler)
	woops_logger.setLevel(log_level)
	return woops_logger

if __name__ == '__main__':
	log_write('haha').info('成功')
	log_write('haha').error('错误')
	log_write('haha').warning('警告')
