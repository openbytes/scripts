# coding=utf8
import time
import requests
import json

DingAPI = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxx'

headers = {'Content-Type': 'application/json;charset=utf-8'}


def recover(app, describe):
    """
    发送钉钉恢复信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "推广业务接口恢复",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#00dd00\">推广业务接口恢复</font><br /> \n\n" +
                    "> ### 项目名称: {app}\n\n".format(app=app) +
                    "> ### 项目: {describe}\n\n".format(describe=describe)
        },
        "at": {
            "atMobiles": [
                "xxxxxxxxxxx"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


def alarm(app, describe):
    """
    发送钉钉报警信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "推广业务接口异常",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#dd0000\">推广业务接口异常</font><br /> \n\n" +
                    "> ### 项目名称: {app}\n\n".format(app=app) +
                    "> ### 项目描述: `{describe}`\n\n".format(describe=describe)
        },
        "at": {
            "atMobiles": [
                "xxxxxxxxxxx"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)
