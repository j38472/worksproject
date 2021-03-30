# 数据库手机号码处理

import pymysql
import re
import time

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    db='bafangdata',
    user='root',
    password='root ',
    charset='utf8'
)
cursor = conn.cursor()

# 查询表名
table_name_list = []
sql_table = "show tables;"
cursor.execute(sql_table)
# 将获取的数据库名放入列表中
data_tuple = cursor.fetchall()
for data in data_tuple:
    table = data[0]
    if (table != 'ziyouname'):
        table_name_list.append(table)

for table_name in table_name_list:
    # 查询表的最大值
    # sql1 = "SELECT max(id) from {};".format(table_name)
    sql1 = "SELECT max(id) from {};".format(table_name)
    # 从备份中导入的数据格式都是varchar（255），字符类型不同，可以在max函数中+0解决
    cursor.execute(sql1)

    data = cursor.fetchone()
    if not data[0]:
        continue
    data = int(data[0])
    # print(int(data))
    print('表{}更新'.format(table_name))
    start_time = time.time()
    for d in range(1, int(data) + 1):
        # 查询语句
        sql = "SELECT phone, telephone, address from {} where id={};".format(table_name, str(d))
        # sql = "SELECT phone, telephone, address from ganxiantiaowei where id='1451';"
        res = cursor.execute(sql)
        # print(res)
        if res == 0:
            continue
        # msg = cursor.fetchall()
        msg = cursor.fetchone()
        # print(msg)
        phone = msg[0]
        if phone:
            # 数据处理
            phone = phone.replace('+', '').lstrip('86-')
            # 判断长度
            if len(phone) == 11:
                phone_str = re.findall(r'^[1][3,5,6,7,8,9][0-9]\d{8}$', phone)
                phone = phone_str[0] if phone_str else ''
            elif len(phone) < 11:
                phone = ''
            elif len(phone) > 11:
                # if len(phone) == 12:
                # 双号码类型的数据
                if phone[0] == '0':
                    phone_data1 = re.findall(r'[1][3,5,6,7,8,9][0-9]\d{8}$', phone)
                    phone = phone_data1[0] if phone_data1 else ''
                else:
                    phone_data2 = re.findall(r'^[1][3,5,6,7,8,9][0-9]\d{8}', phone)
                    phone = phone_data2[0] if phone_data2 else ''
                    # 手机号带有0的数据
            # print(phone)
        telephone = msg[1]
        # print(telephone)
        telephone_z = ''
        address = msg[2]
        if telephone:
            # 将字符串处理成相似的格式
            telephone = telephone.replace(' ', '-').replace(")", "-").replace('+', '').replace('—', '').lstrip('86-')
            # 判断字符长度
            if len(telephone) < 10:
                telephone = ''
            elif len(telephone) > 13:
                data = re.findall(r'[0]\d{2,3}-[0,2,3,4,5,6,7,8,9]\d{6,7}|[0]\d{2,3}[1-9]\d{6,7}', telephone)
                telephone = data[0] if data else ''
            elif telephone[0] != '0':
                telephone = ''
            # 电话号码区号设置
            elif '-' not in telephone:
                for i in ['北京', '天津', '上海', '重庆', '沈阳', '成都']:
                    if i in address:
                        telephone_z = telephone[:3] + '-' + telephone[3:]
                telephone = telephone[:4] + '-' + telephone[4:]
            # elif '—' in telephone:
            #     telephone = telephone.replace('—', '')
            # print(telephone, type(telephone))
        sql_up_phone = "UPDATE {} set phone=%s,telephone=%s WHERE id=%s;".format(table_name)
        # # 变量的sql语句拼接推荐使用cursor.execute()
        if telephone_z:
            cursor.execute(sql_up_phone, (phone, telephone_z, d))
            conn.commit()
            continue
        cursor.execute(sql_up_phone, (phone, telephone, d))
        conn.commit()
    end_time = time.time()
    print('总耗时{}s：'.format(round(end_time - start_time, 2)))
    # 去除联系方式为空的记录
    sql = """
    delete from {} where id in
    (select id from (select id from {} where telephone='' and phone='') t);
    """.format(table_name, table_name)
    conn.commit()

cursor.close()
conn.close()

# print(res, msg)  # None 0 None
# print(res, type(msg[0]), msg[1])

# 查询表的最大值
# sql1 = "SELECT max(id) from jiulei;"
# cursor.execute(sql1)
#
# data = cursor.fetchone()[0]
# if not data:
#     pass
# for d in range(1, 8166):
#     # 查询语句
#     sql = "SELECT phone, telephone, address from yinliao where id={};".format(str(d))
#     # sql = "SELECT phone, telephone, address from ganxiantiaowei where id='1451';"
#     res = cursor.execute(sql)
#     # print(res)
#     if res == 0:
#         continue
#     # msg = cursor.fetchall()
#     msg = cursor.fetchone()
#     print(msg)
#     phone = msg[0]
#     if phone:
#         # 判断长度
#         if len(phone) == 11:
#             pass
#         elif len(phone) < 11:
#             phone = ''
#         elif len(phone) > 11:
#             # if len(phone) == 12:
#             if phone[0] == '0':
#                 phone_data1 = re.findall(r'[1][3,5,7,8][0-9]\d{8}$', phone)
#                 phone = phone_data1[0] if phone_data1 else ''
#             phone_data2 = re.findall(r'^[1][3,5,7,8][0-9]\d{8}', phone)
#             phone = phone_data2[0] if phone_data2 else ''
#         # print(phone)
#     telephone = msg[1]
#     telephone_z = ''
#     address = msg[2]
#     if telephone:
#         # 将字符串处理成相似的格式
#         telephone = telephone.replace(' ', '-').replace('+', '').lstrip('86-')
#         # 判断字符长度
#         if len(telephone) < 10:
#             telephone = ''
#         elif len(telephone) > 13:
#             # 去除手机号加区号的格式
#             data = re.findall('[0]\d{2,3}-[2-9]\d{6,7}', telephone)
#             telephone = data[0] if data else ''
#         elif telephone[0] != '0':
#             telephone = ''
#         # 电话号码区号设置
#         elif '-' not in telephone:
#             for i in ['北京', '天津', '上海', '重庆', '沈阳', '成都']:
#                 if i in address:
#                     telephone_z = telephone[:3] + '-' + telephone[3:]
#             telephone = telephone[:4] + '-' + telephone[4:]
#         elif '—' in telephone:
#             telephone = telephone.replace('—', '')
#
#         # print(telephone, type(telephone))
#         sql_up_phone = "UPDATE yinliao set phone=%s,telephone=%s WHERE id=%s;"
#         # # 变量的sql语句拼接推荐使用cursor.execute()
#         if telephone_z:
#             cursor.execute(sql_up_phone, (phone, telephone_z, d))
#             conn.commit()
#             continue
#         cursor.execute(sql_up_phone, (phone, telephone, d))
#         conn.commit()

# print(res, msg)  # None 0 None
# print(res, type(msg[0]), msg[1])
