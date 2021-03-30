import pymysql


class AutoDB:
    # 数据库连接
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='huangye88',
            user='root',
            password='97655',
            charset='utf8'
        )
        print('链接数据库')
        # 游标
        self.cursor = self.conn.cursor()
        self.table_list = []

    # 数据库自动化操作
    # 查找库中所有表名称
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

    # 数据库数据处理
    def process(self):
        # 删除表中重复的数据，以公司名称分组
        sql = """
        DELETE FROM gansu_shuiguoshucai WHERE company IN
(SELECT company FROM (SELECT company FROM gansu_shuiguoshucai GROUP BY company HAVING COUNT(company)>1) e)
AND Id NOT IN 
(SELECT Id FROM (SELECT MIN(Id) AS Id FROM gansu_shuiguoshucai GROUP BY company HAVING COUNT(company)>1) t);
        """
        self.cursor.execute(sql)
        # 删除表中无用数据
        sql1 = """
        DELETE FROM gansu_shuiguoshucai where id in 
(SELECT id from (SELECT * from gansu_shuiguoshucai WHERE phone='' and telephone='') t);
"""

        self.cursor.execute(sql1)
        # 删除多表中无用的企业
        sql2 = """
        DELETE FROM gansu_shuiguoshucai where lianxiren in ('大树', '陈义华', '续永辉经理', '周菊跳', '李慧', '方鑫 经理');
        """
        self.cursor.execute(sql2)
        sql3 = """
        DELETE FROM gansu_shuiguoshucai where telephone='86-0755-81809079'; 
        """
        self.cursor.execute(sql3)
        # print(self.cursor.fetchall())
        self.conn.commit()

    # 关闭数据库
    def __del__(self):
        print('关闭数据库库')
        self.cursor.close()
        self.conn.close()


auto_db = AutoDB()
auto_db.auto_data()
auto_db.process()