#!/usr/bin/env python3
# encoding: utf-8


class Gbrarscrapy(object):
    def __init__(self):
        # 种子下载地址唯一id
        self.id_xpa = '//a[contains(@href,"/torrent/")]/@href'
        # 全称标题（包含质量，音轨，编码方式等)
        self.title_xpa = '//a[@onmouseover]/text()'
        # 评分
        self.score_xpa = '//span[@style="color:DarkSlateGray"]/text()'
        # 种子下载完成并做种的虚值
        self.seed_xpa = '//td[@align="center" and @width="50px"]/font/text()'
        # 规则限制加入cookies
        self.cookies = ('skt=v97mrzygux; gaDts48g=q8h5pp9t; ' +
                        'skt=v97mrzygux; gaDts48g=q8h5pp9t; expla=1; ' +
                        'tcc; aby=2; ppu_main_9ef78edf998c4df1e1636c9' +
                        'a474d9f47=1; ppu_sub_9ef78edf998c4df1e1636c9' +
                        'a474d9f47=1; ppu_delay_9ef78edf998c4df1e1636' +
                        'c9a474d9f47=1')

    def carry(self, response):
        # title_li = response.xpath(self.title_xpa)  # title
        # id_li = response.xpath(self.id_xpa)  # id
        # seed_li = response.xpath(self.seed_xpa)  # seed
        score_li = response.xpath(self.score_xpa)  # score
        return score_li

    def torrent_addr(self, title, id):
        pass

    def cookie(self):
        return self.cookies
