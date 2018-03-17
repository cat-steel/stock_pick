import tushare as ts
import mysql.connector
import re,time
#创建所有股票的表格以及插入每支股票的近段时间的行情，这个文件只需要执行一次！！！
#想要写入哪一段时间的数据只需要修改starttime,endtime的时间就可以了
def everdate(starttime,endtime):
	#获取所有有股票
	stock_info = ts.get_stock_basics()
	#连接数据库
	conn = mysql.connector.connect(user='root',password='password',database='test')
	cursor = conn.cursor()

	codes = stock_info.index
	a = 0
	#通过for循环以及获取A股只数来遍历每一只股票
	for x in range(0,len(stock_info)):
		#匹配深圳股票（因为整个A股太多，所以我选择深圳股票做个筛选）
		if re.match('000',codes[x]) or re.match('002',codes[x]):
			#以stock_加股票代码为表名称创建表格
			cursor.execute('create table stock_' + codes[x] + ' (date varchar(32),open varchar(32),close varchar(32),high varchar(32),low varchar(32),volume varchar(32),p_change varchar(32),unique(date))')
			#利用tushare包获取单只股票的阶段性行情
			df = ts.get_hist_data(codes[x],starttime,endtime)
			print('%s的表格创建完成'%codes[x])
			a += 1
			#这里使用try，except的目的是为了防止一些停牌的股票，获取数据为空，插入数据库的时候失败而报错
			#再使用for循环遍历单只股票每一天的行情
			try:
				for i in range(0,len(df)):
					#获取股票日期，并转格式（这里为什么要转格式，是因为之前我2018-03-15这样的格式写入数据库的时候，通过通配符%之后他居然给我把-符号当做减号给算出来了查看数据库日期就是2000百思不得其解想了很久最后决定转换格式）
					times = time.strptime(df.index[i],'%Y-%m-%d')
					time_new = time.strftime('%Y%m%d',times)
					#插入每一天的行情
					cursor.execute('insert into stock_'+codes[x]+ ' (date,open,close,high,low,volume,p_change) values (%s,%s,%s,%s,%s,%s,%s)' % (time_new,df.open[i],df.close[i],df.high[i],df.low[i],df.volume[i],df.p_change[i]))
					
			except:
				print('%s这股票目前停牌'%codes[x])

	conn.close()
	cursor.close()
	#统计总共插入了多少张表的数据
	print('所有股票总共插入数据库%d张表格'%a)

everdate('2018-01-01','2018-03-14')