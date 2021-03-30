import pymysql
from lxml import etree
import requests
import re


class ShunQi:

    # 数据库链接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='97655',
            db='bafang',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
        }
        self.company_list = []

    # 关闭数据库
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # # 获取表名
    # def get_table(self, url):
    #     response = requests.get(url=url, headers=self.headers)
    #     print(response.status_code)
    #     pages_text = response.text
    #     html = etree.HTML(pages_text)
    #
    #     # 查找数据
    #     a_list = html.xpath('//div[@class="classify-food-detial"]/a')
    #     print(a_list)
    #     for a in a_list:
    #         href = a.xpath('./@href')[0]
    #         print(href)

    # 创建表
    def creat_table(self):
        for url in url_list:
            table = url.split('/')[2]
            try:
                sql = """
                    CREATE TABLE %s (
                      `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
                      `company` varchar(64) NULL COMMENT '公司名称',
                      `produce` varchar(512) NULL COMMENT '主营产品',
                      `name` varchar(32) NULL COMMENT '联系人',
                      `phone` varchar(32) NULL COMMENT '手机',
                      `telephone` varchar(64) NULL COMMENT '电话',
                      `address` varchar(255) NULL COMMENT '地址',
                      `href` varchar(255) NULL COMMENT '网址',
                      PRIMARY KEY (`id`)
                    );
                    """ % table
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)


    # def save_data(self, dic):
    #     try:
    #         # 获取数据库表名
    #         table = url.split('/')[-1]
    #         print(table)
    #         # sql语句
    #         # 保存数据值和表字段不对称，需要加上对应的字段名
    #         sql1 = """
    #             insert into {} (company, produce, name, phone, telephone, address, href) values (%s, %s, %s, %s, %s, %s, %s);
    #                        """.format(table)
    #         self.cursor.execute(sql1, (
    #             str(dic.get('company')) if dic.get('company') else '',
    #             str(dic.get('produce')) if dic.get('produce') else '',
    #             # str(dic.get('company_type')) if dic.get('company_type') else '',
    #             str(dic.get('name')) if dic.get('name') else '',
    #             str(dic.get('phone')) if dic.get('phone') else '',
    #             str(dic.get('telephone')) if dic.get('telephone') else '',
    #             str(dic.get('address')) if dic.get('address') else '',
    #             str(dic.get('href')) if dic.get('href') else ''
    #         ))
    #         self.conn.commit()
    #         print('%s保存成功' % dic.get('company'))
    #     except Exception as e:
    #         print(e)
    #         self.conn.rollback()


url_list = [
    '/shipin/youjishipin/youjichuqinchanpin/',
    '/shipin/youjishipin/youjishuichanpin/',
    '/shipin/youjishipin/youjishiyongjunchanpin/',
    '/shipin/youjishipin/youjinongchanpin/',
    '/shipin/youjishipin/youjinaizhipin/',
    '/shipin/youjishipin/youjifengchanpin/',
    '/shipin/tangjiu/tangjiang/',
    '/shipin/tangjiu/tangguo/',
    '/shipin/tangjiu/shatang/',
    '/shipin/tangjiu/mianbaitang/',
    '/shipin/tangjiu/hongtang/',
    '/shipin/tangjiu/fangtang/',
    '/shipin/tangjiu/bingtang/',
    '/shipin/tangjiu/baishatang/',
    '/shipin/shuiguoshucai/youjishucai/',
    '/shipin/shuiguoshucai/yecaileishucai/',
    '/shipin/shuiguoshucai/guoshulei/',
    '/shipin/shuiguoshucai/shuishengshucai/',
    '/shipin/shuiguoshucai/shiyongjun/',
    '/shipin/shuiguoshucai/qieguoshucai/',
    '/shipin/shuiguoshucai/jinkoushucai/',
    '/shipin/shuiguoshucai/huacaileishucai/',
    '/shipin/shuiguoshucai/gualeishucai/',
    '/shipin/shuiguoshucai/genjingshucai/',
    '/shipin/shuiguoshucai/ganlanleishucai/',
    '/shipin/shuiguoshucai/doujialeishucai/',
    '/shipin/shuiguoshucai/xinlashucai/',
    '/shipin/shuiguoshucai/congsuanleishucai/',
    '/shipin/shuiguoshucai/xinxianshucai/',
    '/shipin/shuiguoshucai/baicaileishucai/',
    '/shipin/shuiguoshucai/shucaizhipin/',
    '/shipin/shiyongyou/zhuyou/',
    '/shipin/shiyongyou/shiyongyou/',
    '/shipin/shiyongyou/shenhaiyuyou/',
    '/shipin/shiyongyou/niuyou/',
    '/shipin/shiyongyou/mianziyou/',
    '/shipin/shiyongyou/mayou/',
    '/shipin/shiyongyou/kuihuaziyou/',
    '/shipin/shiyongyou/huashengyou/',
    '/shipin/shiyongyou/hetaoyou/',
    '/shipin/shiyongyou/ganlanyou/',
    '/shipin/shiyongyou/dadouyou/',
    '/shipin/shiyongyou/chaziyou/',
    '/shipin/shiyongyou/caiziyou/',
    '/shipin/shipinyuanfuliao/zhuoseji/',
    '/shipin/shipinyuanfuliao/zengweiji/',
    '/shipin/shipinyuanfuliao/zengchouji/',
    '/shipin/shipinyuanfuliao/yingyangqianghuaji/',
    '/shipin/shipinyuanfuliao/xiaopaoji/',
    '/shipin/shipinyuanfuliao/wendingji/',
    '/shipin/shipinyuanfuliao/tianweiji/',
    '/shipin/shipinyuanfuliao/qitashipintianjiaji/',
    '/shipin/shipinyuanfuliao/suandudiaojieji/',
    '/shipin/shipinyuanfuliao/shuifenbaochiji/',
    '/shipin/shipinyuanfuliao/shiyongxiangjing/',
    '/shipin/shipinyuanfuliao/shipinyuanliao/',
    '/shipin/shipinyuanfuliao/shipinfuliao/',
    '/shipin/shipinyuanfuliao/ruhuaji/',
    '/shipin/shipinyuanfuliao/piaobaiji/',
    '/shipin/shipinyuanfuliao/pengsongji/',
    '/shipin/shipinyuanfuliao/mianfenchuliji/',
    '/shipin/shipinyuanfuliao/meizhiji/',
    '/shipin/shipinyuanfuliao/kangyanghuaji/',
    '/shipin/shipinyuanfuliao/kangjieji/',
    '/shipin/shipinyuanfuliao/huseji/',
    '/shipin/shipinyuanfuliao/fangfuji/',
    '/shipin/shipinyuanfuliao/beimoji/',
    '/shipin/shengxianrou/zhurou/',
    '/shipin/shengxianrou/yangrou/',
    '/shipin/shengxianrou/yarou/',
    '/shipin/shengxianrou/turou/',
    '/shipin/shengxianrou/niurou/',
    '/shipin/shengxianrou/marou/',
    '/shipin/shengxianrou/jirou/',
    '/shipin/shengxianrou/gourou/',
    '/shipin/shengxianrou/erou/',
    '/shipin/mimian/yumimian/',
    '/shipin/mimian/mian/',
    '/shipin/mimian/xiaomimian/',
    '/shipin/mimian/teshumimian/',
    '/shipin/mimian/maimi/',
    '/shipin/mimian/miantiao/',
    '/shipin/mimian/mianfen/',
    '/shipin/mimian/mixian/',
    '/shipin/mimian/mifen/',
    '/shipin/mimian/jiangmimian/',
    '/shipin/mimian/huangmimian/',
    '/shipin/mimian/heimimian/',
    '/shipin/mimian/guamian/',
    '/shipin/mimian/fensi/',
    '/shipin/mimian/fenpi/',
    '/shipin/mimian/dami/',
    '/shipin/liangshiculiang/yumi/',
    '/shipin/liangshiculiang/youjizaliang/',
    '/shipin/liangshiculiang/yanmai/',
    '/shipin/liangshiculiang/xiaomi/',
    '/shipin/liangshiculiang/xiaomai/',
    '/shipin/liangshiculiang/xiaodouhongdou/',
    '/shipin/liangshiculiang/xianmi/',
    '/shipin/liangshiculiang/liangzhipin/',
    '/shipin/liangshiculiang/qiaomai/',
    '/shipin/liangshiculiang/pimai/',
    '/shipin/liangshiculiang/nuomi/',
    '/shipin/liangshiculiang/malingshutudou/',
    '/shipin/liangshiculiang/lvdou/',
    '/shipin/liangshiculiang/jingmi/',
    '/shipin/liangshiculiang/heidou/',
    '/shipin/liangshiculiang/gaoliang/',
    '/shipin/liangshiculiang/fanshuhongshubaishu/',
    '/shipin/liangshiculiang/damai/',
    '/shipin/liangshiculiang/dadouhuangdou/',
    '/shipin/jiagongshipin/jiangyancai/',
    '/shipin/jiagongshipin/xiuxianshipin/',
    '/shipin/jiagongshipin/qitashipin/',
    '/shipin/jiagongshipin/teshujiagongshipin/',
    '/shipin/jiagongshipin/teseshipin/',
    '/shipin/jiagongshipin/sudongshipin/',
    '/shipin/jiagongshipin/shipintiquwu/',
    '/shipin/jiagongshipin/ruzhipin/',
    '/shipin/jiagongshipin/rouzhipin/',
    '/shipin/jiagongshipin/qingzhenshipin/',
    '/shipin/jiagongshipin/mimianlei/',
    '/shipin/jiagongshipin/jinkoujiagongshipin/',
    '/shipin/jiagongshipin/shiyongjunguantou/',
    '/shipin/jiagongshipin/ganguojianguo/',
    '/shipin/jiagongshipin/fangbianshipin/',
    '/shipin/jiagongshipin/douzhipin/',
    '/shipin/jiagongshipin/danzhipin/',
    '/shipin/jiagongshipin/chongwushipin/',
    '/shipin/jiagongshipin/beikaoshipin/',
    '/shipin/jiagongshipin/baojianshipin/',
    '/shipin/xuqinshuichanpin/zhu/',
    '/shipin/xuqinshuichanpin/youjixuqin/',
    '/shipin/xuqinshuichanpin/youjishuichanpin/',
    '/shipin/xuqinshuichanpin/ya/',
    '/shipin/xuqinshuichanpin/tuzi/',
    '/shipin/xuqinshuichanpin/shuichanpin/',
    '/shipin/xuqinshuichanpin/shiyongyu/',
    '/shipin/xuqinshuichanpin/shiyongxie/',
    '/shipin/xuqinshuichanpin/shiyongxia/',
    '/shipin/xuqinshuichanpin/shiyongbie/',
    '/shipin/xuqinshuichanpin/shiyongbei/',
    '/shipin/xuqinshuichanpin/ji/',
    '/shipin/xuqinshuichanpin/e/',
    '/shipin/xuqinshuichanpin/danlei/',
    '/shipin/tiaoweipin/zhimayou/',
    '/shipin/tiaoweipin/zhimajianghuashengjiang/',
    '/shipin/tiaoweipin/yanliao/',
    '/shipin/tiaoweipin/xiangxinliao/',
    '/shipin/tiaoweipin/weijingjijing/',
    '/shipin/tiaoweipin/tiaoweipin/',
    '/shipin/tiaoweipin/tangliao/',
    '/shipin/tiaoweipin/shiyan/',
    '/shipin/tiaoweipin/shicu/',
    '/shipin/tiaoweipin/liaojiuhuangjiu/',
    '/shipin/tiaoweipin/jinkoutiaoweipin/',
    '/shipin/tiaoweipin/jiangyou/',
    '/shipin/tiaoweipin/jiangcai/',
    '/shipin/tiaoweipin/jijing/',
    '/shipin/tiaoweipin/huoguoliao/',
    '/shipin/tiaoweipin/guojiang/',
    '/shipin/tiaoweipin/fuhetiaoweipin/',
    '/shipin/tiaoweipin/dunbaoxilie/',
    '/shipin/tiaoweipin/tiaoweizhi/',
    '/shipin/tiaoweipin/tiaoweiyou/',
    '/shipin/tiaoweipin/tiaoweixiangliao/',
    '/shipin/tiaoweipin/tiaoweijiang/',
    '/shipin/tiaoweipin/tiaoweifen/',
    '/shipin/tiaoweipin/dianfen/',
]

creat = ShunQi()
creat.creat_table()



