import requests
from time import sleep
from lxml import etree

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
}



# 获取代理
def pro_get():
    get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
    res = requests.post(url=get_url).text
    # print(res.status_code)
    # print(res.text)
    code = res.split(',')[0].split(':')[-1]
    # print(code)
    if code == '0':
        ip = ''
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
        # print(sf_ip)
        url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
        requests.post(url=url)
        # print(url)
        sleep(3)
        ip, port = pro_get()
        return ip, port


# 释放代理
def pro_close(ip):
    url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
    requests.post(url=url)


if __name__ == '__main__':
    ip, port = pro_get()
    # 目标请求地址
    targetUrl = "https://httpbin.org/ip"
    # 代理服务器
    # proxyHost = ip  # ip地址
    # proxyPort = port  # 端口号
    # proxyMeta = "http://%(host)s:%(port)s" % {
    #     "host": proxyHost,
    #     "port": proxyPort,
    # }
    proxyMeta = "http://%s:%s" % (ip, port)
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    response = requests.get(targetUrl, headers=headers, proxies=proxies)
    # 获得源码
    page_text = response.text
    print(page_text)
    print(requests.get(url='https://www.21food.cn/company/companylist_catid-03007.html', headers=headers, proxies=proxies).status_code)

"""
requests.get(url,headers=headers,verify=False)
以上咱们需要记住，因为代理软件的证书是自己生成的，
所以requests请求https类型的网站会验证失败导致请求不成功，
所以在requests请求把verify字段设置为False，略过证书验证。

from functools import partial 
批量设置verify
requests.get=partial(requests.get,verify=False)
requests.post=partial(requests.post,verify=False)

如果代理不在本机或者代理未开启全局代理
from functools import partial 
proxy={"http":"127.0.0.1:8888","https":"127.0.0.1:8888"}
requests.get=partial(requests.get,verify=False,proxies=proxy)
requests.post=partial(requests.post,verify=False,proxies=proxy)
"""