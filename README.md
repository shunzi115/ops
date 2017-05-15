# ops
ops 运维管理平台演进

1.#### 安装数据库 ####

yum -y remove mariadb-libs.x86_64 1:5.5.52-1.el7

wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm

rpm -ivh mysql57-community-release-el7-11.noarch.rpm

yum -y install mysql-community-server.x86_64 mysql-community-devel.x86_64 mysql-community-client.x86_64 mysql-connector-python.x86_64

yum -y install MySQL-python python-devel

2.#### 安装 flask ####

pip  install  flask

3.#### 数据库操作 ####

create database dev_ops;

use dev_ops;

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

INSERT INTO `dev_ops`.`users` (`login_name`, `name_cn`, `password`, `mobile`, `email`, `role`, `status`, `update_time`, `last_login_time`) VALUES ( 'admin', '诸葛孔明', '4bfd3be6dbd0c6888250de0640ec5905', '15811110333', '111@111.com', '0', '0', '2017-05-07 22:20:13', '2017-05-14 16:03:42');


CREATE TABLE `serverinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `HostName` varchar(20) NOT NULL COMMENT '主机名',
  `PrivateIP` varchar(15) NOT NULL COMMENT '私网IP',
  `PublicIP` varchar(15) DEFAULT NULL COMMENT '公网IP',
  `ENV` varchar(50) NOT NULL COMMENT '所属环境',
  `ServerBrand` varchar(50) DEFAULT NULL COMMENT '服务器品牌',
  `ServerModel` varchar(50) DEFAULT NULL COMMENT '服务器型号',
  `OS` varchar(50) NOT NULL COMMENT '系统版本',
  `Kernel` varchar(50) NOT NULL COMMENT '内核版本',
  `CpuType` varchar(50) NOT NULL COMMENT 'CPU类型',
  `CpuCount` tinyint(2) NOT NULL COMMENT 'CPU数量',
  `RAM_GB` tinyint(3) NOT NULL COMMENT '内存',
  `PhyDiskSize` varchar(50) NOT NULL COMMENT '物理磁盘',
  `IDC` varchar(50) NOT NULL COMMENT '归属机房',
  `status` tinyint(2) NOT NULL COMMENT '服务器状态：0-在线,1-下线',
  `OnlineTime` varchar(30) NOT NULL COMMENT '上线时间',
  `OfflineTime` varchar(30) DEFAULT NULL COMMENT '下线时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_private_ip` (`PrivateIP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务器资产信息表';

INSERT INTO `dev_ops`.`serverinfo` (`id`, `HostName`, `PrivateIP`, `PublicIP`, `ENV`, `ServerBrand`, `ServerModel`, `OS`, `Kernel`, `CpuType`, `CpuCount`, `RAM_GB`, `PhyDiskSize`, `IDC`, `status`, `OnlineTime`, `OfflineTime`) VALUES ('1', '10-32-48-164', '10.32.48.164', '202.183.25.138', 'online', 'Dell Inc.', 'OptiPlex 7040', 'CentOS 6.8', '2.6.32-642.el6.x86_64', 'Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz', '8', '15', 'sda:1.5T', '阿里云华东1区', '0', '2017-05-14 22:37:17', NULL);


