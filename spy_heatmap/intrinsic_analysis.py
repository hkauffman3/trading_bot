#!/usr/bin/python
#Yasir was here
import time
#import numpy as np
import csv
from datetime import datetime
import urllib
import urllib2
import json
import stock_utilities as ut

'''
get dividends
get shares outstanding
get share price

using 3% for discount rate
this number may be high
'''


def run():
    syms=ut.get_dow()
    #syms=['IBM','AAPL']
    print syms, len(syms)
    
def write_intrinsic_values(symbols):
    symbols=ut.get_symbols()
    for industry in symbols:
        print industry
        for sym in symbols[industry]:
            div=ut.get_div(sym)
            stats=get_stats(sym)
            num_shares=stats['sharesOutstanding']
            price=get_last_price(sym)
            dr=.03
            print sym,div
            if type(div)=='str':
                div=0
            iv=float(div)*4/dr
            if iv>price:
                #print sym
                print 'Quarterly Dividend: '+str(div)
                print 'Shares Outstanding: ' +str(num_shares)
                print "Intrinsic Price: " +str(div*4/dr)
                print "Last Price: " + str(price)
    #for stat in stats:
    #    print stat+": "+str(stats[stat])


def get_stats(symbol):
    url='https://api.iextrading.com/1.0/stock/'+symbol+'/stats'
    response = urllib2.urlopen(url)
    rsp=response.read()
    data=json.loads(rsp)
    return data

def get_last_price(symbol):
    url='https://api.iextrading.com/1.0/stock/'+symbol+'/quote'
    response = urllib2.urlopen(url)
    rsp=response.read()
    data=json.loads(rsp)
    return data['close']

if __name__=='__main__':
    run()
#    div=ut.get_div("MAT")
#    print div
#    print type(div)
#    print len(div)
