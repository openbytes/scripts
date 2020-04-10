# coding=utf8

from modle import *
from alarmTemp import *

urlDict = {"Nodejs-dy_circle_page": "https://example.com/circle/getDownLinkxx",
           "Nodejs-payfor": "https://example.com/payfor/payxx"}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"}


def main():
    for nodeName, url in urlDict.items():
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            if query_table(App, 0):
                for describe in query_describe(App, url):
                    recover(nodeName, describe)
                    update_table(App, 1, nodeName)
            else:
                pass
        elif r.status_code == 404 and "微信" in r.text:
            if query_table(App, 0):
                for describe in query_describe(App, url):
                    recover(nodeName, describe)
                    update_table(App, 1, nodeName)
            else:
                pass
        else:
            print(query_table(App, 0))
            for describe in query_describe(App, url):
                alarm(nodeName, describe)
                update_table(App, 0, nodeName)


if __name__ == '__main__':
    main()
