# coding=utf8
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import pymysql
import requests
import datetime
import json

headers = {'Content-Type': 'application/json;charset=utf-8'}
DingAPI = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxx"


class ConnDB:
    def __init__(self):
        self.host = "1.1.1.1"
        self.user = "root"
        self.password = "123456"
        self.db = "db"

    def connection_db(self, sql):
        conn = pymysql.connect(self.host, self.user, self.password, self.db)
        cursor = conn.cursor()
        cursor.execute(sql)
        content = cursor.fetchone()
        return content


def alert(day, person1, person2, phone1, week, phone2):
    """
    自动发送值班消息
    :return:
    """
    msg = """
> ### 值班日期: {day}({week})

> ### 值班时间: 18:30-01:00(第二天) | 06:00-09:00(第二天)

> ### 业务值班人员: <font color="#dd0000">{person1}({phone1})</font><br />

> ### 监控值班人员: <font color="#dd0000">{person2}({phone2})</font><br />

> ### 值班详情: 戳我查看详情--->[值班](http://zhiban.chigua.cn:10002/)
""".format(day=day, person1=person1, person2=person2, phone1=phone1, week=week, phone2=phone2)
    contents = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日值班信息",
            "text": msg
        },
        "at": {
            "isAtAll": True
        }
    }
    print(requests.post(DingAPI, data=json.dumps(contents), headers=headers).json())

if __name__ == '__main__':
    # 今天(业务值班)
    today = str(datetime.date.today())
    # 前天(监控值班).三个人值班是-2,四个人值班就是-3,依次类推
    day_before_yestoday = str((datetime.datetime.now() + datetime.timedelta(days=-2)).strftime("%Y-%m-%d"))
    # 明天值班(监控值班)
    tomorrow = str((datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d"))
    a = ConnDB()  # 连接数据库
    # 今天的值班人员
    today_content = a.connection_db(f"select * from duty_dutytable where duty_day = '{today}'")
    # 前天值班的人员
    day_before_yestoday_content = a.connection_db(
        f"select * from duty_dutytable where duty_day = '{day_before_yestoday}'")
    # 明天值班人员
    tomorrow_content = a.connection_db(
        f"select * from duty_dutytable where duty_day = '{tomorrow}'")
    # 如果今天和明天都有记录,直接从数据库里面拿数据
    if today_content and tomorrow:
        alert(day=today, person1=today_content[3], person2=tomorrow_content[3], phone1=today_content[4],
              week=today_content[2], phone2=tomorrow_content[4])
    # 如果明天没有记录,业务值班人员信息直接去前天的人员
    # 值班信息是一个月生成一次,月底最后一天获取第二天的值班人员是没有数据的.所以是取前天的人员.
    # 如果是4个人值班,那么就取大前天的人员.
    else:
        alert(day=today, person1=today_content[3], person2=day_before_yestoday_content[3], phone1=today_content[4],
              week=today_content[2], phone2=day_before_yestoday_content[4])
