import requests
from lxml import etree
import re

url = 'https://www.b2b168.com/shipin/tiaoweipin/zhimajianghuashengjiang/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
# 企业信息获取
li_list = html.xpath('//div[@class="cations"]/ul/li')
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
        produce = li.xpath('./div[2]/p[2]/span[2]/text()')
        dic['produce'] = produce[0].split('：')[-1] if produce else ''
        name = li.xpath('./div[2]/p[2]/span[1]/text()')
        if name:
            name = re.findall(r'.*?\)', name[0])
            dic['name'] = name[0] if name else ''
        print(dic)
