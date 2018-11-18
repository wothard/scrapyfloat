#!/usr/bin/env python3
# encoding: utf-8

import os


def load_ua():
    with open(os.getcwd()+'/data/user-agent.txt', 'r') as f:
        return f.readlines()


def fakeheader():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=' +
        '0.9,image/webp,image/apng,*/*;q=0.8'
    }
    return headers
