import requests
from time import sleep
from lxml import etree
from functools import partial


headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
}

# 代理设置
def get_proxy():
    get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
    res = requests.post(url=get_url).text
    code = res.split(',')[0].split(':')[-1]
    if code == '0':
        # 获取代理
        ip = res.split(',')[1].split(':')[-1].strip('"')
        port = res.split(',')[2].split(':')[-1].strip('"')
        print('获取代理：', ip, port)
        return ip, port
    else:
        try:
            print('没有可用通道，释放通道')
            sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
            page_test = requests.post(sf_url).text
            sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
            print('释放代理')
            sleep(5)
            url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
            requests.post(url=url)
            # 代理获取时长限制
            sleep(6)
            ip, port = get_proxy()
            return ip, port
        except Exception as e:
            print(e)
            # sleep(3)
            ip, port = get_proxy()
            return ip, port


# 释放代理
def close_proxy(ip):
    print('释放代理')
    close_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
    requests.post(url=close_url)


if __name__ == '__main__':
    ip, port = get_proxy()
    # 目标请求地址
    targetUrl = "https://httpbin.org/ip"
    proxyMeta = "http://%s:%s" % (ip, port)
    proxies = {
        # 根据请求方式（http/https）的不同，可以选择不同的代理
        "http": proxyMeta,
        "https": proxyMeta
    }
    # 证书问题
    requests.get = partial(requests.get, verify=False, proxies=proxies)
    response = requests.get(url=targetUrl, headers=headers, proxies=proxies)
    # 获得源码
    page_text = response.text
    print(page_text)
    print(response.status_code)


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