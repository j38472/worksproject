import requests
from lxml import etree
from fake_useragent import UserAgent

urls_list = []
url = 'https://www.21food.cn/company/companylist_catid-03.html'
print(UserAgent().random)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
print(response.status_code)
html = etree.HTML(response.text)

li_list = html.xpath('//div[@class="ec_tit_nv ec_tit_nvg"]/ul/li')

for li in li_list:
    href = 'https://www.21food.cn' + li.xpath('./a/@href')[0]  # /company/companylist_catid-03007.html
    # print(href)
    urls_list.append(href)

for pa in range(3, 6):
    company_list = []
    # 选择一个分类进行网站反爬测试
    company_url = urls_list[pa]
    c_response = requests.get(url=company_url, headers=headers)
    print(c_response.status_code)
    c_html = etree.HTML(c_response.text)
    dd_list = c_html.xpath('//div[@class="qy_list_main auto"]/div[1]/dl/dd')
    # dd_list = c_html.xpath('/html/body/div[4]')
    for dd in dd_list:

        c_href = dd.xpath('.//span[@class="qylis_tt"]/a/@href')[0]
        c_name = dd.xpath('.//span[@class="qylis_tt"]/a/text()')[0]
        c_produce = dd.xpath('.//div[@class="qy_lis_l_jmo_ll"]/ul/li[2]/span/text()')[0].strip(' \n')
        company_list.append(c_href)
    for c_href in company_list:
        print('获取网页信息', c_href)
        detail_response = requests.get(url=c_href, headers=headers)

        data = detail_response.text
        print(detail_response.status_code)


        # print(c_name, c_produce)





