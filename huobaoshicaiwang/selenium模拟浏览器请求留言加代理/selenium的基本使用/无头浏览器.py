from selenium import webdriver
import time

# 配置
# ch_options = Options()
# ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
#
# # 在启动浏览器时加入配置
# driver = webdriver.Chrome(options=ch_options)  # => 注意这里的参数
#
# driver.get('http://cn.bing.com')
#
# time.sleep(2)
#
# # 只有截图才能看到效果咯
# driver.save_screenshot('./ch.png')
#
# # 关闭所有页面
# driver.quit()

ch_options = webdriver.ChromeOptions()
ch_options.add_argument("--headless")  # => 为Chrome配置无头模式

# 在启动浏览器时加入配置
driver = webdriver.Chrome(options=ch_options)  # => 注意这里的参数

driver.get('http://cn.bing.com')

time.sleep(2)

# 只有截图才能看到效果咯
driver.save_screenshot('./ch.png')

# 关闭所有页面
driver.quit()