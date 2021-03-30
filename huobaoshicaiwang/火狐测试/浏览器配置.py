from selenium import webdriver
from selenium.webdriver.common.proxy import *
from fake_useragent import UserAgent

'''
设置代理的方式一
# 这种方法在py3好像有点问题隐藏了
# 代理
myProxy = '202.202.90.20:8080'
# 代理格式
proxy = Proxy({
  'proxyType': ProxyType.MANUAL, 
  'httpProxy': myProxy, 
  'ftpProxy': myProxy, 
  'sslProxy': myProxy, 
  'noProxy': ''
 })

profile = webdriver.FirefoxProfile()
profile = get_firefox_profile_with_proxy_set(profile, proxy)
'''
"""
# 方式三
# 第二步：开启“手动设置代理”
options.set_preference('network.proxy.type', 1)
# 第三步：设置代理IP
options.set_preference('network.proxy.http', '221.180.170.104')
# 第四步：设置代理端口，注意端口是int类型，不是字符串
options.set_preference('network.proxy.http_port', 8080)
"""
# 方式二
ip = '60.184.194.251'
port = 62862
# 实例化FirefoxProfile对象
profile = webdriver.FirefoxProfile()
# 配置代理设置
profile.set_preference('network.proxy.type', 1)
# 默认值是0，直接连接；1，手工设置代理
profile.set_preference('network.proxy.http', ip)
profile.set_preference('network.proxy.http_port', port)
# profile.set_preference('network.proxy.ssl', ip)
# profile.set_preference('network.proxy.ssl_port', port)
# 随机设置UA
ua = UserAgent()
profile.set_preference("general.useragent.override", ua.random)
profile.update_preferences()

# 实例化FirefoxOptions对象
options = webdriver.FirefoxOptions()
# Firefox无头模式
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# 设置屏幕宽度
# options.add_argument('--window-size=1240x1080')
driver = webdriver.Firefox(firefox_profile=profile, options=options)

driver.get('https://www.baidu.com')


