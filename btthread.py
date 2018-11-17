#!/usr/bin/env python3
# encoding: utf-8

import threading
import queue
import proxy
import btpanscrapy
import os


up_list = list()
down_list = list()
douban_list = list()


class Scrapy_thread(threading.Thread, object):
    def __init__(self, queue_bt, pl):
        threading.Thread.__init__(self)
        self.queue = queue_bt
        self.proxy = pl

    def run(self):
        while 1:
            url_roll = self.queue.get()
            # btpanscrapy.Btpanscrapy(url_roll).run()
            result = btpanscrapy.Btpanscrapy(url_roll, self.proxy).run()
            douban_list.append(result)
            # btpanscrapy.Btpanscrapy(url_roll, self.proxy).run()
            # result = btpanscrapy.Btpanscrapy(url_roll, self.proxy).run()
            # up_list.append(result[0])
            # down_list.append(result[1])
            self.queue.task_done()


def startbt():
    queue_bt = queue.Queue()
    proxy_list = proxy.read_proxy()
    btlink = read_btlink()
    # for i in range(1, 1073):
    #     i = "http://www.btpan.com/film/?page={}".format(i)
    #     queue_bt.put(i)
    for i in btlink[:1000]:
        queue_bt.put(i.split("\n")[0])
    for i in range(400):
        t = Scrapy_thread(queue_bt, proxy_list)
        t.setDaemon(True)
        t.start()
    queue_bt.join()


def save_dict():
    with open(os.getcwd()+'/data/up.txt', 'w') as f:
        for i in up_list:
            for j, k in i.items():
                f.write(j)
                f.write(",")
                f.write(k)
                f.write("\n")
    with open(os.getcwd()+'/data/down.txt', 'w') as f2:
        for i in down_list:
            for j, k in i.items():
                f2.write(j)
                f2.write(",")
                f2.write(k)
                f2.write("\n")


def douban_save():
    print("开始写入文件。。。。。")
    with open(os.getcwd()+'/data/doub2.txt', 'a') as f:
        for i in douban_list:
            if i is None:
                f.write("NONE")
            else:
                f.write(i)
            f.write("\n")


def read_btlink():
    btlink_li = list()
    with open(os.getcwd()+'/data/up.txt', 'r') as f:
        for i in f.readlines():
            btlink_li.append(i.split(",")[1])
    return btlink_li


# read_btlink()
startbt()
douban_save()
# save_dict()
