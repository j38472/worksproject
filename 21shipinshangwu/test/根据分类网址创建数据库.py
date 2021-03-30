import requests
from lxml import etree
from fake_useragent import UserAgent
import pymysql


urls_list = []
url = 'https://www.21food.cn/company/companylist_catid-03.html'
print(UserAgent().random)
headers = {
    'user-agent': UserAgent().random
}

response = requests.get(url=url, headers=headers)
print(response.status_code)
html = etree.HTML(response.text)

li_list = html.xpath('//div[@class="ec_tit_nv ec_tit_nvg"]/ul/li')

for li in li_list:
    href = 'https://www.21food.cn' + li.xpath('./a/@href')[0]  # /company/companylist_catid-03007.html
    db_name = li.xpath('./a/text()')[0]
    dic ={
        '网址': href,
        '类型': db_name
    }
    urls_list.append(dic)

