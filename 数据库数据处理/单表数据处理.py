import pymysql


class AutoDB:
    # 数据库连接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='58shipin',
            user='root',
            password='97655',
            charset='utf8'
        )
        print('链接数据库')
        # 游标
        self.cursor = self.conn.cursor()
        # self.table_list = ['shanghai', 'zhengzhou', 'chongqing']
        self.table_list = []

    # 数据库自动化操作
    # 1 查找库中所有表名称
    def auto_data(self):
        sql = 'show tables;'
        self.cursor.execute(sql)
        # 获取查询结果
        # print(self.cursor.fetchmany())  # (('danlei',),)
        # print(self.cursor.fetchone())  # ('danlei',)
        # print(self.cursor.fetchall(), type(self.cursor.fetchall()))
        # (('danlei',), ('shandong_shiyongyou',), ('shipin',)) <class 'tuple'>
        # 将获取的数据库名放入列表中
        data_tuple = self.cursor.fetchall()
        for data in data_tuple:
            table = data[0]
            if table == 'shipinpeiliao2':
                self.table_list.append(table)

    # 2 数据库数据处理,数据库语句
    def process(self):
        # 删除表中重复的数据，以公司名称分组
        for table_name in self.table_list:
            print('更新表： %s 数据' % table_name)
            sql = """
            DELETE FROM %s WHERE href IN
             (SELECT href FROM (SELECT href FROM %s GROUP BY href HAVING COUNT(href)>1) e)
             AND Id NOT IN 
             (SELECT Id FROM (SELECT MIN(Id) AS Id FROM %s GROUP BY href HAVING COUNT(href)>1) t);
            """ % (table_name, table_name, table_name)
            self.cursor.execute(sql)
            # 删除表中手机号为空的数据
            sql_phone = """
            DELETE FROM %s where id in 
            (SELECT id from (SELECT * from %s WHERE phone='' and telephone='') t);
                      """ % (table_name, table_name)
            self.cursor.execute(sql_phone)
            # # 删除主营产品为空的记录
            sql_is_produce = """
            DELETE from {} where id in 
            (SELECT id FROM (SELECT * from {} WHERE produce='主营：') t);""".format(table_name, table_name)
            self.cursor.execute(sql_is_produce)
            self.conn.commit()
            # sql_produce = """
            # DELETE from {} where id in
            # (SELECT id FROM (SELECT * from {} WHERE produce='主营产品： 销售：') t);""".format(table_name, table_name)
            # self.cursor.execute(sql_produce)

            self.conn.commit()

            # 数据处理
            # 处理公司名称中的记录
            del_company_list = [
                '%起重%', '%兽药%', '%电子科技%',
                '%展览%', '%物业%', '%宠物%',
                '%科技发展%', '%文化%', '%药业%',
                '%医药%', '%软件%', '%种业%',
                '%秸秆%', '%动物%', '%策划%',
                '%生物工程%', '%早点%', '配件',
                '%美容%', '%医学%', '%摄影%',
                '%网络%', '%日用品%', '%医疗%',
                '%木材%', '%咨询%', '%水站%',
                '%家政%', '%时尚%', '%化妆品%',
                '%茶%', '%制药%', '%信息科技%',
                '%量贩%', '%烟酒%', '%印刷%',
                '%桶装水%', '%评估%', '%书店%',
                '%车辆%', '%中学%', '%配件%',
                '%认证%', '%渔具%', '%机床%',
                '%中药%', '%电器%', '%锦鲤%',
                '%孕安%', '%进出口%', '%会展%',
                '%酒%', '%广告%', '%娱乐%',
                '%货运%', '%玻璃%', '%207%',
                '%纸业%', '%工作站%', '%模具%',
            ]
            for data in del_company_list:
                sql_company = """DELETE FROM {} where id in
                            (SELECT id from (SELECT * FROM {} WHERE company like %s) e);""".format(table_name, table_name)
                self.cursor.execute(sql_company, data)
                self.conn.commit()

            # 根据主营产品相关处理库中的所有记录
            del_produce_list = [
                '%提升%', '%礼品%', '%化肥%',
                '%化妆%', '%塑料%', '%医药%',
                '%化工%', '%电动%', '%电子%',
                '%物流%', '%展览%', '%展会%',
                '%茶叶%', '%咖啡%', '%兽药%',
                '%胶囊%', '%藻粉%', '%工艺品%',
                '%螺旋藻%', '%普洱茶%', '%白酒%',
                '%葡萄酒%', '%羊绒%', '%厂房%',
                '%玩具%', '%木珠%', '%建筑%',
                '%汽车%', '%日用%', '%服装%',
                '%文具%', '%体育%', '%饲料%',
                '%贸易%', '%房地产%', '%激光%',
                '%住宿%', '%农药%', '%装备%',
                '%信息服务%', '%em%', '%铜%',
                '%铝%', '%锌%', '%种子%',
                '%剂%', '%禽药%', '%家电%',
                '%技术咨询%', '%FD%', '%网络%',
                '%服饰%', '%商贸%', '%石墨%',
                '%自动化%', '%面膜%', '%水晶%',
                '%日用品%', '%复合肥%', '%小吃车%',
                '%技术开发%', '%轮胎%', '%软件%',
                '%笔记本%', '%石油%', '%美容%',
                '%医疗%', '%虹膜%', '%沐浴%',
                '%安利%', '%衣服%', '%粉粉%',
                '%桶装%', '%纯净水%', '%项目%',
                '%祛斑%', '%肌肤%', '%多肽%',
                '%口服液%', '%安全套%', '%相机%',
                '%观赏%', '%黄沙%', '%钢材%',
                '%五金%', '%u%', '%手机%',
                '%宠物%', '%宣传推广%', '%VIP%',
                '%药材%', '%飞机%', '%系统%',
                '%印刷%', '%瓶盖%', '%电器%',
                '%运输带%', '%搅拌机%', '%矿泉水%',
                '%浪漫%', '%阀%', '%咨询%',
                '%阿胶%', '%香香%', '%网友%',
                '%种植%', '%装修%', '%网友%',
            ]
            for detail in del_produce_list:
                sql_produce = """DELETE FROM {} where id in
                (SELECT id from (SELECT * FROM {} WHERE produce like %s) e);""".format(table_name, table_name)
                self.cursor.execute(sql_produce, detail)
                self.conn.commit()

    # 关闭数据库
    def __del__(self):

        print('关闭数据库')
        self.cursor.close()
        self.conn.close()


auto_db = AutoDB()
auto_db.auto_data()
auto_db.process()

"""
休闲食品
冻品干鲜
食品配料

"""