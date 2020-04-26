#!coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
import tools.Tools as tools
import json
import time
import random



def get_Comments(book_url, count, eachCommentList):

    # 拼接出图书对应的详情页
    commennt_url = book_url + 'comments/hot' + '?' + 'p-'+str(count)
    print(commennt_url)

    html_data = tools.get_html(commennt_url)

    soup = bs(html_data, 'html.parser')
    # print(soup)
    # 搜索到评论所在div
    comment_div_lits = soup.find_all('div', 'comment')


    for item in comment_div_lits:
        # print(item)
        if item.find('p').span.string is not None:
            eachCommentList.append(item.find('p').span.string)
    print(eachCommentList)


def run(book_url):
    count = 1

    # 新建数组用于存放评论信息
    eachCommentList = []

    # 翻页
    while count <= 2:
        get_Comments(book_url, count, eachCommentList)
        count += 1

    # 为了方便进行数据进行清洗，我们将列表中的数据放在一个字符串数组中
    commits = ''
    for k in range(len(eachCommentList)):
        commits = commits + (str(eachCommentList[k])).strip()

    words_stat = tools.get_word_cut(commits)
    words_arr = []
    count = 0

    # 将DataFrame格式数据转为字典，来为词云使用

    # 先将每一列提取出来
    df1 = words_stat['word'].tolist()
    df2 = words_stat['count'].tolist()
    # 合并两个列表为字典数组
    for name in df1:
        words_dict = {}
        words_dict['name'] = name
        words_dict['value'] = df2[count]
        count += 1
        words_arr.append(words_dict)

    # 合并两个列表为字典
    # words_arr = dict(zip(df1, df2))
    # count = 0

    # DataFrame格式数据转为json
    # df_json = words_stat.to_json(orient='split', force_ascii=False)

    # 处理为json返回
    return json.dumps(words_arr)
