import mysql.connector
import re,time
import datetime,os

#因为之前创建表格的时候没加唯一性约束，容易插入重复的数据，导致最后计算记过不准确，所以穿件一个函数给之前没加约束的加上去
def addunique():
	conn = mysql.connector.connect(user='root',password='password',database='test')
	cursor = conn.cursor()

	cursor.execute('select code from allstock')
	value_code = cursor.fetchall()
	a = 0
	for i in range(0,len(value_code)):
		if re.match('000',value_code[i][0]) or re.match('002',value_code[i][0]):
			cursor.execute('alter table stock_'+ value_code[i][0]+ ' add unique (date)')  #删除重复的数据
			print('%s已添加唯一性约束完成'%value_code[i][0])
	conn.close()
	cursor.close()

addunique()

