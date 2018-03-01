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
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response=urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    starter='<td>'
    ender='</td>'
    sig="nofollow"
    data=response.read()
    nyse="XNYS:"
    nasdaq="symbol/"
    while data.find(starter)!=-1 and data.find(ender)!=-1:
        section=data[(data.find(starter)+len(starter)):data.find(ender)]
        if sig in section and (nasdaq in section or nyse in section):
            symbols.append(section[section.find('">')+2:section.find("</a>")])
        data=data[data.find(ender)+len(ender):]
    return symbols
'''
            if nyse in section:
                symbols.append(section[section.find(nyse)+len(nyse):section.find('"',section.find(nyse))])
            elif nasdaq in section:
                symbols.append(section[section.find(nasdaq)+len(nasdaq):section.find('"',section.find(nasdaq))])
'''

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

if __name__=="__main__":
    syms=get_symbols()
    #this eventually fails because of a limit of 1 request per second
    #todo: use the endpoint to get up to 100 at a time
    for sym in syms:
        ticker=get_ticker(sym)
        print sym,ticker['4. close']
        '''
    ticker=get_ticker(syms[0])
    print syms[0]
    for key in ticker:
        print key, ticker[key]
'''
