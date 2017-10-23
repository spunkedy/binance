# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:26:20 2017

@author: Administrator

客户端调用，用于查看API返回结果

"""


from BinanceSpotAPI import BinanceSpotAPI

#初始化apikey，secretkey,url
apikey=b"vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A"
secretkey=b"NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"

spotHandle = BinanceSpotAPI('www.binance.com',apikey,secretkey)


#print (u"time:", int(time.time()*1e3))
#print (spotHandle.time())

#print (u"AllPrice")
#print (spotHandle.all_price())

#print (u"Price")
#print (spotHandle.price())
#
#print (u"price:")
#print (spotHandle.price("ETHBTC"))
##
#print (u"depth:")
#print (spotHandle.depth("ETHBTC"))

#print (u"ticker_24hr")
#print (spotHandle.ticker_24hr("ETHBTC"))

#print (u'allBookTickers')
#print (spotHandle.all_book_tickers())

#print (u'BookTicker')
#print (spotHandle.book_tickers("ETHBTC"))
#
print (u"order_new:")
print (spotHandle.order_new("MDABTC","SELL","LIMIT","GTC",100,0.0003))

#print (u"order_query:")
##print (spotHandle.order_query("MDABTC", 168083))
#print (spotHandle.order_query("MDABTC", 343723))
#
#print (u"order_cancel:")
#print (spotHandle.order_cancel("MDABTC", 343723))

#print (u"get_open_orders:")
#print (spotHandle.get_open_orders("MDABTC"))

#print (u"get_all_open_orders:")
#print (spotHandle.get_all_open_orders("MDABTC"))

#print (u"account_info:")
#print (spotHandle.account_info())

#print (u"balance:")
#print (spotHandle.balance("MDA"))





