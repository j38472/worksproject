import requests
from lxml import etree
import re

url = 'https://www.b2b168.com/c168-4800553.html'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
response = requests.get(url, headers=headers)
c_html = etree.HTML(response.text)
# 企业信息获取
dic = {}
# 判断网页类型
p_list = c_html.xpath('//div[@class="footer"]/ul/li[2]/span/p')
data_str = c_html.xpath('//dl[@class="codl"]/dd/text()')
if not data_str:
    for p in p_list:
        try:
            detail = p.xpath('./text()')
            if '地址' in detail[0]:
                dic['address'] = detail[0]
            elif '手机' in detail[0]:
                dic['phone'] = detail[0]
            elif '电话' in detail[0]:
                dic['telephone'] = detail[0]
        except:
            pass
    print(dic)
data_str =c_html.xpath('//dl[@class="codl"]/dd/text()')
for data in data_str:
    telephone = re.findall(r'[0]\d{2,3}-[2-9]\d{6,7}|[0]\d{2,3}[2-9]\d{6,7}|[0]\d{2,3}\)[2-9]\d{6,7}', data)
    phone = re.findall(r'[1][3,5,7,8][0-9]\d{8}', data)
    print(data)
    if '（' in data:
        dic['name'] = data
    elif telephone:
        dic['telephone'] = telephone[0]
    elif phone:
        dic['phone'] = phone[0]
    elif len(data) > 7:
        if not data[0].isdigit():
            dic['address'] = data
print(dic)
# detail = ''.join(data_str).replace('\r\n', '')
# print(data_str)
