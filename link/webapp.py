# coding=utf8

from orm import *


def create_table(table):
    u"""
    如果table不存在，新建table
    """
    if not table.table_exists():
        table.create_table()
        table.create(id=1, appName='dy_circle_page', link="https://example.com/circle/getDownLink", statusCode=1,
                     describe="app下载二维码页面")
        table.create(id=2, appName='payfor', link="https://example.com/payfor/pay", statusCode=1,
                     describe="支付页面二维码")


def drop_table(table):
    u"""
    table 存在，就删除
    """
    if table.table_exists():
        table.drop_table()


def query_table(table,n):
    data = []
    if table.table_exists:
        query = table.select().where(table.statusCode == n)
        for i in range(len(query)):
            data.append(query[i].appName)

    return data


def query_describe(table,n):
    data = []
    if table.table_exists:
        query = table.select().where(table.link == n)
        for i in range(len(query)):
            data.append(query[i].describe)

    return data


def update_table(table, n, name):
    if table.table_exists:
        update = table.update(statusCode=n).where(table.appName == name).execute()
        if update:
            return True
        else:
            return False

