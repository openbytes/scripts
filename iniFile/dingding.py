# coding=utf8
import time
import requests
import json

DingAPI = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers = {'Content-Type': 'application/json;charset=utf-8'}


def recover(app, IP):
    """
    发送钉钉恢复信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "App分发网站恢复",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#00dd00\">App分发网站恢复</font><br /> \n\n" +
                    "> ### 主机IP: {IP}\n\n".format(IP=IP) +
                    "> ### 项目名称: {app}\n\n".format(app=app)

        },
        "at": {
            "atMobiles": [
                "xxxxxxxxxxxx"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


def alarm(app, IP):
    """
    发送钉钉报警信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "App分发网站异常",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#dd0000\">App分发网站异常</font><br /> \n\n" +
                    "> ### 主机IP: `{IP}`\n\n".format(IP=IP) +
                    "> ### 项目名称: {app}\n\n".format(app=app)

        },
        "at": {
            "atMobiles": [
                "xxxxxxxx"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)
