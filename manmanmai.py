#!coding=utf-8
import requests
import json
import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

requests.packages.urllib3.disable_warnings()

# 慢慢买历史价格爬取
class ManManMai:

    def __init__(self):
        # 无界面运行
        chrome_opt = Options()  # 创建参数设置对象.
        chrome_opt.add_argument('--headless')  # 无界面化.
        # chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
        chrome_opt.add_argument('no-sandbox')
        chrome_opt.add_argument('disable-dev-shm-usage')
        # chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.
        # # 创建Chrome对象并传入设置信息.
        # '/usr/bin/chromedriver',
        self.driver = webdriver.Chrome( options=chrome_opt)

    # 获取京东链接
    def get_jd_url(self, full_url):
        # 模拟用户点击
        self.driver.get(full_url)
        full_url = self.driver.current_url
        match_obj = re.match(r'[a-zA-z]+://[^\s]*[?]', full_url)
        jd_url = match_obj.group(0)[:-1]
        # self.driver.quit()
        return jd_url

    def raw(self, text):  # 转化URL字符串

        escape_dict = {
            '/': '%252F',
            '?': '%253F',
            '=': '%253D',
            ':': '%253A',
            '&': '%26',

        }
        new_string = ''
        for char in text:
            try:
                new_string += escape_dict[char]
            except KeyError:
                new_string += char
        return new_string

    # 分析与数据清洗
    def mmm(self, item):
        item = self.raw(item)
        url = 'https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'
        s = requests.session()
        headers = {
            'Host': 'apapia.manmanbuy.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Proxy-Connection': 'close',
            'Cookie': 'ASP.NET_SessionId=uwhkmhd023ce0yx22jag2e0o; jjkcpnew111=cp46144734_1171363291_2017/11/25',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 mmbWebBrowse',
            'Content-Length': '457',
            'Accept-Encoding': 'gzip',
            'Connection': 'close',
        }
        postdata = 'c_devid=2C5039AF-99D0-4800-BC36-DEB3654D202C&username=&qs=true&c_engver=1.2.35&c_devtoken=&c_devmodel=iPhone%20SE&c_contype=wifi&' \
                   't=1537348981671&c_win=w_320_h_568&p_url={}&' \
                   'c_ostype=ios&jsoncallback=%3F&c_ctrl=w_search_trend0_f_content&methodName=getBiJiaInfo_wxsmall&c_devtype=phone&' \
                   'jgzspic=no&c_operator=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8&c_appver=2.9.0&bj=false&c_dp=2&c_osver=10.3.3'.format(item)

        s.headers.update(headers)
        req = s.get(url=url, data=postdata, verify=False).text

        # print(req)
        try:
            js = json.loads(req)
            title = js['single']['title']  ##名称
        except Exception as e:
            print(e)
            # exit(mmm(item))
        ###数据清洗
        pic = js['single']['smallpic']  ##图片
        jiagequshi = js['single']['jiagequshi']  ##价格趋势
        lowerPrice = js['single']['lowerPrice']  ##最低价格
        lowerDate = js['single']['lowerDate']  ##最低价格日期
        lowerDate = re.search('[1-9]\d{0,9}', lowerDate).group(0)
        # print(lowerDate)
        lowerDate = time.strftime("%Y-%m-%d", time.localtime(int(lowerDate)))
        itemurl = js['single']['url']  ##商品链接
        qushi = js['single']['qushi']  ##趋势
        changPriceRemark = js['single']['changPriceRemark']  ##趋势变动
        date_list = []  ##日期
        price_list = []  ##价格
        ##日期转换
        datalist = jiagequshi.replace('[Date.UTC(', '').replace(')', '').replace(']', '').split(',')
        for i in range(0, len(datalist), 5):

            day = int(datalist[i + 2])
            if int(datalist[i + 1]) == 12:
                mon = 1
                year = int(datalist[i]) + 1
            else:
                mon = int(datalist[i + 1]) + 1
                year = int(datalist[i])

            date = datetime.date(year=year, month=mon, day=day)
            price = float(datalist[i + 3])
            date_list.append(date.strftime('%Y-%m-%d'))
            price_list.append(price)

        data = {'date': date_list, 'price': price_list}
        data['title'] = title
        data['pic'] = pic
        data['lowerPrice'] = lowerPrice
        data['lowerDate'] = lowerDate
        data['itemurl'] = itemurl
        data['qushi'] = qushi
        data['changPriceRemark'] = changPriceRemark

        print(data)
        return data
