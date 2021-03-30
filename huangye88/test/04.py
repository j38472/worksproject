import requests
from lxml import etree
url = 'http://b2b.huangye88.com/gongsi/27r2pd8eb6c1/company_contact.html'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

response = requests.get(url=url, headers=headers, allow_redirects=False)
print(response.status_code)
# print(response.headers)
html = etree.HTML(response.text)
print(html)



# s = requests.session()
# s.headers['User-Agent'] =  "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
# response = s.get(url=url)
# print(response.status_code)
# page_text = response.text
# print(page_text)
