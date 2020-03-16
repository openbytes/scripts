# coding=utf8
__data__ = '2019/12/9'
__author__ = 'Administrator'
"""
where the hope? The hope is on you hand

"""
# coding = utf-8


import oss2
import time

auth = oss2.Auth('xxxx', 'xxxxx')
bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'xxxx')

f_handle = open('C:\\Users\\Administrator\\Desktop\\oss.txt', 'r')

start = time.time()
http_count = 0
error_count = 0
while True:
    # 注意一定要strip()去掉换行，文件默认是\n换行，这样无法做判断
    video_file = f_handle.readline().strip()
    # print type(video_file)

    # 文件结束后跳出循环
    if video_file == '':
        break
    # 判断是否是mp4文件
    if video_file.startswith('dianyou'):
        exist = bucket.object_exists(video_file)

        if exist:
            print("资源存在,正在删除中...", video_file)
            bucket.delete_object(video_file)
            print("资源已删除...", video_file)
            http_count += 1
            print(http_count)
        else:
            print('资源不存在或者已删除--->', video_file)
            error_count += 1

print("已成功删除{}条".format(http_count))
print("未删除{}条".format(error_count))
end = time.time()
print("共耗时%.2f s" % (end - start))
