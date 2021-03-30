import pymysql


class AutoDB:
    # 数据库连接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='21shuju',
            user='root',
            password='97655',
            charset='utf8'
        )
        print('链接数据库')
        # 游标
        self.cursor = self.conn.cursor()
        self.table_list = []

    # 数据库自动化操作
    # 1 查找库中所有表名称
    def auto_data(self):
        sql = 'show tables;'
        self.cursor.execute(sql)
        # 获取查询结果
        # print(self.cursor.fetchmany())  # (('danlei',),)
        # print(self.cursor.fetchone())  # ('danlei',)
        # print(self.cursor.fetchall(), type(self.cursor.fetchall()))  # (('danlei',), ('shandong_shiyongyou',), ('shipin',)) <class 'tuple'>

        # 将获取的数据库名放入列表中
        data_tuple = self.cursor.fetchall()
        for data in data_tuple:
            table = data[0]
            # data = str(data).split("'")[1]
            # print(data, type(data))  # ('danlei',) <class 'tuple'>
            # print(table, type(table))
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
            sql1 = """
            DELETE FROM %s where id in 
            (SELECT id from (SELECT * from %s WHERE phone='' and telephone='') t);
                      """ % (table_name, table_name)
            self.cursor.execute(sql1)

            # 删除多表中无用重复的企业
            sql9_1 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%机电%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_1)
            sql9_2 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%机械%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_2)
            sql9_3 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%自动化%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_3)
            sql9_4 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%提取物%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_4)
            sql9_5 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company_type='商业服务') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_5)
            sql9_6 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%信息技术%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_6)
            sql9_7 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%袋%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_7)
            sql9_8 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%铁%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_8)
            sql9_8 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%铁%') t);""".format(
                table_name, table_name)
            self.cursor.execute(sql9_8)
            self.conn.commit()

    # 关闭数据库
    def __del__(self):

        print('关闭数据库')
        self.cursor.close()
        self.conn.close()


auto_db = AutoDB()
auto_db.auto_data()
auto_db.process()