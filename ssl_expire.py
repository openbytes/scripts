# coding=utf-8

import ssl
import socket
import time
import datetime
from ssl_vaild import dingding


class SSL_expire:

    def __init__(self, hostname):
        self.hostname = hostname

    def cert_info(self):
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=self.hostname) as s:
            s.connect((self.hostname, 443))
            cert = s.getpeercert()
        return cert

    def notafter(self):
        """
        证书过期时间
        :return:
        """
        return self.cert_info()["notAfter"]
        # pass

    def notbefore(self):
        """
        证书申请时间
        :return:
        """
        return self.cert_info()["notBefore"]

    def format_gmt_time(self, start_date):
        """
        格式化格林威治时间为北京时间
        :return:
        """
        gmt_time = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
        gmt_format = time.strftime("%Y-%m-%d", gmt_time)
        return gmt_format

    def issuer(self):
        """
        返回域名通用名
        :return:
        """
        subject = dict(x[0] for x in self.cert_info()['subject'])
        return subject["commonName"]


if __name__ == '__main__':
    domain_list = ["oauth.idianyou.cn", "oauth.chigua.cn", "im.api.chigua.cn", "app.ineice.cn"]

    for domain in domain_list:
        try:
            cert = SSL_expire(domain)
            apply_time = cert.format_gmt_time(cert.notbefore())  # 申请时间(GMT格式)
            expire_day = cert.format_gmt_time(cert.notafter())  # 过期时间(GMT格式)
            current_day = datetime.datetime.now().strftime("%Y-%m-%d")  # 当前时间()
            current_day_str = datetime.datetime.strptime(current_day, "%Y-%m-%d")
            expire_day_str = datetime.datetime.strptime(expire_day, "%Y-%m-%d")
            left_days = (expire_day_str - current_day_str).days
            if left_days < 120:  # 小于120天就报警.每天执行一次.
                print("通用名: ", cert.issuer())
                print("申请时间: ", apply_time)
                print("过期时间: ", expire_day)
                print("当前时间: ", current_day)
                print("剩余时间: ", left_days)
                print("*" * 30)
                dingding.alarm(cert.issuer(), apply_time, expire_day, left_days)
            else:
                pass
        except Exception as e:
            print("域名不可用", domain)
