import pymysql


class AutoDB:
    # 数据库连接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='huangye882',
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

    # 2 数据库数据处理
    def process(self):
        # 删除表中重复的数据，以公司名称分组
        for table_name in self.table_list:
            print('更新表： %s 数据: ' % table_name)
            sql = """
            DELETE FROM %s WHERE company IN
             (SELECT company FROM (SELECT company FROM %s GROUP BY company HAVING COUNT(company)>1) e)
             AND Id NOT IN 
             (SELECT Id FROM (SELECT MIN(Id) AS Id FROM %s GROUP BY company HAVING COUNT(company)>1) t);
            """ % (table_name, table_name, table_name)
            self.cursor.execute(sql)

            # 删除表中手机号为空的数据
            sql1 = """
            DELETE FROM %s where id in 
            (SELECT id from (SELECT * from %s WHERE phone='' and telephone='') t);
                      """ % (table_name, table_name)
            self.cursor.execute(sql1)
            # 删除多表中无用重复的企业
            sql2 = """
            DELETE FROM %s where lianxiren in ('大树', '陈义华', '续永辉经理', '周菊跳', '李慧', '方鑫 经理');
            """ % table_name
            self.cursor.execute(sql2)
            sql3 = """
            DELETE FROM %s where telephone='86-0755-81809079'; 
            """ % table_name
            self.cursor.execute(sql3)

            # # 删除银行等于食品企业无关的相关企业
            sql4 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%银行%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4)
            sql4_1 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%管理%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_1)
            sql4_2 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%婴儿用品%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_2)
            sql4_3 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%电子%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_3)
            sql4_4 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%木材加工%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_4)
            sql4_5 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%塑胶%' ) t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_5)
            sql4_6 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%塑料%' ) t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_6)
            sql4_7 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%皮毛%' ) t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_7)
            sql4_8 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%轮胎%' ) t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_8)
            sql4_9 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%服饰%' ) t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_9)
            sql4_10 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%服饰%' ) t);
            """.format(table_name, table_name)
            self.cursor.execute(sql4_10)
            sql5 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%设备%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5)
            sql5_1 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%工艺品%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_1)
            sql5_2 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%服饰%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_2)
            sql5_3 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%灌装%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_3)
            sql5_4 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%玉%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_4)
            sql5_5 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%五金%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_5)
            sql5_6 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%标签%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_6)
            sql5_7 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%试验台%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_7)
            sql5_8 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%灯%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_8)
            sql5_9 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%液化%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_9)
            sql5_10 = """
            DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%液态%') t);
            """.format(table_name, table_name)
            self.cursor.execute(sql5_10)

            sql6_1 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%设备%') t);
                        """.format(table_name, table_name)
            self.cursor.execute(sql6_1)

            sql6_2 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%液化气%') t);
                      """.format(table_name, table_name)
            self.cursor.execute(sql6_2)

            sql6_3 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%瓶盖%') t);
                        """.format(table_name, table_name)
            self.cursor.execute(sql6_3)

            sql6_4 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%塑料%') t);
                        """.format(table_name, table_name)
            self.cursor.execute(sql6_4)

            sql6_5 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%内衣%') t);
                        """.format(table_name, table_name)
            self.cursor.execute(sql6_5)

            sql6_6 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%机械%') t);
                        """.format(table_name, table_name)
            self.cursor.execute(sql6_6)

            sql6_7 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%机械%') t);
                                    """.format(table_name, table_name)
            self.cursor.execute(sql6_7)

            sql6_8 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%百货%') t);
                                    """.format(table_name, table_name)
            self.cursor.execute(sql6_8)

            sql6_9 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%饲料%') t);
                                    """.format(table_name, table_name)
            self.cursor.execute(sql6_9)

            sql7_1 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%漆%') t);
                                    """.format(table_name, table_name)
            self.cursor.execute(sql7_1)

            sql7_2 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%泵%') t);
                                    """.format(table_name, table_name)
            self.cursor.execute(sql7_2)

            sql7_3 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%配件%') t);
                                    """.format(table_name, table_name)
            self.cursor.execute(sql7_3)
            sql7_4 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%教育%') t);""".format(table_name, table_name)
            self.cursor.execute(sql7_4)
            sql7_5 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%教育%') t);""".format(table_name, table_name)
            self.cursor.execute(sql7_5)
            sql7_6 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%混凝土%') t);""".format(table_name, table_name)
            self.cursor.execute(sql7_6)
            sql7_7 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%报表%') t);""".format(table_name, table_name)
            self.cursor.execute(sql7_7)
            sql7_8 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%出租%') t);""".format(table_name, table_name)
            self.cursor.execute(sql7_8)
            sql7_9 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%金属%') t);""".format(table_name, table_name)
            self.cursor.execute(sql7_9)
            sql8_1 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%机动%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_1)
            sql8_2 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%汽车%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_2)
            sql8_3 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%服装%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_3)
            sql8_4 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%广告%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_4)
            sql8_5 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%广告%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_5)
            sql8_6 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%加工%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_6)
            sql8_7 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%邮政%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_7)
            sql8_8 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%兽%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_8)
            sql8_9 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%化学%') t);""".format(table_name, table_name)
            self.cursor.execute(sql8_9)
            sql9_1 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%日用品%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_1)
            sql9_2 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%开发%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_2)
            sql9_3 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%未分类%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_3)
            sql9_4 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%文化%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_4)
            sql9_5 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%原煤%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_5)
            sql9_6 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%生产技术%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_6)
            sql9_7 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%输送%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_7)
            sql9_8 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%系统%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_8)
            sql9_9 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%水泥%') t);""".format(table_name, table_name)
            self.cursor.execute(sql9_9)
            sql10_1 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%科技%') t);""".format(table_name, table_name)
            self.cursor.execute(sql10_1)
            sql10_2 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where company like '%自动化%') t);""".format(table_name, table_name)
            self.cursor.execute(sql10_2)
            sql10_3 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} where produce like '%器材%') t);""".format(table_name, table_name)
            self.cursor.execute(sql10_3)
            # 删除主营产品为空或无效信息
            sql10_4 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} WHERE produce='主营产品：') t);""".format(table_name, table_name)
            self.cursor.execute(sql10_4)
            sql10_5 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} WHERE produce='主营>产品：') t);""".format(table_name, table_name)
            self.cursor.execute(sql10_5)
            sql10_6 = """DELETE from {} where id in (SELECT id FROM (SELECT * from {} WHERE produce is null) t);""".format(table_name, table_name)
            self.cursor.execute(sql10_6)

            # print(self.cursor.fetchall())

    # 关闭数据库
    def __del__(self):
        self.conn.commit()
        print('关闭数据库')
        self.cursor.close()
        self.conn.close()


auto_db = AutoDB()
auto_db.auto_data()
auto_db.process()