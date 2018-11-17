#!/usr/bin/env python3
# encoding: utf-8

import os


def load_ua():
    with open(os.getcwd()+'/data/user-agent.txt', 'r') as f:
        return f.readlines()
