#!/usr/bin/env python3
# encoding: utf-8

import random
import requests
import lxml


def same_request(url, agent, headers, proxy):
    temp_agent = (random.choice(agent)).split("\n")[0]
    headers["User-Agent"] = temp_agent
    s = requests.get(url, headers=headers, proxies=proxy, timeout=4)
    print(s.text)
    if s.status_code == 403:
        raise Warning
    s.encoding = "utf-8"
    response = lxml.html.fromstring(s.text)
    return response
