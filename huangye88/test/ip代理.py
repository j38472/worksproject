import requests

# 获取地址
get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
res = requests.post(url=get_url)
print(res.status_code)
print(res.text)
code = res.text.split(',')[0].split(':')[-1]
ip = ''
# 字符串的显示
ip = res.text.split(',')[1].split(':')[-1].strip('"')
# print(type(ip))
post = res.text.split(',')[2].split(':')[-1]
# print(ip, post)

# 目标请求地址
targetUrl = "https://www.baidu.com"

# 代理服务器
proxyHost = ip # ip地址
proxyPort = post # 端口号

proxyMeta = "http://%(host)s:%(port)s" % {
"host" : proxyHost,
"port" : proxyPort,
}

proxies = {
"http" : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)
print(resp.status_code)
print(resp.text)

# 释放地址

url = 'https://proxy.qg.net/release?Key=861F8C9M&IP=' + ip
close_url = url
response = requests.post(url=close_url)
print(url)




# #目标请求地址
# targetUrl = "https://proxy.qg.net/allocate?Key=861F8C9M"
#
# #代理服务器
# proxyHost = "117.86.11.181" #ip地址
# proxyPort = "24795" #端口号
#
# proxyMeta = "http://%(host)s:%(port)s" % {
# "host" : proxyHost,
# "port" : proxyPort,
# }
#
# #pip install -U requests[socks] socks5代理
# # proxyMeta = "socks5://%(host)s:%(port)s" % {
# # "host" : proxyHost,
# # "port" : proxyPort,
# # }
#
# proxies = {
# "http" : proxyMeta,
# }
#
# resp = requests.get(targetUrl, proxies=proxies)
# print(resp.status_code)
# print(resp.text)