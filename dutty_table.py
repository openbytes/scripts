# coding=utf8

import datetime
# import pymysql
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
# conn = pymysql.connect(
#     host='172.10.4.92',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='dianyou',
#     charset='utf8'
# )

phone_info = {
    "王维": "131xxxxxxxxxxxx",
    "于华云": "137xxxxxxxxxxx",
    "雷善义": "153xxxxxxxxxxx"
}

duty_people_info = ['王维', '于华云', '雷善义']
weekdays = {0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四", 4: "星期五", 5: "星期六", 6: "星期天"}


def leap_year():
    """
    判断是否为闰年
    :return:
    """
    current_year = datetime.datetime.now().year
    return datetime.datetime.strptime("{}-02-29".format(current_year), "%Y-%m-%d")
  


def nums_of_days():
    "当月有几天"
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    return calendar.monthrange(year, month)[1]


def left_days():
    """执行脚本当前的日期距离月底剩余的天数"""
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    end = nums_of_days()
    current_date = f"{year}-{month}-{day}"
    # start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{end}"
    format_start_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    format_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    return (format_end_date - format_start_date).days +1


def main():
    # cursor = conn.cursor()
    for i in range(left_days()):
        # for i in range(month_day[str(datetime.datetime.now().month)]):  # 本月的天数
        # 今天的日期: datetime.date.today()
        # 距离今天几天的日期: datetime.date.today() + datetime.timedelta(days=+i)
        today = datetime.date.today() + datetime.timedelta(days=+i)  # 当天日期
        # if duty_yestoday():
        if True:
            # 当天值班的人
            current_duty_people = duty_people_info[
                # (duty_people_info.index(duty_yestoday()) + 1 + i) % len(duty_people_info)]
                (duty_people_info.index("王维") + 1 + i) % len(duty_people_info)]
            # 当天值班是周几
            current_duty_weekday = weekdays[datetime.date.weekday(today)]
            SQL = "insert into duty_dutytable (duty_day,duty_week_day,duty_people,phone) values ('{0}','{1}','{2}','{3}')".format(
                today, current_duty_weekday, current_duty_people, phone_info[current_duty_people])
            # return  SQL
            print(today,current_duty_people)
            # cursor.execute(SQL)  # 执行sql
            # conn.commit()  # 提交事务
            # return "Error duty_yesterday 方法数据返回为空,请检查数据是否正确"
    # cursor.close()  # 游标关闭
    # conn.close()  # 连接关闭

if __name__ == '__main__':
    main()
