#!/usr/bin/env python3
# encoding: utf-8

import threading
import queue
import proxy
import btpanscrapy
import os
import json

up_list = list()
down_list = list()
douban_list = list()
down = list()
fuck_dict = dict()


class Scrapy_thread(threading.Thread, object):
    def __init__(self, queue_bt, pl):
        threading.Thread.__init__(self)
        self.queue = queue_bt
        self.proxy = pl

    def run(self):
        while 1:
            url_roll = self.queue.get()
            result = btpanscrapy.Btpanscrapy(url_roll, self.proxy).run()
            fuck_dict[result[0]] = result[1]
            self.queue.task_done()


def startbt():
    queue_bt = queue.Queue()
    proxy_list = proxy.read_proxy()
    btlink = read_btlink()
    for i in btlink[8000:]:
        queue_bt.put(i.split("\n")[0])
    for i in range(500):
        t = Scrapy_thread(queue_bt, proxy_list)
        t.setDaemon(True)
        t.start()
    queue_bt.join()


def save_dict():
    print("开始写入文件")
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


# 将所有的 btpan 链接获取其 种子地址，电影名称，种子大小 封装成字典
# 后面添加豆瓣评分和评论数


def save_json():
    print("开始写入文件。。。。。")
    with open(os.getcwd()+'/data/result.json', 'a') as f:
        json.dump(fuck_dict, f)
        f.write("\n")


def load_json():
    with open(os.getcwd()+'/data/result.json', 'r') as f:
        da = json.load(f)
        for k, v in da.items():
            print(k, v)


def read_btlink():
    btlink_li = list()
    with open(os.getcwd()+'/data/doub3.txt', 'r') as f:
        for i in f.readlines():
            btlink_li.append(i.split(",")[0])
    return btlink_li


startbt()
save_json()
