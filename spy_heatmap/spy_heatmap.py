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
    url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'
    response = urllib2.urlopen(base_url + "/book/ethusd",data)
    #print(type(response))
    #sp=response.read().split('},{')
    rsp=response.read()
    data=json.loads(rsp)
    
    return data

if __name__=="__main__":
    data=get_symbols()
    print data
