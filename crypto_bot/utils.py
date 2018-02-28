#!/usr/bin/python

import urllib2
import urllib
import json
import math

BIDS="bids"
ASKS="asks"

def get_book(num_bids=50):
    base_url = "https://api.gemini.com/v1"
    # or, for sandbox
    # base_url = "https://api.sandbox.gemini.com/v1"
    data={}
    response = urllib2.urlopen(base_url + "/book/ethusd",data)
    #print(type(response))
    #sp=response.read().split('},{')
    rsp=response.read()
    data=json.loads(rsp)
    asks=[]
    bids=[]
    for ask in data[ASKS]:
        asks.append([float(ask['price']),float(ask['amount'])])
    for bid in data[BIDS]:
        bids.append([float(bid['price']),float(bid['amount'])])

    return [asks,bids]

def scale_book(book, scale=1):
    #book = get_book()
    asks = book[0] #.reverse()
    bids = book[1]
    #print type(asks)
    #print type(book[0])
    ask_set=set()
    print "Asks:"
    for ask in reversed(asks):
        ask[0]=math.floor(ask[0])
        ask_set.add(ask[0])
    #for ask in asks:
    print "Bids:"
    for bid in bids:
        print bid
    print type(asks)

def get_price(ticker='ethusd'):
    import urllib2
    base_url = "https://api.gemini.com/v1"
    # or, for sandbox
    # base_url = "https://api.sandbox.gemini.com/v1"
    url=base_url + "/pubticker/"+ticker
    values={} #'timestamp':'timestampms'}
    values['timestamp']='timestampms'
    data = urllib.urlencode(values)
    print data
    #req = urllib2.Request(url, data)
    req = url + '?' +data
    response = urllib2.urlopen(req)
    #response = urllib2.urlopen(base_url + "/pubticker/"+ticker+"?timestamp=timestampms") #data=data)
    #print(response.read())
    return json.loads(response.read())

if __name__ == '__main__':
    #book=get_book()
    #scaled=scale_book(book,1)
    ticker = get_price()
    for key in ticker:
        print key,ticker[key]
    '''
    bids=book[BIDS]
    asks=book[ASKS]
    print "Asks:"
    for ask in asks:
        ask['price']=float(ask['price'])
        ask['amount']=float(ask['amount'])
        print ask


    print "Bids:"
    for bid in bids:
        bid['price']=float(bid['price'])
        bid['amount']=float(bid['amount'])
        print bid
'''
