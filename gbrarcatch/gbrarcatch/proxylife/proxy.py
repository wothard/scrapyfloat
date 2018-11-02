#!/usr/bin/env python3
# encoding: utf-8

from lxml import html
from random import choice
import requests
import json
import os
import telnetlib
import threading
import queue
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
    ' (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,' +
    'image/webp,image/apng,*/*;q=0.8'
    }

rule_list = []

scrap_site_all = [
    ["https://www.kuaidaili.com/free/inha/", '//td[@data-title="IP"]/text()',
     '//td[@data-title="PORT"]/text()', '//td[@data-title="类型"]/text()',
     5],
    ["http://ip.jiangxianli.com/?page=", '//tbody/tr/td[2]/text()',
     '//tbody/tr/td[3]/text()', '//tbody/tr/td[5]/text()', 5],
    ["https://ip.ihuan.me/?page=",
     '//table[contains(@class,"table-h")]/tbody/tr/td[1]/a/text()',
     '//table[contains(@class,"table-h")]/tbody/tr/td[2]/text()',
     '//table[contains(@class,"table-h")]/tbody/tr/td[5]/text()', 5],
    ["http://www.freeproxylist.net/zh/?page=", '//td/a/text()',
     '//table[contains(@class, "Odd") and ' +
     'contains(@class, "Even")]/td[2]/text()',
     '//table[contains(@class, "Odd") and ' +
     'contains(@class, "Even")]/td[3]/a/text()', 5]
    ]
global_result = []
list_page_code = ["b97827cc", "4ce63706", "5crfe930", "f3k1d581",
                  "ce1d45977", "881aaf7b5", "eas7a436", "981o917f5",
                  "2d28bd81a", "a42g5985d", "came0299", "e92k59727",
                  "242r0e7b5", "bc265a560", "622b6a5d3", "ae3g7e7aa",
                  "b01j07395", "68141a2df", "904545743", "0134c4568",
                  "885t249e8", "ed442164b", "806fe4987", "0558da7f4",
                  "3734334de", "636g6d8ca", "3252d86d1", "d67sbb99f",
                  "0e1q9e209", "078e9d9eb"]


class Test_IP(threading.Thread, object):
    def __init__(self, queue_new, proxy_li):
        threading.Thread.__init__(self)
        self.queue = queue_new
        self.proxy_li = proxy_li

    def run(self):
        addr_ip_and_port = self.queue.get()
        self.test_ip(addr_ip_and_port)
        self.queue.task_done()

    def test_ip(self, addr_ip_and_port):
        test = addr_ip_and_port.split(":")
        try:
            telnetlib.Telnet(test[0], port=test[1], timeout=3)
        except Exception:
            # 在这里输出代理出错的ip，及其原因，所以不必要输出
            pass
        else:
            print("IP 可用")
            self.proxy_li.append(addr_ip_and_port)
            print("IP 已添加")


class Scrap_IP(threading.Thread):
    def __init__(self, scrap_info, rt, rts):
        threading.Thread.__init__(self)
        self.scrap_info = scrap_info
        self.rt = rt
        self.rts = rts

    def run(self):
        scrap_ip(self.scrap_info, self.rt, self.rts)


def thread_run(addr_ip_and_port):
    proxy_li = []
    queue_new = queue.Queue()
    for i in addr_ip_and_port:
        queue_new.put(i)
    for i in range(len(addr_ip_and_port)):
        t = Test_IP(queue_new, proxy_li)
        t.setDaemon(True)
        t.start()
    queue_new.join()
    return proxy_li


def scrap_ip(scrap_info, rt, rts):
    addr_mix = [[], []]
    sta_li_check = ["yes", "HTTPS", "支持"]
    lio = [4, 5, 6]
    # proxy_read = None
    # proxies=pro,
    print(scrap_info[0])
    try:
        for i in range(scrap_info[4]):
            # pro = {"http": "http://" + choice(proxy_read)}
            s = requests.get((scrap_info[0] + str(i+1)),
                             headers=headers, timeout=10)
            tree = html.fromstring(s.text)
            addr_ip = tree.xpath(scrap_info[1])
            addr_port = tree.xpath(scrap_info[2])
            addr_sta = tree.xpath(scrap_info[3])
            for j in range(len(addr_ip)):
                address_temp = addr_ip[j] + ":" + addr_port[j]
                if addr_sta[j] in sta_li_check:
                    addr_mix[0].append(address_temp)
                else:
                    addr_mix[1].append(address_temp)
            print("-------------------------")
            print("------读取完第{}页--------".format(str(i)))
            time.sleep(choice(lio))
        print("总共获取到{}个HTTPS类型的IP".format(len(addr_mix[0])))
        print("总共获取到{}个HTTP类型的IP".format(len(addr_mix[1])))
        thread_run(addr_mix[0])
        thread_run(addr_mix[1])
        print("提取到{}个HTTPS类型的IP".format(len(addr_mix[0])))
        print("提取到{}个HTTP类型的IP".format(len(addr_mix[1])))
    except Exception as e:
        print("Reason:", e)
    rt.extend(addr_mix[1])
    rts.extend(addr_mix[0])


def read_proxy():
    with open(os.getcwd()+'/gbrarcatch/proxylife/proxy_pool/proxy_http.json', 'r') as f:
        try:
            read_dict_http = json.loads(f.readline())
            result = read_dict_http["proxy"]
            proxy = thread_run(result)
            print("读取{}个可用IP".format(len(proxy)))
            return proxy
        except Exception as e:
            print("Reason:", e)
            return None


def save_proxy():
    proxy_dict = dict()
    proxy_https_dict = dict()
    th1_li = []
    th1s_li = []
    scrap_info = scrap_site_all[3]
    th1 = Scrap_IP(scrap_info, th1_li, th1s_li)
    # # th2 = Scrap_IP(url_list[1], ip_xpa_list[1],
    # #                port_xpa_list[1], sta_xpa_list[1],
    # #                25, "proxy")
    # #
    start = time.time()
    th1.start()
    # # th2.start()
    th1.join()
    # # th2.join()
    # # save_proxy()
    stop = time.time()
    print(stop-start)
    proxy_dict["proxy"] = th1_li
    proxy_https_dict["proxy"] = th1s_li
    with open(os.getcwd()+'/gbrarcatch/proxylife/proxy_pool/proxy_http.json', 'w') as f:
        json.dump(proxy_dict, f)
        f.write("\n")
    with open(os.getcwd()+'/gbrarcatch/proxylife/proxy_pool/proxy_https.json', 'w') as f:
        json.dump(proxy_https_dict, f)
        f.write("\n")


# save_proxy()

def read_proxy():
    cv = []
    with open(os.getcwd()+'/gbrarcatch/proxylife/proxy_pool/vghj.txt', 'r') as f:
        d = f.readlines()
    for i in d:
        cv.append(i.split("\n")[0])
    aa = thread_run(cv)
    return aa
