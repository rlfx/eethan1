# -*- coding: utf-8 -*-
def  initialize(context):
	# set_symbol_lookup_date('2017-08-20')#搭配symbol
	# set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025,price_impact=0.1))#模擬真實狀況
	context.aapl = sid(24)
	context.spy = sid(8554)
	#sid()比symbol()安全，不須指定日期
	context.message = 'hello'
	context.security_list = [sid(24),sid(8554),sid(5061)]
	#handle_data預設每分鐘呼叫一次的樣子，schedule_function提供不同時間的買賣動作
	schedule_function(
		func=long_f,#交易函式
		date_rule=date_rules.every_day(),#日期
		time_rule=time_rules.market_open(),#時間
		half_days=True#有時會碰到節日只開半天(?)
	)
	schedule_function(
		func=close_out_f,
		date_rule=date_rules.every_day(),
		time_rule=time_rules.market_close(minutes=1),
		half_days=True
	)


def handle_data(context, data):
	hist = data.history(sid(24), 'volume', 11, '1d')#hist含current,故取11以得到前十天
	# mean_price =hist.mean()
	# if data.can_trade(sid(24)):
	# 	order_target_percent(sid(24),0.5)#下單,總資產百分比,有正負
	
	# print context.message
	data.current(sid(24),'price')
	print data.current([sid(24), sid(8554)],['price','low','high'])



def long_f(context, data):
	for security in context.security_list:
		if data.can_trade(security):
  			order_target_percent(security, 0.5)
#平倉
def close_out_f(context, data):
 	for security in context.portfolio.positions:#紀錄持有投資物的資訊
  		order_target_percent(security, 0)


# def before_trading_start(context, data):
