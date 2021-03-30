"""
webrtc，一种可以通过建立特殊的会话形式，如语音，聊天等，能够查找到查找真实ip的方法
此文件通过测试，可以使用，隐藏真实IP地址
测试网址：
"""

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
chrome_options.add_argument("--proxy-server=http://60.182.37.133:15134")
preferences = {
    "webrtc.ip_handling_policy": "disable_non_proxied_udp",
    "webrtc.multiple_routes_enabled": False,
    "webrtc.nonproxied_udp_enabled": False
}
chrome_options.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.1588.tv/company/")