#!/usr/bin/env python3
# encoding: utf-8

from lxml import html
import requests
import os
import random
import time
from fake_agent import fakeagent


class Gbrarscrapy(object):
    def __init__(self, url_li, proxy_single):
        self.title_xpa = '//a[@onmouseover]/text()'
        self.score_list_xpa = '//span[@style="color:DarkSlateGray"]/text()'
        self.id_xpa = '//a[contains(@href,"/torrent/")]/@href'
        self.ch_xpa = '//tr[@class="lista2"][{}]/td[2]/span/text()'
        # self.date_list_xpa = '//td[contains(@align,"center")
        # and contains(@width,"150px")]/text()'
        self.seli_xpa = '//td[@align="center" and @width="50px"]/font/text()'
        self.tor_dict = dict()  # 地址字典（包含地址，健康度，评分)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=' +
            '0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookies': 'skt=gkyxehd1ym; gaDts48g=q8h5pp9t; skt=gkyxehd1ym; gaDts48g=q8h5pp9t; aby=2; ppu_main_9ef78edf998c4df1e1636c9a474d9f47=1; expla=1; tcc; ppu_sub_9ef78edf998c4df1e1636c9a474d9f47=3'
        }
        self.url = url_li
        self.pro = proxy_single
        self.user_agent = fakeagent.load_ua()

    def run(self):
        try:
            temp_agent = random.choice(self.user_agent)
            agent = temp_agent.split("\n")[0]
            self.headers["User-Agent"] = agent
            pro = {"http": "http://" + random.choice(self.pro)}
            s = requests.get(self.url, headers=self.headers,
                             proxies=pro, timeout=10)
            response = html.fromstring(s.text)
            title_l = response.xpath(self.title_xpa)  # title
            id = (response.xpath(self.id_xpa))  # id
            seed = response.xpath(self.seli_xpa)  # seed
            torrent_f = self.torent_front(id)
            for i in range(25):
                # tor_addr 是完整种子下载地址
                address = torrent_f[i] + title_l[i] + "-[rarbg.to].torrent"
                check_sc = response.xpath(self.ch_xpa.format(i + 1))
                # 电影名称提取
                title = title_l[i].split(".1080p.")[0]
                # 标记分数 无分数则为 0
                if not check_sc or ('/' not in check_sc[0]):
                    score = 0
                if '/' in check_sc[0]:
                    score = float((check_sc[0].split(" ")[-1]).split('/')[0])
                if score >= 5:
                    self.torrent_dict(title_l[i], seed[i],
                                      title, address, score)
            time.sleep(2)
            print(len(self.tor_dict), self.tor_dict)
            print(self.url)
            self.torrent_save()
            print("保存成功一页")
        except Exception as e:
            print("REason: ", e)
            print(self.url)
            self.error_save_page(self.url)

    def torent_front(self, id):
        torrent_f = []  # 地址前缀
        for i in range(len(id) - 8):
            te = id[i + 8].split("torrent/")[-1]
            if "comment" not in te:
                temp = "https://rarbgprx.org/download.php?id={}&f=".format(te)
                torrent_f.append(temp)
        return torrent_f

    def torrent_dict(self, title_l, seed, title, address, score):
        # 检查是否重复
        if title_l in self.tor_dict.keys():
            # 检查健康度 及评分在5.0以上的数据
            if seed > self.tor_dict[title][0]:
                self.tor_dict[title] = [str(seed), address, str(score)]
            else:
                self.tor_dict[title] = [str(seed), address, str(score)]
        else:
            self.tor_dict[title] = [str(seed), address, str(score)]

    def torrent_save(self):
        with open(os.getcwd()+'/data/dianying.txt', 'a') as f:
            for (i, j) in self.tor_dict.items():
                f.write(i)
                f.write(", ")
                for k in j:
                    f.write(k)
                    f.write(", ")
                f.write("\n")

    def error_save_page(self, url):
        with open(os.getcwd()+'/data/error_page_1.txt', 'a') as f:
            f.write(url)
            f.write("\n")
