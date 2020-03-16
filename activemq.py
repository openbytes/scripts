#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import os
import sys
import commands
import pycurl
import StringIO
import requests
import json
import time

DingAPI = "https://xxxxxxxxxxxx" # 这里的url就是webhook的Api接口
headers = {'Content-Type': 'application/json;charset=utf-8'}


if len(sys.argv) != 2:
    print 'Usage:python check_amq.py ip queue'
    exit(1)

ip_input = sys.argv[1]
queue_input ="dev_im_push_private_notice"
hosts = ['110']


def getpendingData():
    count = 0
#判断集群61616端口在哪台服务器启动
    for host in hosts:
        order1 = 'nc -z ' + '172.x.x.' + host + ' 61616'
        #print order
        output1 = commands.getstatusoutput(order1)
        status1 = int(output1[0])
        if status1 == 0:
            ip = host
            count = count + 1
            #判断集群的8161端口在哪台服务器启动，并获取监控数据
            order2 = 'nc -z ' + '172.x.x.' + host + ' 8161'
            output2 = commands.getstatusoutput(order2)
            status2 = int(output2[0])
            if status2 == 0:
                #从此url中获取监控数据
                url = 'http://172.x.x.' + ip + ':8161/admin/queues.jsp'
                #print url
                curl = pycurl.Curl()
                body = StringIO.StringIO()
                curl.setopt(pycurl.URL, url)
                curl.setopt(pycurl.USERPWD, 'admin:admin')
                #连接时间
                curl.setopt(pycurl.CONNECTTIMEOUT, 5)
                #超时时间
                curl.setopt(pycurl.TIMEOUT, 5)
                #写回调
                curl.setopt(pycurl.WRITEFUNCTION, body.write)

                curl.perform()
                response =  body.getvalue()

                body.close()
                curl.close()

                lines = response.split('\n')
                data = {}
                #获取每个队列的名称,pending,consumers,enqueue,dequeue
                for i in range(len(lines)):
                    #for k in queue_list:
                        temp = queue_input + '</a></td>'
                        if  lines[i].find(temp) == 0:
                            queue = lines[i].strip('</td>').rstrip('</a')
                            pending = lines[i+1].strip('</td>')
                            consumers = lines[i+2].strip('</td>')
                            enqueue = lines[i+3].strip('</td>')
                            dequeue = lines[i+4].strip('</td>')

                            data["Pending Message"]=pending
                            data["Queue"]=queue_input
    #集群中有一台存活即正常,没有存活即集群无法对外提供服务;另收集集群8161web页面的数据用于监控队列情况
    #if count == 1:
    #    data = {}
        # print 'OK:activemq ' + ip + ' is online|pending=' + pending + ';consumers=' + consumers + ';enqueue='+ enqueue + ';dequeue=' + dequeue
        # print 'OK:activemq ' + ip + ' is online|pending=' + pending + ';consumers=' + consumers + ';enqueue='+ enqueue + ';dequeue=' + dequeue
    #    data["Pending Message"]=pending
    #    data["Queue"]=queue_input
                return data

        # exit(0)
    #else :
    #    print 'ERROR:all activemq are offline'
    #    exit(2)


def alter_error(msg):
    """
    发送钉钉报警信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Activemq 消息已堵塞!!!",
            "text": msg
        },
        "at": {
            "atMobiles": [
                "xxxx"
            ],
            "isAtAll": True
        }
    }

    print(requests.post(DingAPI, json.dumps(content), headers=headers).json())  # 将返回的数据编码成 JSON 字符串)


def alter_ok(msg):
    """
    发送钉钉报警信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Activemq 已恢复",
            "text": msg
        },
        "at": {
            "atMobiles": [
                "xxxx"
            ],
            "isAtAll": True
        }
    }

    print(requests.post(DingAPI, json.dumps(content), headers=headers).json())  # 将返回的数据编码成 JSON 字符串)


if __name__ == '__main__':
    data=getpendingData()
    print(data)
    error_msg = """
> ### 告警时间: {t}

> ### 告警类型: <font color="#FF0000">Activemq 消息已堵塞</font><br />

> ### 堵塞数量: `{pending}`条

> ### 堵塞队列: `{queue}`
    """.format(t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), pending=data["Pending Message"], queue=queue_input)

    ok_msg = """
> ### 恢复时间: {t}

> ### 恢复类型: <font color="#00dd00">Activemq 消息堵塞已恢复</font><br />

> ### 堵塞数量: `{pending}`条

> ### 恢复队列: `{queue}`
    """.format(t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), pending=data["Pending Message"], queue=queue_input)
    if int(data["Pending Message"])>=10:
        with open("/opt/yunwei/count.txt","w") as f:
            alter_error(error_msg)
            f.write("error\n")
            print(data["Pending Message"])
            print(type(data["Pending Message"]))
    else:
        with open("/opt/yunwei/count.txt","a+") as file:
            lines = file.readlines()
            if lines[-1].strip()=="error":
                alter_ok(ok_msg)
                file.write("ok\n")
