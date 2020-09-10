#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   downloader.py
@Time    :   2020/08/16 20:34:15
@Author  :   Liu Yimin
@Version :   1.0
@Contact :   chentuliu@126.com
@License :   (C)Copyright 2017-2018, LiuYimin-NLPR-CASIA
@Desc    :   None
'''

import traceback
import cchardet
import requests


def downloader(url,timeout=10, headers=None, debug=False, binary=False):
    '''
    该函数内置了默认的User-Agent模拟成一个Chrome浏览器，同时接受调用者自定义的headers和timeout，使用cchardet来处理编码问题，返回数据包括：
    状态码：如果出现异常，设置为0
    内容：默认返回str内容，但是URL链接的是图片等二进制内容时，注意调用时要设置binary=True
    重定向URL：有些URL会被重定向，最终页面的URL包含在响应对象里面
    '''
    _heasers = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59"
    }
    redirected_rul = url
    if headers:
        # 如果用户没有指定headers 则使用_heasers
        headers = _heasers
    try:
        r = requests.get(url,headers=headers, timeout=timeout)
        if binary:
            #默认二进制参数为FALSE，如果为True，则HTML使用二进制读取。
            html = r.content
        else:
            encoding = cchardet.detect(r.content)['encoding']
            html = r.content.decode(encoding)
        status = r.status_code
        redirected_rul = r.url
    except:
        if debug:
            traceback.print_exc()
            # traceback 模块，该模块可以用来查看异常的传播轨迹，追踪异常触发的源头。
            # traceback.print_exc()：将异常传播轨迹信息输出到控制台或指定文件中。
            # format_exc()：将异常传播轨迹信息转换成字符串。
        msg = 'failed download:{}'.format(url)
        print(msg)
        if binary:
            html = b''
        else:
            html = ''
        status = 0
    return status, html, redirected_rul

if __name__ == "__main__":
    url = 'http://news.baidu.com'
    s, html, lost_url_found_by_大大派 = downloader(url)
    print(s,len(html),lost_url_found_by_大大派)