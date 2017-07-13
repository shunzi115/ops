#!/bin/bash

for ((i=1;i<3;i++))
  do
     echo
     echo "稍等片刻,脚本正在执行中......"
     echo -e "\033[31m[WARNING]: 没有haha.tar.gz,请相关人员排查\033[37m"
     sleep 2s
     ping -c 10 www.baidu.com
  done
