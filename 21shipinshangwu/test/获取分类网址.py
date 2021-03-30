import requests
from lxml import etree
from fake_useragent import UserAgent
import re


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

url = 'https://www.21food.cn/company/companylist_catid-04.html'
ua = UserAgent().random
headers = {
    "user-agent": ua
}
dic = {}

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
# print(page_text)
html = etree.HTML(page_text)
#
li_list = html.xpath('//dd[@class="last"]/div[1]/ul/li')
print(li_list)
for li in li_list:
    data = li.xpath('./a/@href')
    if data:
        href = 'https://www.21food.cn' + data[0]
        print(href)

        # 获取数据条数与页码数
        data = html.xpath('//div[@class="pro_tit_top"]/em/i[2]/text()')
        data = int(data[0]) if data else ''




