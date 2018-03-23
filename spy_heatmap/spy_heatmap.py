#!/usr/bin/python
import time
#import numpy as np
import csv
from datetime import datetime
import urllib
import urllib2
import json
import stock_utilities as ut
from termcolor import colored


API_KEY='WM49A5VBG9UVXZTD'

def get_symbols():
    symbols=[]
    syms={}
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response=urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    starter='<td>'
    ender='</td>'
    tab_i='<tr>'
    tab_f='</tr>'
    sig="nofollow"
    data=response.read()
    nyse="XNYS:"
    nasdaq="symbol/"
    #print data
    while data.find(tab_i)!=-1 and data.find(tab_f)!=-1:
        section=data[(data.find(tab_i)+len(tab_i)):data.find(tab_f)]
        if sig in section:
            #print section
            industry = section.split('\n')[4][4:-5]
            sym_line = section.split('\n')[1]
            #print sym_line
            sym = sym_line[sym_line.find('">')+2:sym_line.find("</a>")]
            if industry in syms.keys():
                syms[industry].append(sym)
            else:
                syms[industry]=[sym]
                
            #print '**********************************************************'
        data=data[data.find(tab_f)+len(tab_f):]
    return syms

''' this function gets the following data for a symbol
{
  "symbol": "AAPL",
  "companyName": "Apple Inc.",
  "primaryExchange": "Nasdaq Global Select",
  "sector": "Technology",
  "calculationPrice": "tops",
  "open": 154,
  "openTime": 1506605400394,
  "close": 153.28,
  "closeTime": 1506605400394,
  "high": 154.80,
  "low": 153.25,
  "latestPrice": 158.73,
  "latestSource": "Previous close",
  "latestTime": "September 19, 2017",
  "latestUpdate": 1505779200000,
  "latestVolume": 20567140,
  "iexRealtimePrice": 158.71,
  "iexRealtimeSize": 100,
  "iexLastUpdated": 1505851198059,
  "delayedPrice": 158.71,
  "delayedPriceTime": 1505854782437,
  "previousClose": 158.73,
  "change": -1.67,
  "changePercent": -0.01158,
  "iexMarketPercent": 0.00948,
  "iexVolume": 82451,
  "avgTotalVolume": 29623234,
  "iexBidPrice": 153.01,
  "iexBidSize": 100,
  "iexAskPrice": 158.66,
  "iexAskSize": 100,
  "marketCap": 751627174400,
  "peRatio": 16.86,
  "week52High": 159.65,
  "week52Low": 93.63,
  "ytdChange": 0.3665,
}
'''
def get_ticker(symbol):
    url='https://api.iextrading.com/1.0/stock/'+symbol+'/quote'
    #print url
    response = urllib2.urlopen(url)
    rsp=response.read()
    data=json.loads(rsp)
    return data

def get_batch_tickers(symbols):
    if len(symbols)>100:
        return -1
    syms=','.join(symbols)
    url='https://api.iextrading.com/1.0/stock/market/batch?symbols='+syms+'&types=quote'
    response = urllib2.urlopen(url)
    rsp=response.read()
    data=json.loads(rsp)
    #print rsp
    return data


def get_div(symbol):
    div=0
    url = 'https://api.iextrading.com/1.0/stock/'+symbol+'/dividends/1y'
    #url='https://finance.yahoo.com/quote/'+symbol+'/' 
    response = urllib2.urlopen(url)
    rsp=response.read()
    data=json.loads(rsp)
    for disp in data:
        for key in disp:
            print key,disp[key]
    
    return div

def slow_daily_performance():
    syms=get_symbols()
    print syms
    #sum=0
    #ibm_div=get_div('IBM')
    print "Symbol, Open, Last, Change"
    for ind in syms:
        for sym in syms[ind]:
            data=get_ticker(sym)
            o=data['open']
            l=data['latestPrice']
            change=(l-o)/o
            s=sym,o,l,change
            color='green'
            if change<0:
                color='red'
            print colored(s,color)
    return 1

def faster_daily_performance():
    syms=get_symbols()
    print syms
    print "Symbol, Open, Last, Change"
    for ind in syms:
        data=get_batch_tickers(syms[ind])
        for sym in data:
            o=data[sym]['quote']['open']
            l=data[sym]['quote']['latestPrice']
            change=(l-o)/o*100
            s=sym,o,l,change
            color='green'
            if change<0:
                color='red'
            print colored(s,color)

'''
        for sym in syms[ind]:
            data=get_ticker(sym)
            
'''

if __name__=="__main__":
    faster_daily_performance()
'''
    print syms
    for ind in syms:
        sum+=len(syms[ind])
        print ind, len(syms[ind])
    print sum
'''


    #this eventually fails because of a limit of 1 request per second
    #todo: use the endpoint to get up to 100 at a time
    #for sym in syms:
    #    ticker=get_ticker(sym)
    #    print sym,ticker['4. close']
'''
    data=get_batch_tickers(syms[:10])
    for item in data['Stock Quotes']:
        print item

    ticker=get_ticker(syms[0])
    print syms[0]
    for key in ticker:
        print key, ticker[key]
'''
