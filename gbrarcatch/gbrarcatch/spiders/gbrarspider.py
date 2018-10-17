# -*- coding: utf-8 -*-
# !/usr/bin/env python3


import scrapy


class GbrarSpider(scrapy.spiders.Spider):
    name = "gbrarcatch"
    start_urls = [
        "http://rarbgprx.org/torrents.php?category=movies"
    ]

    def __init__(self):
        self.title_list_xpath = '//a[@onmouseover]/text()'
        self.score_list_xpath = '//span[@style="color:DarkSlateGray"]/text()'
        self.date_list_xpath = '//td[contains(@align,"center") and contains(@width,"150px")]/text()'
        self.seed_list_xpath = '//td[@align="center" and @width="50px"]/font/text()'
        self.leech_list_xpath = '//td[@align="center" and @width="50px"][2]/text()'
        self.score_list = []
        self.torrent_file_list = []

    def parse(self, response):
        # exchange score string to digtal
        score_string = response.xpath(self.score_list_xpath).extract()
        for i in score_string:
            if '/' not in i:
                self.score_list.append(0)
            else:
                self.score_list.append(float((i.split(" ")[-1]).split('/')[0]))
        # 电影名称提取
        torrent_title = response.xpath(self.title_list_xpath).extract()
        torrent_address_b = "-[rarbg.to].torrent"
        torrent_address_f_list = []
        # 检查id匹配，并去除掉评论的url
        torrent_id_temp = response.xpath('//a[contains(@href,"/torrent/")]')
        torrent_id = torrent_id_temp.xpath('@href').extract()
        print(len(torrent_id))
        for i in range(26):
            id = torrent_id[i+8].split("torrent/")[-1]
            if "comment" not in id:
                torrent_address_f = "https://rarbgprx.org/download.php?id={}&f=".format(id)
                torrent_address_f_list.append(torrent_address_f)
        # 完整的种子资源地址列表
        print(torrent_address_f_list)
        print(len(torrent_address_f_list),len(torrent_title))
        for i in range(25):
            torrent_titles = torrent_address_f_list[i] + torrent_title[i] + torrent_address_b
            self.torrent_file_list.append(torrent_titles)
