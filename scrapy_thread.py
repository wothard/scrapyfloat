#!/usr/bin/env python3
# encoding: utf-8

import threading
import queue
import os
import gbrarscrapy
import proxy


class Scrapy_thread(threading.Thread, object):
    def __init__(self, queue_ghost, pl):
        threading.Thread.__init__(self)
        self.queue = queue_ghost
        self.proxy = pl

    def run(self):
        url_roll = self.queue.get()
        gbrarscrapy.Gbrarscrapy(url_roll, self.proxy).run()
        self.queue.task_done()


def ghost():
    queue_ghost = queue.Queue()
    url = ("https://rarbgprx.org/torrents.php?category=" +
           "44%3B50%3B51%3B52%3B42&page=")
    print("输入数字，选择代理列表: ", end="")
    pro_list_sele = input()
    pro_li = proxy.read_proxy(str(pro_list_sele))
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
    for i in range(20):
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

# print(load_ep())
