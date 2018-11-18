#!/usr/bin/env python3
# encoding: utf-8

import random
import requests
import lxml


def same_request(url, agent, headers, proxies):
    temp_agent = (random.choice(agent)).split("\n")[0]
    headers["User-Agent"] = temp_agent
    proxy = {"http": "http://" + random.choice(proxies)}
    s = requests.get(url, headers=headers, proxies=proxy, timeout=8)
    s.encoding = "utf-8"
    response = lxml.html.fromstring(s.text)
    return response
