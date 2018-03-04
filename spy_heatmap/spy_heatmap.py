#!/usr/bin/python
import time
#import numpy as np
import csv
from datetime import datetime
import urllib
import urllib2
import json



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

def get_ticker(symbol):
    #https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=15min&outputsize=full&apikey=demo
    url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+symbol+'&interval=1min&outputsize=compact&apikey='
    response = urllib2.urlopen(url+API_KEY)
    #print(type(response))
    #sp=response.read().split('},{')
    rsp=response.read()
    data=json.loads(rsp)
    last_time=data["Meta Data"]["3. Last Refreshed"]
    ticker=data['Time Series (1min)'][last_time]
    return ticker

def get_batch_tickers(symbols):
    if len(symbols)>100:
        return -1
    syms=','.join(symbols)
    url='https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols='+syms+'&apikey='+API_KEY
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


if __name__=="__main__":
    syms=get_symbols()
    sum=0
    ibm_div=get_div('IBM')

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
