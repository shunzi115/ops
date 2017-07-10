#!/bin/bash

for ((i=1;i<10;i++))
  do
     echo -e "\033[31m[WARNING]: 没有haha.tar.gz,请相关人员排查\033[37m"
     sleep 2s
     ping -c 10 www.baidu.com
  done
