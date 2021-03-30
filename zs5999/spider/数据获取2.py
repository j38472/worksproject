"""
网页页码的获取问题，查找标签不能够统一获取下一页的url地址
采取页面查找的方式获取相应分类的页码
使用代理可以加快速度，但网站的承受能力可能不行

"""

import re
from time import sleep
from random import randint
import requests
from fake_useragent import UserAgent
from lxml import etree
import pymysql


# 数据获取类
class M:

    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='97655',
            db='zhaoshang5999',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        # 全局变量
        self.headers = {
            'user-agent': UserAgent().random
        }
        self.pages = 0
        self.page = 48

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def __call__(self, *args, **kwargs):
        self.get_data(*args, **kwargs)

    # 添加代理
    
    # 网页请求
    def get_response(self, g_url):
        try:
            # 随机延时
            sleep(randint(3, 6))
            response = requests.get(url=g_url, headers=self.headers, timeout=10, stream=True)
            status = response.status_code
            print(status, g_url)
            page_text = response.text
            if status != 200:
                print('网页响应失败')
                if status == 404:
                    return
                elif status == 503:
                    return
            return etree.HTML(page_text)
        # url网址格式问题
        except requests.exceptions.InvalidURL as e:
            print('网址格式错误，无法请求', e)
            return
        except Exception as e:
            print("请求出错", e)

    # 获取页面中所有企业数据和下一页网址链接
    def get_data(self, n_url):
        # print('第{}个数据'.format(index))
        html = self.get_response(n_url)
        # if html is None:
        #     print('网页为空')
        #     return
        if html is None:
            print('网页为空')
            self.get_response(n_url)
        # 获取网页中的页码数
        # data_str = html.xpath('//div[@class="pageLt pageLeft"]//text()')
        data_str = html.xpath('//div[@class="pageLt pageLeft"]//text()')
        data = ''.join(data_str)
        page = re.findall(r'/(.*?)页', data)
        self.pages = int(page[0]) if page else 0
        print('第{}个数据, 共有{}页'.format(index, self.pages))
        for pn in range(self.page, self.pages + 1):
            # 拼接网页，获取下一页地址
            if pn > 1:
                print('第{}个数据，第{}页'.format(index, pn))
                next_url = 'http://www.5999.tv/qiyeku%s/%s.html' % (url, pn)
                html = self.get_response(next_url)
                if html is None:
                    print('网页响应为空')
                    sleep(3)
                    html = self.get_response(next_url)
            # 获取页面中所有企业的信息
            li_list = html.xpath('//div[@class="companies-left"]/ul/li')
            # print(li_list)
            for li in li_list:
                dic = {}
                href = li.xpath('./div/div/h3/a/@href')
                # print(href)
                if not href:
                    continue
                dic['href'] = href[0]
                company = li.xpath('./div/div/h3/a/text()')
                produce_list = li.xpath('./div/div/p[2]//text()')
                produce_str = ''.join(produce_list).replace('\t', '').replace('\n', '')
                dic['company'] = company[0] if company else ''
                dic['produce'] = produce_str
                # print(dic)
                # 拼接网页，获取联系信息网址
                data = dic.get('href').split('/')[-1].split('.')[0]
                detail_url = 'http://m.5999.tv/company/%s/jianjie.html' % data
                # print(data, next_url)
                self.get_detail(detail_url, dic)

    # 获取联系信息
    def get_detail(self, d_url, dic):
        # 网址可能无效
        html = self.get_response(d_url)
        if html is None:
            print('没有此页面')
            return
        data_str = html.xpath('//div[@class="BItroText"]/ul//text()')
        data = ''.join(data_str).replace('\t', '').replace('\n', '').replace(' ', '')
        # 使用re获取电话或手机数据
        telephone = re.findall(r'[0]\d{2,3}-[2-9]\d{6,7}|[0]\d{2,3}\)[2-9]\d{6,7}|[0]\d{2,3}[2-9]\d{6,7}', data)
        phone = re.findall(r'[1][3,5,7,8][0-9]\d{8}', data)
        dic['telephone'] = telephone[0] if telephone else ''
        dic['phone'] = phone[0] if phone else ''
        # print(telephone, phone)
        li_list = html.xpath('//div[@class="BItroText"]/ul/li')
        for li in li_list:
            detail = li.xpath('./text()')[0]
            # print(detail)
            if '联 系 人:' in detail:
                dic['name'] = detail.split(':')[-1]
            elif '公司地址：' in detail:
                dic['address'] = detail.split('：')[-1]
        # 保存数据
        self.save_data(dic)

    def save_data(self, dic):
        try:
            # 获取数据库表名
            table = url.split('/')[-1]
            # sql语句
            # 保存数据值和表字段不对称，需要加上对应的字段名
            sql1 = """
                insert into {} (company, produce, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s);
                           """.format(table)
            self.cursor.execute(sql1, (
                str(dic.get('company')) if dic.get('company') else '',
                str(dic.get('produce')) if dic.get('produce') else '',
                # str(dic.get('company_type')) if dic.get('company_type') else '',
                str(dic.get('name')) if dic.get('name') else '',
                str(dic.get('phone')) if dic.get('phone') else '',
                str(dic.get('telephone')) if dic.get('telephone') else '',
                str(dic.get('address')) if dic.get('address') else '',
                str(dic.get('href')) if dic.get('href') else ''
            ))
            self.conn.commit()
            print('%s保存成功' % dic.get('company'), '在表{}中'.format(table))
        except Exception as e:
            print(e)
            self.conn.rollback()


if __name__ == '__main__':
    url_list = [
        '/xiuxianshipin',
        '/sudongshipin',
        '/guantoushipin',
        '/fangbianshipin',
        '/tl',
        '/sxspzs',
        '/tsspzs',
        '/spyl',
        '/shiyongyou',
        '/baojianshipin',
        '/yzxc',
        '/bgl',
        '/kxt',
        '/ttc',
        '/sszs',
        '/scpzs',
        '/shengwuyinliao',
        '/ruanyinliao',
        '/congyinpin',
        '/lengyin',
        '/zwyc',
        '/ruyin',
        '/gnyl',
        '/gzylzs',
        '/tsylzs',
        '/yinliaobaozhuang',
        '/shipinbaozhuang',
        '/yinliaojixie',
        '/shipinjixie',
        '/plshiyongyou',
        '/pltl',
        '/plgxsp',
        '/pllsgw',
        '/tjzcj',
        '/tjsyss',
        '/tjxj',
        '/tjxl',
        '/tjtwj',
        '/tjffj',
        '/tjkyhj',
        '/tjrhj',
        '/tjbxj',
        '/tjsdtjj',
        '/tjpsj',
        '/tjzbj',
        '/tjsfbcj',
        '/tjyyqhj',
        '/tjpzglj',
        '/tjwdj',
        '/tjmzj',
        '/tjxpj',
        '/tjkjj',
        '/tjbmj',
        '/tjfjiaoj',
        '/tjzwj',
        '/tjmfclj',
        '/tjqita',
]
    bro = M()
    for index, url in enumerate(url_list):
        if index > 2:
            c_url = 'http://www.5999.tv/qiyeku' + url
            bro(c_url)




"""
start  96
end    170

0  193  
0  360

第四个数据未获取
第3个数据，第48页
"""