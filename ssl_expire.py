# coding=utf-8
# from urllib3.contrib import pyopenssl as reqs
# from datetime import datetime

# def get_domain_list():
#     obj_list = []
#     with open('domain.txt') as f:
#         for i in f:
#             obj_list.append({'domain': i.split()[0], 'tag': i.split()[1]})
#     return obj_list


# 调用openssl，获取过期时间
# def get_expire_org(url):
#     x509 = reqs.OpenSSL.crypto.load_certificate(reqs.OpenSSL.crypto.FILETYPE_PEM,
#                                                 reqs.ssl.get_server_certificate((url, 443)))
#     return x509.get_issuer().O
#
#
# def get_expire_time(url):
#     cert = reqs.OpenSSL.crypto.load_certificate(reqs.OpenSSL.crypto.FILETYPE_PEM,
#                                                 reqs.ssl.get_server_certificate((url, 443)))
#
#     notafter = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')  # 获取到的时间戳格式是ans.1的，需要转换
#     print(notafter)  # 获取证书到期时间
#     remain_days = notafter - datetime.now()  # 用证书到期时间减去当前时间
#     print(remain_days.days)  # 获取剩余天数


# get_expire_time111("app.ineice.cn")

# import OpenSSL
# import ssl

# def check_cert_valid():
#     domain_list = ["cashapi.chigua.cn", "miniappsapi.idianyou.cn", "miniappsapi.chigua.cn"]
#     # 这里还有一些代码，用来获取域名列表，情况不同，不阐述了
#     for domain in domain_list:  # 这里是一些域名的列表，可以使用其他方式
#         # 这里我直接使用了下述方法来获取证书，并没有将证书写入文件
#         cert = ssl.get_server_certification((domain, 443))  # 一般是443端口,并且这里默认返回
#                                                             # 的是PEM证书
#         # 如果有cert文件的话，直接执行这里
#         # cert_file_path = ''  # cert证书文件路径
#         # cert = open(cert_file_path).read()  # 当然这里也可以使用with来进行上下文管理
#         certification = OpenSSL.crypto.load_certification(OpenSSL.crypto.FILETYPE_PEN, cert)
#         valid_start_time = certification.get_notBefore()  # 有效期起始时间
#         valid_end_time = certification.get_notAfter()  # 有效期结束时间
#         # pass  #  接下来执行各自的操作即可
#
#         print(valid_end_time)

# def main(domain):
#     f = StringIO()
#     comm = f"curl -Ivs https://{domain} --connect-timeout 10"
#     # comm = "curl/ -Ivs https://{domain} --connect-timeout 10"
#
#     result = subprocess.getstatusoutput(comm)
#     f.write(result[1])
#
#     m = re.search('start date: (.*?)\n.*?expire date: (.*?)\n.*?common name: (.*?)\n.*?issuer: CN=(.*?)\n',
#                   f.getvalue(), re.S)
#     start_date = m.group(1)
#     expire_date = m.group(2)
#     common_name = m.group(3)
#     issuer = m.group(4)
#
#     # time 字符串转时间数组
#     start_date = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
#     start_date_st = time.strftime("%Y-%m-%d %H:%M:%S", start_date)
#     # datetime 字符串转时间数组
#     expire_date = datetime.strptime(expire_date, "%b %d %H:%M:%S %Y GMT")
#     expire_date_st = datetime.strftime(expire_date, "%Y-%m-%d %H:%M:%S")
#
#     # 剩余天数
#     remaining = (expire_date - datetime.now()).days
#
#     print('域名:', domain)
#     print('通用名:', common_name)
#     print('开始时间:', start_date_st)
#     print('到期时间:', expire_date_st)
#     print(f'剩余时间: {remaining}天')
#     print('颁发机构:', issuer)
#     print('*' * 30)
#
#     time.sleep(0.5)

# def domain_analysis(domain):
#     """
#     # 查询域名证书到期
#     :param domain:
#     :return:
#     """
#     f = StringIO()
#     try:
#         domain_str = f"curl -vIs https://{domain} --connect-timeout 10"
#         return_code, output = subprocess.getstatusoutput(domain_str)
#
#         m = re.search('SSL connection using (.*?)\n.*?start date: (.*?)\n.*?expire date: (.*?)\n.*?issuer: (.*?)\n.*?',
#                       output, re.S)
#         print(output)
#         if m:
#             start_date = m.groups()[1]
#             expire_date = m.groups()[2]
#             issuer = m.groups()[3]
#             agreement = m.groups()[0]
#             # time 字符串转时间数组
#             start_date = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
#             start_date_st = time.strftime("%Y-%m-%d %H:%M:%S", start_date)
#             # datetime 字符串转时间数组
#             expire_date = datetime.strptime(expire_date, "%b %d %H:%M:%S %Y GMT")
#             expire_date_st = datetime.strftime(expire_date, "%Y-%m-%d %H:%M:%S")
#
#             # 剩余天数
#             # remaining = (expire_date-datetime.now()).days
#             version = ''
#             encryption = ''
#             if agreement:
#                 version = agreement.split(' / ')[0]
#                 encryption = agreement.split(' / ')[1]
#
#             dic = {i.split("=")[0]: i.split("=")[1] for i in issuer.split("; ")}
#             return {
#                 "domain": domain,
#                 "start_date": start_date_st,
#                 "expire_date": expire_date_st,
#                 "issuer": dic['CN'],
#                 "tls_version": version,
#                 "encryption": encryption
#             }
#     except Exception as e:
#         print(e)


import ssl, socket, time, datetime


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
        return SSL_expire.cert_info(self)["notAfter"]
        # pass

    def notbefore(self):
        """
        证书申请时间
        :return:
        """
        return SSL_expire.cert_info(self)["notBefore"]

    def format_gmt_time(self, start_date):
        """
        格式化格林威治时间为北京时间
        :return:
        """
        gmt_time = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
        gmt_format = time.strftime("%Y-%m-%d", gmt_time)
        return gmt_format


# domain_list = ["im.api.chigua.cn"]
# for hostname in domain_list:
#     print(cert)
#     subject = dict(x[0] for x in cert['subject'])  # 域名
#     notBefore = cert['notBefore']  # 申请时间
#     notAfter = cert['notAfter']  # 过期时间
#
#     print("*" * 80)
#     print(subject)
#     print(notBefore)
#     print(notAfter)
#     issued_to = subject['commonName']
# print(issued_to)
#
# issuer = dict(x[0] for x in cert['issuer'])
# issued_by = issuer['commonName']
# print(issued_by)
# print(subject)


# def ssl_expire(domain):
#     current_time=datetime.now().strftime('%Y-%m-%d')
#     print("当前时间:",current_time)
#     gmt_date = "%b %d %H:%M:%S %Y GMT"
#     domain_str = "curl -lvs https://{domain} --connect-timeout 10".format(domain=domain)
#     return_code, output = subprocess.getstatusoutput(domain_str)
#     m = re.search(
#         'subject: (.*?)\n.*?start date:(.*?)\n.*?expire date:(.*?)\n.*?subjectAltName:(.*?)\n.*?issuer:(.*?)\n',
#         output)
#     print('域名:', domain)
#     # print('作用域:', m.group(1))
#     # Nov 11 00:00:00 2019 GMT
#     # print('证书申请时间:', m.group(2))
#     print('证书申请时间-format:', datetime.date(datetime.strptime(m.group(2).strip(), gmt_date)))
#
#     # datetime.strftime("Jun 23 00:00:00 2020 GMT", gmt_date)
#     print('证书过期时间-format:', datetime.date(datetime.strptime(m.group(3).strip(), gmt_date)))
#     print("剩余天数:" ,datetime.strptime(datetime.date(datetime.strptime(m.group(3).strip(), gmt_date))) - datetime.strptime(current_time))
#     # print('证书详情:', m.group(4))
#     # print('申请机构:', m.group(5))
#     print('*' * 80)
#     # print(GMT_time)


if __name__ == '__main__':
    domain_list = ["oauth.idianyou.cn", "oauth.chigua.cn", "im.api.chigua.cn"]
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
                print("域名: ", domain)
                print("申请时间: ", apply_time)
                print("当前时间: ", current_day)
                print("过期时间: ", expire_day)
                print("剩余时间: ", left_days)
                print("*" * 80)
            else:
                pass
        except Exception as e:
            print("域名不可用", domain)
