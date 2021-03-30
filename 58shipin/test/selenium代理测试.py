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
# options.add_argument('--headless')
# 谷歌文档，about:black空白页问题   无效
# options.add_argument('--disable-gpu')
# 随机UA库
ua = UserAgent()
options.add_argument('--user-agent={}'.format(ua.random))
options.add_argument('--window-size=1240,1080')
# 设置代理,options.to_capabilities()方式
ip, port = pro_get()
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
driver.get('http://www.58food.com/qy-l-0-0-3-0-335.html')
print(driver.page_source)
# sleep(60)
# driver.quit()

"""
// 启动就最大化
// options.addArguments("start-fullscreen");
// options.addArguments("--start-maximized");
// 禁止弹出拦截
options.addArguments("--disable-popup-blocking");
// 取消沙盘模式
options.addArguments("no-sandbox");
// 禁止扩展
options.addArguments("disable-extensions");
// 禁止默认浏览器检查
options.addArguments("no-default-browser-check");
options.addArguments("about:histograms");
options.addArguments("about:cache");
// 设置浏览器固定大小
options.addArguments("--window-size=1600,900");
// chrome正受到自动测试软件的控制
options.addArguments("disable-infobars");
WebDriver driver=new ChromeDriver(options);
// 设置浏览器的位置：
Point point=new Point(0,0);
driver.manage().window().setPosition(point);
// 注意：设定了浏览器固定大小后，浏览器打开后浏览器的位置可能会变到其他位置，因此可以使用设置刘浏览器的位置方法和设置浏览器的大小方法一起使用；
// driver.manage().window().maximize();
// 设置获取页面元素的最大等待时间
driver.manage().timeouts().implicitlyWait(15, TimeUnit.SECONDS);
// 打开网址
driver.get("www.baidu.com");
// 关闭浏览器
driver.quit();
//谷歌插件
options.addExtensions(new File("/path/to/extension.crx"))
options.setBinary(new File("/path/to/chrome"));

// For use with ChromeDriver:
ChromeDriver driver = new ChromeDriver(options);
//用户工作目录
options.addArguments("user-data-dir=/path/to/your/custom/profile");

//无头浏览器
options.addArguments("--headless");

//每当我们使用selenium启动chrome浏览器时，将为每个新会话创建一个新实例/临时配置文件。如果我们要加载默认的Chrome浏览器或自定义Chrome配置文件，
//我们可以将'user-data-dir'参数传递给ChromeOptions，这是Chrome命令行切换，告诉Chrome使用哪个配置文件。如果路径不存在，chrome将在指定的路径中创建新的配置文件。
ChromeOptions options = new ChromeOptions();
options.addArgument("user-data-dir=/path/to/your/custom/profile");

启动参数	作用
--user-agent=""	设置请求头的User-Agent
--window-size=1366,768	设置浏览器分辨率（窗口大小）
--headless	无界面运行（无窗口）
--start-maximized	最大化运行（全屏窗口）
--incognito	隐身模式（无痕模式）
--disable-javascript	禁用javascript
--disable-infobars	禁用浏览器正在被自动化程序控制的提示
"""


