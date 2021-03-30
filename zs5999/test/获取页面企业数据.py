import requests
from time import sleep
from lxml import etree
from functools import partial


targetUrl = 'http://www.5999.tv/qiyeku/sudongshipin/'
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
    li_list = html.xpath('//div[@class="companies-left"]/ul/li')
    # print(li_list)
    for li in li_list:
        dic = {}
        href = li.xpath('./div/div/h3/a/@href')
        # print(href)
        if href:
            dic['href'] = href[0]
            company = li.xpath('./div/div/h3/a/text()')
            produce_list = li.xpath('./div/div/p[2]//text()')
            produce_str = ''.join(produce_list).replace('\t', '').replace('\n', '')
            dic['company'] = company[0] if company else ''
            dic['produce'] = produce_str
            print(dic)
            data = dic.get('href').split('/')[-1].split('.')[0]
            next_url = 'http://m.5999.tv/company/%s/jianjie.html' % data
            print(data, next_url)

