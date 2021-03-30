import requests
from time import sleep
from lxml import etree
from functools import partial
import re

targetUrl = 'http://m.5999.tv/company/fsgdsp/jianjie.html'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
}

if __name__ == '__main__':
    # ip, port = get_proxy()
    # # 目标请求地址
    # targetUrl = "https://httpbin.org/ip"
    # proxyMeta = "http://%s:%s" % (ip, port)
    # proxies = {
    #     # 根据请求方式（http/https）的不同，可以选择不同的代理
    #     "http": proxyMeta,
    #     "https": proxyMeta
    # }
    # # 证书问题
    # requests.get = partial(requests.get, verify=False, proxies=proxies)
    response = requests.get(url=targetUrl, headers=headers)
    # 获得源码
    page_text = response.text
    # print(page_text)
    print(response.status_code)
    html = etree.HTML(page_text)
    data_str = html.xpath('//div[@class="BItroText"]/ul//text()')
    data = ''.join(data_str).replace('\t', '').replace('\n', '').replace(' ', '')
    # 使用re获取电话或手机数据
    telephone = re.findall(r'[0]\d{2,3}-[2-9]\d{6,7}|[0]\d{2,3}\)[2-9]\d{6,7}|[0]\d{2,3}[2-9]\d{6,7}', data)
    phone = re.findall(r'[1][3,5,7,8][0-9]\d{8}', data)
    print(telephone, phone)
    li_list = html.xpath('//div[@class="BItroText"]/ul/li')

    for li in li_list:
        detail = li.xpath('./text()')[0]
        print(detail)
        if '联 系 人:' in detail:
            name = detail.split('；')[-1]
        elif '公司地址：' in detail:
            address = detail.split('：')[-1]
    print(name, address)

    # print(data)

