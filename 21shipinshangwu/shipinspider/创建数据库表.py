import pymysql

name_list = [
    'xiuxianshipin',
    'yinliao',
    'baojianpin',
    'fangbianshipin',
    'ruzhipin',
    'chaye',
    'guantou',
    'chongtiaoyinpin',
    'penghuashipin'
    'danzhipin',
    'yingyouershipin',
    'lingyin',
]

conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='97655',  # 密码是字符串形式
                db='21shipinwang',
                charset='utf8'
    )
cursor = conn.cursor()
for db_name in name_list:
    sql = """
    CREATE TABLE %s (
      `id` int NOT NULL AUTO_INCREMENT COMMENT '编号',
      `company` varchar(64) NULL COMMENT '公司名称',
      `produce` varchar(512) NULL COMMENT '主营产品',
      `company_type` varchar(32) NULL COMMENT '经营类型',
      `name` varchar(32) NULL COMMENT '联系人',
      `phone` varchar(32) NULL COMMENT '手机',
      `telephone` varchar(64) NULL COMMENT '电话',
      `address` varchar(255) NULL COMMENT '地址',
      `href` varchar(255) NULL COMMENT '网址',
      PRIMARY KEY (`id`)
    );
    """ % db_name
    cursor.execute(sql)
    conn.commit()

cursor.close()
conn.close()