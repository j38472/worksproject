import pymysql


class AutoDB:
    # 数据库连接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='shunqi',
            user='root',
            password='97655',
            charset='utf8'
        )
        print('链接数据库')
        # 游标
        self.cursor = self.conn.cursor()
        self.table_list = ['shanghai', 'zhengzhou', 'chongqing']

    # 数据库自动化操作
    # 1 查找库中所有表名称
    # def auto_data(self):
    #     sql = 'show tables;'
    #     self.cursor.execute(sql)
    #     # 获取查询结果
    #     # print(self.cursor.fetchmany())  # (('danlei',),)
    #     # print(self.cursor.fetchone())  # ('danlei',)
    #     # print(self.cursor.fetchall(), type(self.cursor.fetchall()))
    #     # (('danlei',), ('shandong_shiyongyou',), ('shipin',)) <class 'tuple'>
    #     # 将获取的数据库名放入列表中
    #     data_tuple = self.cursor.fetchall()
    #     for data in data_tuple:
    #         table = data[0]
    #         # data = str(data).split("'")[1]
    #         # print(data, type(data))  # ('danlei',) <class 'tuple'>
    #         # print(table, type(table))
    #         self.table_list.append(table)

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
            (SELECT id FROM (SELECT * from {} WHERE produce is null) t);""".format(table_name, table_name)
            self.cursor.execute(sql_is_produce)

            self.conn.commit()

            # 数据处理
            # 处理公司名称中的记录
            del_company_list = [
                '%起重%', '%兽药%', '%电子科技%',
                '%展览%', '%物业%', '%宠物%',
                '%科技发展%', '%文化%', '%管理%',
                '%摊%', '%医药%', '%软件%',
                '%店%', '%坊%', '%点%',
                '%种业%', '%笔%', '%秸秆%',
                '%馆%', '%动物%', '%生物工程%',
                '%社%', '%户%', '%%',
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
                '%信息服务%', '%苗%', '%铜%',
                '%铝%', '%锌%', '%养殖%',
                '%剂%', '%禽药%', '%家电%',
                '%技术咨询%', '%FD%', '%网络%',
                '%服饰%', '%商贸%', '%网络%',
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
# auto_db.auto_data()
auto_db.process()

"""
-- DELETE FROM dongpinshengxian where id in 
-- (SELECT id FROM (SELECT min(id) as id FROM dongpinshengxian GROUP BY href HAVING count(href)>1) t)
-- AND href not in 
-- (SELECT href FROM (SELECT href from dongpinshengxian GROUP BY href HAVING count(href)>1) e);
-- 
-- DELETE FROM ganxiantiaowei WHERE id in (SELECT id FROM (SELECT * from  ganxiantiaowei GROUP BY href HAVING count(href)>1) t);
-- SELECT * FROM ganxiantiaowei WHERE href='http://piaoyingh1207.58food.com/';
-- SELECT * FROM dongpinshengxian WHERE id='811';
-- SELECT * FROM dongpinshengxian WHERE name=' 纪歆德';
-- SELECT * FROM dongpinshengxian WHERE company like '%管理%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%物流%';
-- SELECT * FROM dongpinshengxian WHERE company like '%电子科技%';
-- SELECT * FROM dongpinshengxian WHERE company like '%健康%';
-- SELECT * FROM dongpinshengxian WHERE company like '%起重%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%电动%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%化工%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%医药%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%塑料%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%化妆%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%化肥%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%礼品%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%提升%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%电子%';
-- SELECT * FROM dongpinshengxian WHERE company like '%兽药%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%保健品%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%展会%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%咖啡%'；
-- SELECT * FROM dongpinshengxian WHERE company like '%物业%';
-- SELECT * FROM dongpinshengxian WHERE company like '%展览%';
-- SELECT * FROM dongpinshengxian WHERE produce like '%展览%';
-- SELECT * FROM dongpinshengxian WHERE produce='';
-- DELETE FROM shipinpeiliao where id>9251;
-- 
-- DELETE FROM dongpinshengxian where id in 
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%提升%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%礼品%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%化肥%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%化妆%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%塑料%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%医药%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%化工%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%电动%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%电子%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE company like '%起重%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE company like '%兽药%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE company like '%健康%') e)
-- and not company in 
-- (SELECT company from (SELECT company FROM dongpinshengxian WHERE company like '%健康食品%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE company like '%电子科技%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%物流%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%展会%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%保健品%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce='') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%展览%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE company like '%展览%') e);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE company like '%物业%') e);
-- SELECT id from (SELECT * from dongpinshengxian WHERE phone is NULL AND telephone is NULL) t;
-- (SELECT id from (SELECT * from dongpinshengxian WHERE phone='' and telephone='') t);
-- (SELECT id from (SELECT * FROM dongpinshengxian WHERE produce like '%咖啡%') e);
"""