# coding=utf8

import configparser

configfile = "config.ini"


class Update_Read_Config:

    def __init__(self):
        """
        初始化config实例
        """
        self.cf = configparser.ConfigParser()
        self.cf.read(configfile)

    def read(self, n):
        """
        :param n: 状态码
        :return: 返回特定符合码的列表
        """
        rule = []
        sections = self.cf.sections()
        for section in sections:
            if self.cf.getint(section, "status") == n:
                items = dict(self.cf.items(section))
                rule.append({section: items})
        return rule


    def read_all(self):
        rule = []
        sections = self.cf.sections()
        for section in sections:
            items = dict(self.cf.items(section))
            rule.append(items)

        return rule

    def read_sections(self):
        """
        返回配置文件里面所有的sections
        :return:
        """
        sections = self.cf.sections()
        return sections

    # def read_key(self):
    #     self.read_sections(

    def update(self, section, n):
        """
        更新ini文件
        :param section: 更新的节点
        :param n: 更新的值
        :return: 不返回,不做判断
        """
        self.cf.set(section, "status", n)
        with open(configfile, "w") as f:
            self.cf.write(f)
