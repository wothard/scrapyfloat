#!/usr/bin/env python3
# encoding: utf-8

from fake_agent import fakeagent
from request_same.same import same_request
from daily_update import fairone
import requests


class Ingscrapy(object):
    '''传入两个参数， [url列表] 和 [prox代理列表]'''
    def __init__(self, url, proxies):
        self.url = url
        self.proxies = proxies
        self.user_agent = fakeagent.load_ua()
        self.headers = fakeagent.fakeheader()
        # 定义一个列表或者字典 用于存储返回的数据
        # self.result = list()
        # 最多修改的地方，创建 xpath 语法 抓取对应内容
        # self.temp_xpa = '//div[@class="content"]/div/text()'
        # self.temp_xpa2 = '//div[@class="content"]/div/a/@href'

    def run(self):
        result = None
        while 1:
            try:
                response = same_request(
                    self.url, self.user_agent,
                    self.headers, self.proxies
                    )
                result = self.analysis(response)
                # result = fairone.page_detail(response)
                return result
            except requests.exceptions.ReadTimeout:
                pass
            # except Exception as e:
            #     print(type(e), e)
            except Exception as e:
                print(e)

    def analysis(self, response):
        '''将获取到的网页转换成字符串后，提取所需内容'''
        link_l = '//h3/a[2]/@href'
        link = response.xpath(link_l)
        print(link[0])
        return link[0]
        # result = wind.listdetail(response)
        # return result
        # temp_li = list()
        # link_l = response.xpath(self.temp_xpa2)
        # for i in link_l:
        #     if "pan.baidu" in i:
        #         temp_li.append(i)
        # code_s = response.xpath(self.temp_xpa)
        # if len(link_l) > 0 and len(code_s) > 0:
        #     for i in code_s:
        #         if "密码" in i:
        #             if "\n" in i:
        #                 temp_li.append(i.split("\n")[0])
        #             else:
        #                 temp_li.append(i)
        #         if ("取码" in i) and (len(temp_li) == 1):
        #             temp_li.append(i.split("\n")[0])
        #     print(temp_li)
        #     return temp_li
        # else:
        #     return "None"
