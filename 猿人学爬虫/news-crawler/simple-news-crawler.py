#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   simple-news-crawler.py
@Time    :   2020/08/15 21:02:25
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2017-2018, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

import requests
import re
import time
import tldextract


def save_to_db(url, html):
    # 保存网页到数据库,我们暂时用打印相关信息替代
    print('%s : %s' % (url, len(html)))

def crawl():
    # 1. 下载百度新闻
    hub_url='http://news.baidu.com'
    res=requests.get(hub_url)
    html=res.text

    # 2. 提取新闻链接
    # 2.1 提取所有关于'href'得到链接
    links=re.findall(r'href=[\'"]?(.*?)[\'"\s]', html)
    print('find links: ', len(links))
    news_links=[]
    # 2.2  过滤非新闻链接
    for link in links:
        if not link.startswith('http'):  
            #string.startswith(obj, beg=0,end=len(string))检查字符串是否是以 obj 开头，是则返回 True，否则返回 False。如果beg 和 end 指定值，则在指定范围内检查.类似的还有 string.endswith(obj, beg=0, end=len(string))检查结尾是否obj，string.find(str, beg=0, end=len(string))检查是否包含obj.
            continue
        tld=tldextract.extract(link)
        # tldextract 第三方模块，顶级域名提取，URL news.baidu.com结构中，news.baidu.com叫做host，它是注册域名baidu.com的子域名，而com就是顶级域名TLD。
        if tld.domain == 'baidu':
            continue
        news_links.append(link)

    print('find news links:', len(news_links))

    # 3. 下载新闻并且保存到数据库
    for link in news_links:
        html=requests.get(link).text
        save_to_db(link, html)
    print('works done!')

def main():
    # 简历死循环，每爬取一次，休息300秒
    while 1:
        crawl()
        time.sleep(300)


if __name__ == "__main__":
    main()
