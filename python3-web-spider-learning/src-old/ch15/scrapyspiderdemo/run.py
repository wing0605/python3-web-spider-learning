#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: run.py
@time: 2022/1/19 14:55
@project: python3-web-spider-learning
@desc: 15.4 Spider的使用（P759）
"""
from scrapy.cmdline import execute

execute(['scrapy', 'crawl', 'httpbin', '--nolog'])
