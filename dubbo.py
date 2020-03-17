# coding=utf8


import json
import time
from urllib.parse import unquote

from kazoo.client import KazooClient
import pymysql
import requests

query_sql_api = "select * from dubbo where service_type='api'"
query_sql_base = "select * from dubbo where service_type='base'"
query_sql = "select * from dubbo"
DingDingWebHook = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
headers = {'Content-Type': 'application/json;charset=utf-8'}


def query_db(SQL):
    """:arg
    查询数据库
    """
    conn = pymysql.connect(
        host='172.10.4.92',
        user='root',
        password='123456',
        db='monitor',
        charset='utf8mb4'
    )
    try:
        cur = conn.cursor()
        cur.execute(SQL)
        content = cur.fetchall()
        return content
    except:
        return "DB is not connection"


def update_db(SQL):
    """:arg
    更新服务的状态码
    """
    conn = pymysql.connect(
        host='172.10.4.92',
        user='root',
        password='123456',
        db='monitor',
        charset='utf8mb4'
    )
    try:
        cur = conn.cursor()
        cur.execute(SQL)
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass


def dubbo():
    """
    检查zk里面的服务节点数
    :return:
    """
    data = {}  # 返回数据的字典
    svc_list = []  # 单节点服务列表
    nosvc_list = []  # 无服务节点列表
    start = time.time()
    zk = KazooClient(hosts='172.10.x.x:2181')
    zk.start()
    for service in query_db(query_sql):
        if service[3] == 'base':
            if zk.exists('/dubbo/{serviceName}/providers'.format(serviceName=service[1])):
                node = zk.get_children('/dubbo/{serviceName}/providers'.format(serviceName=service[1]))
                if len(node) < 1:
                    svc_list.append(service)
                    data["SingleSvc"] = svc_list
                else:
                    pass
            else:
                nosvc_list.append(service)
                data["WithoutSvc"] = nosvc_list
        else:
            if zk.exists('/dubbo/{serviceName}/consumers'.format(serviceName=service[1])):
                node = zk.get_children('/dubbo/{serviceName}/consumers'.format(serviceName=service[1]))
                if str(node).count("{service}".format(service=service[1])) < 1:
                    svc_list.append(service)
                    data["SingleSvc"] = svc_list
            else:
                nosvc_list.append(service)
                data["WithoutSvc"] = nosvc_list

    zk.stop()
    stop = time.time()
    coast = stop - start
    return data


def alarm(proName, svcName, num):
    """
    发送钉钉报警信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "服务注册异常",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#660000\">服务注册异常</font><br /> \n\n" +
                    "> ### 项目名:{proName} \n\n".format(proName=proName) +
                    "> ### 服务名: {svcName}\n\n".format(svcName=svcName) +
                    "> ### 服务节点数: {num}".format(num=num)
        },
        "at": {
            "atMobiles": [
                "131xxxxxxxx", "131xxxxxxx"
            ],
            "isAtAll": False
        }
    }

    requests.post(DingDingWebHook, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


if __name__ == '__main__':
    # keys = ["SingleSvc", "WithoutSvc"]
    start = time.time()
    print(json.dumps(dubbo()))
    if len(dubbo()) == 1:
        if "SingleSvc" in dubbo():
            for item in dubbo()["SingleSvc"]:
                alarm(item[0],item[1],1)
        elif "WithoutSvc" in dubbo():
            for item in dubbo()["WithoutSvc"]:
                alarm(item[0],item[1],0)
    elif len(dubbo()) == 2:
        for item in dubbo()["SingleSvc"]:
            alarm(item[0], item[1], 1)
        for item in dubbo()["WithoutSvc"]:
            alarm(item[0], item[1], 0)
    else:
        print("I'm OK")
        pass
        # 如果dubbo()为空,需要查询数据库,判断是否需要发送恢复通知.
    stop = time.time()
    print(stop - start)
