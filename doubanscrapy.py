#!/usr/bin/env python3
# encoding: utf-8


from fake_agent import fakeagent
from request_same.same import same_request
import random
import time


class Doubanscrapy(object):
    def __init__(self, url, proxies):
        self.user_agent = fakeagent.load_ua()
        self.url = url
        self.proxies = proxies
        self.score = '//strong[@class="ll rating_num"]/text()'
        self.comment = '//a[@href="collections"]/span/text()'
        self.headers = fakeagent.fakeheader()
        self.result_list = list()

    def run(self):
        while 1:
            proxy = {"http": "http://" + random.choice(self.proxies)}
            try:
                response = same_request(self.url, self.user_agent,
                                        self.headers, proxy)
                result = self.request_douban(response)
                time.sleep(10)
                return (result, self.url)
                break
            except Exception:
                pass
                # print(e)

    def request_douban(self, response):
        score_s = response.xpath(self.score)
        comment_s = response.xpath(self.comment)
        # print(score_s, comment_s)
        return [score_s[0], comment_s[0]]
