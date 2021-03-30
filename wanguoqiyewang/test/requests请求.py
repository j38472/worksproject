import requests
from lxml import etree
from fake_useragent import UserAgent


# 分类网址
classify_url_list = []

url = 'https://qiye.trustexporter.com/food/'
ua = UserAgent().random
headers = {
    "user-agent": ua
}
response = requests.get(url=url, headers=headers)
# print(response.status_code)
html = etree.HTML(response.text)
div_list = html.xpath('//div[@class="left_box"]/div/div/div')
# print(div_list)
for div in div_list:
    name_str = div.xpath('./strong/a/text()')
    name = name_str[0] if name_str else ''
    href_str = div.xpath('./strong/a/@href')
    href = href_str[0] if href_str else ''
    dic = {
        '分类名': name,
        '网址': href
    }
    classify_url_list.append(dic)





