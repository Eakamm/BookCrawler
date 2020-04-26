#!coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
import tools.Tools as tools


def get_top250_book(html_data, topchart_list):
        # 转化为BeautifulSoup对象
        soup = bs(html_data, 'html.parser')

        # 搜索Top250图书div
        topchart_book = soup.find('div', 'indent')

        # 搜索列表中所有图书
        topchart_book_list = topchart_book.find_all('tr', 'item')
        # print(topchart_book_list[0])
        # 遍历图书馆列表，从中过滤出我们所需的信息
        for item in topchart_book_list:
            # 新建字典用于存放我们的图书信息，之后可用class来存储
            topchart_dict = {}
            # print(item)
            # 搜索到具体信息的位置
            commentsNumber = item.find('span','pl')
            # print(commentsNumber)

            # 得到图书评价人数
            topchart_dict['value'] = re.search(r'[0-9]+',commentsNumber.string.strip()).group()

            # 得到图书名称
            topchart_dict['name'] = ''
            for string in item.find('div', 'pl2').a.stripped_strings:
                if string is not None:
                   topchart_dict['name'] = topchart_dict['name'] + string
           
            # print(topchart_dict)
            # 将图书信息加入到数组中
            topchart_list.append(topchart_dict)
            # print(topchart_list)


def run():
    topchart_list = []
    count = 0
    url = 'https://book.douban.com/top250?start='
    url2 = url
    while count <= 250:
        # print(url2)
        html_data = tools.get_html(url2)
        # print(url2)
        get_top250_book(html_data, topchart_list)
        count += 25
        url2 = url+str(count)
    return topchart_list



