#!/usr/bin/env python3
# encoding: utf-8

import threading
import queue
import os
import json
import gbrarscrapy
import doubanscrapy
import proxy


score_dict = dict()


class Scrapy_thread(threading.Thread, object):
    def __init__(self, queue_in, proxies):
        threading.Thread.__init__(self)
        self.queue = queue_in
        self.proxies = proxies

    def run(self):
        while 1:
            url_roll = self.queue.get()
            # a = doubanscrapy.Doubanscrapy(url_roll, self.proxies).run()
            # score_dict[a[1]] = a[0]
            gbrarscrapy.Gbrarscrapy(url_roll, self.proxies).run()
            self.queue.task_done()


def ghost():
    queue_ghost = queue.Queue()
    url = ("https://rarbgprx.org/torrents.php?category=" +
           "44%3B50%3B51%3B52%3B42&page=")
    pro_li = proxy.read_proxy()
    print("爬新输入1，爬旧输入2：", end="")
    main = input()
    if int(main) == 1:
        print("输入数字，开始从该页爬起: ", end="")
        new_catch_sta = input()
        print("输入数字，到该页结束爬取（必须比起始页大）: ", end="")
        new_catch_end = input()
        for i in range(int(new_catch_sta), int(new_catch_end)):
            urls = url + str(i)
            queue_ghost.put(urls)
    else:
        pages = load_ep()
        print("未爬取{}页".format(len(pages)))
        print("是否从上次爬错页面列表中爬起：(Y/N) ", end="")
        error_catch = input()
        if error_catch == "Y":
            for i in pages:
                queue_ghost.put(i.split("\n")[0])
    for i in range(100):
        t = Scrapy_thread(queue_ghost, pro_li)
        t.setDaemon(True)
        t.start()
    queue_ghost.join()
    print("抓取完成！！！！！！！！！！！！！！！")


def load_ep():
    if os.path.getsize(os.getcwd()+'/data/error_page_2.txt') == 0:
        print("dsa")
        with open(os.getcwd()+'/data/error_page_1.txt', 'r') as f:
            page = f.readlines()
            return page
    else:
        page2 = []
        with open(os.getcwd()+'/data/error_page_2.txt', 'r') as fq:
            page2 = fq.readlines()
        with open(os.getcwd()+'/data/error_page_1.txt', 'w') as fw:
            for i in page2:
                fw.write(i)
        with open(os.getcwd()+'/data/error_page_2.txt', 'w') as fe:
            fe.write("")
        return page2


ghost()


def read_url():
    url = list()
    with open(os.getcwd()+'/data/doub3.txt', 'r') as f:
        for i in f.readlines():
            temp = (i.split("\n")[0]).split(",")[1]
            url.append(temp)
    return url


def read_url2():
    url = list()
    with open(os.getcwd()+'/data/doub3.txt', 'r') as f:
        for i in f.readlines():
            temp = (i.split("\n")[0]).split(",")
            url.append(temp)
    return url


def convert():
    all = dict()
    readurl = read_url2()
    for i in readurl:
        all[i[1]] = i[0]
    for i in score_dict.keys():
        if i in all:
            score_dict[i].append(all[i])


def thread_start():
    queue_in = queue.Queue()
    # 读取 url 列表
    url = read_url()
    for i in url[:1]:
        queue_in.put(i)
    # 读取代理
    proxies = proxy.read_proxy()
    # 开启线程
    for i in range(1):
        t = Scrapy_thread(queue_in, proxies)
        t.setDaemon(True)
        t.start()
    queue_in.join()


def save_json():
    print("开始写入文件。。。。。")
    with open(os.getcwd()+'/data/score.json', 'a') as f:
        json.dump(score_dict, f)
        f.write("\n")


# thread_start()
# convert()
# save_json()
# print(score_dict)
# convert()
# read_url()
