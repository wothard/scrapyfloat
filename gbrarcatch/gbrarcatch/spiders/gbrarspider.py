# -*- coding: utf-8 -*-
# !/usr/bin/env python3


import scrapy


class GbrarSpider(scrapy.spiders.Spider):
    name = "gbrarcatch"
    start_urls = [
        # "http://rarbgprx.org/torrents.php?category=movies"
        "http://0.0.0.0:8000/RARBG%20Torrents%20%2C%20filmi%20%2C%20download.html"
    ]

    def __init__(self):
        self.title_list_xpath = '//a[@onmouseover]/text()'
        self.score_list_xpath = '//span[@style="color:DarkSlateGray"]/text()'
        self.date_list_xpath = '//td[contains(@align,"center") and contains(@width,"150px")]/text()'
        self.seed_list_xpath = '//td[@align="center" and @width="50px"]/font/text()'
        self.leech_list_xpath = '//td[@align="center" and @width="50px"][2]/text()'
        self.score_list = []  # 评分列表
        self.torrent_file_list = []  # 种子资源列表
        self.torrent_title = []  # 资源标题
        self.torrent_status_list = []  # 健康度列表

    def parse(self, response):
        # exchange score string to digtal
        score_string = response.xpath(self.score_list_xpath).extract()
        print(score_string)
