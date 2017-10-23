# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 22:55:55 2017

币安交易API
API文档地址:https://www.binance.com/restapipub.html
@author: Administrator

"""
import http.client
import urllib
import json
import hashlib
import time
import hmac
import collections

class BinanceSpotAPI:

    def __init__(self,url,apikey,secretkey, recv_window=None):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey
        self.__recv_window = recv_window #default: 5000(ms)
    
    def set_recv_window(self, recv_window):
        self.__recv_window = recv_window
        
    def __signature(self, params={}):
        '''set recvWindow/timestamp and signing the payload'''
        if self.__recv_window:
            params['recvWindow'] = self.__recv_window
        params['timestamp'] = int(time.time()*1e3)
        this_params = urllib.parse.urlencode(params).encode('utf-8')
        this_signature = hmac.new(self.__secretkey, this_params, hashlib.sha256).hexdigest()
        params['signature'] = this_signature

    def __do_http_func(self, resource, method,params={}, sign=False):
        '''internal http function(As a query string)'''
        if sign == True:
            self.__signature(params)
        headers = {"X-MBX-APIKEY": self.__apikey}
        print("HHHE:0====>", params)
        #try:
        conn = http.client.HTTPSConnection(self.__url, timeout=10)
        temp_params = urllib.parse.urlencode(params)
        conn.request("GET", resource + temp_params, None, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        params.clear()
        conn.close()
#        except:
#            print("_do_http_func failed")
#            return None
        
        try:
            return json.loads(data)
        except:
            print(data)
            return None
            
    def http_get(self, resource,params={},sign=False):
        return self.__do_http_func(resource, "GET", params,sign)
        
    def http_post(self, resource,params):
        return self.__do_http_func(resource, "POST", params,True)
        
    def http_delete(self, resource,params):
        return self.__do_http_func(resource, "DELETE", params,True)
    
    '''General endpoints:'''
    
    def ping(self):
        '''Test connectivity to the Rest API.'''
        THIS_RESOURCE = "/api/v1/ping"
        return self.http_get(THIS_RESOURCE,sign=False)
        
    def time(self):
        '''Test connectivity to the Rest API and get the current server time.'''
        THIS_RESOURCE = "/api/v1/time"
        return self.http_get(THIS_RESOURCE,sign=False)
        
    '''Market Data endpoints:'''
       
    def depth(self, symbol, limit=None):
        '''Getting depth of a symbol'''
        THIS_RESOURCE = "/api/v1/depth?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        if limit:
            params['limit'] = limit
        return self.http_get(THIS_RESOURCE, params, sign=False)

    
    def agg_trades(self, symbol, interval,limit=None,startTime=None,endTime=None):
        '''Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.'''
        THIS_RESOURCE = "/api/v1/aggTrades?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        params['interval'] = interval
        if limit:
            params['limit'] = limit
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        return self.http_get(THIS_RESOURCE, params, sign=False)
    
    def candlesticks(self, symbol, interval,limit=None,startTime=None,endTime=None):
        '''Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.'''
        THIS_RESOURCE = "/api/v1/klines?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        params['interval'] = interval
        if limit:
            params['limit'] = limit
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        return self.http_get(THIS_RESOURCE, params, sign=False)
        
    def ticker_24hr(self, symbol):
        '''24 hour price change statistics'''
        THIS_RESOURCE = "/api/v1/ticker/24hr?"
        params = collections.OrderedDict()
        params['symbol'] = symbol

        return self.http_get(THIS_RESOURCE, params, sign=False)
        
    def all_price(self):
        '''Latest price for all symbols.'''
        THIS_RESOURCE = "/api/v1/ticker/allPrices?"
        params = collections.OrderedDict()
        return self.http_get(THIS_RESOURCE, params, sign=False)
        
    def price(self, symbol=None):
        '''Getting latest price of a symbol'''
        prices = self.all_price()
        if prices ==  None:
            return None
        if symbol == None:
            return prices
        for pric in prices:
            if symbol == pric['symbol']:
                return pric
        return None
         
    def book_tickers(self, symbol=None):
        '''Best price/qty on the order book for a symbols.'''
        this_tickers = self.all_book_tickers()
        if this_tickers ==  None:
            return None
            
        if symbol == None:
            return this_tickers
            
        for ticker in this_tickers:
            if symbol == ticker['symbol']:
                return ticker
        return None
        
    '''Account endpoints:'''
    
    def order_new(self, symbol,side,type,timeInforce,quantity,price,newClinentOrderId=None,stopPrice=None,icebergQty=None,recvWindow=None):        
        '''Send in a new order'''
        THIS_RESOURCE = "/api/v3/order?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        params['side'] = side
        params['type'] = type        
        params['timeInForce'] = timeInforce
        params['quantity'] = quantity
        params['price'] = price

        if newClinentOrderId:
            params['newClinentOrderId'] = newClinentOrderId
        if stopPrice:
            params['stopPrice'] = stopPrice
        if icebergQty:
            params['icebergQty'] = icebergQty

        return self.http_post(THIS_RESOURCE,params)
    
    def order_query(self,symbol, orderId=None,origClientOrderId=None):
        '''Check an order's status.'''
        THIS_RESOURCE = "/api/v3/order?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        return self.http_get(THIS_RESOURCE,params, sign=True)
        
    def order_cancel(self,symbol, orderId=None,origClientOrderId=None,newClientOrderId=None):
        '''Cancel an active order.'''
        THIS_RESOURCE = "/api/v3/order?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        if newClientOrderId:
            params['newClientOrderId'] = newClientOrderId
        return self.http_delete(THIS_RESOURCE,params)
        
    def get_open_orders(self,symbol, recvWindow=None):
        '''Get all open orders on a symbol.'''
        THIS_RESOURCE = "/api/v3/openOrders?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow
        return self.http_get(THIS_RESOURCE,params, sign=True)
    
    def get_all_open_orders(self,symbol, orderId=None,limit=None,recvWindow=None):
        '''Get all account orders; active, canceled, or filled.'''
        THIS_RESOURCE = "/api/v3/allOrders?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        if orderId:
            params['orderId'] = orderId
        if limit:
            params['limit'] = limit
        return self.http_get(THIS_RESOURCE,params, sign=True)
        
    def account_info(self):
        '''Gect current account information.'''
        THIS_RESOURCE = "/api/v3/account?"
        params = collections.OrderedDict()
        return self.http_get(THIS_RESOURCE, params,sign=True)

    def balance(self, asset):
        '''Gect balance information of a asset.'''
        accounts =  self.account_info()
        #print(accounts)
        if accounts == None:
            return None
        balances = accounts['balances']
        if balances == None:
            return None
        for balance_t in balances:
            if asset == balance_t['asset']:
                return balance_t
        return None
 
    def account_trade_list(self,symbol,limit=None,fromId=None,recvWindow=None):
        '''Get trades for a specific account and symbol.'''
        THIS_RESOURCE = "/api/v3/myTrades?"
        params = collections.OrderedDict()
        params['symbol'] = symbol
        if limit:
            params['limit'] = limit
        if fromId:
            params['fromId'] = fromId

        return self.http_get(THIS_RESOURCE,params, sign=True)
        
    #Deposit & Withdraw
    
        