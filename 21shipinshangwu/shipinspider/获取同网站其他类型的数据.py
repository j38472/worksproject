"""
使用代理进行网站爬取
7
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
from pymysql import connect
from time import sleep
from random import randint
import re


# 定义数据获取类 ， 21食品商务网
class ShiPin:

    # 1.启动函数，开启数据库
    def __init__(self):
        print('开启数据库')
        self.conn = connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='97655',
            db='21shuju',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.page = 1
        self.pages = 0
        self.n = 1
        self.headers = {
            'user-agent': UserAgent().random
        }
        self.ip, self.port = self.get_proxy()

    def __call__(self, *args, **kwargs):
        self.get_pages(*args, *kwargs)

    # 2.关闭数据库
    def __del__(self):
        print('关闭数据库')
        self.cursor.close()
        self.conn.close()

    # 代理设置
    def get_proxy(self):
        get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
        res = requests.post(url=get_url).text
        code = res.split(',')[0].split(':')[-1]
        if code == '0':
            # 获取代理
            ip = res.split(',')[1].split(':')[-1].strip('"')
            port = res.split(',')[2].split(':')[-1].strip('"')
            print('获取代理：', ip, port)
            return ip, port
        else:
            # 代理请求错误
            try:
                print('重新释放代理')
                sleep(5)
                sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
                page_test = requests.post(sf_url).text
                sleep(5)
                sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
                url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
                # 释放代理
                requests.post(url=url)
                print('代理释放')
                # 代理获取时长限制
                sleep(6)
                ip, port = self.get_proxy()
                print('代理获取')
                return ip, port
            except Exception as e:
                print(e, self.page)
                sleep(6)
                ip, port = self.get_proxy()
                return ip, port

    # 释放代理
    def close_proxy(self, ip):
        print('释放代理')
        close_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
        requests.post(url=close_url)

    # 网页请求与源码解析
    def get_response(self, url):
        if self.n > 66:
            self.ip, self.port = self.get_proxy()
            self.n = 1
        # 代理服务器
        proxyMeta = "http://%s:%s" % (self.ip, self.port)
        # print(proxyMeta)
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        try:
            sleep(0.3)
            response = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=10, stream=True)
            print('网页获取状态:', response.status_code)
            page_text = response.text
            # print(page_text)
            # 发起请求，获取页面信息
            self.n += 1
            return etree.HTML(page_text)
        except Exception as e:
            print(e)
            self.n += 1
            self.ip, self.port = self.get_proxy()
            html = self.get_response(url)
            return html

    # 获取分类链接
    # def get_url(self, g_url):
    #     html = self.get_response(g_url)
    #     li_list = html.xpath('//dd[@class="last"]/div[1]/ul/li')
    #     # print(li_list)
    #     for li in li_list:
    #         data = li.xpath('./a/@href')
    #         if data:
    #             href = 'https://www.21food.cn' + data[0]
    #             # print(href)

    # 获取页码与企业信息
    def get_pages(self, t_url):
        html = self.get_response(t_url)
        # 获取数据条数与页码数
        data = html.xpath('//div[@class="pro_tit_top"]/em/i[2]/text()')
        data = int(data[0]) if data else ''
        print(t_url)
        if data > 6400:
            li_list = html.xpath('//dd[@class="last"]/div[1]/ul/li')
            # print(li_list)
            for li in li_list:
                data_str = li.xpath('./a/@href')
                if data:
                    href = 'https://www.21food.cn' + data_str[0]
                    print(href)
                    self.get_pages(href)
            return
        # 确定页数
        self.pages, s = divmod(data, 32)
        if s:
            self.pages = self.pages + 1
        print(t_url, self.pages)
        # 获取分页地址
        for pn in range(self.page, self.pages+1):
            print('第{}页'.format(pn))
            if pn > 1:
                detail = t_url.split('.')[-2].split('-')[-1]
                # 拼接分类页码网址
                page_url = 'https://www.21food.cn/company/search.html?catID=%s&pageNo=%s' % (detail, pn)
                print('数据获取中，第%s页' % pn)
                html = self.get_response(page_url)
            # 获取企业信息
            dd_list = html.xpath('//div[@class="qy_list_main auto"]/div[1]/dl/dd')
            for dd in dd_list:
                c_href = dd.xpath('.//span[@class="qylis_tt"]/a/@href')
                c_href = c_href[0] if c_href else ''
                c_name = dd.xpath('.//span[@class="qylis_tt"]/a/text()')
                c_name = c_name[0] if c_name else ''
                c_produce = dd.xpath('.//div[@class="qy_lis_l_jmo_ll"]/ul/li[2]/span/text()')
                c_produce = c_produce[0].strip(' \n') if c_produce else ''
                c_type = dd.xpath('.//div[@class="qy_lis_l_jmo_ll"]/ul/li[1]/span/text()')
                c_type = c_type[0] if c_type else ''
                dic = {
                    'href': c_href,
                    'company': c_name,
                    'produce': c_produce,
                    'company_type': c_type,
                }
                # company_list.append(dic)
                self.get_contact_url(dic)

    # 代理不能进入详情页面
    # 在公司主页中获取联系信息
    def get_contact_url(self, dic):
        c_url = dic['href']
        sleep(0.3)
        c_html = self.get_response(c_url)
        # 获取信息页网址
        li_list = c_html.xpath('//div[@id="leftPlate"]/div[2]/div[2]/ul/li')
        # print(li_list)
        # 判断li_list有值
        for li in li_list:
            data_str = li.xpath('./text()')
            # print(data_str)
            if data_str:
                if '联系人：' in data_str[0]:
                    name = data_str[0].split('：')[1].strip('\r\n\t')
                    dic['name'] = name
                elif '手机：' in data_str[0]:
                    phone = data_str[0].split('：')[1]
                    dic['phone'] = phone
                elif '电话：' in data_str[0]:
                    # telephone = data_str[0].split('：')[1]
                    telephone = data_str[0].split('：')[1]
                    dic['telephone'] = telephone
                elif '地址：' in data_str[0]:
                    address = data_str[0].split('：')[1]
                    dic['address'] = address
        if not li_list:
            li_list = c_html.xpath('//table[6]/tr/td[1]/table[1]/tr[2]/td/table/tr/td/text()')
            detail_str = ''.join(li_list).strip('\r\n ').replace('\r\n', '').replace(' ', '')
            str_list = detail_str.split('\t')
            name = str_list[0]
            dic['name'] = name
            if not name:
                li_list = c_html.xpath('//table[6]/tr/td[1]/table[2]/tr[2]/td/table/tr/td/text()')
                detail_str = ''.join(li_list).strip('\r\n ').replace('\r\n', '').replace(' ', '')
                # print(detail_str)
                str_list = detail_str.split('\t')
                name = str_list[0]
                dic['name'] = name
            for s in str_list:
                if '电话' in s:
                    # telephone = s.split('：')[1]
                    telephone = s.split('：')[1]
                    dic['telephone'] = telephone
                elif '手机' in s:
                    phone = s.split('：')[1]
                    dic['phone'] = phone
                elif '地址' in s:
                    address = s.split('：')[1]
                    dic['address'] = address
        self.save_data(dic)

    # 数据库保存
    def save_data(self, dic):
        # num = 1
        # sql语句
        # 保存数据值和表字段不对称，需要加上对应的字段名
        sql1 = """
            insert into shipinjixie (company, produce, company_type, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s, %s);
                       """
        self.cursor.execute(sql1, (
            str(dic.get('company')) if dic.get('company') else '',
            str(dic.get('produce')) if dic.get('produce') else '',
            str(dic.get('company_type')) if dic.get('company_type') else '',
            str(dic.get('name')) if dic.get('name') else '',
            str(dic.get('phone')) if dic.get('phone') else '',
            str(dic.get('telephone')) if dic.get('telephone') else '',
            str(dic.get('address')) if dic.get('address') else '',
            str(dic.get('href')) if dic.get('href') else ''
        ))
        self.conn.commit()
        print('%s保存成功' % dic.get('company'))


if __name__ == '__main__':
    url = 'https://www.21food.cn/company/companylist_catid-04.html'
    T = ShiPin()
    T(url)

"""超过200页后数据不能使用
脚本自动抓取网页链接并请求的数据质量太差，建议手动输入网址
"""

