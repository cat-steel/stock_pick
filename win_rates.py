#这个文件可以联合find_stock单独运行，输入todays的日期可以直接查找当天出现过的股票
import mysql.connector
import re,time
import datetime
import find_stock
#统计当天满足阳包阴所有股票，在设置的这段时间里面有没有出现过类似的行情，并且计算如果出现过，那么那天之后的5天收益率是多少
def rate(todays):
	print(todays)
	#将满足阳包阴的这些股票，以及它们之前满足的时候收益率都写到报告里面方便查看整体情况
	count,a = find_stock.valid_stock(todays)
	dir_repor = 'D:\\python\\work\\stock\\WD\\run\\report\\'
	filename = dir_repor + todays +'.txt'	
	fp = open(filename,'w')
	fp.write('总共找到%d支满足条件的股票分别是\n%s\n'%(a,count))

	#连接数据库
	conn = mysql.connector.connect(user='root',password='password',database='test')
	cursor = conn.cursor()
	#遍历满足条件的这些股票
	for x in count:
		#从数据库里挑出它们的行情
		cursor.execute('select * from stock_'+x+' order by date desc')
		value = cursor.fetchall()
	#	print(value)
		for i in range(0,len(value)):  #遍历这支股票的所有天数
			try:
				dates = value[i][0]
				opens2 = float(value[i][1])  #第i行的第一列
				opens1 = float(value[i+1][1])
				close2 = float(value[i][2])  #第i行的第二列
				close1 = float(value[i+1][2]) 
				p_change1 = float(value[i+1][6])  #第i行的第六列
				p_change2 = float(value[i][6])
				if opens2<close1 and close2>opens1 and p_change1<-2 and p_change2>9.8:
					#这一句很重要，就是在出现阳包阴之后得有5天的数据区统计，否则就会变成-5就会从开始统计的那天去取数据，结果就导致当天的这些股票统计收益的时候也有不过都是错的
					if i-6>0:
						#收益率
						wins = (float(value[i-6][2])-float(value[i-1][1]))/float(value[i-1][1])*100
						print('%s的%s之后5天收率为百分之%d'%(x,dates,wins))
						fp.write('%s在%s之后5天收率为百分之%d\n'%(x,dates,wins))
					else:
						fp.write('%s在%s之前没有满足条件的行情\n'%(x,dates))
			except:
				pass
	#			print('%s前3个月无满足条件的情况'%x)
	fp.close()
	conn.close()
	cursor.close()
#rate('2018-03-16')