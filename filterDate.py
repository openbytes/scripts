# coding=utf8
__data__ = '2019/12/2'
__author__ = 'Administrator'
"""
where the hope? The hope is on you hand

"""
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor as executor


def filteID(id):
    start = time.time()
    # command = "source /etc/profile;hadoop fs -cat /flume/data/logs/20191123/* | grep " + str(id) + " >>" + str(
        # id) + '.log'
    command = "source /etc/profile;hadoop fs -cat /flume/data/logs/202003" + id +"/* " +" | grep 'DEFFDFDFFFFFF'  >> " + id +".log"
    r = subprocess.getstatusoutput(command)
    end = time.time()
    print(end - start)
    # print(command)
pool = executor(max_workers=8)
with open('id') as f:
    for line in f:
        a = pool.submit(filteID, line.strip())
