#!/usr/bin/python

import utils as ut
import time
#import numpy as np
import csv
from datetime import datetime

OUT_FILE="eth_asks_bids_price.csv"

def run():
    book=ut.get_book()
    asks=book[0]
    bids=book[1]

    total_ask=0
    for ask in asks:
        total_ask+=ask[1]
    total_bid=0
    for bid in bids:
        total_bid+=bid[1]
    print "asks:" + str(total_ask)
    print "Bids: "+ str(total_bid)

def add_dp():
    book=ut.get_book()
    asks=book[0]
    bids=book[1]

    total_ask=0
    for ask in asks:
        total_ask+=ask[1]
    total_bid=0
    for bid in bids:
        total_bid+=bid[1]
    #print "asks:" + str(total_ask)
    #print "Bids: "+ str(total_bid)
    row=[str(datetime.now())]
    row.append(ut.get_price()['last'])
    row.append(total_ask)
    row.append(total_bid)
    fd = open(OUT_FILE,'a')
    fd.write(row)
    fd.close()
    return row
if __name__ =='__main__':
    while True:
        #add_dp()
        run()
        time.sleep(5)
