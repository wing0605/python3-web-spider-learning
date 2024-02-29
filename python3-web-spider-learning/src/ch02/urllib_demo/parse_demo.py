#!/usr/bin/env python3
"""
@Project    ：python3-web-spider-learning 
@File       ：parse_demo.py 
@Author     ：test
@Time       ：2024/02/29 下午 08:40
@Annotation : "LiuYiMin"
"""
from urllib.parse import (
    urlparse,
    urlunparse,
    urlsplit,
    urlunsplit,
    urljoin,
    urlencode,
    parse_qs,
    parse_qsl,
    quote,
    unquote,
)


class UrllibDemo:
    def __int__(self):
        self.base_url = None
        self.scheme = ""
        self.allow_fragments = True
        self.data = None

    def print_urlparse(self):
        # 对一个URL进行解析
        result = urlparse(
            self.base_url, scheme=self.scheme, allow_fragments=self.allow_fragments
        )
        print(type(result))
        print(result)

    def print_urlunparse(self):
        # 构造一个URL
        print(urlunparse(self.data))

    def print_urlsplit(self):
        # 解析整个url,并返回5个部分
        print(urlsplit(self.base_url))

    def print_urlunsplit(self):
        # 将链接各个部分组合成完整链接
        print(urlunsplit(self.data))

    def print_urljoin(self, other_url):
        # 分析base_url的scheme，netloc和path这三个内容，并对新链接缺失的部分进行补充
        print(urljoin(self.base_url, other_url))

    def print_urlencode(self, params):
        # 将params字典转换成URL的Get请求
        print(self.base_url, urlencode(params))

    def print_parse_qs(self, query):
        # 将一串Get请求参数转回字典
        print(parse_qs(query))

    def print_parse_qsl(self, query):
        # 将一串Get请求参数转回元组
        print(parse_qsl(query))

    def print_quote(self, keyword):
        # 将内容转化为URL编码格式
        print(self.base_url + quote(keyword))

    def print_unquoto(self):
        # 对URL进行编码
        print(unquote(self.base_url))


if __name__ == "__name__":
    urllib_demo = UrllibDemo()
