import requests
from lxml import etree
import re

url = 'https://www.b2b168.com/beijing-shipin/shuiguoshucai/guoshulei/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
# 页码
# 确定页码
page = html.xpath('//div[@class="pages"]/text()')
if page:
    page_str = ''.join(page).replace('\r\n','').replace(' ','')
    pages_l = re.findall(r'共(.*?)页', page_str)
    print(page_str)
    pages = int(pages_l[0]) if pages_l else ''
    print(pages)

