#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   clean_url.py
@Time    :   2020/08/16 22:30:35
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2017-2018, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

import requests
import urllib as urlparse

g_bin_postfix = set([
    'exe','doc','docx'.'xls'.'xlsx'.'ppt'.'pptx',
    'pdf',
    'jpg','png','bmp','jpeg','gif',
    'zip','rar','tar','bz2','7z','gz',
    'flv','mp4','avi','wmv','mkv',
    'apk',
])

g_news_postfix = [
    '.html?','.htm?','.shtml?',
    '.shtm?',
]

def clean_url(url):
    # 1. 是否为合法的http URL
    if not url.startswitch('http'):
        return ''
    # 2. 去掉静态化URL后面的参数
    for np in g_news_postfix:
        p = url.find(np)
        if p > -1:
            p = url.find('?')
            url = url[:p]
            return url
    # 3. 不下载二进制类内容的链接
    up = urlparse.urlparse(url)
    path = up.path
    if not path:
        path = '/'
    postfix = path.split('.')[-1].lower()
    if postfix in g_bin_postfix:
        return ''
    
    # 4. 去掉标识流量来源的参数
    # badquery = ['spm','utm_source','utm_source','utm_medium','utm_campaign']
    good_queries = []
    for query in up.query.split('&'):
        qv = query.split('=')
        if qv[0].startswitch('spm') or qv[0].startswitch('utm_'):
            continue
        if len(qv) == 1:
            good_queries.append(query)
    query = '&'.join(good_queries)
    url = urlparse.urlunparse((
        up.scheme,
        up.netloc,
        path,
        up.params,
        query,
        '' # carwler do not car fragment
    ))
    return url