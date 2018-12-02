#!/usr/bin/env python3
# encoding: utf-8

import threading
import queue
import os
import json
import proxy
from initscrapy import Ingscrapy
# import gbrarscrapy
# import doubanscrapy


'''写一个或多个全局列表(字典)，保存数据，并将内容写入文件'''
# temp_dict = dict()
temp_list = list()
score_dict = dict()


class Scrapy_thread(threading.Thread, object):
    def __init__(self, queue_in, proxies):
        threading.Thread.__init__(self)
        self.queue = queue_in
        self.proxies = proxies

    def run(self):
        '''在 while 循环写入需要执行的爬虫'''
        while 1:
            url_roll = self.queue.get()
            result = Ingscrapy(url_roll, self.proxies).run()
            # temp_dict[result[1]] = result[0]
            temp_list.append(result)
            # temp_list.extend(result)
            # a = doubanscrapy.Doubanscrapy(url_roll, self.proxies).run()
            # score_dict[a[1]] = a[0]
            # gbrarscrapy.Gbrarscrapy(url_roll, self.proxies).run()
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


# ghost()


def read_url():
    ''' 读取抓取的url列表 '''
    url = list()
    with open(os.getcwd()+'/data/fairone.txt', 'r') as f:
        for i in f.readlines():
            temp = (i.split("\n")[0])
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
    '''线程创建和启动的函数'''
    queue_in = queue.Queue()
    # 读取 url 列表， 或者根据 url 规则创建列表
    # for i in range(400, 454):
    #     url = "https://www.meinvtu123.net/a/cn/list_2_{}.html".format(i)
    #     queue_in.put(url)
    url = read_url()
    for i in url[:100]:
        # ue = "https://www.weifengz.com" + i
        # ue = "https://www.meinvtu123.net/a/cn/list_2_{}.html".format(i+1)
        # queue_in.put(ue)
        queue_in.put(i)
    # 读取代理
    proxies = proxy.read_proxy()
    # 开启线程， range() 中的数字代表线程数
    for i in range(50):
        t = Scrapy_thread(queue_in, proxies)
        t.setDaemon(True)
        t.start()
    queue_in.join()
    save_data()


def save_data():
    print("开始写入文件。。。。。")
    # 如果是写 json 文件则修改此代码
    # with open(os.getcwd()+'/data/score.json', 'a') as f:
    #     json.dump(score_dict, f)
    #     f.write("\n")
    # 如果写 txt 文件则修改此代码
    with open(os.getcwd()+'/data/faironeaddr.txt', 'a') as f:
        for i in temp_list:
            f.write(i)
            # for j in i:
            #     f.write(j)
            # f.write(",")
            f.write("\n")


thread_start()
# print(temp_list)
