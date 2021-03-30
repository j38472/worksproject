from selenium import webdriver
from time import sleep
from lxml import etree
import random as rd
import requests
from pymysql import connect

# UA 标识
UA_list = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
    'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
]
# 尺寸
xy_window = [
    '1024,768', '1366,768', '1920,1080', '800,600'
]

# 姓氏列表
xing_list = [
'赵','钱','孙','李','周','吴','郑','王','冯','陈','褚','卫','蒋','沈','韩','杨','朱','秦','尤','许',
'何','吕','施','张','孔','曹','严','华','金','魏','陶','姜','戚','谢','邹','喻','柏','水','窦','章','云'
]
# 名字
ming_list = [
'涛','昌进','林','有','坚','邦','承','乐','绍功','松','善','厚','庆','磊','民','友裕',
'河','哲','江','浩','亮','政','谦','旭','鹏泽','晨','辰士','以','建','致树','炎','德','行'
]
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
}

# 企业网址信息
list_company_dic = [{'网址': 'http://ddrzsp.1588.tv/'}]  # 从分页中获取的网站网址和主营产品信息

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
        ip, port  = pro_get()
        return ip, port


# 释放代理
def pro_close(ip):
    url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
    requests.post(url=url)


# 设置页数，获得网址
def page_get():
    # 循环分页，手动设定页数
    for page in range(6, 8):
        sleep(6)
        # 获取页数
        url = 'http://www.1588.tv/company/diqu_beijing-{}.html'.format(page)
        print('获取第%s页' % page)
        response = requests.get(url=url, headers=headers)
        # 获得源码
        page_text = response.text
        # 解析网页
        html = etree.HTML(page_text)
        # 获取网页中的企业网址和主营产品数据
        div_list = html.xpath('//div[@class="Com_Library_R"]')
        for div in div_list:
            sleep(0.5)
            dic = {}
            msg = ''
            href = div.xpath('./div[@class="Caption"]/div[1]/a/@href')[0]
            name = div.xpath('./div[@class="Caption"]/div[1]/a/text()')[0]
            # print(name)
            # print(href)
            a_list = div.xpath('./div[@class="Matter"]/a')
            for a in a_list:
                msg = msg + a.xpath('./text()')[0] + ' '
            # print(msg)
            dic['网址'] = str(href).strip('\n')
            dic['公司名称'] = str(name).strip(' \n')
            dic['主营产品'] = str(msg).strip('\n')
            # print(dic)
            companys_dic_list.append(dic)


# 数据库保存
def save_data(dic):
    # 连接数据库
    conn = connect(
        host='localhost',
        port=3306,
        db='hbsc',
        user='root',
        password='963',
        charset='utf8'
    )
    # 获取游标
    cur = conn.cursor()
    # sql语句
    sql1 = """
        insert into sudongshipin (lianxiren, phone, telephone, company, produce, address, href) values (%s, %s, %s, %s, %s, %s, %s);
        """
    cur.execute(sql1, (
        str(dic.get('联系人')) if str(dic.get('联系人')) else '', str(dic.get('手机')) if str(dic.get('手机')) else '',
        str(dic.get('电话')) if str(dic.get('电话')) else '', str(dic.get('公司名称')) if str(dic.get('公司名称')) else '',
        str(dic.get('主营产品')) if str(dic.get('主营产品')) else '', str(dic.get('地址')) if str(dic.get('地址')) else '',
        str(dic.get('网址')) if str(dic.get('网址')) else ''))
    conn.commit()
    cur.close()
    print('保存成功', dic.get('网址'))
    conn.close()


# 自动留言
def zdly(type, dic):
    if type == 'vip':
        # 点击留言标签
        sleep(1)
        a_ele = bro.find_element_by_xpath('//p[@class="wenziya"]/a[1]')
        # print(a_ele)
        # selenium的点击方式不能使用
        # 使用js代码点击
        bro.execute_script("arguments[0].click();", a_ele)
        # a_ele.click()
        sleep(rd.randint(1, 3))
        # 操作js代码移动滑块
        bro.execute_script('window.scrollTo(0, window.innerHeight)')
        # 自动输入文字
        # 每次输入随机间隔，姓名
        lianxiren_ele = bro.find_element_by_id('ctl00_Liuyan_txtInputer')
        xing = rd.choice(xing_list)
        ming = rd.choice(ming_list)
        xm = xing + ming
        lianxiren_ele.send_keys(xm)
        sleep(rd.randint(1, 3))
        phone_ele = bro.find_element_by_id('ctl00_Liuyan_txtTelephone')
        # 填入信息，手机号
        phone = '1' + str(rd.randint(30,88)) + str(rd.randint(10,88)) + str(rd.randint(10,99)) + str(rd.randint(30,88)) + str(rd.randint(10,99))
        phone_ele.send_keys(phone)
        sleep(rd.randint(1, 5))
        wechat_ele = bro.find_element_by_id('ctl00_Liuyan_txtWeixin')
        wechat_ele.send_keys(phone)
        sleep(rd.randint(1, 3))
        qq_ele = bro.find_element_by_id('ctl00_Liuyan_txtqq')
        qq = str(rd.randint(7, 88)) + str(rd.randint(10, 88)) + str(rd.randint(10, 99)) + str(rd.randint(30, 88)) + str(rd.randint(10,99))
        qq_ele.send_keys(qq)
        # 点击提交按钮，提交留言
        sleep(rd.randint(1, 3))
        sumbit_ele = bro.find_element_by_id('ctl00_Liuyan_btnSubmit')
        # sumbit_ele.click()
        bro.execute_script("arguments[0].click();", sumbit_ele)
        sleep(rd.randint(1, 3))
        # 弹窗信息
        # 获取alert对话框
        dig_alert = bro.switch_to.alert
        if dig_alert:
            sleep(1)
            # 打印警告对话框内容
            print(dig_alert.text)
            # alert对话框属于警告对话框，我们这里只能接受弹窗
            dig_alert.accept()
            return True
        ly_page_text = bro.page_source
        ly_html = etree.HTML(ly_page_text)
        p_list = ly_html.xpath('//div[@class="lxleft"]/p')
        if p_list:
            save_data(dic)
            # for p in p_list:

    elif type == 'lxbod':
        span = bro.find_element_by_xpath('//*[@id="ctl00_contact_lblLinkman"]/a')
        # span.click()
        bro.execute_script("arguments[0].click();", span)
        sleep(rd.randint(1, 3))
        # 操作js代码移动滑块
        bro.execute_script('window.scrollTo(0, window.innerHeight)')
        # 自动输入文字信息
        sleep(rd.randint(1, 3))
        lianxiren_ele = bro.find_element_by_id('ctl00_Liuyan_txtInputer')
        xing = rd.choice(xing_list)
        ming = rd.choice(ming_list)
        xm = xing + ming
        lianxiren_ele.send_keys(xm)
        sleep(rd.randint(1, 3))
        phone_ele = bro.find_element_by_id('ctl00_Liuyan_txtTelephone')
        # 填入手机号
        phone = '1' + str(rd.randint(30, 88)) + str(rd.randint(10, 88)) + str(rd.randint(10, 99)) + str(
            rd.randint(30, 88)) + str(rd.randint(10, 99))
        phone_ele.send_keys(phone)
        sleep(rd.randint(1, 3))
        wechat_ele = bro.find_element_by_id('ctl00_Liuyan_txtWeixin')
        wechat_ele.send_keys(phone)
        sleep(rd.randint(1, 5))
        qq_ele = bro.find_element_by_id('ctl00_Liuyan_txtqq')
        qq = str(rd.randint(7, 88)) + str(rd.randint(10, 88)) + str(rd.randint(10, 99)) + str(rd.randint(30, 88)) + str(
            rd.randint(10, 99))
        qq_ele.send_keys(qq)
        # 点击提交按钮，提交留言
        sleep(rd.randint(1, 3))
        sumbit_ele = bro.find_element_by_id('ctl00_Liuyan_btnSubmit')
        # sumbit_ele.click()
        bro.execute_script("arguments[0].click();", sumbit_ele)
        sleep(rd.randint(2, 5))
        # 弹窗信息
        # 获取alert对话框
        dig_alert = bro.switch_to.alert
        if dig_alert:
            sleep(1)
            # 打印警告对话框内容
            print(dig_alert.text)
            # alert对话框属于警告对话框，我们这里只能接受弹窗
            dig_alert.accept()
            return True
        but_ele = bro.find_element_by_id('ctl00_Liuyan_Button2')
        sleep(rd.randint(1, 3))
        bro.execute_script("arguments[0].click();", but_ele)
        # 等待网页加载，获取信息
        sleep(3)
        ly_html = etree.HTML(bro.page_source)
        div_ly = ly_html.xpath('//div[@id="ctl00_contact_youliuyan"]')
        data1_list = div_ly[0].xpath('.//text()')
        for data in data1_list:
            # 获取具体信息数据，赋值到字典中
            if '联系人：' in data:
                dic['联系人'] = data.split('：')[-1]
            elif '品牌运营' in data:
                dic['联系人'] = data.split('：')[-1]
            elif '手\u3000机：' in data:
                dic['手机'] = data.split('：')[-1]
            elif '招商热线' in data:
                dic['手机'] = data.split('：')[-1]
            elif '地\u3000址：' in data:
                dic['地址'] = data.split('：')[-1]
            elif '邮\u3000箱：' in data:
                dic['邮箱'] = data.split('：')[-1]
            elif '电\u3000话：' in data:
                dic['电话'] = data.split('：')[-1]
            elif '招商电话' in data:
                dic['电话'] = data.split('：')[-1]
        save_data(dic)


if __name__ == '__main__':
    # 获取网址
    # page_get()
    # 使用selenium打开企业详情页，获取数据
    for dic in companys_dic_list:
        print('休眠1分半')
        # sleep(90)
        # 设置浏览器参数
        # 实例化option对象
        option = webdriver.ChromeOptions()
        # 设置成无头浏览器尝试请求，爬取js渲染之后的页面
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        # 设置UA
        # user_agent = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64)" +
        #               "AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
        option.add_argument('--user-agent={}'.format(rd.choice(UA_list)))
        # option.add_argument('user-agent=%s'%user_agent)
        # 设置屏幕宽度
        option.add_argument('--window-size={}'.format(rd.choice(xy_window)))
        # 获取代理地址，添加代理
        ip, port = pro_get()
        # option.add_argument='--proxy-server={}:{}'.format(ip, port)
        option.add_argument('–proxy-server=http://{}:{}'.format(ip, port))
        # 以最高权限运行
        # option.add_argument('--no-sandbox')
        # 防止window.navigator.webdriver检测
        # 隐藏会话暴露的真实ip
        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False
        }
        option.add_experimental_option("prefs", preferences)
        # 开启实验性功能参数，去除提示，防止检测
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 无效
        option.add_experimental_option('useAutomationExtension', False)
        # 就是这一行告诉chrome去掉了webdriver痕迹
        option.add_argument("disable-blink-features=AutomationControlled")
        option.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')

        # 生成浏览器对象
        bro = webdriver.Chrome(options=option)

        href = dic.get('网址')
        # 无法发送Ajax请求
        bro.get(href)
        sleep(3)
        page_text = bro.page_source
        # 解析网页
        html = etree.HTML(page_text)
        # 判断网页类型
        div_vip = html.xpath('//div[@class="cecec"]')
        # print('vip', div_vip)
        if div_vip:
            # 判断是否需要留言
            a_ele = div_vip[0].xpath('./p/a/font')
            # 滑动到留言区域
            sleep(1)
            bro.execute_script('window.scrollTo(0, 2*window.innerHeight)')

            # print(a_ele)
            # 需要留言，调用留言模块
            if a_ele:
                msg = 'vip'
                zdly(msg, dic)
                continue
            data_list = div_vip[0].xpath('./p//text()')
            # print(data_list)
            for data in data_list:
                # 获取具体信息数据，赋值到字典中
                if '联系人：' in data:
                    dic['联系人'] = data.split('：')[-1]
                elif '品牌运营' in data:
                    dic['联系人'] = data.split('：')[-1]
                elif '手\u3000机：' in data:
                    dic['手机'] = data.split('：')[-1]
                elif '招商热线' in data:
                    dic['手机'] = data.split('：')[-1]
                elif '地\u3000址：' in data:
                    dic['地址'] = data.split('：')[-1]
                elif '电\u3000话：' in data:
                    dic['电话'] = data.split('：')[-1]
                elif '招商电话' in data:
                    dic['电话'] = data.split('：')[-1]
            save_data(dic)
            continue
        # print(list)
        # 判断网页是否需要留言
        div = html.xpath('//div[@id="ctl00_contact_meiliuyan"]')
        div_show = html.xpath('//div[@id="ctl00_contact_youliuyan"]')
        # print('div',div)
        if div:
            # 滑动到留言区域
            sleep(1)
            bro.execute_script('window.scrollTo(0, 2*window.innerHeight)')
            msg = 'lxbod'
            res = zdly(msg, dic)
            if res:
                continue
        elif div_show:
            # 滑动到留言区域
            sleep(1)
            bro.execute_script('window.scrollTo(0, 2*window.innerHeight)')
            data1_list = div_show[0].xpath('.//text()')
            print(data1_list)
            for data in data1_list:
                # 获取具体信息数据，赋值到字典中
                if '联系人：' in data:
                    dic['联系人'] = data.split('：')[-1]
                elif '品牌运营' in data:
                    dic['联系人'] = data.split('：')[-1]
                elif '手\u3000机：' in data:
                    dic['手机'] = data.split('：')[-1]
                elif '招商热线' in data:
                    dic['手机'] = data.split('：')[-1]
                elif '地\u3000址：' in data:
                    dic['地址'] = data.split('：')[-1]
                elif '邮\u3000箱：' in data:
                    dic['邮箱'] = data.split('：')[-1]
                elif '电\u3000话：' in data:
                    dic['电话'] = data.split('：')[-1]
                elif '招商电话' in data:
                    dic['电话'] = data.split('：')[-1]
            save_data(dic)

        sleep(3)
        # 释放代理
        pro_close(ip=ip)
        # 关闭浏览器
        bro.quit()

