#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2020/08/18 22:29:41
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2017-2018, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

from ezpymysql import Connection

db = Connection(
    '118.25.49.252',
    'crawler',
    'root',
    '123456'
)

#获取一条记录
sql = 'SELECT * from test_table where id=%s'
data = db.get(sql, 2)
print(data)

# #获取多条记录
# sql = 'SELECT * from test_table where  id > %s'
# data = db.query(sql,2)

# #插入一条数据
# sql = 'INSERT INTO test_table(title,url) VALUES(%s, %s)'
# last_id = db.execute(sql, 'test', 'http://a.com/')
# #或者
# last_id = db.insert(sql, 'test','http://a.com/')

# #使用更高级的方法插入数据
# item = {
#     'title' : 'test',
#     'url' : 'http://a.com/'
# }

# last_id = db.table_insert('test_table', item)