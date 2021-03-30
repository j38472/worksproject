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
            db='shunqi',
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

    # 获取表名
    def get_table(self, url):
        response = requests.get(url=url, headers=self.headers)
        print(response.status_code)
        pages_text = response.text
        html = etree.HTML(pages_text)

        # 查找数据
        a_list = html.xpath('//div[@class="boxcontent"]/dl/a')
        # print(a_list)
        for a in a_list:
            href = a.xpath('./@href')[0]
            table = re.findall('com/(.*?)/search/', href)
            self.company_list.append(table[0])

    # 创建表
    def creat_table(self):
        for table in self.company_list:
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


url = 'http://b2b.11467.com/search/3361.htm'
creat = ShunQi()
creat.get_table(url)
creat.creat_table()


