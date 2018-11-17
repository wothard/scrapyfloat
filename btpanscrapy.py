#!/usr/bin/env python3
# encoding: utf-8


import lxml
from fake_agent import fakeagent
import requests
import random
import os
import time


class Btpanscrapy(object):
    def __init__(self, urls, pl):
        self.title_xpa = '//p[@class="title"]/a/span[1]/text()'
        self.score_xpa = '//p[@class="title"]/a/span[2]/text()'
        self.btlink_xpa = '//p[@class="title"]/a/@href'
        self.dl_xpa = '//p[@class="douban"]/a/@href'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=' +
            '0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate'
        }
        self.user_agent = fakeagent.load_ua()
        self.btflink = "http://www.btpan.com"
        self.url = urls
        self.sour_dict = dict()
        self.deour_dict = dict()
        self.pro = pl

    def run(self):
        result = None
        while True:
            pro = {"http": "http://" + random.choice(self.pro)}
            try:
                temp_agent = random.choice(self.user_agent)
                agent = temp_agent.split("\n")[0]
                self.headers["User-Agent"] = agent
                s = requests.get(self.url, headers=self.headers,
                                 proxies=pro, timeout=4)
                s.encoding = "utf-8"
                response = lxml.html.fromstring(s.text)
                result = self.doubanlink(response=response)
                return result
                break
            except requests.ConnectTimeout:
                pass
            except requests.ReadTimeout:
                pass
            except requests.HTTPError:
                pass
            except requests.exceptions.ProxyError:
                time.sleep(5)
                pass
            except requests.exceptions.ConnectionError:
                pass
            except requests.TooManyRedirects:
                pass
            except IndexError:
                pass
            except requests.exceptions.ChunkedEncodingError:
                pass
            except lxml.etree.ParserError:
                pass
            except Exception as e:
                print("其他：", type(e), e)

    def doubanlink(self, response):
        dblink = response.xpath(self.dl_xpa)
        print(self.url, ">>>>>>>>>>>>>>>>>>", dblink[0])
        return dblink[0]

    def btlink(self, response):
        title_l = response.xpath(self.title_xpa)
        score_l = response.xpath(self.score_xpa)
        btblink = response.xpath(self.btlink_xpa)
        if len(title_l) != len(score_l):
            title_l = []
            score_l = []
            sa_xpa = '//div[@class="content"]/div[{}]/div[2]/p/a/span['
            for i in range(1, 21):
                ti = (sa_xpa + '1]/text()').format(i)
                sc = (sa_xpa + '2]/text()').format(i)
                if len(response.xpath(ti)) == 0:
                    title_l.append("None")
                else:
                    title_l.append(response.xpath(ti)[0])
                if response.xpath(sc)[0] == "d":
                    score_l.append("0")
                else:
                    score_l.append(response.xpath(sc)[0])
        for i in range(20):
            btblink[i] = self.btflink + btblink[i]
            if float(score_l[i]) >= 5:
                self.sour_dict[title_l[i]] = btblink[i]
            else:
                self.deour_dict[title_l[i]] = btblink[i]
        # 将两个字典返回
        return (self.sour_dict, self.deour_dict)
