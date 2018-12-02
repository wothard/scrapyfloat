#!/usr/bin/env python3
# encoding: utf-8


def page_detail(response):
    link_xpa = '//h3[@class="tit"]/a/@href'
    links = response.xpath(link_xpa)
    return links
