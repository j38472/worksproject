import requests
from lxml import etree
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}
url = 'http://b2b.11467.com/search/3361.htm'

produce_type_list = [
    '9100.htm',
    '9118.htm',
    '9126.htm',
    '9134.htm',
    '9135.htm',
    '9152.htm',
    '9159.htm',
    '9160.htm',
    '9161.htm',
    '9166.htm',
    '9175.htm',
    '9181.htm',
    '9193.htm',
    '9194.htm',
    '9207.htm',
    '9208.htm',
    '9209.htm',
    '9210.htm',
    '9222.htm',
    '9229.htm',
    '9234.htm',
    '9244.htm',
    '9256.htm',
    '9267.htm',
    '9274.htm',
    '9281.htm',
    '9282.htm',
    '9283.htm',
    '9284.htm',
    '9285.htm',
    '9286.htm',
    '9305.htm',
    '9306.htm',
    '9318.htm',
    '9319.htm',
    '9320.htm',
    '9321.htm',
    '11981.htm',
]

# 拼接分类网址

dic = {}
url = 'http://b2b.11467.com/search/3361.htm'
response = requests.get(url=url, headers=headers)
print(response.status_code)
pages_text = response.text
html = etree.HTML(pages_text)
# 查找分类网址
dd_list = html.xpath('//div[@id="il"]/div[1]/div[1]/dl/dd')
print(dd_list)
for dd in dd_list:
    url = 'http://b2b.11467.com/search/' + dd.xpath('./a/@href')[0]
    response = requests.get(url=url, headers=headers)
    pages_text = response.text
    detail = re.findall('等在内的(.*?)家', pages_text)[0]
    page = re.findall('共分为(.*?)页', pages_text)[0]
    if int(detail) < 2000:
        print(url)
        # 获取下一级分类网址
        # 查找分类网址

