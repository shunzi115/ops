
### 创建 数据库

create database dev_ops;

### 切换数据库

use dev_ops;

### 记录用户信息

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(20) NOT NULL COMMENT '登录名',
  `name_cn` varchar(50) NOT NULL COMMENT '中文名',
  `password` varchar(50) NOT NULL COMMENT '登录密码',
  `mobile` varchar(11) NOT NULL COMMENT '手机号码',
  `email` varchar(100) NOT NULL COMMENT '电子邮件',
  `role` tinyint(2) NOT NULL COMMENT '账号角色:0-admin;1-ops;2-dev;3-qa;4-guest',
  `status` tinyint(2) NOT NULL COMMENT '账号状态:0-正常；1-锁定',
  `update_time` varchar(30) NOT NULL COMMENT '最后修改时间',
  `last_login_time` varchar(30) NOT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_login_name` (`login_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';

INSERT INTO dev_ops.users (login_name, name_cn, password, mobile, email, role, status, update_time, last_login_time) VALUES ( 'admin', '诸葛孔明', '4bfd3be6dbd0c6888250de0640ec5905', '15811110333', '111@111.com', '0', '0', now(), now());

### 记录服务器硬件信息

CREATE TABLE `serverinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `HostName` varchar(20) DEFAULT NULL COMMENT '主机名',
  `SSH_port` varchar(5) NOT NULL COMMENT 'SSH 端口号',
  `PrivateIP` varchar(15) NOT NULL COMMENT '私网IP',
  `PublicIP` varchar(15) DEFAULT NULL COMMENT '公网IP',
  `ENV` varchar(50) NOT NULL COMMENT '所属环境',
  `ServerBrand` varchar(50) DEFAULT NULL COMMENT '服务器品牌',
  `ServerModel` varchar(50) DEFAULT NULL COMMENT '服务器型号',
  `OS` varchar(50) DEFAULT NULL COMMENT '系统版本',
  `Kernel` varchar(50) DEFAULT NULL COMMENT '内核版本',
  `CpuType` varchar(50) DEFAULT NULL COMMENT 'CPU类型',
  `CpuCount` varchar(5) DEFAULT NULL COMMENT 'CPU数量',
  `RAM_GB` varchar(20) DEFAULT NULL COMMENT '内存',
  `SWAP_size` varchar(10) DEFAULT NULL COMMENT 'SWAP 空间',
  `PhyDiskSize` varchar(50) DEFAULT NULL COMMENT '物理磁盘',
  `Part_mount` varchar(100) DEFAULT NULL COMMENT '分区挂载情况',
  `IDC` varchar(50) NOT NULL COMMENT '归属机房',
  `status` tinyint(2) NOT NULL COMMENT '服务器状态：0-在线,1-下线',
  `OnlineTime` varchar(30) NOT NULL COMMENT '上线时间',
  `OfflineTime` varchar(30) DEFAULT NULL COMMENT '下线时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_private_ip` (`PrivateIP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务器资产信息表'

### 记录线上cmdb 信息

CREATE TABLE `cmdb_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(20) NOT NULL COMMENT '应用名',
  `app_ip` varchar(100) NOT NULL COMMENT 'IP 地址',
  `app_describe` varchar(100) DEFAULT NULL COMMENT '描述',
  `domain` varchar(100) DEFAULT NULL COMMENT '域名',
  `cdn_domain` varchar(100) DEFAULT NULL COMMENT 'CDN 域名',
  `app_path` varchar(100) NOT NULL COMMENT '部署路径',
  `app_shell` varchar(100) NOT NULL COMMENT '启动脚本',
  `app_log` varchar(100) DEFAULT NULL COMMENT '日志路径',
  `app_ports` varchar(30) DEFAULT NULL COMMENT '开启的端口',
  `app_way` varchar(30) NOT NULL COMMENT '部署方式:nginx php tomcat jar',
  `status` tinyint(2) NOT NULL COMMENT '应用状态:0-online；1-offline',
  `online_time` varchar(30) NOT NULL COMMENT '上线时间',
  `offline_time` varchar(30) DEFAULT NULL COMMENT '下线时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_app_name` (`app_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='线上 CMDB 表';

### 记录发布与回滚工单信息

CREATE TABLE `publish_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_title` varchar(100) NOT NULL COMMENT '发布主题',
  `workform_type` varchar(50) NOT NULL COMMENT '工单类型',
  `pub_level` varchar(50) NOT NULL COMMENT '发布优先级',
  `pub_module` varchar(100) NOT NULL COMMENT '发布的模块名',
  `pub_content` varchar(1000) NOT NULL COMMENT '发布详情',
  `pub_SQL` varchar(10) NOT NULL COMMENT '是否有SQL',
  `pub_SQL_detail` varchar(1000) DEFAULT NULL COMMENT 'SQL详情',
  `pub_application_people` varchar(50) NOT NULL COMMENT '申请人',
  `pub_status` tinyint(2) NOT NULL COMMENT '状态-跟用户表角色相关联:3-QA审批中；1-OPS处理中；0-经理审批中；5-处理完成；6-经理/QA不同意发布；7-OPS发布异常;',
  `pub_audit_people` varchar(50) DEFAULT NULL COMMENT '上线审批人',
  `pub_submit_time` varchar(30) NOT NULL COMMENT '发布申请时间',
  `pub_done_time` varchar(30) DEFAULT NULL COMMENT '发布完成时间',
  `pub_operation_people` varchar(50) DEFAULT NULL COMMENT '上线操作人',
  `QA_audit` varchar(1000) DEFAULT NULL COMMENT '经理/QA审批意见',
  `QA_audit_result` varchar(10) DEFAULT NULL COMMENT '经理/QA审批结果',
  `audit_time` varchar(30) DEFAULT NULL COMMENT '经理/QA审批时间',
  `OPS_audit` varchar(1000) DEFAULT NULL COMMENT 'OPS发布备注',
  `OPS_pub_result` varchar(10) DEFAULT NULL COMMENT 'OPS发布结果',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pub_title` (`pub_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='模块发布表';

### 记录线上数据库所有表的行数变化

CREATE TABLE `online_table_rows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `TABLE_SCHEMA` varchar(50) NOT NULL COMMENT '数据库名',
  `TABLE_NAME` varchar(50) NOT NULL COMMENT '表名',
  `TABLE_ROWS` int(20) DEFAULT '0' COMMENT '数据行数',
  `UpdateTime` varchar(30) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='表数据行数统计';

### 记录线上版本状态: 打包-上线-使用中-回滚-使用过 

CREATE TABLE `pub_version_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_app_name` varchar(50) NOT NULL COMMENT '应用名',
  `pub_app_version` varchar(100) NOT NULL COMMENT '版本',
  `pub_app_version_status` varchar(20) DEFAULT NULL COMMENT '版本的状态：当前在用-using,曾经使用过的-used,回滚过的-rollbacked,刚打包的-packaged,正在发布中的-publishing,正在回滚中的-rollbacking,只上线了部分IP-part_used',
  `package_time` varchar(30) DEFAULT NULL COMMENT '打包时间',
  `pub_app_addr` varchar(100) DEFAULT NULL COMMENT '已发布的 IP 地址',
  `rollback_to_version` varchar(100) DEFAULT NULL COMMENT '回滚到的版本',
  `rollback_addr` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_app_version` (`pub_app_version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='线上版本状态';

### 记录上线的历史记录

CREATE TABLE `pub_history_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name_detail` varchar(20) NOT NULL COMMENT '应用名称',
  `app_version_detail` varchar(100) NOT NULL COMMENT '应用的版本',
  `app_opera_type` varchar(50) NOT NULL COMMENT '操作类型',
  `app_ip_detail` varchar(50) NOT NULL COMMENT '应用IP',
  `app_opera_detail` varchar(1000) DEFAULT NULL COMMENT '操作详情',
  `app_opera_status` varchar(50) DEFAULT NULL COMMENT '操作状态:success-正常；fail-失败；publishing-发布中；rollbacking-回滚中',
  `opera_start_time` varchar(30) DEFAULT NULL COMMENT '操作开始时间',
  `opera_end_time` varchar(30) DEFAULT NULL COMMENT '操作结束时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_version_type_ip` (`app_name_detail`,`app_version_detail`,`app_opera_type`,`app_ip_detail`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='发布历史记录表';
