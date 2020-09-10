#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   URLDB.py
@Time    :   2020/08/30 11:45:12
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2020-2021, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

import leveldb

class URLDB:
    ''' 使用LevelDB存储url已完成的操作（成功或失败）
    '''
    status_failure = b'0'
    status_success = b'1'

    def __init__(self,db_name):
        self.name = db_name + '.urldb'
        self.db = leveldb.LevelDB(self.name)

    def set_success(self, url):
        if isinstance(url, str): #判断URL是不是字符串类型
            url = url.encode('utf8')  # 设置URL编码格式为utf8
        try:
            self.db.Put(url, self.set_success) # 将下载成功的ULR存入levelDB数据库中
            s = True
        except:
            s = False
        return s

    def set_failure(self, url):
        if isinstance(url, str):
            url = url.encode('utf8')
        try:
            self.db.Put(url, self.set_failure) # 将下载失败的ULR存入levelDB数据库中
            s = True
        except:
            s = False
        return s

    def has(self, url):
        # 查看是否已经存在某url
        if isinstance(url, str):
            url = url.encode('utf8')
        try:
            attr = self.db.Get(url)
            return attr
        except:
            pass
        return False

if __name__ == "__main__":
    url = 'http://news.baidu.com'
    stu = URLDB('ww').has(url)
    print(stu)