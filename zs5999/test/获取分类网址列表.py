import requests
from time import sleep
from lxml import etree
from functools import partial


targetUrl = 'http://m.5999.tv/company_list/'
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
    a_list = html.xpath('//div[@class="classify-food-detial"]/a')
    print(a_list)
    for a in a_list:
        href = a.xpath('./@href')[0]
        print(href)