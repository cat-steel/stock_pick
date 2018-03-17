#每天下午三点之后进行股票数据添加到数据库，这个文件一般只需要每天执行一次，也可以用来补行情，如果数据库缺少那天的数据的话，只需修改new_time就行，如下示例
import tushare as ts
import mysql.connector
import re,time
#每天行情出来了之后，插入当天的行情到每支股票的每个表格中
def everystock():
	#获取所有股票列表
	stock_info = ts.get_stock_basics()
	#获取股票代码列
	codes = stock_info.index
	#连接数据库
	conn = mysql.connector.connect(user='root',password='password',database='test')
	cursor = conn.cursor()
	#获取当前时间
	new_time = time.strftime('%Y-%m-%d')
	#new_time = '2018-03-13'
	a = 0
	##使用for循环遍历所有的股票
	for x in range(0,len(stock_info)):
		try:
			if re.match('000',codes[x]) or re.match('002',codes[x]):
				#获取单只股票当天的行情
				df = ts.get_hist_data(codes[x],new_time,new_time)
				#将时间转换格式
				times = time.strptime(new_time,'%Y-%m-%d')
				time_new = time.strftime('%Y%m%d',times)
#				#将当天的行情插入数据库
				cursor.execute('insert into stock_'+codes[x]+ ' (date,open,close,high,low,volume,p_change) values (%s,%s,%s,%s,%s,%s,%s)' % (time_new,df.open[0],df.close[0],df.high[0],df.low[0],df.volume[0],df.p_change[0]))
				
				print('%s的数据插入完成'%codes[x])
				a += 1
		except:
			print('%s无行情或者数据库已经存在当天的数据'%codes[x])
	#统计当天插入数据库的股票数量
	dir_log = 'D:\\python\\work\\stock\\WD\\run\log\\'
	filename = dir_log + new_time +'.log'
	flog = open(filename,'w')
	flog.write('今天的行情插入完成%s条'%a)
#	print('今天的行情插入完成%s条'%a)
	flog.close()
	conn.commit()
	conn.close()
	cursor.close()

#everystock()
