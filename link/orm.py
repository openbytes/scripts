# coding=utf8

from peewee import *
import os

db = SqliteDatabase(os.getcwd() + '\\qrcode.db')  # 使用os.getcwd()获取当前文件路径,将当前文件路径下的test.db作为数据库操作对象


class BaseModel(Model):
    class Meta:
        database = db


class App(BaseModel):
    id = PrimaryKeyField()
    appName = CharField()  # string
    link = CharField()  # string
    statusCode = SmallIntegerField()  # int
    describe = CharField()  # string

    # class Meta:
    #     order_by = ('appName',)
    #     db_table = 'app'
