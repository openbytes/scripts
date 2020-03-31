# coding=utf8
__data__ = '2019/11/19'
__author__ = 'Administrator'

# coding=utf8

import paramiko
import time
import requests
import json
import pymysql

APP_INFO_LIST = [
    [["172.10.4.15"], "root", "xxxxxx", "ReadCrawlerKafka"]
]

APP_PROJECT_DICT = {"doc2vec": "咨询去重分类"
                    }

DingAPI = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers = {'Content-Type': 'application/json;charset=utf-8'}


def query_db(SQL):
    conn = pymysql.connect(
        host='172.10.4.92',
        user='root',
        password='xxxxx',
        db='monitor',
        charset='utf8'
    )
    try:
        cur = conn.cursor()
        cur.execute(SQL)
        content = cur.fetchall()
        return content
    except:
        return "DB is not connection"


def update_db(SQL):
    conn = pymysql.connect(
        host='172.10.4.92',
        user='root',
        password='xxxxxx',
        db='monitor',
        charset='utf8'
    )
    try:
        cur = conn.cursor()
        cur.execute(SQL)
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass


def sshConnect(ip, password, cmd_args):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username='root', password=password, timeout=60)
        stdin, stdout, stderr = ssh.exec_command('ps -ef | grep -v grep | grep ' + cmd_args, get_pty=True)
        channel = stdout.channel
        status = channel.recv_exit_status()
        ssh.close()
        return status
    except:
        return False


def restart(ip, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username='root', password=password, timeout=60)
        stdin, stdout, stderr = ssh.exec_command("source /etc/profile;cd /zywa/python_doc2vec_kafka;sh start.sh",
                                                 get_pty=True)
        channel = stdout.channel
        status = channel.recv_exit_status()
        ssh.close()
        return status
    except:
        return False


def alarm(host, info):
    """
    发送钉钉报警信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "咨询去重分类进程异常",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#660000\">咨询去重分类进程异常</font><br /> \n\n" +
                    "> ### 主机: {host}\n\n".format(host=host) +
                    "> ### 进程: {info}\n\n".format(info=info) +
                    "> ### 正在尝试重启进程!!!"
        },
        "at": {
            "atMobiles": [
                "13612919120", "13128841321"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


def recover(host, info):
    """
    发送钉钉恢复信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "咨询去重分类已恢复",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#00dd00\"></font>咨询去重分类已恢复<br /> \n\n" +
                    "> ### 主机: {host}\n\n".format(host=host) +
                    "> ### 进程: {info}\n\n".format(info=info) +
                    "> ### 重启成功!!!"

        },
        "at": {
            "atMobiles": [
                "13612919120", "13128841321"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


def restartSuccess(host, info):
    """
    发送钉钉恢复信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "咨询去重分类重启成功",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#00dd00\"></font>咨询去重分类已重启成功<br /> \n\n" +
                    "> ### 主机: {host}\n\n".format(host=host) +
                    "> ### 进程: {info}\n\n".format(info=info)
        },
        "at": {
            "atMobiles": [
                "xxxxxxxxxx", "xxxxxxxxxxxxx"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


def restartFaild(host, info):
    """
    发送钉钉恢复信息
    :param msg:
    :return:
    """
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": "咨询去重分类重启失败",
            "text": "## %s\n" % time.strftime("%Y-%m-%d %X") +
                    "> ### 状态: <font color=\"#00dd00\"></font>咨询去重分类重启失败<br /> \n\n" +
                    "> ### 主机: {host}\n\n".format(host=host) +
                    "> ### 进程: {info}\n\n".format(info=info)
        },
        "at": {
            "atMobiles": [
                "xxxxxxxxxxxxx", "xxxxxxxxxxxxx"
            ],
            "isAtAll": True
        }
    }

    requests.post(DingAPI, json.dumps(content), headers=headers).content  # 将返回的数据编码成 JSON 字符串)


def status():
    """
    把异常进程的状态码写入到数据库 status=0
    :return:
    """
    result = []
    for i in range(len(APP_INFO_LIST)):
        for j in APP_INFO_LIST[i][0]:
            passwd = APP_INFO_LIST[i][2]
            project = APP_INFO_LIST[i][3]
            codes = sshConnect(ip=j, password=passwd, cmd_args=project)
            if codes != 0:
                result.append({'HOST': j, '咨询去重分类进程': project})
                # update_db("update doc2vec set Status =0 where IP ='{host}' and SPIDER ='{project}'".format(host=j,
                #                                                                                          project=project))
    return result


if __name__ == '__main__':
    monitor_status = status()
    if monitor_status:
        for i in range(len(monitor_status)):
            host = monitor_status[i]['HOST']
            spiderProcess = monitor_status[i]['咨询去重分类进程']
            alarm(host, spiderProcess)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname="172.10.4.15", port=22, username='root', password="xxxxxxxxx", timeout=60)
            stdin, stdout, stderr = ssh.exec_command(
                "source /etc/profile;cd /opt/python_doc2vec_kafka/;sh start.sh;ps -ef|grep  ReadCrawlerKafka",
                get_pty=True)
            channel = stdout.channel
            status = channel.recv_exit_status()
            ssh.close()
            # 程序报警之后,修改数据库状态码为0
            update_db(
                "update doc2vec set Status =0 where IP ='{host}' and AppName ='{p}'".format(host=host, p=spiderProcess))
            time.sleep(20)
            if status == 0:
                restartSuccess("172.10.4.15", "doc2vec")
                update_db("update doc2vec set Status =1 where IP ='{host}' and AppName ='{p}'".format(host=host,
                                                                                                      p=spiderProcess))
            else:
                restartFaild("172.10.4.15", "doc2vec")

    else:
        conent = query_db("select * from doc2vec where Status='0'")
        for j in range(len(conent)):
            host = conent[j][1]
            spiderProcess = conent[j][0]
            recover(host, spiderProcess)
            # 程序恢复之后,修改数据库状态码为1
            update_db(
                "update doc2vec set Status =1 where IP ='{host}' and AppName ='{p}'".format(host=host,
                                                                                            p=spiderProcess))
