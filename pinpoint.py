#!/usr/local/bin/python
# 功能：调用pinpoint接口，监控每个应用的调用错误数，并将告警信息发送到钉钉。
import sys
import os
import requests
import time
import datetime
import json
from multiprocessing import Process
from dingtalkchatbot.chatbot import DingtalkChatbot  # pip install dingtalkchatbot

'''获取最近1分钟内的时间戳'''
From_Time = datetime.datetime.now() + datetime.timedelta(seconds=-60)
To_Time = datetime.datetime.now()
From_TimeStamp = int(time.mktime(From_Time.timetuple())) * 1000
To_TimeStamp = int(time.mktime(datetime.datetime.now().timetuple())) * 1000

webhook = "https://oapi.dingtalk.com/robot/send?access_token=1111111111111111111111111111"

PPURL = "http://172.10.x.c:8079"


def get_applications():
    '''return application dict
    '''
    applicationListUrl = PPURL + "/applications.pinpoint"
    res = requests.get(applicationListUrl)
    if res.status_code != 200:
        print("请求异常,请检查")
        return
    applicationLists = []
    for app in res.json():
        applicationLists.append(app)
    applicationListDict = {}
    applicationListDict["applicationList"] = applicationLists
    print(applicationListUrl)
    return applicationListDict


'''传入服务名，返回该服务的节点数和各节点的节点名'''


def getAgentList(appname):
    AgentListUrl = PPURL + "/getAgentList.pinpoint"
    param = {
        'application': appname
    }
    res = requests.get(AgentListUrl, params=param)
    if res.status_code != 200:
        print("请求异常,请检查")
        return
    return len(res.json().keys()), json.dumps(list(res.json().keys()))


'''获取调用失败次数'''


def update_servermap(appname, from_time=From_TimeStamp, to_time=To_TimeStamp, serviceType='TOMCAT'):
    '''更新app上下游关系
    :param appname: 应用名称
    :param serviceType: 应用类型
    :param from_time: 起始时间
    :param to_time: 终止时间
    :
    '''
    # https://pinpoint.*****.com/getServerMapData.pinpoint?applicationName=test-app&from=1583808042000&to=1583808642000&callerRange=1&calleeRange=1&serviceTypeName=TOMCAT&_=1547720614229
    param = {
        'applicationName': appname,
        'from': from_time,
        'to': to_time,
        'callerRange': 1,
        'calleeRange': 1,
        'serviceTypeName': serviceType
    }

    # serverMapUrl = PPURL + "/getServerMapData.pinpoint"
    serverMapUrl = "{}{}".format(PPURL, "/getServerMapData.pinpoint")
    res = requests.get(serverMapUrl, params=param)
    if res.status_code != 200:
        print("请求异常,请检查")
        return
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    links = res.json()["applicationMapData"]["linkDataArray"]
    # links包含该app的上下游调用关系链，以及相互之间调用的次数和失败的次数等信息。
    # print(links)
    # print(len(links))
    #    totalCount=0
    # errorCount = 0
    slowCount = 0
    errorCount = 0
    for link in links:
        ###排除test的应用
        if link['sourceInfo']['applicationName'].startswith('test'):
            continue
        # 应用名称、应用类型、下游应用名称、下游应用类型、应用节点数、下游应用节点数、总请求数、 错误请求数、慢请求数(本应用到下一个应用的数量)
        #        application = link['sourceInfo']['applicationName']
        #        serviceType = link['sourceInfo']['serviceType']
        #        to_application = link['targetInfo']['applicationName']
        #        to_serviceType = link['targetInfo']['serviceType']
        #        agents = len(link.get('fromAgent',' '))
        #        to_agents =  len(link.get('toAgent',' '))
        '''总错误数进行累计'''
        # errorCount += link['totalCount']
        errorCount += link['errorCount']
        slowCount += link['slowCount']

    # return totalCount
    # return errorCount
    return {"slowCount": slowCount, "errorCount": errorCount}


'''原生钉钉报警，此脚本中没用到'''


def messages(application_name, service_type, slow_count):  # 定义信息函数
    headers = {'Content-Type': 'application/json;charset=utf-8'}  # 头部信息，Zabbix官方文档写法，可以查看zabbix官方文档
    text = """
报警策略：SLOW COUNT
报警内容：SLOW COUNT value is {slow_count} during the past 5 mins.
服务类型：{service_type}
   服务名：{application_name}
""".format(slow_count=slow_count, service_type=service_type, application_name=application_name)
    text_info = {  # 编写规则可以查看Zabbix官方文档的Zabbix Api
        "msgtype": "text",
        "at": {
            "atMobiles": [
                "13128841321", "13728978429"
            ],
            "isAtAll": False
        },
        "text": {
            "content": text
        }
    }

    print(requests.post(webhook, json.dumps(text_info), headers=headers).content)
    # for i in webhook_list:
    #     将返回的数据编码成 JSON 字符串
    requests.post(webhook, json.dumps(text_info), headers=headers).content  # 将返回的数据编码成 JSON 字符串


if __name__ == "__main__":
    #    start = time.time()
    '''初始化钉钉对象'''
    xiaoding = DingtalkChatbot(webhook)
    at_mobiles = ['131xxxxxxxxxxxxxx']
    '''获取所有服务的app名和服务类型，并存到字典中'''
    applicationLists = get_applications()
    # applicationLists = [x for x in get_applications() if 'dute-chigua-manager' not in x["applicationName"]]
    # print(applicationLists)

    '''调试update_servermap函数，需要改动该函数的返回值:totalCount、errotCount、slowCount'''
    # count=update_servermap('push-base', from_time=From_TimeStamp,to_time=To_TimeStamp,serviceType='TOMCAT')
    # print(count)

    '''轮询application，查询每个application在过去一分钟内的总错误数，并通过钉钉报警'''
    for app, v in applicationLists.items():
        for i in range(len(v)):
            application_name = v[i]['applicationName']
            service_type = v[i]['serviceType']
            count = update_servermap(application_name, from_time=From_TimeStamp, to_time=To_TimeStamp,
                                     serviceType=service_type)

            '''如果总调用错误数超过阈值0(根据实际需求进行设置)，则报警'''

            for i in ["slowCount", "errorCount"]:
                if count[
                    i] >= 1 and application_name != 'xx-service' and application_name != 'yy-service:
                    text_error = """
<font color=#FF0000>pinpoint错误报警</font>\n\n
> <font color=#0A0A0A>报警策略：</font>{type}\n\n
> <font color=#0A0A0A>报警内容：</font>{type} value is <font color=#FF0000>{slow_count}</font> during the past 1 mins.\n\n
> <font color=#0A0A0A>服务类型：</font>{service_type}\n\n
> &emsp;<font color=#0A0A0A>服务名：</font>{application_name}
""".format(type=i, slow_count=count[i], service_type=service_type,
           application_name=application_name)
                    text_slow = """
<font color=#FFD700>pinpoint慢查询报警</font>\n\n
> <font color=#0A0A0A>报警策略：</font>{type}\n\n
> <font color=#0A0A0A>报警内容：</font>{type} value is <font color=#FF0000>{slow_count}</font> during the past 1 mins.\n\n
> <font color=#0A0A0A>服务类型：</font>{service_type}\n\n
> &emsp;<font color=#0A0A0A>服务名：</font>{application_name}
""".format(type=i, slow_count=count[i], service_type=service_type,
           application_name=application_name)
                    if i == "slowCount":
                        xiaoding.send_markdown(title='pp报警', text=text_slow, at_mobiles=at_mobiles)
                    elif i == "errorCount":
                        xiaoding.send_markdown(title='pp报警', text=text_error, at_mobiles=at_mobiles)
                else:
                    pass
