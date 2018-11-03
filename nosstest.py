#!/usr/bin/env python3
# encoding: utf-8

from lxml import html
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
    ' (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,' +
    'image/webp,image/apng,*/*;q=0.8'
    }


def noss():
    url = "http://www.xilebox.com/box/671269?t=4"
    url2 = "http://www.a2p1.com"
    s = requests.get(url, headers=headers, timeout=10)
    tree = html.fromstring(s.text)
    print(s.text)


noss()
