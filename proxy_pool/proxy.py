#!/usr/bin/env python3
# encoding: utf-8

from lxml import html
import requests
import json
import os
import telnetlib
import threading
import _thread
import queue
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
    ' (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,' +
    'image/webp,image/apng,*/*;q=0.8'
    }

url_list = ["https://www.kuaidaili.com/free/inha/",
            "http://ip.jiangxianli.com/?page="]
ip_xpa_list = ['//td[@data-title="IP"]/text()',
               '//tbody/tr/td[2]/text()']
port_xpa_list = ['//td[@data-title="PORT"]/text()',
                 '//tbody/tr/td[3]/text()']
sta_xpa_list = ['//td[@data-title="类型"]/text()',
                '//tbody/tr/td[5]/text()']


class Test_IP(threading.Thread, object):
    def __init__(self, queue_new, addr_dict):
        threading.Thread.__init__(self)
        self.queue = queue_new
        self.dict = addr_dict

    def run(self):
        addr_ip_and_port = self.queue.get()
        self.test_ip(addr_ip_and_port)
        self.queue.task_done()

    def test_ip(self, addr_ip_and_port):
        test = addr_ip_and_port.split(":")
        try:
            telnetlib.Telnet(test[0], port=test[1], timeout=3)
        except Exception as e:
            print("原因:", e)
        else:
            print("IP 可用")
        self.dict.append(addr_ip_and_port)


def read_page():
    with open(os.getcwd()+'/proxy_pool/page.txt', 'r') as f:
        result = f.readlines()
    return result


ihuan_page_list = read_page()


def thread_run(addr_ip_and_port, addr_dict):
    queue_new = queue.Queue()
    for i in addr_ip_and_port:
        queue_new.put(i)
    for i in range(len(addr_ip_and_port)):
        t = Test_IP(queue_new, addr_dict)
        t.setDaemon(True)
        t.start()
    queue_new.join()


def scrap_ip(address, ip_x, port_x, sta_x, scrap_count, website_name):
    addr_dict_http = dict()
    addr_dict_https = dict()
    addr_dict_http[website_name] = []
    addr_dict_https[website_name] = []
    http_temp = []
    https_temp = []
    try:
        for i in range(1, scrap_count):
            s = requests.get((address + str(i)), headers=headers)
            tree = html.fromstring(s.text)
            addr_ip = tree.xpath(ip_x)
            addr_port = tree.xpath(port_x)
            addr_sta = tree.xpath(sta_x)
            for j in range(len(addr_ip)):
                address_temp = addr_ip[j] + ":" + addr_port[j]
                if addr_sta[j] == "yes" or addr_sta[j] == "HTTPS":
                    https_temp.append(address_temp)
                else:
                    http_temp.append(address_temp)
            time.sleep(2)
        thread_run(http_temp, addr_dict_http[website_name])
        thread_run(https_temp, addr_dict_https[website_name])
        with open(os.getcwd()+'/proxy_pool/proxy_https.json', 'w') as f:
            json.dump(addr_dict_https, f)
            f.write("\n")
        with open(os.getcwd()+'/proxy_pool/proxy_http.json', 'w') as f:
            json.dump(addr_dict_http, f)
            f.write("\n")
    except Exception as e:
        print("Reason:", e)
    print(len(addr_dict_http['proxy']))


def main():
    try:
        start = time.time()
        for i in range(2):
            _thread.start_new_thread(
                scrap_ip(url_list[i], ip_xpa_list[i],
                         port_xpa_list[i], sta_xpa_list[i],
                         scrap_count=20, website_name="proxy"))
        stop = time.time()
        print(str(stop - start) + "秒")
    except Exception as e:
        print("出错:", e)


main()
