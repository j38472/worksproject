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
url = 'https://www.11467.com/beijing/co/748622.htm'
response = requests.get(url=url, headers=headers)
print(response.status_code)
pages_text = response.text
html = etree.HTML(pages_text)
detail_str = html.xpath('//div[@id="contact"]/div/dl//text()')
detail = ''.join(detail_str).strip().replace(' ', '')
print(detail)
telephone = re.findall('[0]\d{2,3}-[2-9]\d{6,7}|[0]\d{2,3} [2-9]\d{6,7}|[0]\d{2,3}[2-9]\d{6,7}', detail)
telephone = telephone[0] if telephone else ''
# if telephone:
#     telephone = telephone[0]
phone = re.findall('[1][3,5,7,8][0-9]\\d{8}', detail)
phone = phone[0] if phone else ''

name_str = re.findall('经理：.{2,3}|联系人：.{2,3}|厂长：.{2,3}', detail)  # [('','')]
# name_str = re.findall('经理：(.{2,3})|联系人：(.{2,3})', detail)[0]  # [('','')]
name = name_str[0] if name_str else ''
# name = name_str[0]
# if not name_str[0]:
#     name = name_str[1]
name = '' if name == '未提供' else name
print(telephone, phone, name)
"""['010-63300177', '010-63300620'] ['13701302061']"""

