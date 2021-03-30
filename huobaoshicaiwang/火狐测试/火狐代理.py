"""
文档案例，不能使用

"""
from selenium import webdriver

PROXY = "<115.211.228.110:41550>"
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",

}
driver = webdriver.Firefox()
driver.get("https://www.baidu.com")