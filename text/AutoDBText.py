import pymysql



class AutoDBText:

    # 数据库连接
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            db='qiyangdata',
            user='root',
            password='root',
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
            if table != 'ziyouname':
                self.table_list.append(table)


auto_db = AutoDBText()
auto_db.auto_data()