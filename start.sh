#!/bin/bash
source /etc/profile

#变量
PHY_MEM_SIZE="$(cat /proc/meminfo |grep MemTotal|awk '{print $2/1024}')"
XMS_SIZE=`awk 'BEGIN{print int(int("'$PHY_MEM_SIZE'")*0.4)}'`
XMX_SIZE=`awk 'BEGIN{print int(int("'$PHY_MEM_SIZE'")*0.8)}'`
IP=`ip addr |grep ens192 | grep inet |egrep -v "inet6|127.0.0.1" |awk '{print $2}' |awk -F "/" '{print $1}' |  awk -F "." '{print $4}'`

# 启动之前,请修改以下两个变量的值.
PackageName=jar包名
AppName=项目名

#启动命令
echo "--------starting------->>"
nohup java -Xms${XMS_SIZE}m -Xmx${XMX_SIZE}m -XX:-UseGCOverheadLimit -Ddubbo.shutdown.hook=true -javaagent:/opt/pp-agent/pinpoint-bootstrap-1.8.1.jar -Dpinpoint.agentId=$AppName-${IP} -Dpinpoint.applicationName=$AppName -jar /opt/$AppName/$PackageName &
