"""
网站的服务器对同一ip请求的频率有限制，会限制请求或响应重复内容

"""
import random
import requests
from lxml import etree
from time import sleep
from pymysql import connect
import re
from pymysql.err import DataError
from fake_useragent import UserAgent


NUM = 0  # 全局变量，保存数据条数

companys_url_list = []  # 企业详情页网址

invalid_list = []  # 无效网址
company_data_list = []  # 企业信息数据
ua = UserAgent()
headers = {
    "user-agent": ua.random
}


# 获取代理
def pro_get():
    url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
    res = requests.post(url=url).text
    # print(res.status_code)
    # print(res.text)
    code = res.split(',')[0].split(':')[-1]
    # print(code)
    if code == '0':
        # 字符串的显示
        ip = res.split(',')[1].split(':')[-1].strip('"')
        # print(type(ip))
        port = res.split(',')[2].split(':')[-1].strip('"')
        print(ip, port)
        return ip, port
    else:
        sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
        page_test = requests.post(sf_url).text
        sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
        print(sf_ip)
        t_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
        requests.post(url=t_url)
        sleep(3)
        ip, port = pro_get()
        return ip, port


# # 释放代理
# def pro_close(ip):
#     c_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
#     requests.post(url=c_url)


# 请求网址
def get_url(url, ip, port):
    # 设置重连次数
    N = 0
    while N < 3:
        try:
            # 代理服务器
            proxyHost = ip  # ip地址
            proxyPort = port  # 端口号
            proxyMeta = "http://%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
            }
            proxies = {
                "http": proxyMeta,
                "https": proxyMeta,
            }
            # allow_redirects = False 不允许重定向，超时设置
            response = requests.get(url=url, headers=headers, timeout=15, allow_redirects=False, proxies=proxies)
            # response = requests.get(url=url, headers=headers, timeout=15, proxies=proxies)
            # print(response.status_code)
            page_text = response.text
            html = etree.HTML(page_text)
            return html
        except Exception as e:
            print(e)
            sleep(3)
            print('等待重新链接：----', url)
            N += 1
            # 重新请求网址
            html = get_url(url, ip, port)
            return html


# 分页
def pages(page_url):
    print(page_url)
    company_html = get_url(page_url, IP, Port)
    # 判断num的值，极限分类的数据条数异常处理
    num = company_html.xpath('//div[@class="main730"]/div/div[1]/span/em/text()')[0]
    num = int(num)
    # 确定页数
    page, nums = divmod(num, 40)
    if nums:
        page += 1
    print('获取分页数--', page)
    # 不允许重定向错误
    # 循环获取网址数据
    for pn in range(1, page + 1):
        sleep(random.randint(1, 3))
        print('第%s页'% pn)
        if pn == 1:
            url_company = page_url
        # 页码的拼接
        else:
            url_company = page_url + 'pn%s/' % pn
        # print(company_url)
        html = get_url(url_company, IP, Port)
        # print(html)
        dl_list = html.xpath('//div[@class="mach_list2"]/form/dl')
        # print(dl_list)
        for dl in dl_list:
            href = dl.xpath('./dt/h4/a/@href')
            # name = dl.xpath('./dt/h4/a/@title')
            if len(href) != 0:
                href = href[0]
                # name = name[0]
                # data = '%s %s'%(name, href)
                companys_url_list.append(href)
    print(len(companys_url_list))


# 企业信息格式化
def company_data(company_url):
    # 休眠3秒
    # sleep(random.randint(1, 3))
    dic = {}
    dic['网址'] = str(company_url)
    # company_list = []
    print('网页：', company_url)
    # 获取企业详情页数据，重定向
    html = get_url(company_url, IP, Port)
    # 禁止重定向，网页内容为空，异常处理
    try:
        li_list = html.xpath('//div[@class="r-content"]//ul/li')
    except Exception as e:
        print('网页不可用', e)
        return
    # 判断li_list中是否有值，借此判断网页是否有效
    if not li_list:
        return company_url
    # 获取主营产品
    produce = html.xpath('//div[@class="l-content"]//li[@class="contro-num"]/text()')
    # print(produce)
    if produce:
        produce = str(produce[0])
    else:
        produce = ''
    dic["主营产品"] = produce
    for li in li_list:
        name, value = li.xpath('.//text()')
        name = str(name)
        value = str(value)
        name = name.strip('：')
        # print(name, value, type(name), type(value))
        if name == '手机号':
            name = '手机'
        elif name in ['座机号', '座机', '电话号']:
            name = '电话'
        dic[name] = value
        # 修改None值
        phone1 = str(dic.get('手机'))
        # print("phone1", phone1, type(phone1))
        if phone1:
            if not re.match('\d+', phone1):
                dic['手机'] = ''
        phone2 = str(dic.get('联系人'))
        if phone2 == 'None':
            dic['联系人'] = ''
        phone4 = str(dic.get('地址'))
        if not phone4:
            dic['地址'] = ''
        phone3 = str(dic.get('电话'))
        # print("phone3", phone3,type(phone3))
        if phone3:
            if not re.match('\d*-?\d+', phone3):
                dic['电话'] = ''
        # print(phone1,phone3)
        # print(re.match('al', 'alex make love').group())
    company_data_list.append(dic)


# 数据库保存
def save_data(data_list):
    # 连接数据库
    conn = connect(
        host='localhost',
        port=3306,
        db='huangye88',
        user='root',
        password='97655',
        charset='utf8'
    )
    # 获取游标
    cur = conn.cursor()
    # sql语句
    sql1 = """
        insert into shanxi_baijiu (lianxiren, phone, telephone, company, address, produce, href) values (%s, %s, %s, %s, %s, %s, %s);
        """
    for dic in data_list:
        try:
            cur.execute(sql1, (
                str(dic.get('联系人')), str(dic.get('手机')),
                str(dic.get('电话')), str(dic.get('公司名称')),
                str(dic.get('地址')), str(dic.get('主营产品')),
                str(dic.get('网址'))))
            conn.commit()
        except DataError as e:
            conn.rollback()
            print(e)
            continue
    cur.close()
    print('保存成功')
    conn.close()


# 主函数
if __name__ == '__main__':
    # 获取动态ip
    IP, Port = pro_get()
    # 切换省级分类网址
    fenlei_url = 'https://b2b.huangye88.com/shanxisheng/baijiu20185/'
    # 获取网址
    pages(fenlei_url)
    for company_url in companys_url_list:
        # 拼接网页
        data_url = company_url + 'company_contact.html'
        res = company_data(data_url)
        if res:
            invalid_list.append(company_url)
    # 拼接详情页网址
    for company_url2 in invalid_list:
        company_url2 = company_url2 + 'contact.html'
        company_data(company_url2)
    save_data(company_data_list)



