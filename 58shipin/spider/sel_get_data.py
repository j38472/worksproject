"""
不使用代理，只使用延时，尝试获取相关数据
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
from pymysql import connect
from time import sleep
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
            db='58shipin',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.page = 411  # 页码
        self.s = 1
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
                sleep(3)
                sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
                page_test = requests.post(sf_url).text
                sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
                url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
                # 释放代理
                requests.post(url=url)
                # 代理获取时长限制
                sleep(6)
                ip, port = self.get_proxy()
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
        # 代理服务器
        proxyMeta = "http://%s:%s" % (self.ip, self.port)
        # print(proxyMeta)
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        try:
            response = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=3, stream=True)
            # self.s += 1
            # if s > 99:
            # print(response.status_code, type(response.status_code))
            # print(response.status_code)
            # 网页获取错误，自动重置代理
            if response.status_code != 200:
                print('第%s次获取网页' % self.s, url)
                self.s += 1
                self.close_proxy(self.ip)
                sleep(10)
                self.ip, self.port = self.get_proxy()
                if self.s > 3:
                    # self.s = 1
                    return
                html = self.get_response(url)

                return html
            page_text = response.text
            return etree.HTML(page_text)
        # url网址格式问题
        except requests.exceptions.InvalidURL as e:
            print('无效网址，无法请求', e)
            return
        except Exception as e:
            print(e)
            self.s += 1
            self.ip, self.port = self.get_proxy()
            html = self.get_response(url)
            return html

    # 获取页码
    def get_pages(self, t_url):
        html = self.get_response(t_url)
        # 确定页码
        data = html.xpath('//div[@class="content-add"]/div/span/text()')
        data = int(data[0]) if data else ''
        self.pages, s = divmod(data, 15)
        if s:
            self.pages = self.pages + 1
        print('总页数 ', self.pages)
        if self.page == 1:
            self.page += 1
            sleep(0.3)
            self.get_data(t_url)
        elif self.page > 1:
            # 拼接网址
            self.page_urls()

    # 获取页面中的信息，分页
    def page_urls(self):
        # print('新一页')
        # 获取新的代理
        # self.close_proxy(self.ip)
        # sleep(3)
        # self.ip, self.port = self.get_proxy()
        if self.page < self.pages + 1:
            # 拼接分类页码网址
            page_url = 'http://www.58food.com/qy-l-0-0-6-0-%d.html' % self.page
            print('数据获取中，第%s页' % self.page)
            self.page += 1
            self.get_data(page_url)

    # 获取页面中所有企业的信息
    def get_data(self, page_url):
        html = self.get_response(page_url)
        # 获取企业信息
        # 数据获取
        div_list = html.xpath('//div[@class="company-page-box"]/div')
        # print(div_list)
        for div in div_list:
            dic = {}
            data_str = div.xpath('./div[1]/div[1]/a[1]/@href')
            # print(data_str)
            data_str1 = div.xpath('./div[1]/div[1]/a[1]/text()')
            # print(data_str)
            if data_str:
                dic['href'] = data_str[0]
                try:
                    dic['company'] = data_str1[0]
                except IndexError as e:
                    print(e)
                    dic['company'] = ''
                detail_str = div.xpath('./div[1]/div[3]//text()')
                for data in detail_str:
                    if '主营：' in data:
                        dic['produce'] = data
                    elif '所在地：' in data:
                        dic['address'] = data
                    elif '经营模式：' in data:
                        dic['company_type'] = data
                self.get_contact_url(dic)
        self.page_urls()

    # 进入公司主页，获取联系信息
    def get_contact_url(self, dic):
        sleep(0.3)
        c_html = self.get_response(dic.get('href'))
        # print(c_html, type(c_html))  # None <class 'NoneType'>
        if c_html is None:
            return
        # print(c_html)
        # 判断网页类型
        li_list = c_html.xpath('//ul[@id="floor"]')
        # print(li_list)
        if li_list:
            # 获取数据
            li_list = c_html.xpath('//div[@class="i93"]/ul/li')
            for li in li_list:
                data_str = ''.join(li.xpath('.//text()'))
                if '联系电话：' in data_str:
                    dic['telephone'] = data_str.split('：')[1]
                elif '联系手机：' in data_str:
                    dic['phone'] = data_str.split('：')[1]
                elif '联  系  人：' in data_str:
                    dic['name'] = data_str.split('：')[1]
            self.save_data(dic)
            # self.get_detail_contact_thr(dic)
        else:
            # 获取信息页网址
            li_list = c_html.xpath('//div[@class="nav"]/ul/li')
            if not li_list:
                li_list = c_html.xpath('//div[@id="menu"]/ul/li')
                # 判断li_list有值
                for li in li_list:
                    data_str = li.xpath('./a/span/text()')
                    # print(data_str)
                    try:
                        if data_str[0] == '联系方式':
                            dic['detail'] = li.xpath('./a/@href')[0]
                    except Exception as e:
                        print(e, dic, self.page)
                        return
                self.get_detail_contact_sel(dic)
            else:
                for li in li_list:
                    data_str = li.xpath('./a/text()')
                    try:
                        if data_str[0] == '联系方式':
                            dic['detail'] = li.xpath('./a/@href')[0]
                            # print(detail)
                    except Exception as e:
                        print(e, dic, self.page)
                        return
                if not dic.get('detail'):
                    data_str_list = c_html.xpath('//div[@class="ctt2"]//text()')
                    # print(data_str_list)
                    data_str = ''.join(data_str_list).strip('\r\n ').replace('\xa0 ', '').replace('\u3000 ', '').replace('\r\n', '')
                    # 利用re表达式获取信息
                    name_list = re.findall('联系人：(.*?)联', data_str)
                    dic['name'] = name_list[0] if name_list[0] else ''
                    telephone_list = re.findall('联系电话：(.*?)联', data_str)
                    dic['telephone'] = telephone_list[0] if telephone_list[0] else ''
                    phone_list = re.findall('联系手机：(\d+)', data_str)
                    dic['phone'] = phone_list[0] if phone_list[0] else ''
                    # print(dic)
                    self.save_data(dic)
                else:
                    self.get_detail_contact_reg(dic)

    # 联系我们页面, 类型一div
    def get_detail_contact_reg(self, dic):
        if not dic.get('detail'):
            print('网址无效', dic.get('href'))
            return
        html = self.get_response(dic.get('detail'))
        div_list = html.xpath('//div[@class="rcleftlist"]//text()')
        if not div_list:
            data_list = html.xpath('//div[@class="contactus"]/div[1]/p//text()')
            data_str = ''.join(data_list).strip('\n').replace('\n', '')
            # 利用re表达式获取信息
            name_list = re.findall('联  系  人：(.*?)联', data_str)
            # print(name_list)
            dic['name'] = name_list[0] if name_list else ''
            telephone_list = re.findall('联系电话：(.*?)传', data_str)
            dic['telephone'] = telephone_list[0] if telephone_list else ''
            phone_list = re.findall('联系手机：(\d+)', data_str)
            dic['phone'] = phone_list[0] if phone_list else ''
            self.save_data(dic)
            return
        data_str = ''.join(div_list).strip('\r\n ').replace('\xa0 ', '').replace('\u3000 ', '').replace('\r\n', '')
        # 利用re表达式获取信息
        name_list = re.findall('联系人：(.*?)联', data_str)
        dic['name'] = name_list[0] if name_list else ''
        telephone_list = re.findall('联系电话：(.*?)联', data_str)
        dic['telephone'] = telephone_list[0] if telephone_list else ''
        phone_list = re.findall('联系手机：(\d+)', data_str)
        dic['phone'] = phone_list[0] if phone_list else ''
        # print(dic)
        # 将数据传递给数据库保存函数
        self.save_data(dic)

    # 类型二
    def get_detail_contact_sel(self, dic):
        if not dic.get('detail'):
            print('网址无效', dic.get('href'))
            return
        html = self.get_response(dic.get('detail'))
        # 查找到需要点击显示的标签
        p_list = html.xpath('//div[@id="glo_contactway_content"]/div/p')
        for p in p_list:
            data_str = p.xpath('./text()')
            if '手机号码：' in data_str[0]:
                dic['phone'] = data_str[0].split('：')[1]
            elif '电话号码：' in data_str[0]:
                dic['telephone'] = data_str[0].split('：')[1]
            elif '联系姓名：' in data_str[0]:
                dic['name'] = data_str[0].split('：')[1]
        self.save_data(dic)

    # 数据库保存
    def save_data(self, dic):
        try:
            # sql语句
            # 保存数据值和表字段不对称，需要加上对应的字段名
            sql1 = """
                insert into dongpinshengxian (company, produce, company_type, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s, %s);
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
        except Exception as e:
            print(e)


if __name__ == '__main__':
    url = 'http://www.58food.com/qy-l-0-6.html'
    T = ShiPin()
    T(url)


