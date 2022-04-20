from binance.client import Client
import csv
from datetime import date
import datetime
import time

startdate = date(2016, 1, 1)
enddate = date.today()
delta = enddate-startdate

def gatherdata():
    client = Client("BuhI6hTvPa2AkieQ3IBWWjEO5uzKjW7bcBL8o5dKblnULDtb7Z9irt9UK8ZguaWJ", "okW9lDhUEh8ilB8CNcOyYU0bSyqjkKXt0hNLRJviMblNxgSofh2o7XLHSJGR4QBl", {"verify": True, "timeout": 20})
    prices = client.get_all_tickers()
    ticker = ['AVAXBTC','DOGEBTC','DOTBTC']      #f['symbol']
    for tick in ticker:
        with open('/mnt/binance/gatherdata/'+str(tick)+str(delta.days)+'_5min.csv', 'w', newline='') as csvfile:
            fieldnames = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                          'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
            thewriter = csv.DictWriter(csvfile, fieldnames)
            thewriter.writeheader()
            i = 0
            for kline in client.get_historical_klines_generator(tick, Client.KLINE_INTERVAL_5MINUTE, str(delta.days)+" days"):
                thewriter.writerow({'Open time' : kline[0], 'Open': kline[1], 'High' : kline[2], 'Low' : kline[3], 'Close' : kline[4], 'Volume':kline[5], 'Close time':kline[6],'Quote asset volume':kline[7],'Number of trades':kline[8],'Taker buy base asset volume':kline[9],'Taker buy quote asset volume':kline[10]})
                print(i)
                i += 1

if __name__ == '__main__':
    gatherdata()
