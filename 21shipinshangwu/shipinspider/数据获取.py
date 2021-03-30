"""
使用代理进行网站爬取
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
from pymysql import connect
from time import sleep
from random import randint


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
            try:
                print('重新释放代理')
                sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
                page_test = requests.post(sf_url).text
                sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
                url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
                requests.post(url=url)
                # 代理获取时长限制
                sleep(6)
                ip, port = self.get_proxy()
                return ip, port
            except Exception as e:
                print(e, self.page)
                sleep(3)
                ip, port = self.get_proxy()
                return ip, port

    # 释放代理
    def close_proxy(self, ip):
        print('释放代理')
        close_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
        requests.post(url=close_url)

    # 网页请求与源码解析
    def get_response(self, url):
        # 代理服务器
        proxyMeta = "http://%s:%s" % (self.ip, self.port)
        # print(proxyMeta)
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        try:
            response = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=10, stream=True)
            print(response.status_code)
            page_text = response.text
            # print(page_text)
            # 发起请求，获取页面信息
            # print(response.status_code)
            # self.n += 1
            return etree.HTML(page_text)
        except Exception as e:
            print(e)
            self.ip, self.port = self.get_proxy()
            html = self.get_response(url)
            return html

    # 获取页码
    def get_pages(self, t_url):
        html = self.get_response(t_url)
        # 确定页码
        data = html.xpath('//div[@class="pro_tit_top"]/em/i[2]/text()')
        data = int(data[0]) if data else ''
        self.pages, s = divmod(data, 32)
        if s:
            self.pages = self.pages + 1
        print('总页数 ', self.pages)
        if self.page == 1:
            self.page += 1
            self.get_data(t_url)
        elif self.page > 1:
            # 拼接网址
            self.page_urls()

    # 获取页面中的信息，分页
    def page_urls(self):
        # 获取新的代理
        self.close_proxy(self.ip)
        sleep(3)
        self.ip, self.port = self.get_proxy()
        if self.page < self.pages + 1:
            # 拼接分类页码网址
            page_url = 'https://www.21food.cn/company/search.html?catID=04001020&pageNo=%d' % self.page
            print('数据获取中，第%s页' % self.page)
            self.page += 1
            self.get_data(page_url)

    # 获取页面中32个企业的信息
    def get_data(self, page_url):
        html = self.get_response(page_url)
        # 获取企业信息
        dd_list = html.xpath('//div[@class="qy_list_main auto"]/div[1]/dl/dd')
        for dd in dd_list:
            c_href = dd.xpath('.//span[@class="qylis_tt"]/a/@href')[0]
            c_name = dd.xpath('.//span[@class="qylis_tt"]/a/text()')[0]
            c_produce = dd.xpath('.//div[@class="qy_lis_l_jmo_ll"]/ul/li[2]/span/text()')[0].strip(' \n')
            try:
                c_type = dd.xpath('.//div[@class="qy_lis_l_jmo_ll"]/ul/li[1]/span/text()')[0]
            except Exception as e:
                print(e)
                c_type = ''
            dic = {
                '网址': c_href,
                '企业名称': c_name,
                '主营产品': c_produce,
                '经营类型': c_type,
            }
            # company_list.append(dic)
            self.get_contact_url(dic)
        self.page_urls()

    # 进入公司主页，获取联系信息
    def get_contact_url(self, dic):
        c_url = dic['网址']
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
                    dic['联系人'] = name
                elif '手机：' in data_str[0]:
                    phone = data_str[0].split('：')[1]
                    dic['手机'] = phone
                elif '电话：' in data_str[0]:
                    # telephone = data_str[0].split('：')[1]
                    telephone = data_str[0].split('：')[1].replace('+86', '')

                    dic['电话'] = telephone
                elif '地址：' in data_str[0]:
                    address = data_str[0].split('：')[1]
                    dic['地址'] = address
        if not li_list:
            li_list = c_html.xpath('//table[6]/tr/td[1]/table[1]/tr[2]/td/table/tr/td/text()')
            detail_str = ''.join(li_list).strip('\r\n ').replace('\r\n', '').replace(' ', '')
            str_list = detail_str.split('\t')
            name = str_list[0]
            dic['联系人'] = name
            if not name:
                li_list = c_html.xpath('//table[6]/tr/td[1]/table[2]/tr[2]/td/table/tr/td/text()')
                detail_str = ''.join(li_list).strip('\r\n ').replace('\r\n', '').replace(' ', '')
                # print(detail_str)
                str_list = detail_str.split('\t')
                name = str_list[0]
                dic['联系人'] = name
            for s in str_list:
                if '电话' in s:
                    # telephone = s.split('：')[1]
                    telephone = s.split('：')[1].replace('+86', '')

                    dic['电话'] = telephone
                elif '手机' in s:
                    phone = s.split('：')[1]
                    dic['手机'] = phone
                elif '地址' in s:
                    address = s.split('：')[1]
                    dic['地址'] = address
        self.save_data(dic)

    # 数据库保存
    def save_data(self, dic):

        # sql语句
        # 保存数据值和表字段不对称，需要加上对应的字段名
        sql1 = """
            insert into shipinjixie (company, produce, company_type, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s, %s);
                       """
        self.cursor.execute(sql1, (
            str(dic.get('企业名称')) if dic.get('企业名称') else '',
            str(dic.get('主营产品')) if dic.get('主营产品') else '',
            str(dic.get('经营类型')) if dic.get('经营类型') else '',
            str(dic.get('联系人')) if dic.get('联系人') else '',
            str(dic.get('手机')) if dic.get('手机') else '',
            str(dic.get('电话')) if dic.get('电话') else '',
            str(dic.get('地址')) if dic.get('地址') else '',
            str(dic.get('网址')) if dic.get('网址') else ''
        ))
        self.conn.commit()
        print('%s保存成功' % dic.get('企业名称'))


if __name__ == '__main__':
    url = 'https://www.21food.cn/company/companylist_catid-04001020.html'
    T = ShiPin()
    T(url)


