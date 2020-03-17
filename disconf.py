# coding=utf8
__data__ = '2019/8/27'
__author__ = 'Administrator'
"""
where the hope? The hope is on you hand

"""

import requests
import json

url = "http://172.x.x.x:8080/api/account/signin"
# 头部信息

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': '172.10.4.122:8080',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}



def GetCookie():
    """
    获取登录cookies
    :return:
    """
    s = requests.session()
    loginUrl = 'http://172.x.x.x:8080/api/account/signin'
    postData = {'name': 'admin', 'password': 'admin', 'remember': '1'}
    rs = s.post(loginUrl, postData)
    c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
    c.set('cookie-name', 'cookie-value')
    s.cookies.update(c)
    return s.cookies.get_dict()


# 登陆方法
def login(id):
    s = requests.session()
    rs = s.get("http://172.x.x.x:8080/api/web/config/" + id, headers=headers, cookies=GetCookie(), verify=False)
    rs.encoding = 'utf-8'
    return rs.text


if __name__ == '__main__':
    count = 0
    key_words_list = ['zookeeper']
    appList = []
    with open('configID.txt') as f:
        for id in f:
            res = json.loads(login(str(id)))
            try:
                for word in key_words_list:
                    if word in res["result"]["value"]:
                        # print(res["result"]["value"])
                        appList.append({word: res["result"]["appName"]})
                    # print(res["result"]["appName"])
            except Exception as e:
                print(id,"无项目有此配置")
    for i in appList:
        print(i,"有此配置")
