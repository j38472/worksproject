
import requests
from lxml import etree
from time import sleep
from pymysql import connect
import re

NUM = 0  # 全局变量，保存数据条数

url2_list = []  # 二级
url3_list = []  # 三级
url4_list = []  # 四级
companys_url_list = []  # 企业详情页网址
small_list = []  # 数据少于40的分类网址
small_company_list = []  # 数据少于40的企业网址
invalid_list = []  # 无效网址
company_data_list = []  # 企业信息数据
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}


# 请求网址
def get_url(url):
    try:
        page_text = requests.get(url=url, headers=headers, timeout=15, allow_redirects=False).text
        html = etree.HTML(page_text)
        return True, html
    except requests.exceptions.ConnectionError as e:
        print('请求超时：', url)
        sleep(3)
        print('等待重新链接：----')
        return False, url





# 获取分类网址, 省内分类网址获取
def get_url2(url1):
    sleep(0.1)
    # 声明全局变量
    global NUM
    print('爬取：%s' % url1)
    res2, html2 = get_url(url1)
    num = html2.xpath('//div[@class="main730"]//span/em/text()')[0]
    NUM = int(num)
    # print(NUM)
    li2_list = html2.xpath('//div[@class="main730"]/div[@class="box"]/ul/li')
    # 判断是否存在分类
    if li2_list:
        for li2 in li2_list:
            href2 = li2.xpath('./a/@href')[0]
            url2_list.append(href2)  # 山东生鲜水果公司
    else:
        url3_list.append(url1)


# 获取分类网址, 极限分类网址
def get_url3(url2):
    sleep(0.1)
    print('爬取: %s' % url2)
    res3, html3 = get_url(url2)
    li3_list = html3.xpath('//div[@class="main730"]/div[@class="box"]/ul/li')
    # 判断是否存在分类
    if li3_list:
        for li3 in li3_list:
            href3 = li3.xpath('./a/@href')[0]
            url4_list.append(href3)  # 山东生鲜水果公司
    else:
        url3_list.append(url2)


# 分页
def pages(page_url):
        res_page, company_html = get_url(page_url)

        num = company_html.xpath('//div[@class="main730"]/div/div[1]/span/em/text()')[0]
        num = int(num)
        # 判断num的值，极限分类的数据条数异常处理
        # 如果num小于40，数据会重复，数据条数大于2000，数据异常，返回网址异常
        # num为0或NUM，数据分类异常错误，返回错误
        if num == 0:
            return False
        elif num < 40:
            return page_url
        elif num == NUM:
            return False

        # 确定页数
        page, nums = divmod(num, 40)
        if nums:
            page += 1
        if page > 50:
            page = 50
        print('获取分页数--', page)

        for pn in range(1, page + 1):
            sleep(0.1)
            # print('第%s页'%pn)
            company_utl = page_url + 'pn%s' % pn
            res_page, html = get_url(company_utl)
            dl_list = html.xpath('//div[@class="mach_list2"]/form/dl')
            for dl in dl_list:
                href = dl.xpath('./dt/h4/a/@href')
                # name = dl.xpath('./dt/h4/a/@title')
                if len(href) != 0:
                    href = href[0]
                    # name = name[0]
                    # data = '%s %s'%(name, href)
                    companys_url_list.append(href)
        # print(len(companys_url_list))


# 数据条数小于40的网址
def page(small_url):
    res_spage, company_html = get_url(small_url)
    num = company_html.xpath('//div[@class="main730"]/div/div[1]/span/em/text()')[0]
    num = int(num)
    # 循环num次
    dl_list = company_html.xpath('//div[@class="mach_list2"]/form/dl')
    for p in range(num):
        # print("第%s个", p)
        dl = dl_list[p]
        href = dl.xpath('./dt/h4/a/@href')
        # name = dl.xpath('./dt/h4/a/@title')
        if len(href) != 0:
            href = href[0]
            # name = name[0]
            # data = '%s %s'%(name, href)
            companys_url_list.append(href)


# 企业信息格式化
def company_data(company_url):
    dic = {}
    dic['网址'] = str(company_url)
    # company_list = []
    print('网页：', company_url)
    # page_text = requests.get(url=company_url, headers=headers).text
    # html = etree.HTML(page_text)
    res, msg = get_url(company_url)
    if not res:
        return False
    # 获取主营产品
    produce = msg.xpath('//div[@class="l-content"]//li[@class="contro-num"]/text()')
    # print(produce)
    if produce:
        produce = str(produce[0])
    else:
        produce = ''
    dic["主营产品"] = produce
    li_list = msg.xpath('//div[@class="r-content"]//ul/li')

    # print(li_list)
    # 判断li_list中是否有值，借此判断网页是否有效
    if not li_list:
        return company_url
    for li in li_list:
        name, value = li.xpath('.//text()')
        # print(result)
        name = str(name)
        value = str(value)
        name = name.strip('：')
        # print(name, value, type(name), type(value))
        if name == '手机号':
            name = '手机'
        if name in ['座机号', '座机', '电话号']:
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
        insert into guangdong_mimian (lianxiren, phone, telephone, company, produce, address, href) values (%s, %s, %s, %s, %s, %s, %s);
        """
    for dic in data_list:
        cur.execute(sql1, (
            str(dic.get('联系人')), str(dic.get('手机')),
            str(dic.get('电话')), str(dic.get('公司名称')),
            str(dic.get('主营产品')), str(dic.get('地址')),
            str(dic.get('网址'))))

        conn.commit()
    cur.close()
    conn.close()


#主函数
if __name__ == '__main__':
    # 切换省级分类网址
    fenlei_url = 'https://b2b.huangye88.com/guangdong/mimian13476/'
    get_url2(fenlei_url)
    for url2 in url2_list:
        get_url3(url2)
    for url3 in url3_list:
        result = pages(url3)
        if result:
            small_list.append(result)
            continue
        else:
            continue
    # print(small_list)
    for small_url in small_list:
        page(small_url)
    for company_url in companys_url_list:
        # 拼接网页
        data_url = company_url + 'company_contact.html'
        res = company_data(data_url)
        if res == None:
            pass
        elif res:
            invalid_list.append(company_url)
        else:
            company_data(res)
    # 拼接详情页网址
    # https://b2b.huangye88.com/gongsi/company1305543/contact.html
    for company_url2 in invalid_list:
        company_url2 = company_url2 + 'contact.html'
        res = company_data(company_url2)
    save_data(company_data_list)



