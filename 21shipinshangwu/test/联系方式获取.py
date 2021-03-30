import requests
from lxml import etree
from fake_useragent import UserAgent
import pymysql


url = 'http://oksyp.21food.cn/company/contact1516816.html'
ua = UserAgent().random
headers = {
    "user-agent": ua
}
dic = {}
response = requests.get(url=url, headers=headers)
# print(response.status_code)
pages_text = response.text
html = etree.HTML(pages_text)
# print(pages_text)
# div_list = html.xpath('//div[@class="first"]//text()')
div_list = html.xpath('//div[@class="contact"]/div[@class="contact-info"]/div')
for div in div_list:
    data_str = div.xpath('.//text()')
    if '联系人：' in data_str:
        name = data_str[-1].strip('\r\n\t').replace('\r\n\t\t\t', '')
        dic['联系人'] = name
    elif '手机：' in data_str:
        phone = data_str[-1].strip('\r\n\t').replace('\r\n\t\t\t', '')
        dic['手机'] = phone
    elif '电话：' in data_str:
        telephone = data_str[-1].strip('\r\n\t').replace('\r\n\t\t\t', '')
        dic['电话'] = telephone
    elif '地址：' in data_str:
        address = data_str[-1].strip('\r\n\t').replace('\r\n\t\t\t', '')
        dic['地址'] = address


conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='97655',
    db='21shipinwang',
    charset='utf8'
)
cursor = conn.cursor()
sql1 = """
    insert into jiulei (company, produce, company_type, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s, %s);
               """
cursor.execute(sql1, (
    str(dic.get('公司名称')) if dic.get('公司名称') else '',
    str(dic.get('主营产品')) if dic.get('主营产品') else '',
    str(dic.get('经营类型')) if dic.get('经营类型') else '',
    str(dic.get('联系人')) if dic.get('联系人') else '',
    str(dic.get('手机')) if dic.get('手机') else '',
    str(dic.get('电话')) if dic.get('电话') else '',
    str(dic.get('地址')) if dic.get('地址') else '',
    str(dic.get('网址')) if dic.get('网址') else ''
))
conn.commit()

print('保存成功')
cursor.close()
conn.close()







