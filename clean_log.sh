#!/bin/bash
source /etc/profile

#你需要修改的参数,改成对应的项目名
AppName=(cjb-service)

for i in ${AppName[@]}
do
	if [ -f "/opt/${i}.log" ];then
		find /opt -name "${i}*" -mtime +3 -exec rm -rf {} \;
	else
        echo '文件不存在'
	fi
done
