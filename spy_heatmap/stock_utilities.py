#!/usr/bin/python
import time
#import numpy as np
import csv
from datetime import datetime
import urllib
import urllib2
import json

def get_div(symbol):
    url = 'https://api.iextrading.com/1.0/stock/'+symbol+'/dividends/3m'
    response = urllib2.urlopen(url)
    rsp=response.read()
    data=json.loads(rsp)
    #print data
    if len(data)==0 or data[0]['flag']=='SU':
        div=0
    else:
        div=float(data[0]['amount'])
    return div

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


def run():
    div=get_div('IBM')
    print 'Quarterly Dividend: '+str(div)

if __name__=='__main__':
    run()
