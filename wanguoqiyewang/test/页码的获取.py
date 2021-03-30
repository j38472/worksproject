import requests
import re
from fake_useragent import UserAgent


url = 'https://qiye.trustexporter.com/tutechan/'
ua = UserAgent().random
headers = {
    "user-agent": ua
}
response = requests.get(url=url, headers=headers)
# print(response)  # <Response [200]>
# print(response.status_code)
pages = re.findall('条/(.*?)页', response.text)  # ['3']
page = int(pages[0])
for pn in range(1, page+1):
    pass

