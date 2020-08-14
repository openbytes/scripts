# coding=utf8

import datetime
import pymysql
import calendar

'''创建连接'''
db_config = {
    "host": '172.10.4.92',
    "port": 3306,
    "user": 'root',
    "passwd": '123456',
    "db": 'dianyou',
    "charset": 'utf8'
}
conn = pymysql.connect(
    host='172.10.4.92',
    port=3306,
    user='root',
    passwd='123456',
    db='dianyou',
    charset='utf8'
)

phone_info = {
    "王维": "13128843121",
    "于华云": "13728618304",
    "雷善义": "15361503661"
}

duty_people_info = ['王维', '于华云', '雷善义']
# duty_people_info = ['肖恒', "陈锦龙"]
weekdays = {0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四", 4: "星期五", 5: "星期六", 6: "星期天"}


def duty_yestoday():
    """:arg
    昨天值班的人
    """
    cursor = conn.cursor()
    cursor.execute(
        "select * from duty_dutytable where duty_day='{0}'".format(datetime.date.today() + datetime.timedelta(days=-1)))
    res = cursor.fetchone()
    return res[3]


def leap_year():
    """
    判断是否为闰年
    :return:
    """
    current_year = datetime.datetime.now().year
    try:
        datetime.datetime.strptime("{}-02-29".format(current_year), "%Y-%m-%d")
        return True
    except:
        return False


def nums_of_days():
    "当月有几天"
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    return calendar.monthrange(current_year, current_month)[1]


def main():
    count = 0
    cursor = conn.cursor()
    for i in range(nums_of_days()):
        # for i in range(month_day[str(datetime.datetime.now().month)]):  # 本月的天数
        # 今天的日期: datetime.date.today()
        # 距离今天几天的日期: datetime.date.today() + datetime.timedelta(days=+i)
        today = datetime.date.today() + datetime.timedelta(days=+i)  # 当天日期
        # 当天值班的人
        current_duty_people = duty_people_info[
            (duty_people_info.index(duty_yestoday()) + 1 + i) % len(duty_people_info)]
        # 当天值班是周几
        current_duty_weekday = weekdays[datetime.date.weekday(today)]
        SQL = "insert into duty_dutytable (duty_day,duty_week_day,duty_people,phone) values ('{0}','{1}','{2}','{3}')".format(
            today, current_duty_weekday, current_duty_people, phone_info[current_duty_people])
        cursor.execute(SQL)  # 执行sql
        conn.commit()  # 提交事务
    cursor.close()  # 游标关闭
    conn.close()  # 连接关闭


def third_day():
    count = 0
    cursor = conn.cursor()
    for i in range(nums_of_days()):
        # for i in range(month_day[str(datetime.datetime.now().month)]):  # 本月的天数
        # 今天的日期: datetime.date.today()
        # 距离今天几天的日期: datetime.date.today() + datetime.timedelta(days=+i)
        today = datetime.date.today() + datetime.timedelta(days=+i)  # 当天日期
        # 当天值班的人
        current_duty_people = duty_people_info[
            (duty_people_info.index(duty_yestoday()) + 1 + i) % len(duty_people_info)]
        # 当天值班是周几
        current_duty_weekday = weekdays[datetime.date.weekday(today)]
        SQL = "insert into duty_dutytable (duty_day,duty_week_day,duty_people,phone) values ('{0}','{1}','{2}','{3}')".format(today, current_duty_weekday, current_duty_people, phone_info[current_duty_people])

        cursor.execute(SQL)  # 执行sql
        conn.commit()  # 提交事务
    cursor.close()  # 游标关闭
    conn.close()  # 连接关闭


if __name__ == '__main__':
    # main()
    third_day()
