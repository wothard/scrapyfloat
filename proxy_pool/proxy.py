#!/usr/bin/env python3
# encoding: utf-8

from lxml import html
import requests
import json
import os
from random import choice


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

url_list = ["https://proxy.l337.tech/",
            "http://free-proxy.cz/en/proxylist/country/all/http/ping/all/",
            "https://free-proxy-list.net/#"]


def proxy1():
    # for i in range(10):
    #     s = requests.get(url_list[i], headers=headers)
    #     tree = html.fromstring(s.text)
    #     result = tree.xpath('/html/body/pre/text()')
    s = requests.get(url_list[2], headers=headers)
    tree = html.fromstring(s.text)
    result = tree.xpath('//title/text()')
    print(result)
    # result = tree.xpath('/html/body/pre/text()')
    # result = result[0].split('\n')
    # result_dict = dict()
    # result_dict['proxy'] = result[1:len(result)-1]
    # with open(os.getcwd()+'/proxy_pool/proxy.json', 'a') as f:
    #     json.dump(result_dict, f)
    #     f.write("\n")


def proxy2():
    url = "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-"
    ip_xpa = '//tr[contains(@onmouseover,"this.class")]/td[2]/text()'
    port_xpa = '//tr[contains(@onmouseover,"this.class")]/td[3]/text()'
    address_dict = dict()
    address_dict["proxylistplus"] = []
    for i in range(1, 7):
        s = requests.get((url + str(i)), headers=headers)
        tree = html.fromstring(s.text)
        address_ip = tree.xpath(ip_xpa)
        address_port = tree.xpath(port_xpa)
        for i in range(len(address_ip)):
            address_temp = address_ip[i] + ":" + address_port[i]
            address_dict["proxylistplus"].append(address_temp)
    with open(os.getcwd()+'/proxy_pool/proxy.json', 'a') as f:
        json.dump(address_dict, f)
        f.write("\n")


a = []


def proxy3():
    list_page_code = ["b97827cc", "4ce63706", "5crfe930", "f3k1d581",
                      "ce1d45977", "881aaf7b5", "eas7a436", "981o917f5",
                      "2d28bd81a", "a42g5985d", "came0299", "e92k59727",
                      "242r0e7b5", "bc265a560", "622b6a5d3", "ae3g7e7aa",
                      "b01j07395", "68141a2df", "904545743", "0134c4568",
                      "885t249e8", "ed442164b", "806fe4987", "0558da7f4",
                      "3734334de", "636g6d8ca", "3252d86d1", "d67sbb99f",
                      "0e1q9e209", "078e9d9eb"]
    ip_xpa = '//table[contains(@class,"table-hover")]/tbody/tr/td[1]/a/text()'
    port_xpa = '//table[contains(@class,"table-hover")]/tbody/tr/td[2]/text()'

    with open(os.getcwd()+'/proxy_pool/proxy.json', 'r') as f:
        tes = f.readline()
        fg = json.loads(tes)
        pro = fg['proxylistplus']
    for i in range(30):
        url = "https://ip.ihuan.me/?page=" + list_page_code[i]
        proxies = {"http": choice(pro), "https": choice(pro)}
        print(proxies)
        try:
            tefg(url, ip_xpa, port_xpa, proxies)
            # s = requests.get(url, headers=headers, proxies=proxies)
            # tree = html.fromstring(s.text)
            # address_ip = tree.xpath(ip_xpa)
            # address_port = tree.xpath(port_xpa)
            # for i in range(len(address_ip)):
            #     address_temp = address_ip[i] + ":" + address_port[i]
        except requests.exceptions.ProxyError:
            proxies = {"http": choice(pro), "https": choice(pro)}
            tefg(url, ip_xpa, port_xpa, proxies)
            print("Fuck up")
        print(len(a))
    # url = "https://ip.ihuan.me/?page="
    print(a)


def tefg(url, ip_xpa, port_xpa, proxies):
    s = requests.get(url, headers=headers, proxies=proxies)
    print("dadsadasdas")
    tree = html.fromstring(s.text)
    address_ip = tree.xpath(ip_xpa)
    address_port = tree.xpath(port_xpa)
    for i in range(len(address_ip)):
        address_temp = address_ip[i] + ":" + address_port[i]
        a.append(address_temp)


def proxy4():
    url = ["https://www.kuaidaili.com/free/intr/1/",
           "https://www.kuaidaili.com/free/intr/2/",
           "https://www.kuaidaili.com/free/inha/1/",
           "https://www.kuaidaili.com/free/intr/2/"]
    s = requests.get(url[0], headers=headers)
    tree = html.fromstring(s.text)
    result_ip = tree.xpath('//td[@data-title="IP"]/text()')
    result_port = tree.xpath('//td[@data-title="PORT"]/text()')
    a = []
    for i in range(len(result_ip)):
        address_temp = result_ip[i] + ":" + result_port[i]
        a.append(address_temp)
    return a


def proxy5():
    a = []
    for i in range(1, 35):
        url = "http://www.66ip.cn/areaindex_{}/1.html".format(str(i))
        s = requests.get(url, headers=headers)
        tree = html.fromstring(s.text)
        ip_xpa = '//table[contains(@bordercolor, "#6699ff")]/tr/td[1]/text()'
        port_xpa = '//table[contains(@bordercolor, "#6699ff")]/tr/td[2]/text()'
        address_ip = tree.xpath(ip_xpa)
        address_port = tree.xpath(port_xpa)
        for i in range(1, len(address_ip)):
            address_temp = address_ip[i] + ":" + address_port[i]
            a.append(address_temp)
    print(a)
    return a


proxy5()
