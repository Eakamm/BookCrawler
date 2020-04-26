#!coding=utf-8
from bs4 import BeautifulSoup as bs
import re
import jieba  # 分词包
import pandas as pd  # 分词用到
import requests
from fake_useragent import UserAgent #伪装
import random
import time


def get_html(url):
    ua = UserAgent()
    user_agent = {
        'User-Agent': ua.google
    }
    # 使用代理，防止反爬 https://www.xicidaili.com/nn/
    proxies = {
        "http": "101.132.190.101:80",
        "https": "110.243.10.182:9999",
    }
    # print(ua.google)
    r = requests.get(url=url, headers=user_agent)
    # r.raise_for_status()
    r.encoding = 'utf-8'
    time.sleep(random.random()*4)
    return r.text


def get_word_cut(commits):

    # 可以看到所有的评论已经变成一个字符串了，但我们发现评论中还有不少标点符号等
    # 这些符号对我们进行词频统计根本就没有用，因此将他们清除，所用的方法是正则表达式
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, commits)
    cleaned_comments = ''.join(filterdata)
    # print('评论数组')
    # print(eachCommentList)
    # print('评论字符串')
    # print(commits)
    # print('去除标点符号的评论')
    # print(cleaned_comments)
    # exit()

    # 在这里使用的是结巴分词，如果没有安装结巴分词，可以在控制台用 pip install jieba安装
    segment = jieba.lcut(cleaned_comments)
    # print(segment)
    # exit()
    # 可以使用pandas库将分词转化成dataframe格式，head()方法只查看前五项内容
    words_df = pd.DataFrame({'word': segment})

    # 可以看到我们的数据中有“我”、“很”等虚词（停用词）
    # 而这些词在任何场景中都是高频时，并且没有实际含义，所以我们要对他们进行清除
    # 把停用词放在一个stopwords.txt文件中，将我们的数据与停用词进行对比即可

    stopwords = pd.read_csv("./stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='utf-8')
    # print(stopwords)

    words_df = words_df[~words_df.word.isin(stopwords.stopword)]
    # print(words_df.head())
    # exit()

    # 接下来进行词频统计
    words_stat = words_df.groupby(by=['word'])['word'].agg(['count'])
    # print(words_stat.head())

    # 对统计结果进行排序
    words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)

    return words_stat

