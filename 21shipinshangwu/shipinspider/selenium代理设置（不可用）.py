"""
使用代理进行网站爬取
"""
import requests
from selenium import webdriver
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
            db='21shipinwang',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.page = 6
        self.pages = 0
        self.ua = UserAgent().random
        self.headers = {
            'user-agent': self.ua
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
            print('释放代理')
            sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
            page_test = requests.post(sf_url).text
            sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
            url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
            requests.post(url=url)
            # 代理获取时长限制
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
        # 浏览器设置
        options = webdriver.ChromeOptions()
        # 实现无可视化界面操作
        options.add_argument('--headless')
        # 谷歌文档，about:black空白页问题   无效
        options.add_argument('--disable-gpu')
        options.add_argument('--user-agent={}'.format(self.ua))
        options.add_argument('--window-size=1240,1080')
        # 设置代理,options.to_capabilities()方式
        PROXY = '{}:{}'.format(self.ip, self.port)
        desired_capabilities = options.to_capabilities()
        desired_capabilities['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }
        # 隐藏会话暴露的真实ip
        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        options.add_experimental_option("prefs", preferences)
        # 开启实验性功能参数，去除提示，防止检测
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 无效
        options.add_experimental_option('useAutomationExtension', False)
        # 就是这一行告诉chrome去掉了webdriver痕迹
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        # 无图模式
        # prefs = {"profile.managed_default_content_settings.images": 2}              # 不显示图片提高代码速度
        # options.add_experimental_option("prefs", prefs)
        # 最高权限
        # options.add_argument('--no-sandbox')

        """不添加desired_capabilities参数也可以使用代理"""

        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
        # driver.get('https://httpbin.org/ip')
        driver.get('http://cnftjy.21food.cn/company/contact8858.html')
        # sleep(60)
        driver.quit()

    # 获取页码
    def get_pages(self, t_url):
        html = self.get_response(t_url)
        # 确定页码
        data = html.xpath('//div[@class="pro_tit_top"]/em/i[2]/text()')
        data = int(data[0]) if data else ''
        self.pages, s = divmod(data, 32)
        if s:
            self.pages = self.pages + 1
        print(self.pages)
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
        self.ip, self.port = self.get_proxy()
        if self.page < self.pages + 1:
            # 拼接分类页码网址
            page_url = 'https://www.21food.cn/company/search.html?catID=03007&pageNo=%d' % self.page
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
            c_type = dd.xpath('.//div[@class="qy_lis_l_jmo_ll"]/ul/li[1]/span/text()')[0]
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
        sleep(randint(1, 3))
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
            insert into jiulei (company, produce, company_type, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s, %s);
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
        # 数据保存成功，获取下一页网页信息
        # self.page_urls()


if __name__ == '__main__':
    url = 'https://www.21food.cn/company/companylist_catid-03009.html'
    T = ShiPin()
    T(url)


