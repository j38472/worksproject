import requests
from selenium import webdriver
from time import sleep
import random
from fake_useragent import UserAgent


# 尺寸
xy_window = ['1024,768', '1366,768', '1920,1080', '800,600']


# # 获取代理
# def get_proxy(self):
#     get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
#     res = requests.post(url=get_url).text
#     code = res.split(',')[0].split(':')[-1]
#     if code == '0':
#         # 获取代理
#         ip = res.split(',')[1].split(':')[-1].strip('"')
#         port = res.split(',')[2].split(':')[-1].strip('"')
#         print('获取代理：', ip, port)
#         return ip, port
#     else:
#         try:
#             print('重新释放代理')
#             sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
#             page_test = requests.post(sf_url).text
#             sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
#             url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
#             requests.post(url=url)
#             # 代理获取时长限制
#             sleep(6)
#             ip, port = self.get_proxy()
#             return ip, port
#         except Exception as e:
#             print(e, self.page)
#             sleep(3)
#             ip, port = self.get_proxy()
#             return ip, port
#
#
# # 释放代理
# def close_proxy(self, ip):
#     print('释放代理')
#     close_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
#     requests.post(url=close_url)


# selenium添加代理
# 实例化ChromeOptions对象
option = webdriver.ChromeOptions()
# 设置UA
option.add_argument('--user-agent=%s' % UserAgent().random)

# 设置屏幕宽度
option.add_argument('--window-size=%s' % random.choice(xy_window))
# 添加代理
# ip, port = get_proxy()
# option.add_argument('--proxy-server=http://{}:{}'.format(ip, port))
# 以最高权限运行
option.add_argument('--no-sandbox')
# 防止window.navigator.webdriver检测
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
# 就是这一行告诉chrome去掉了webdriver痕迹
option.add_argument("disable-blink-features=AutomationControlled")
option.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
# 生成浏览器对象
bro = webdriver.Chrome(options=option)  # 驱动自动加载
# bro.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
# })

bro.get('https://www.21food.cn/company/companylist_catid-06001.html')
# print(bro.page_source)

"""
未使用代理
网页可点击
"""