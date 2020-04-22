# coding=utf8

import requests
from AppDistri import dingding
from AppDistri import updateFile

url = "https://www.baidu.com"
userAgent = "user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit" \
            "/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
header = {
    'User-Agent': userAgent
}


def main():
    r = requests.get(url=url, headers=header)
    _ = updateFile.Update_Read_Config()
    if r.status_code == 200:
        if "xxxx" in r.text:
            res = _.read(0)
            if res:
                for item in res:
                    for i in item.values():
                        dingding.recover(i["describe"], i["ip"])
                    for i in item.keys():
                        _.update(i, "1")
            else:
                print("Web is ok!")
        else:
            res = _.read_all()
            for item in res:
                dingding.alarm(item["describe"],item["ip"])
            for sec in _.read_sections():
                _.update(sec, "0")
    else:
        for x in _.read_all():
            dingding.alarm(x["describe"], x["ip"])
        for sec in _.read_sections():
            _.update(sec, "0")

if __name__ == '__main__':
    main()
