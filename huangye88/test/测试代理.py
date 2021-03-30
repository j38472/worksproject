import requests
from fake_useragent import UserAgent
from time import sleep

"""
可以使用，速度较慢
"""

ua = UserAgent()
headers = {
    "user-agent":ua.random
}


# 获取代理
def pro_get():
    url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
    res = requests.post(url=url).text
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
        t_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
        requests.post(url=t_url)
        sleep(3)
        ip, port = pro_get()
        return ip, port


# # 释放代理
# def pro_close(ip):
#     c_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
#     requests.post(url=c_url)

url = 'https://httpbin.org/ip'
ip, port = pro_get()
N = 0
while N < 3:
    N += 1
    # 代理服务器
    proxyHost = ip  # ip地址
    proxyPort = port  # 端口号
    proxyMeta = "http://%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    # allow_redirects = False 不允许重定向，超时设置
    response = requests.get(url=url, headers=headers, timeout=15, allow_redirects=False, proxies=proxies)
    # print(response.status_code)
    page_text = response.text
    print(page_text)