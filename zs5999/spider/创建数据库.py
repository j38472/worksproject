import pymysql
from lxml import etree
import requests
import re


class ShunQi:

    # 数据库链接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='97655',
            db='zhaoshang5999',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
        }
        self.company_list = []

    # 关闭数据库
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # # 获取表名
    # def get_table(self, url):
    #     response = requests.get(url=url, headers=self.headers)
    #     print(response.status_code)
    #     pages_text = response.text
    #     html = etree.HTML(pages_text)
    #
    #     # 查找数据
    #     a_list = html.xpath('//div[@class="classify-food-detial"]/a')
    #     print(a_list)
    #     for a in a_list:
    #         href = a.xpath('./@href')[0]
    #         print(href)

    # 创建表
    def creat_table(self):
        for url in url_list:
            table = url.split('/')[-1]
            sql = """
                CREATE TABLE %s (
                  `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
                  `company` varchar(64) NULL COMMENT '公司名称',
                  `produce` varchar(512) NULL COMMENT '主营产品',
                  `name` varchar(32) NULL COMMENT '联系人',
                  `phone` varchar(32) NULL COMMENT '手机',
                  `telephone` varchar(64) NULL COMMENT '电话',
                  `address` varchar(255) NULL COMMENT '地址',
                  `href` varchar(255) NULL COMMENT '网址',
                  PRIMARY KEY (`id`)
                );
                """ % table
            self.cursor.execute(sql)
            self.conn.commit()

    def save_data(self, dic):
        try:
            # 获取数据库表名
            table = url.split('/')[-1]
            print(table)
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
            print('%s保存成功' % dic.get('company'))
        except Exception as e:
            print(e)
            self.conn.rollback()


url_list = [
        '/qiyeku/xiuxianshipin',
        '/qiyeku/sudongshipin',
        '/qiyeku/guantoushipin',
        '/qiyeku/fangbianshipin',
        '/qiyeku/tl',
        '/qiyeku/sxspzs',
        '/qiyeku/tsspzs',
        '/qiyeku/spyl',
        '/qiyeku/shiyongyou',
        '/qiyeku/baojianshipin',
        '/qiyeku/yzxc',
        '/qiyeku/bgl',
        '/qiyeku/kxt',
        '/qiyeku/ttc',
        '/qiyeku/sszs',
        '/qiyeku/scpzs',
        '/qiyeku/shengwuyinliao',
        '/qiyeku/ruanyinliao',
        '/qiyeku/congyinpin',
        '/qiyeku/lengyin',
        '/qiyeku/zwyc',
        '/qiyeku/ruyin',
        '/qiyeku/gnyl',
        '/qiyeku/gzylzs',
        '/qiyeku/tsylzs',
        '/qiyeku/yinliaobaozhuang',
        '/qiyeku/shipinbaozhuang',
        '/qiyeku/yinliaojixie',
        '/qiyeku/shipinjixie',
        '/qiyeku/plshiyongyou',
        '/qiyeku/pltl',
        '/qiyeku/plgxsp',
        '/qiyeku/pllsgw',
        '/qiyeku/tjzcj',
        '/qiyeku/tjsyss',
        '/qiyeku/tjxj',
        '/qiyeku/tjxl',
        '/qiyeku/tjtwj',
        '/qiyeku/tjffj',
        '/qiyeku/tjkyhj',
        '/qiyeku/tjrhj',
        '/qiyeku/tjbxj',
        '/qiyeku/tjsdtjj',
        '/qiyeku/tjpsj',
        '/qiyeku/tjzbj',
        '/qiyeku/tjsfbcj',
        '/qiyeku/tjyyqhj',
        '/qiyeku/tjpzglj',
        '/qiyeku/tjwdj',
        '/qiyeku/tjmzj',
        '/qiyeku/tjxpj',
        '/qiyeku/tjkjj',
        '/qiyeku/tjbmj',
        '/qiyeku/tjfjiaoj',
        '/qiyeku/tjzwj',
        '/qiyeku/tjmfclj',
        '/qiyeku/tjqita',
]
dic = {'href': 'www.xxx.com'}
creat = ShunQi()
for url in url_list:
    creat.save_data(dic)


