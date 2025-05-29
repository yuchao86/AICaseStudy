#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by YuChao on 2024/10/12 1021.
# @Link    : http://
# Github   : https://
# @Remark  : Python DBCompareDiff
"""
确保py环境是3以上
并且安装了mysql驱动
pip install mysql-connector

MySQL的SQL占位符是%s，并且带``号
"""
# 导入MySQL驱动
import mysql.connector

# 连接源数据库
source_connector_options = {
    'host': '****.rds.ivolces.com',
    'user': "***",
    'password': "***",
    'database': "***",
    'auth_plugin': 'mysql_native_password',
}
source_connection = mysql.connector.connect(**source_connector_options)

# 连接目标数据库
dest_connector_options = {
    'host': '**.rds.ivolces.com',
    'user': "**",
    'password': "***",
    'database': "***",
    'auth_plugin': 'mysql_native_password',
}
dest_connection = mysql.connector.connect(**dest_connector_options)

# 查询源表
source_cursor = source_connection.cursor()
source_cursor.execute("SHOW TABLES")

source_tables = source_cursor.fetchall()
print(source_tables)
# 查询目标表
dest_cursor = dest_connection.cursor()
dest_cursor.execute("SHOW TABLES")

dest_tables = dest_cursor.fetchall()
print(dest_tables)

if len(source_tables) != len(dest_tables):
    print("表数量不相等",len(source_tables),"#",len(dest_tables))
else:
    print("表数量相等",len(source_tables),"#",len(dest_tables))
count = 0
for table in source_tables:
    if table[0] == "book.bak":
        continue
    source_cursor.execute("CHECKSUM TABLE `%s`" % table[0])
    source_sum = source_cursor.fetchone()[1]
    dest_cursor.execute("CHECKSUM TABLE `%s`" % table[0])
    dest_sum = dest_cursor.fetchone()[1]
    if source_sum != dest_sum:
        print("数据不一致",table[0],source_sum,"#",dest_sum)
    else:
        count += 1
        print("OK数据一致",table[0],source_sum,"#",dest_sum)

print("######数据比对完成,总共校验成功：", count, "张表#######")

source_cursor.close()
source_connection.close()

dest_cursor.close()
dest_connection.close()


# end DBCompareDiff