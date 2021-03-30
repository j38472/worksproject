from selenium import webdriver
from time import sleep
from lxml import etree
import random as rd
import requests
from pymysql import connect
from fake_useragent import UserAgent


class HuoBaoShiCai:

    # 设置参数和数据库的开启
    def __init__(self, x_list, m_list, size):
        self.xing_list = x_list
        self.ming_list = m_list
        self.xy_window = size
        self.company_dic_list = []
        # 连接数据库
        self.conn = connect(
            host='localhost',
            port=3306,
            db='hbsc',
            user='root',
            password='97655',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    # 声明调用
    def __call__(self, *args, **kwargs):
        self.data_company()

    # 获取代理
    def proxy_get(self):
        get_url = "https://proxy.qg.net/allocate?Key=F58B5B03A518E080"
        res = requests.post(url=get_url).text
        # print(res.status_code)
        # print(res.text)
        code = res.split(',')[0].split(':')[-1]
        if code == '0':
            # 字符串的显示
            ip = res.split(',')[1].split(':')[-1].strip('"')
            # print(type(ip))
            port = res.split(',')[2].split(':')[-1].strip('"')
            print('%s:%s' % (ip, port))
            return ip, port
        else:
            sf_url = "https://proxy.qg.net/query?Key=F58B5B03A518E080"
            page_test = requests.post(sf_url).text
            sf_ip = page_test.split(',')[3].split(':')[-1].strip('"')
            print('失效ip：', sf_ip)
            url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + sf_ip
            requests.post(url=url)
            sleep(3)
            ip, port = self.proxy_get()
            return ip, port

    # 释放代理
    def proxy_close(self, ip):
        sf_url = 'https://proxy.qg.net/release?Key=F58B5B03A518E080&IP=' + ip
        requests.post(url=sf_url)

    # 设置浏览器参数，开启浏览器
    def chrome_set(self, href):
        # 实例化浏览器对象
        option = webdriver.ChromeOptions()
        # 实现无可视化界面操作
        # option.add_argument('--headless')
        # option.add_argument('--disable-gpu')
        # 使用useragent随机库
        ua = UserAgent()
        print(ua.chrome)
        option.add_argument('--user-agent=%s' % ua.chrome)
        option.add_argument('--window-size=%s' % rd.choice(self.xy_window))
        ip, port = self.proxy_get()
        option.add_argument('--proxy-server={}:{}'.format(ip, port))
        # 开启实验性功能参数，去除提示，防止检测
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 无效
        option.add_experimental_option('useAutomationExtension', False)
        # 就是这一行告诉chrome去掉了webdriver痕迹
        option.add_argument("disable-blink-features=AutomationControlled")
        option.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        # 生成浏览器对象
        self.bro = webdriver.Chrome(options=option)
        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #   "source": """
        #     Object.defineProperty(navigator, 'webdriver', {
        #       get: () => undefined
        #     })
        #   """
        # })
        # 发起请求
        # self.bro.get('https://qiye.trustexporter.com/ganguojianguo/')
        # self.bro.get('https://httpbin.org/ip')

    # 根据页码获取url地址
    def get_page(self, start_page, end_page, page_url):
        # 设置循环页数
        for pn in range(start_page, end_page):
            sleep(rd.randint(1, 6))
            # 获取页数
            print('获取第%s页' % pn)
            # 拼接网页
            base_url = page_url + '-{}.html'.format(pn)
            self.bro.get(page_url)
            page_text = self.bro.page_source
            # 解析网页
            html = etree.HTML(page_text)
            # 获取网页中的企业网址和主营产品数据
            div_list = html.xpath('//div[@class="Com_Library_R"]')
            if div_list:
                for div in div_list:
                    msg = ''
                    href = div.xpath('./div[@class="Caption"]/div[1]/a/@href')[0]
                    name = div.xpath('./div[@class="Caption"]/div[1]/a/text()')[0]
                    a_list = div.xpath('./div[@class="Matter"]/a')
                    for a in a_list:
                        msg = msg + a.xpath('./text()')[0] + ' '
                    # print(msg)
                    # dic['网址'] = str(href).strip('\n')
                    # dic['公司名称'] = str(name).strip(' \n')
                    # dic['主营产品'] = str(msg).strip('\n')
                    dic = {
                        '网址': href,
                        '公司名称': name,
                        '主营产品': msg
                    }
                    self.company_dic_list.append(dic)

    # 获取详细信息
    def get_data(self, dic, data_list):
        for data in data_list:
            # 获取具体信息数据，赋值到字典中
            if '联系人' in data:
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

    # 自动输入
    def automatic_ly(self):
        # 自动输入文字, 每次输入随机间隔
        sleep(rd.randint(1, 3))
        lianxiren_ele = self.bro.find_element_by_id('ctl00_Liuyan_txtInputer')
        xing = rd.choice(xing_list)
        ming = rd.choice(ming_list)
        xm = xing + ming
        lianxiren_ele.send_keys(xm)
        sleep(rd.randint(1, 3))
        phone_ele = self.bro.find_element_by_id('ctl00_Liuyan_txtTelephone')
        # 填入信息，手机号
        phone = '1%s%s%s%s%s' % \
                (str(rd.randint(30, 88)), str(rd.randint(10, 88)),
                 str(rd.randint(10, 99)), str(rd.randint(30, 88)),
                 str(rd.randint(10, 99))
                 )
        phone_ele.send_keys(phone)
        sleep(rd.randint(1, 3))
        wechat_ele = self.bro.find_element_by_id('ctl00_Liuyan_txtWeixin')
        wechat_ele.send_keys(phone)
        sleep(rd.randint(1, 5))
        qq_ele = self.bro.find_element_by_id('ctl00_Liuyan_txtqq')
        qq = str(rd.randint(7, 88)) + str(rd.randint(10, 88)) + str(rd.randint(10, 99)) + str(
            rd.randint(30, 88)) + str(rd.randint(10, 99))
        qq_ele.send_keys(qq)

    # 弹窗处理
    def handle_popup(self, popup):
        # 异常处理
        try:
            if popup:
                sleep(1)
                # 打印警告对话框内容
                print(popup.text)
                # alert对话框属于警告对话框，我们这里只能接受弹窗
                popup.accept()
        except Exception as e:
            print(e)

    # 自动留言
    def zdly(self, type, dic):
        if type == 'vip':
            # 点击留言标签
            sleep(rd.randint(1, 3))
            a_ele = self.bro.find_element_by_xpath('//p[@class="wenziya"]/a[1]')
            # selenium的点击方式不能使用
            # a_ele.click()
            # 使用js代码点击
            self.bro.execute_script("arguments[0].click();", a_ele)
            # 操作js代码移动滑块
            self.bro.execute_script('window.scrollTo(0, window.innerHeight)')
            self.automatic_ly()
            # 点击提交按钮，提交留言
            sleep(rd.randint(1, 3))
            sumbit_ele = self.bro.find_element_by_id('ctl00_Liuyan_btnSubmit')
            # sumbit_ele.click()
            self.bro.execute_script("arguments[0].click();", sumbit_ele)
            sleep(rd.randint(1, 3))
            # 弹窗信息获取alert对话框
            dig_alert = self.bro.switch_to.alert
            self.handle_popup(dig_alert)
            ly_page_text = self.bro.page_source
            ly_html = etree.HTML(ly_page_text)
            p_list = ly_html.xpath('//div[@class="lxleft"]/p')
            if p_list:
                # 未完成提交留言成功后的点击动作，未找到按钮
                self.save_data(dic)
                print(dic)
                # for p in p_list:

        elif type == 'lxbod':
            span = self.bro.find_element_by_xpath('//*[@id="ctl00_contact_lblLinkman"]/a')
            # span.click()
            self.bro.execute_script("arguments[0].click();", span)
            sleep(rd.randint(1, 3))
            # 操作js代码移动滑块
            self.bro.execute_script('window.scrollTo(0, window.innerHeight)')
            # 自动输入文字信息
            self.automatic_ly()
            # 点击提交按钮，提交留言
            sleep(rd.randint(1, 3))
            sumbit_ele = self.bro.find_element_by_id('ctl00_Liuyan_btnSubmit')
            # sumbit_ele.click()
            self.bro.execute_script("arguments[0].click();", sumbit_ele)
            sleep(rd.randint(2, 5))
            # 弹窗信息获取alert对话框
            dig_alert = self.bro.switch_to.alert
            self.handle_popup(dig_alert)
            but_ele = self.bro.find_element_by_id('ctl00_Liuyan_Button2')
            sleep(rd.randint(1, 3))
            self.bro.execute_script("arguments[0].click();", but_ele)
            # 等待网页加载，获取信息
            sleep(3)
            ly_html = etree.HTML(self.bro.page_source)
            div_ly = ly_html.xpath('//div[@id="ctl00_contact_youliuyan"]')
            data1_list = div_ly[0].xpath('.//text()')
            self.get_data(dic, data1_list)
            self.save_data(dic)

    # 企业详情页
    def data_company(self):
        # 获取企业详情页
        for dic in self.company_dic_list:
            self.bro.get(dic.get('网址'))
            page_text = self.bro.page_source
            # 解析网页
            html = etree.HTML(page_text)
            # 判断网页类型
            div_vip = html.xpath('//div[@class="cecec"]')
            # 判断是否需要留言
            if div_vip:
                # 滑动到留言区域
                sleep(rd.randint(1, 3))
                self.bro.execute_script('window.scrollTo(0, 2*window.innerHeight)')
                # 查找提交留言的标签，点击留言
                a_ele = div_vip[0].xpath('./p/a/font')
                if a_ele:
                    msg = 'vip'
                    self.zdly(msg, dic)
                    continue
                data_list = div_vip[0].xpath('./p//text()')
                # print(data_list)
                self.get_data(dic, data_list)
                self.save_data(dic)
                continue
            # 判断网页是否需要留言
            div = html.xpath('//div[@id="ctl00_contact_meiliuyan"]')
            div_show = html.xpath('//div[@id="ctl00_contact_youliuyan"]')
            # print('div',div)
            if div:
                # 滑动到留言区域
                sleep(rd.randint(1, 3))
                self.bro.execute_script('window.scrollTo(0, 2*window.innerHeight)')
                msg = 'lxbod'
                self.zdly(msg, dic)

            elif div_show:
                # 滑动到留言区域
                sleep(rd.randint(1, 2))
                self.bro.execute_script('window.scrollTo(0, 2*window.innerHeight)')
                data1_list = div_show[0].xpath('.//text()')
                self.get_data(dic, data1_list)
                self.save_data(dic)

    # 数据库保存
    def save_data(self, dic):
        try:
            # sql语句
            sql1 = """
                insert into sudongshipin (lianxiren, phone, telephone, company, produce, address, href) values (%s, %s, %s, %s, %s, %s, %s);
                """
            self.cur.execute(sql1, (
                str(dic.get('联系人')) if str(dic.get('联系人')) else '', str(dic.get('手机')) if str(dic.get('手机')) else '',
                str(dic.get('电话')) if str(dic.get('电话')) else '', str(dic.get('公司名称')) if str(dic.get('公司名称')) else '',
                str(dic.get('主营产品')) if str(dic.get('主营产品')) else '', str(dic.get('地址')) if str(dic.get('地址')) else '',
                str(dic.get('网址')) if str(dic.get('网址')) else ''))
            self.conn.commit()
            print('保存成功', dic.get('网址'))
        except Exception as e:
            print(e)

    # 关闭
    def __del__(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    # 姓名列表
    xing_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云'
    ]
    ming_list = [
        '涛', '昌进', '林', '有', '坚', '邦', '承', '乐', '绍功', '松', '善', '厚', '庆', '磊', '民', '友裕',
        '河', '哲', '江', '浩', '亮', '政', '谦', '旭', '鹏泽', '晨', '辰士', '以', '建', '致树', '炎', '德', '行'
    ]
    # 浏览器宽度
    xy_window = [
        '1024,768',
        '1366,768',
        '1920,1080',
        '800,600'
    ]
    HB = HuoBaoShiCai(xing_list, ming_list, xy_window)
    url = 'http://www.1588.tv/company/diqu_beijing'
    HB.get_page(1, 8, page_url=url)
    HB()
