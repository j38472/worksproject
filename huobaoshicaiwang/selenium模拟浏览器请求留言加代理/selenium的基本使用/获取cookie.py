from selenium import webdriver
import time
import json

options = webdriver.ChromeOptions()
dr = webdriver.Chrome(options=options)

dr.get('https://cn.bing.com/search?q=objective%20lens%20of%20compound%20microscope&qs=ds&form=QBRE')

cookie_test = dr.get_cookies()
# 未整理的cookie
print(cookie_test)

cookie = [item["name"] + "=" + item["value"] for item in cookie_test]
cookiestr = '; '.join(item for item in cookie)
# 整理后的cookie
print(cookiestr)


"""
# 设置cookie
# bro.delete_all_cookies() # 删除所有的cookie
# cookie_test = bro.get_cookies()
# cookie = [item["name"] + "=" + item["value"] for item in cookie_test]
# bro.add_cookie(cookie)
"""