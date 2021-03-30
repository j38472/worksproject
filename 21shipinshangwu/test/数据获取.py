import requests
from lxml import etree
from fake_useragent import UserAgent
import re

url = 'http://pulanchao23.21food.cn'
ua = UserAgent().random
headers = {
    "user-agent": ua
}
dic = {}


# 代理设置
def get_proxy():
    get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
    res = requests.post(url=get_url).text
    code = res.split(',')[0].split(':')[-1]
    if code == '0':
        # 获取代理
        ip = res.split(',')[1].split(':')[-1].strip('"')
        port = res.split(',')[2].split(':')[-1].strip('"')
        print('代理ip值', ip, port)
        return ip, port
    else:
        # 释放代理
        print('释放代理')
        sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
        page_test = requests.post(sf_url).text
        sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
        url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
        requests.post(url=url)
        # 代理获取时长限制
        ip, port = get_proxy()
        return ip, port


# 释放代理
def close_proxy(ip):
    close_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
    requests.post(url=close_url)


# 网页请求与源码解析
def get_response(url):
    ip, port = get_proxy()
    # 代理服务器
    proxyMeta = "http://%s:%s" % (ip, port)
    # print(proxyMeta)
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    response = requests.get(url=url, headers=headers, proxies=proxies)
    print(response.status_code)
    page_text = response.text
    html = etree.HTML(page_text)
    li_list = html.xpath('//div[@id="leftPlate"]/div[2]/div[2]/ul/li')
    # print(li_list)
    for li in li_list:
        data_str = li.xpath('./text()')
        # print(data_str)
        if '备案' in data_str[0]:
            li_list = html.xpath('//div[@id="leftPlate"]/div[1]/div[2]/ul/li')
            break
    for li in li_list:
        data_str = li.xpath('.//text()')
        # print(data_str)
        if '联系人：' in data_str[0]:
            name = data_str[0].split('：')[1].strip('\r\n\t')
            dic['联系人'] = name
        elif '手机：' in data_str[0]:
            phone = data_str[0].split('：')[1]
            dic['手机'] = phone
        elif '电话：' in data_str[0]:
            telephone = data_str[0].split('：')[1]
            dic['电话'] = telephone
        elif '地址：' in data_str[0]:
            address = data_str[0].split('：')[1]
            dic['地址'] = address

    """['\r\n\t\t\t\t\t 实名备案:\r\n\t\t\t\t\t \r\n\t\t\t\t\t\t ', '\r\n\t\t\t\t\t\r\n\t\t\t\t ']
['经营模式：贸易型']
['荣誉资质:2项']
['公司网站：\r\n\t\t\t', '\t\t\r\n\t\t']"""
    if not li_list:
        print(2)
        li_list = html.xpath('//table[6]/tr/td[1]/table[1]/tr[2]/td/table/tr/td/text()')
        # '/table[6]/tbody/tr/td[1]/table[2]/tbody/tr[2]/td/table/tbody/tr/td'
        detail_str = ''.join(li_list).strip('\r\n ').replace('\r\n', '').replace(' ', '')
        # print(detail_str)
        str_list = detail_str.split('\t')
        name = str_list[0]
        print(name)
        dic['联系人'] = name
        if not name:
            li_list = html.xpath('//table[6]/tr/td[1]/table[2]/tr[2]/td/table/tr/td/text()')
            detail_str = ''.join(li_list).strip('\r\n ').replace('\r\n', '').replace(' ', '')
            print(detail_str)
            str_list = detail_str.split('\t')
            name = str_list[0]
            dic['联系人'] = name
        for s in str_list:
            if '电话' in s:
                telephone = s.split('：')[1]
                dic['电话'] = telephone
            elif '手机' in s:
                phone = s.split('：')[1]
                dic['手机'] = phone
            elif '地址' in s:
                address = s.split('：')[1]
                dic['地址'] = address
        print(str_list)
        # print(name, phone)
        # 曹昌平先生 电话：028-84738516，13688318958
    print(dic)
"""
['\r\n\t\t\r\n\t\t', '\r\n\t\t\r\n\t\t\r\n        ', '\r\n        \r\n\t\t', '\r\n\t\t\r\n\t\t']
['联系人：卢世娜 女士\r\n\t\t']
['电话：']
['手机：19953614999']
['地址：山东 潍坊 景芝镇景盛工业园']
['\r\n\t\t', '\r\n\t']
[' \xa0 ']
"""

    # return etree.HTML(page_text)


if __name__ == '__main__':
    get_response(url)

