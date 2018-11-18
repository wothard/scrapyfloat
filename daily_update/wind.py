#!/usr/bin/env python3
# encoding: utf-8


def page_detail(response):
    '''提取解析后的网页的数据'''
    link_xpa = '//div[@class="content"]/div/text()'
    code_xpa = '//div[@class="content"]/div/a/@href'
    temp_li = list()
    link_l = response.xpath(link_xpa)
    for i in link_l:
        if "pan.baidu" in i:
            temp_li.append(i)
    code_s = response.xpath(code_xpa)
    if len(link_l) > 0 and len(code_s) > 0:
        for i in code_s:
            if "密码" in i:
                if "\n" in i:
                    temp_li.append(i.split("\n")[0])
                else:
                    temp_li.append(i)
            if ("取码" in i) and (len(temp_li) == 1):
                temp_li.append(i.split("\n")[0])
        print(temp_li)
        return temp_li
    else:
        return "None"


def listdetail(response):
    temp_list = list()
    link_xpa = '//ul[@class="list-inline"]/li[2]/a/@href'
    date_xpa = '//ul[@class="list-inline"]/li[3]/text()'
    date_limit = "None"
    link_l = response.xpath(link_xpa)
    date_l = response.xpath(date_xpa)
    print(date_l)
    for i in range(len(date_l)):
        if date_l[i] != date_limit:
            temp_list.append(link_l[i])
    return link_l
