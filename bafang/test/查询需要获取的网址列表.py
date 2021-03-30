import requests
from lxml import etree


url = 'https://www.b2b168.com/shipin/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
# 获取网址列表
txt_list = []

# print(dl_list)
li_list = html.xpath('//div[@class="Rbox"]/ul[1]/li')
# print(li_list)
for li in li_list:
    href = li.xpath('./a/@href')[0].split('-')[0] + '-'
    txt_list.append(href)
print(txt_list)

