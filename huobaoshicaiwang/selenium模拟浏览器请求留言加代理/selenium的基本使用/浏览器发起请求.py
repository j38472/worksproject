"""
设置UA，屏幕宽度，代理，防检测参数
"""
from selenium import webdriver
from lxml import etree
from time import sleep
import requests
from fake_useragent import UserAgent


# 手动获取代理ip
# 获取代理
def pro_get():
    get_url = 'https://proxy.qg.net/allocate?Key=F58B5B03A518E080'
    response = requests.post(url=get_url)
    res = response.text
    # print(res.status_code)
    # print(res.text)
    code = res.split(',')[0].split(':')[-1]
    # print(code)
    if code == '0':
        # 字符串的显示
        ip = res.split(',')[1].split(':')[-1].strip('"')
        # print(type(ip))
        port = res.split(',')[2].split(':')[-1].strip('"')
        print(ip, port)
        return ip, port
    else:
        sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
        page_test = requests.post(sf_url).text
        sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
        print(sf_ip)
        base_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
        requests.post(url=base_url)
        print(base_url)
        sleep(3)
        ip, port = pro_get()
        return ip, port


# 释放代理
def pro_close(ip):
    get_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
    requests.post(url=get_url)


# 浏览器参数设置
chrome_option = webdriver.ChromeOptions()
# 实现无可视化界面操作
# chrome_option.add_argument('--headless')
# 谷歌文档，about:black空白页问题   无效
# chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('--user-agent=%s' % UserAgent().random)
ip, port = pro_get()
chrome_option.add_argument('--proxy-server=http://{}:{}'.format(ip, port))
# selenium防检测设置
# 开启实验性功能参数，去除提示，防止检测
chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 无效
chrome_option.add_experimental_option('useAutomationExtension', False)
# 就是这一行告诉chrome去掉了webdriver痕迹
chrome_option.add_argument("disable-blink-features=AutomationControlled")
chrome_option.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
# 实例化浏览器对象
bro = webdriver.Chrome(options=chrome_option)
# js代码防检测，，效果待定
# bro.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
# })
bro.get('https://www.baidu.com')



# #循环分页，手动设定页数
# for page in range(1, 10):
#     sleep(3)
#     # 获取页数
#     url = 'http://www.1588.tv/company/type_hgsc-%s.html' % page
#     print('获取第%s页' % page)
#     bro.get(url=url)
#     # 获得源码
#     page_text = bro.page_source
#
#     #解析网页
#     html = etree.HTML(page_text)
#     # 获取网页中的企业网址和主营产品数据
#     div_list = html.xpath('//div[@class="Com_Library_R"]')
#     for div in div_list:
#         sleep(0.5)
#         dic = {}
#         msg = ''
#         href = div.xpath('./div[@class="Caption"]/div[1]/a/@href')[0]
#         name = div.xpath('./div[@class="Caption"]/div[1]/a/text()')[0]
#         # print(name)
#         # print(href)
#         a_list = div.xpath('./div[@class="Matter"]/a')
#         for a in a_list:
#             msg = msg + a.xpath('./text()')[0] + ' '
#         # print(msg)
#         dic['网址'] = str(href).strip('\n')
#         dic['公司名称'] = str(name).strip(' \n')
#         dic['主营产品'] = str(msg).strip('\n')
#         # print(dic)
#         companys_dic_list.append(dic)

#自动化操作
# div_ele = bro.find_element_by_class_name('Com_Library')
sleep(5)
bro.close()
