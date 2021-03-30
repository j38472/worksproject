import re

import requests
from lxml import etree
from fake_useragent import UserAgent
from pymysql import connect
from time import sleep
from random import randint


class DataShiPin:

    def __init__(self):
        print('开启数据库')
        self.conn = connect(
         host='127.0.0.1',
         port=3306,
         user='root',
         password='97655',
         db='bafang',
         charset='utf8'
        )
        self.cursor = self.conn.cursor()
        # 起始页码
        self.page = 1
        # 总页数
        self.pages = 1
        # 代理使用次数
        self.n = 1
        # ua伪装
        self.headers = {
         'user-agent': UserAgent().random
        }
        # 代理
        # self.ip, self.port = self.get_proxy()

    def __del__(self):
        print('关闭数据库')
        self.cursor.close()
        self.conn.close()

    def __call__(self, *args, **kwargs):
        self.get_data(*args, **kwargs)

    # 获取代理
    def get_proxy(self):
        get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
        # 发起获取请求
        res = requests.post(url=get_url, headers=self.headers).text
        code = res.split(',')[0].split(':')[-1]
        if code == '0':
            # 获取代理
            ip = res.split(',')[1].split(':')[-1].strip('"')
            port = res.split(',')[2].split(':')[-1].strip('"')
            print('获取到的代理值：', ip, port)
            return ip, port
        else:
            # 查询代理
            try:
                print('查询代理')
                sleep(5)
                cx_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
                page_test = requests.post(cx_url).text
                sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
                sleep(6)
                print('释放代理')
                sf_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
                requests.post(url=sf_url, headers=self.headers)
                # 代理获取时长限制
                sleep(6)
                print('再次获取代理')
                ip, port = self.get_proxy()
                return ip, port
            except Exception as e:
                print(e)
                sleep(5)
                ip, port = self.get_proxy()
                return ip, port

    # 释放代理
    def close_proxy(self, ip):
        print('释放代理')
        close_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
        requests.post(url=close_url, headers=self.headers)

    # 发起网络请求
    def get_response(self, r_url):
        # print(r_url)
        # if self.n > 33:
        #     # 获取新代理
        #     self.close_proxy(self.ip)
        #     sleep(6)
        #     self.n = 1
        #     self.ip, self.port = self.get_proxy()
        # # 设置代理
        # # 判断代理是否有值
        # if self.ip is None:
        #     self.ip, self.port = self.get_proxy()
        # proxyMeta = "http://%s:%s" % (self.ip, self.port)
        # # print(proxyMeta)
        # proxies = {
        #     "http": proxyMeta,
        #     "https": proxyMeta
        # }
        # 判断网页获取次数
        try:
            # 手动延时
            sleep(randint(1, 3))
            # requests.get = partial(requests.get, verify=False, proxies=proxies)
            response = requests.get(url=r_url, headers=self.headers, timeout=10, stream=True)  # stream参数控制http请求错误
            # response = requests.get(url=r_url, headers=self.headers, proxies=proxies, timeout=10, stream=True)  # stream参数控制http请求错误
            print(response.status_code)
            page_text = response.text
            # 网页获取错误，自动重置代理
            self.n += 1
            if response.status_code != 200:
                print('网页获取失败')
                return
            html = etree.HTML(page_text)
            return html
        # url网址格式问题
        except requests.exceptions.InvalidURL as e:
            print('无效网址，无法请求', e)
            return
        except requests.exceptions.ReadTimeout as e:
            print('请求超时', e)

            # sleep(randint(5, 10))
            # self.ip, self.port = self.get_proxy()
            # html = self.get_response(r_url)
            # return html
        # 网络请求错误
        except Exception as e:
            print('请求出错', e)
            return

    # 保存数据
    def save_data(self, dic):
        try:
            # sql语句
            # 判断联系信息是否有效
            phone = dic.get('phone') if dic.get('phone') else ''
            telephone = dic.get('telephone') if dic.get('telephone') else ''
            data_str = phone + telephone
            if not data_str:
                print('无效数据')
                return
            # 获取表名称
            # print(dic)
            # print(url)
            table = url.split('/')[-2]
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
            print('%s成功保存到%s中' % (dic.get('company'),table))
        except Exception as e:
            print(e)
            self.conn.rollback()

    # 获取联系信息
    def get_contact(self, dic):
        c_url = dic['href']
        c_html = self.get_response(c_url)
        # 判断获取的网页是否为None
        if c_html is None:
            print('联系信息界面为空')
            return
        # 获取信息页网址
        # 判断网页的类型
        p_list = c_html.xpath('//div[@class="footer"]/ul/li[2]/span/p')
        data_str = c_html.xpath('//dl[@class="codl"]/dd/text()')
        if not data_str:
            detail = c_html.xpath('//div[@class="footer"]/ul/li[1]/h4[2]/text()')
            dic['produce'] = detail[0] if detail else ''
            for p in p_list:
                try:
                    detail = p.xpath('./text()')
                    if '地址' in detail[0]:
                        dic['address'] = detail[0].split('：')[-1]
                    elif '手机' in detail[0]:
                        dic['phone'] = detail[0].split('：')[-1]
                    elif '电话' in detail[0]:
                        dic['telephone'] = detail[0].split('：')[-1]
                except:
                    pass
            self.save_data(dic)
            return
        for da in data_str:
            da = da.replace(' ', '')
            telephone = re.findall(r'[0]\d{2,3}-[2-9]\d{6,7}|[0]\d{2,3}\)[2-9]\d{6,7}|[0]\d{2,3}[2-9]\d{6,7}', da)
            phone = re.findall(r'[1][3,5,7,8][0-9]\d{8}', da)
            if '（' in da:
                dic['name'] = da
            elif telephone:
                dic['telephone'] = telephone[0]
            elif phone:
                dic['phone'] = phone[0]
            elif len(da) > 7:
                if not da[0].isdigit():
                    dic['address'] = da
        self.save_data(dic)

    # 获取网页
    def get_data(self, data_url):
        html = self.get_response(data_url)
        # 判断获取的网页是否为None
        if html is None:
            print('网址{}为空'.format(data_url))
            return
        # 确定页码
        page = html.xpath('//div[@class="pages"]/text()')
        if page:
            page_str = ''.join(page).replace('\r\n', '').replace(' ', '')
            pages_l = re.findall(r'共(.*?)页', page_str)
            if not pages_l:
                print('数据为空')
                return
            self.pages = int(pages_l[0])
        print('第%s  %s个数据，总页数 %s' % (pn, p, self.pages))
        # 循环所有页码中页面企业数据
        for pages in range(self.page, self.pages + 1):
            # print(pages)
            if pages > 1:
                # 拼接分类页码网址
                page_url = data_url + 'l-%d.html' % pages
                # 获取下一页内容
                print('第%s  %s个数据' % (pn, p))
                print('数据获取中，第%s页, 网址：%s' % (pages, page_url))
                html = self.get_response(page_url)
            if html is None:
                print('网页获取失败，页码')
                continue
            li_list = html.xpath('//div[@class="cations"]/ul/li')
            # print(li_list)
            if li_list:
                for li in li_list:
                    dic = {}
                    href = li.xpath('./div[2]/a/@href')
                    # dic['href'] = 'https:' + href[0] if href else ''
                    if href:
                        href = href[0]
                        if 'http' not in href:
                            href = 'https:' + href
                        dic['href'] = href
                    company = li.xpath('./div[2]/a/@title')
                    dic['company'] = company[0] if company else ''
                    detail = li.xpath('./div[2]/p[2]/span[2]/text()')
                    if detail:
                        if '关键' in detail:
                            dic['produce'] = detail[0].split('：')[-1]
                        elif '地址' in detail:
                            dic['address'] = detail[0].split(':')[-1]
                    name = li.xpath('./div[2]/p[2]/span[1]/text()')
                    if name:
                        name = re.findall(r'.*?\)', name[0])
                        dic['name'] = name[0] if name else ''
                    self.get_contact(dic)


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        # for line in f.readlines():
        #     print(line.replace('\n',''))
        line_list = f.readlines()
    get_data = DataShiPin()
    city_list = ['/beijing-', '/tianjin-', '/shanghai-', '/chongqing-', '/aomen-', '/taiwan-', '/hainan-',
                 '/jiangsu-', '/hebei-', '/shanxisheng-', '/neimenggu-', '/liaoning-', '/jilin-', '/heilongjiang-',
                 '/zhejiang-', '/anhui-', '/fujian-', '/jiangxi-', '/shandong-', '/henan-', '/hubei-', '/hunan-',
                 '/guangdong-', '/guangxi-', '/sichuan-', '/guizhou-', '/yunnan-', '/xizang-', '/shanxi-']
    # 拼接想要获取的网页链接
    for pn, data in enumerate(line_list):
        # 断点续传
        for p, city in enumerate(city_list):
            num = city + data.replace('\n', '').strip('/')
            # if pn > 17:
            url = 'https://www.b2b168.com%s' % num
            # 'https://www.b2b168.com/beijing-shipin/tiaoweipin/huoguoliao/'
            print(url)
            get_data(url)


"""


"""