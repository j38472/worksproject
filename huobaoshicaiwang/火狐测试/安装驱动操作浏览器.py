from selenium import webdriver


# 实例化
# driver = webdriver.Firefox(executable_path='./geckodriver.exe')
# 添加驱动到环境变量，和复制到python安装包路径
driver = webdriver.Firefox()
driver.get('https://www.baidu.com')