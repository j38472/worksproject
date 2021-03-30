"""
能进入大众点评，不能进入美团，火爆食材网
"""

from selenium import webdriver
from fake_useragent import UserAgent
from time import sleep
import requests


# 获取代理
def pro_get():
    get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
    res = requests.post(url=get_url).text
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
        url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
        requests.post(url=url)
        print(url)
        sleep(3)
        ip, port = pro_get()
        return ip, port


# 释放代理
def pro_close(ip):
    url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
    requests.post(url=url)


# 浏览器设置
options = webdriver.ChromeOptions()
# 实现无可视化界面操作
options.add_argument('--headless')
# 谷歌文档，about:black空白页问题   无效
options.add_argument('--disable-gpu')
# 随机UA库
ua = UserAgent()
options.add_argument('--user-agent={}'.format(ua.random))
options.add_argument('--window-size=1240,1080')
# 设置代理,options.to_capabilities()方式
ip, port = pro_get()
# ip = '171.35.146.200'
# port = '9999'
PROXY = '{}:{}'.format(ip, port)
desired_capabilities = options.to_capabilities()
desired_capabilities['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "noProxy": None,
    "proxyType": "MANUAL",
    "class": "org.openqa.selenium.Proxy",
    "autodetect": False
}
# 隐藏会话暴露的真实ip
preferences = {
    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled": False
}
options.add_experimental_option("prefs", preferences)
# 开启实验性功能参数，去除提示，防止检测
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 无效
options.add_experimental_option('useAutomationExtension', False)
# 就是这一行告诉chrome去掉了webdriver痕迹
options.add_argument("disable-blink-features=AutomationControlled")
options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
# 无图模式
# prefs = {"profile.managed_default_content_settings.images": 2}              # 不显示图片提高代码速度
# options.add_experimental_option("prefs", prefs)
# 最高权限
# options.add_argument('--no-sandbox')

"""不添加desired_capabilities参数也可以使用代理"""

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
# driver.get('https://httpbin.org/ip')
driver.get('http://majin18.21food.cn/company/contact628798.html')
# print(driver.page_source)
# sleep(60)
# driver.quit()



