#!coding=utf-8
from bs4 import BeautifulSoup as bs
import re
import tools.Tools as tools

# 新建数组用于存放后续的数据
most_watched_book_list = []


def get_book_list(html_data):
    # 转化为BeautifulSoup对象
    soup = bs(html_data, 'html.parser')

    # 搜索最受关注的图书列表
    book_ul = soup.find_all('ul', 'chart-dashed-list')

    # 搜索列表中所有图书
    book_list = book_ul[0].find_all('div', 'media__body')

    # 遍历图书馆列表，从中过滤出我们所需的信息
    for item in book_list:
        # 新建字典用于存放我们的图书信息，之后可用class来存储
        most_watched_book_dict = {}

        # 得到图书名称
        most_watched_book_dict['name'] = item.h2.a.string.strip()

        # 得到图书评价人数（根据评价人数作为词云判断依据）
        evaluation = item.find('span', 'fleft ml8 color-gray').string.strip()
        most_watched_book_dict['value'] = re.search(r'[0-9]+', evaluation).group()

        # 将图书信息加入到字典中
        most_watched_book_list.append(most_watched_book_dict)


def run():
    url1 = 'https://book.douban.com/chart?subcat=I'
    url2 = 'https://book.douban.com/chart?subcat=F'
    r1 = tools.get_html(url1)
    r2 = tools.get_html(url2)
    get_book_list(r1)
    get_book_list(r2)
    return most_watched_book_list


# run()
# print(most_watched_book_list)
