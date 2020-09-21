# coding=utf8
__data__ = '2019/12/2'
__author__ = 'Administrator'

import time
import subprocess
from concurrent.futures import ThreadPoolExecutor as t


def filteID(id):
    start = time.time()
    command = "source /etc/profile;hadoop fs -cat /flume/data/logs/20200311/* | grep " + str(id) + " >>" + str(
        id) + '.log'
    r = subprocess.getstatusoutput(command)
    end = time.time()
    print(end - start)

pool = t(8)
with open('id') as f:
    for line in f:
        a = pool.submit(filteID, line.strip())
