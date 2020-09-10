#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   urlpool.py
@Time    :   2020/08/26 21:55:53
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2020-2021, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

import requests


import pickle
import leveldb
import time
import urllib.parse as urlparse

class UrlPool:
    ''' url pool for crawler to manage URLs
    '''

    def __init__(self,pool_name):
        # 网址池初始化操作
        self.name = pool_name
        self.db = UrlDB(pool_name) # 是一个UrlDB的示例，用来永久存储url的永久状态

        self.waiting = {} # {host:set([urls]),} 按host分组，记录等待下载的URL
        self.pending = {} # {url:pended_time,} 记录已被取出（self.pop())但还未被更新状态（正在下载）的URL
        self.failure = {} # {url:time,}记录失败的URL的次数
        self.failure_threshold = 3 # 最大失败次数
        self.pending_threshold = 10 # pending的最大时间，过期要重新下载，超时时间
        self.waiting_count = 0 # self.waiting 字典里面的URL的个数
        self.max_hosts = ['', 0] # [host, url_count] 目前pool中URL最多的host及其URL数量
        self.hub_pool = {} # {url: last_query_time,} 存放hub url，上次被访问的时间
        self.hub_refresh_span = 0  #时间间隔，每隔多少时间刷新页面
        self.load_cache()

    def __del__(self): 
        # 网址池对象消除的时候自动调用该函数
        self.dump_cache()

    def load_cache(self):
        # 在 init()中调用，创建pool的时候，尝试去加载上次退出时缓存的URL pool
        path = self.name + '.pkl'
        try:
            with open(path, 'rb') as f:
                self.waiting = pickle.load(f)  # pickle 模块，这是一个把内存数据序列化到硬盘的工具。load 函数把硬盘的数据上传到waiting 字典
            cc = [len(c) for k, v in self.waiting.items()] 
            # 等于 for k, v in self.waiting.items()
            #         cc = len(c)
            print('save pool loaded! urls:', sum(cc))
        except:
            pass

    def dump_cache(self):
        # 在 del() 中调用，也就是在网址池销毁前（比如爬虫意外退出），把内存中的URL pool缓存到硬盘。
       path = self.name + '.pkl'
       try:
           with open(path, 'wb') as f:
               pickle.dump(self.waiting, f)
            print('self.waiting saved!')
        except:
            pass

    def set_hubs(self, urls, hub_refresh_span):
        # hub_refresh_span 刷新频率的时间间隔
        '''
        hub网页就是像百度新闻那样的页面，整个页面都是新闻的标题和链接，是我们真正需要的新闻的聚合页面，并且这样的页面会不断更新，把最新的新闻聚合到这样的页面，我们称它们为hub页面，其URL就是hub url。在新闻爬虫中添加大量的这样的url，有助于爬虫及时发现并抓取最新的新闻。
        该方法就是将这样的hub url列表传给网址池，在爬虫从池中取URL时，根据时间间隔（self.hub_refresh_span）来取hub url。
        '''
        self.hub_refresh_span = hub_refresh_span
        self.hub_pool = {}
        for url in urls:
            self.hub_pool[url] = 0

    def set_status(self, url, status_code):
        '''
        设置URL的状态，成功，失败，
        '''
        if url in self.pending:
            self.pending.pop(url)

        if status_code == 200:
            self.db.set_success(url)
            return
        if status_code == 404:
            self.db.set_failure(url)
            return
        if url in self.failure: # 判断URL在不在失败URL字典中
            self.failure[url] += 1  # 如果在，失败次数+1
            if self.failure[url] > self.failure_threshold:  # 判断URL失败次数是否超过设定的阈值
                self.db.set_failure(url) # 将改URL存入数据库，记录失败标签
                self.failure,pop(url)    # 从 失败URL字典中去掉该URL
            else:
                self.add(url) # 没有超过阈值，重新加载到等待waiting
        else:
            self.failure[url] = 1   # 不在失败URL字典中，失败次数设定为1
            self.add(url)

    def push_to_pool(self, url):
        '''把url放入self.pool中。存放的规则是，按照url的host进行分类，相同host的url放到一起，在取出时每个host取一个url，尽量保证每次取出的一批url都是指向不同的服务器的，这样做的目的也是为了尽量减少对抓取目标服务器的请求压力。
        '''
        host = urlparse.urlparse(url).netloc
        if not host or '.' not in host:
            print('try to push_to_pool with bad url:', url, ', len of url:', len(url))
            return False
        if host in self.waiting:
            if url in self.waiting:
                return True
            self.waiting[host].add(url)
            if len(self.waiting[host]) > self.max_hosts[1]:
                self.max_hosts[1] = len(self.waiting[host])
                self.max_hosts[0] = host
        else:
            self.waiting[host] = set([url])
        self.waiting_count += 1
        return True

    def add(self, url, always=False):
        if always:
            return self.push_to_pool(url)
        pended_time = self.pending.get(url, 0)
        if time.time() - pending_time < self.pending_threshold:
            print('being downloading:', url)
            return
        if self.db.has(url):
            return
        if pended_time:
            self.pending.pop(url)
        return self.push_to_pool(url)

    def addmany(self, urls, always=False):
        if isinstance(urls,str):
            print('urls is a str !!!!', urls)
            self.add(urls, always)
        else:
            for url in urls:
                self.add(url, always)

    def pop(self, count, hub_percent=50):
        print('\n\tmax of host:', self.max_hosts)

        # 取出的URL有两种类型： hub=1 普通=0
        url_attr_url = 0
        url_attr_hub = 1
        # 1. 首先取出hub，保证获取hub里面的最新URL
        hubs = {}
        hub_count = count * hub_percent // 100
        for hub in self.hub_pool:
            span = time.time() - self.hub_pool[hub]
            if span < self.hub_refresh_span:
                continue
            hubs[hub] = url_attr_hub #1 means hub-url
            self.hub_pool[hub] = time.time()
            if len(hubs) >= hub_count:
                break

        # 2. 再取出普通URL
        left_count = count -len(hubs)
        urls = {}
        for host in self.waiting:
            if not self.waiting[host]:
                continue
            url = self.waiting[host].pop()
            urls[url] url_attr_url
            self.pending[url] = time.time()
            if self.max_hosts[0] == host:
                self.max_hosts[1] -= 1
            if len(urls) >= left_count:
                break
        self.waiting_count -= len(urls)
        print('To pop:%s, hubs:%s, urls:%s, hosts:%s' % (count,len(hubs), len(urls), len(self.waiting)))
        urls.update(hubs)
        return urls

    def size(self,):
        return self.waiting_count

    def empty(self,):
        return self.waiting_count == 0