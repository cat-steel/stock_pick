import mysql.connector
import re,time
import datetime,os
#从数据库获取股票数据，统计想要查找日期的满足阳包阴并且当天涨停的股票
def valid_stock(dates):
	#载入日志，好查错（因为之前统计出来的股票我去实时查了一下完全不满足条件，所以想到了加入日志好定位是哪个地方出错了）
	dir_log = 'D:\\python\\work\\stock\\WD\\run\log\\'
	filename = dir_log + dates +'.log'
	flog = open(filename,'w')

	# 先将字符串格式的时间转换为时间格式才能计算昨天的日期
	now = datetime.date(*map(int,dates.split('-')))
	oneday = datetime.timedelta(days=1)
	yestody = str(now - oneday)
	#将昨天日期转换为规定的字符串格式
	times = time.strptime(yestody,'%Y-%m-%d')
	str_yestoday = time.strftime('%Y%m%d',times)
	flog.write('执行的时间前一天是%s\n'%str_yestoday)
	#将想要查找的日期转换为规定的字符串格式
	str_today = time.strptime(dates,'%Y-%m-%d')
	today = time.strftime('%Y%m%d',str_today)
	flog.write('执行的时间是%s\n'%today)
	#连接数据库
	conn = mysql.connector.connect(user='root',password='password',database='test')
	cursor = conn.cursor()
	#查找allstock表获取所有股票代码
	cursor.execute('select code from allstock')
	value_code = cursor.fetchall()
	a = 0
	count = []
	#遍历所有股票
	for i in range(0,len(value_code)):
		if re.match('000',value_code[i][0]) or re.match('002',value_code[i][0]):
			#查询所有匹配到的股票，将今天与昨天的数据对比
			try:
				cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s order by date desc'%(today,str_yestoday))  #当天
				#cursor.execute('select * from stock_'+ value_code[i][0]+ ' where date=%s or date =%s'%('20180315','20180314'))
				value = cursor.fetchall()

			#1是昨天，2是今天
				#今天的开盘价
				opens1 = float(value[0][1])
				#今天的收盘价
				close1 = float(value[0][2])
				#今天的涨幅
				p_change1 = float(value[0][6])
				#昨天的。。。。。
				opens2 = float(value[1][1])
				close2 = float(value[1][2])
				p_change2 = float(value[1][6])
				
				#加入这两天的数据满足昨天下跌超过2%，而且今天的开盘价低于昨天的收盘价，且今天的收盘价高于昨天的收盘价，就满足阳包阴的条件
				if opens2<close1 and close2>opens1 and p_change2<-2 and p_change1>9.8:
					flog.write('%s票%s的开盘价是%s\n'%(value_code[i][0],today,opens1))
					flog.write('%s票%s的收盘价是%s\n'%(value_code[i][0],today,close1))
					flog.write('%s票%s的涨幅是%s\n'%(value_code[i][0],today,p_change1))
					flog.write('%s票%s的开盘价是%s\n'%(value_code[i][0],str_yestoday,opens2))
					flog.write('%s票%s的收盘价价是%s\n'%(value_code[i][0],str_yestoday,close2))
					flog.write('%s票%s的涨幅是%s\n'%(value_code[i][0],str_yestoday,p_change2))
					#将满足条件的股票代码放进列表中，统计当天满足条件的股票
					count.append(value_code[i][0])
					a += 1
			except:
				#之前有次sql语句出错了，order by后面没加date，每次寻找都是0支，找了半个多小时才找出来是sql语句的问题
				flog.write('%s停牌无数据,或者请查看sql语句是否正确\n'%value_code[i][0])#一般不用管，除非执行好多天的数据都为0时那可能输sql语句有问题了



	print('总共找到%d支满足条件的股票'%a)
	flog.close()
	conn.close()
	cursor.close()
	return count,a

#valid_stock('2018-3-1')