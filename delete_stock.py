import mysql.connector
import re,time
import datetime,os

def delete(dates):
	conn = mysql.connector.connect(user='root',password='password',database='test')
	cursor = conn.cursor()

	cursor.execute('select code from allstock')
	value_code = cursor.fetchall()
	a = 0
	for i in range(0,len(value_code)):
		if re.match('000',value_code[i][0]) or re.match('002',value_code[i][0]):
			cursor.execute('delete from stock_'+ value_code[i][0]+ ' where date=%s'%(dates))  #删除重复的数据
			a +=1
			print('%s已删除'%value_code[i][0])
	print('共删除%d支股票的数据'%a)
	conn.commit()
	conn.close()
	cursor.close()

delete('20180313')
