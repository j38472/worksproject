import requests
from selenium import webdriver
from time import sleep
import random


# UA 标识
UA_list = [
    # 'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
    'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    # 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    # 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
]
# 尺寸
xy_window = ['1024,768', '1366,768', '1920,1080', '800,600']

# selenium添加代理
# 获取地址
get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
res = requests.post(url=get_url)
print(res.status_code)
print(res.text)
code = res.text.split(',')[0].split(':')[-1]
ip = ''
# 字符串的显示
ip = res.text.split(',')[1].split(':')[-1].strip('"')
# print(type(ip))
port = res.text.split(',')[2].split(':')[-1].strip('"')
# 获取到代理ip地址
# host = '%s:%s' % (ip, port)

# host = '163.125.158.23:8888'
# 实例化option对象
option = webdriver.ChromeOptions()

# 设置UA
# user_agent = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64)" +
#               "AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
option.add_argument('--user-agent=%s' % random.choice(UA_list))
# option.add_argument('user-agent=%s'%user_agent)
# 设置屏幕宽度
option.add_argument('--window-size=%s' % random.choice(xy_window))
# 添加代理
option.add_argument('–proxy-server=http://{}:{}'.format(ip, port))
# 以最高权限运行
option.add_argument('--no-sandbox')
# 防止window.navigator.webdriver检测
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
# 禁用图片加载
# prefs = {
#     'profile.default_content_setting_values' : {
#         'images' : 2
#     }
# }
# option.add_experimental_option('prefs',prefs)

# 生成浏览器对象
bro = webdriver.Chrome(options=option) # 驱动自动加载
bro.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
   'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
try:
    bro.get('http://zshsp.1588.tv/')
    sleep(5)
    # print(bro.page_source)

    # btn = bro.find_element_by_id('ctl00_contact_lblLinkman')
    span = bro.find_element_by_xpath('//*[@id="ctl00_contact_lblLinkman"]/a')
    # span.click()
    bro.execute_script("arguments[0].click();", span)
    sleep(3)
except Exception as e:
    print(e)

# 释放地址
url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
close_url = url
response = requests.post(url=close_url)
print(url)
sleep(5)
# bro.close()
# bro.quit()