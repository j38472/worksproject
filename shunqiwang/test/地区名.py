import requests
from lxml import etree
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}
url = 'http://b2b.11467.com/search/3361.htm'

response = requests.get(url=url, headers=headers)
print(response.status_code)
pages_text = response.text
html = etree.HTML(pages_text)

# 查找数据
a_list = html.xpath('//div[@class="boxcontent"]/dl/a')
for a in a_list:
    href = a.xpath('./@href')[0]
    print(href)
    table = re.findall('com/(.*?)/search/', href)
    print(table)