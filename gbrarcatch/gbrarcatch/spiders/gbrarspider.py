# -*- coding: utf-8 -*-
# !/usr/bin/env python3


import scrapy


class GbrarSpider(scrapy.spiders.Spider):
    name = "gbrarcatch"
    start_urls = [
        "http://rarbgprx.org/torrents.php?category=movies"
        # "http://0.0.0.0:8000/ad.html"
    ]

    def __init__(self):
        self.title_xpa = '//a[@onmouseover]/text()'
        self.score_list_xpa = '//span[@style="color:DarkSlateGray"]/text()'
        self.id_xpa = '//a[contains(@href,"/torrent/")]'
        # self.date_list_xpa = '//td[contains(@align,"center")
        # and contains(@width,"150px")]/text()'
        self.seli_xpa = '//td[@align="center" and @width="50px"]/font/text()'
        self.tor_dict = dict()  # 地址字典（包含地址，健康度，评分）

    def parse(self, response):
        # all extract to list
        score_l = response.xpath(self.score_list_xpa).extract()  # score
        title_l = response.xpath(self.title_xpa).extract()  # title
        id = (response.xpath(self.id_xpa)).xpath('@href').extract()  # id
        seed = response.xpath(self.seli_xpa).extract()  # seed
        torrent_f = []  # 地址前缀
        for i in range(len(id)-8):
            te = id[i+8].split("torrent/")[-1]
            if "comment" not in te:
                temp = "https://rarbgprx.org/download.php?id={}&f=".format(te)
                torrent_f.append(temp)
        for i in range(25):
            # tor_addr 是完整种子下载地址
            address = torrent_f[i] + title_l[i] + "-[rarbg.to].torrent"
            # 电影名称提取
            title = title_l[i].split(".1080p.")[0]
            # 标记分数 无分数则0
            score = 0
            if '/' in score_l[i]:
                # 提取到的分数
                score = float((score_l[i].split(" ")[-1]).split('/')[0])
            if score >= 5:
                # # 检查是否重复
                if title_l[i] in self.tor_dict.keys():
                    # 检查健康度 及评分在5.0以上的数据
                    if seed[i] > self.tor_dict[title][0]:
                        self.tor_dict[title] = [seed[i], address, score]
                else:
                    self.tor_dict[title] = [seed[i], address, score]
        # print(len(seed), self.tor_dict, len(self.tor_dict))
