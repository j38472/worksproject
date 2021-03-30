"""
北京，广州（11 9194）
"""

from time import sleep
import pymysql
from lxml import etree
import requests
import re
from fake_useragent import UserAgent


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
        self.ua = UserAgent().random
        self.headers = {
            # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
            'user-agent': self.ua
        }
        self.space_list = []
        self.produce_types_list = []

    # 关闭数据库
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def __call__(self, *args, **kwargs):
        self.get_type(*args, **kwargs)

    # 网页请求
    def get_response(self, url):
        try:
            sleep(0.3)
            response = requests.get(url=url, headers=self.headers)
            print(response.status_code)
            pages_text = response.text
            html = etree.HTML(pages_text)
            return html, pages_text
        except TimeoutError as e:
            print('网络连接断开，等待连接')
            sleep(10)
            print('重新连接')
            html, pages_text = self.get_response(url)
            return html, pages_text
        except Exception as e:
            print(e)
            return

    # 数据存储
    def save(self, dic):
        try:
            # 数据是否有效
            data_str = dic.get('telephone') + dic.get('phone')
            if not data_str:
                print('无效数据')
                return
            # 电话等联系信息的二次处理
            phone = dic.get('phone')
            telephone = dic.get('telephone')
            address = dic.get('address')
            telephone_z = ''
            if phone:
                # 判断长度
                if len(phone) == 11:
                    phone_str = re.findall('^[1][3,5,7,8][0-9]\\d{8}$', phone)
                    phone = phone_str[0] if phone_str else ''
                elif len(phone) < 11:
                    phone = ''
                elif len(phone) > 11:
                    # if len(phone) == 12:
                    # 双号码类型的数据
                    phone_data2 = re.findall('^[1][3,5,7,8][0-9]\\d{8}', phone)
                    phone = phone_data2[0] if phone_data2 else ''
                    # 手机号带有0的数据
                    if phone[0] == '0':
                        phone_data1 = re.findall('[1][3,5,7,8][0-9]\\d{8}$', phone)
                        phone = phone_data1[0] if phone_data1 else ''

            if telephone:
                # 将字符串处理成相似的格式
                telephone = telephone.replace(' ', '-').replace('+', '').lstrip('86-')
                # 判断字符长度
                if len(telephone) < 10:
                    telephone = ''
                elif len(telephone) > 13:
                    # 去除手机号加区号的格式
                    data = re.findall('[0]\d{2,3}-[2-9]\d{6,7}', telephone)
                    telephone = data[0] if data else ''
                elif telephone[0] != '0':
                    telephone = ''
                # 电话号码区号设置
                elif '-' not in telephone:
                    for i in ['北京', '天津', '上海', '重庆', '沈阳', '成都']:
                        if i in address:
                            telephone_z = telephone[:3] + '-' + telephone[3:]
                    telephone = telephone[:4] + '-' + telephone[4:]
                elif '—' in telephone:
                    telephone = telephone.replace('—', '')
            dic['telephone'] = telephone
            if telephone_z:
                dic['telephone'] = telephone_z
            dic['phone'] = phone
            # print(dic)
            # sql语句
            # if not dic.get('name'):
            #     print("联系人姓名为空")
            # 保存数据值和表字段不对称，需要加上对应的字段名
            sql1 = """
                insert into guangzhou (company, produce, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s);
                           """
            self.cursor.execute(sql1, (
                str(dic.get('company')) if dic.get('company') else '',
                str(dic.get('produce')) if dic.get('produce') else '',
                str(dic.get('name')) if dic.get('name') else '',
                str(dic.get('phone')) if dic.get('phone') else '',
                str(dic.get('telephone')) if dic.get('telephone') else '',
                str(dic.get('address')) if dic.get('address') else '',
                str(dic.get('href')) if dic.get('href') else ''
            ))
            self.conn.commit()
            print('%s保存成功' % dic.get('company'))
        except Exception as e:
            # 数据回滚
            self.conn.rollback()
            print(e)

    # 进入公司主页,获取联系方式
    def get_company(self, dic):
        print('{}公司主页'.format(dic.get('href')))
        c_url = dic.get('href')
        html, page_text = self.get_response(c_url)
        # 查找联系方式
        # detail_str = html.xpath('//div[@id="contact"]/div/dl//text()')
        detail_str = html.xpath('//div[@id="contact"]/div/dl//text()')
        detail = ''.join(detail_str).strip().replace(' ', '')
        # print(detail)
        telephone_list = re.findall('[0]\d{2,3}-[2-9]\d{6,7}|[0]\d{2,3} [2-9]\d{6,7}|[0]\d{2,3}[2-9]\d{6,7}', detail)
        dic['telephone'] = telephone_list[0] if telephone_list else ''
        # if telephone:
        #     telephone = telephone[0]
        phone_list = re.findall('[1][3,5,7,8][0-9]\\d{8}', detail)
        dic['phone'] = phone_list[0] if phone_list else ''
        # name_str = re.findall('经理：.{2,3}|联系人：.{2,3}|厂长：.{2,3}', detail)[0]  # [('','')]
        # dic['name'] = name_str[0]
        # if not name_str[0]:
        #     dic['name'] = name_str[1]
        # dic['name'] = '' if dic['name'] == '未提供' else dic['name']
        # dic['name'] = name_str.split('；')[1] if name_str else ''

        name_str = re.findall('经理：.{2,3}|联系人：.{2,3}|厂长：.{2,3}', detail)  # [('','')]
        if name_str:
            name = name_str[0].split('：')[1]
            if name == '未提供':
                name = ''
            dic['name'] = name

        self.save(dic)
        # print(telephone, phone, name)

    # 获取地区中的食品分类网址
    def get_type(self, url):
        # 拼接分类网址
        html, pages_text = self.get_response(url)
        # 获取数据条数和页码信息
        detail = re.findall('等在内的(.*?)家', pages_text)
        page = re.findall('共分为(.*?)页', pages_text)
        if not page:
            print('没有找到相关分类公司')
            return
        page = page[0]
        detail = detail[0]
        print(url, '{}页'.format(page), detail)
        if int(detail) > 2000:
            print('获取二级网址')
            # 获取下一级分类网址
            # 查找分类网址
            dd_list = html.xpath('//div[@id="il"]/div[2]/div[1]/dl/dd')
            # print(dd_list)
            for dd in dd_list:
                type_url = dd.xpath('./a/@href')
                # 若大于2000，
                if url:
                    # produce_types_list.append(type_url[0])
                    print(url)
                    self.get_type(type_url[0])
            return
        # 循环获取公司信息
        for pn in range(1, int(page) + 1):
            print('\t第{}页\t'.format(pn))
            # 判断页数拼接页码信息
            if pn > 1:
                next_url = 'https://www.11467.com/guangzhou/search/{}-{}.htm'.format(produce_type_list[data], pn)
                html, pages_text = self.get_response(next_url)
                print(next_url)

            # li_list = html.xpath('//div[@class="boxcontent"]/ul/li')
            # 在ul中获取不到所有的li标签，只能获取一个
            li_list = html.xpath('//div[@class="boxcontent"]//li')
            # print(li_list)
            for li in li_list:
                dic = {}
                href = li.xpath('./div[2]/h4/a/@href')
                if href:
                    dic['href'] = 'http://' + href[0].strip('/')
                    dic['company'] = li.xpath('./div[2]/h4/a/text()')[0]
                    dic['produce'] = li.xpath('./div[2]/div[1]/text()')[0]
                    dic['address'] = li.xpath('./div[2]/div[2]/text()')[0]
                    self.get_company(dic)


if __name__ == '__main__':
    produce_type_list = [
        '9118',
        '9126',
        '9134',
        '9135',
        '9152',
        '9159',
        '9160',
        '9161',
        '9175',
        '9181',
        '9193',
        '9194',
        '9208',
        '9209',
        '9222',
        '9229',
        '9234',
        '9244',
        '9256',
        '9267',
        '9274',
        '9281',
        '9282',
        '9283',
        '9284',
        '9285',
        '9305',
        '9318',
        '9321',
    ]

    produce_types_list = []
    auto_get = ShunQi()

    for data in range(len(produce_type_list)):
        print(data, produce_type_list[data])
        url = 'https://www.11467.com/guangzhou/search/{}.htm'.format(produce_type_list[data])
        auto_get(url)












