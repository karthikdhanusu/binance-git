from binance.client import Client
from binance.enums import *
from binance.exceptions import *
import pandas as pd
import ta.trend as tr
import ta.volatility as tv
import numpy as np
import datetime
from finta import TA
import time
import logging
import json


client = Client('roUY76zDwxC2PLvV0BttyXW0NrwUKXWtjkP1qrJfcT5scXjHM0f3f0MH1QZ6PWi0', 'I38nIe0x4O8KKAK1worAIQrLtDCo4kipQFsdWcyMhDKO1TrY5bU9qyHLkvbZ8M2Q' , {"verify": True, "timeout": 20})

stats = {}
prcfle = '/mnt/binance/input/prcfile/BTCUSDT.txt'

def trendline(data, order=1):
    coeffs = np.polyfit(data.index.values, data, order)
    slope = coeffs[-2]
    return slope

def lrincept(data, order=1):
    inpolyfit = np.polyfit(data.index.values, data, order)
    return inpolyfit[1]

def chan_ind():
  df['Highh'] = df['High'].rolling(22, min_periods=22, axis=0).apply(lambda x: x.max())
  df['Lowl'] = df['Low'].rolling(22, min_periods=22, axis=0).apply(lambda x: x.min())
  celg = df['Highh'] - (atro*3)
  cest = df['Lowl'] + (atro*3)
  return celg, cest

class Analyse:

    def __init__(self, high, low, close, volume, vpt):
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.vpt = vpt

    def atr_ind(self, atr_win):
        indicator_atr = tv.AverageTrueRange(self.high, self.low, self.close, window=atr_win)
        df['atr'] = indicator_atr.average_true_range()
        return df['atr']

    def mavpt(self, mawin, vptsl):
        indicator_mavpt = tr.SMAIndicator(self.vpt, window=mawin)
        df['vptma'] = indicator_mavpt.sma_indicator()
        df['vptslo'] = self.vpt.rolling(vptsl, min_periods=vptsl, axis=0).apply(lambda x: trendline(data=x))
        return df[['vptma','vptslo']]

    def stcyc(self, stc_win, stc_slo):
        indicator_stc = tr.STCIndicator(self.close, window_slow=50, window_fast=23, cycle=10, smooth1=stc_win, smooth2=stc_win)
        df['stc'] = indicator_stc.stc()
        df['stcslo'] = df['stc'].rolling(stc_slo, min_periods=stc_slo, axis=0).apply(lambda x: trendline(data=x))
        return df[['stc','stcslo']]

def takeprft(item,prcfle):
    with open(prcfle) as jsonfile:
        data = json.load(jsonfile)
    itmprc = float(data[item])
    traprc = client.get_my_trades(symbol=item)
    itemprc = float(traprc[len(traprc) - 1]['price'])
    curprcall = client.get_all_tickers()
    for i in curprcall:
        if i['symbol'] == item:
            curprc = float(i['price'])
    sl = float(itemprc - ((itemprc * 2) / 100))
    tk1 = float(itemprc + ((itemprc * 1) / 100))
    tk2 = float(itemprc + ((itemprc * 1.5) / 100))
    tk3 = float(itemprc + ((itemprc * 2) / 100))
    tk4 = float(itemprc + ((itemprc * 2.5) / 100))
    tk5 = float(itemprc + ((itemprc * 3) / 100))
    tk6 = float(itemprc + ((itemprc * 3.5) / 100))
    tk7 = float(itemprc + ((itemprc * 4) / 100))
    tk8 = float(itemprc + ((itemprc * 4.5) / 100))
    tk9 = float(itemprc + ((itemprc * 5) / 100))
    tk10 = float(itemprc + ((itemprc * 5.5) / 100))
    tk11 = float(itemprc + ((itemprc * 6) / 100))
    tk12 = float(itemprc + ((itemprc * 6.5) / 100))
    tk13 = float(itemprc + ((itemprc * 7) / 100))
    tk14 = float(itemprc + ((itemprc * 7.5) / 100))
    tk15 = float(itemprc + ((itemprc * 8) / 100))
    tk16 = float(itemprc + ((itemprc * 8.5) / 100))
    tk17 = float(itemprc + ((itemprc * 9) / 100))
    tk18 = float(itemprc + ((itemprc * 9.5) / 100))
    tk19 = float(itemprc + ((itemprc * 10) / 100))
    tk20 = float(itemprc + ((itemprc * 11) / 100))
    tk21 = float(itemprc + ((itemprc * 11.5) / 100))
    tk22 = float(itemprc + ((itemprc * 12) / 100))
    tk23 = float(itemprc + ((itemprc * 12.5) / 100))
    tk24 = float(itemprc + ((itemprc * 13) / 100))
    tk25 = float(itemprc + ((itemprc * 13.5) / 100))
    tk26 = float(itemprc + ((itemprc * 14) / 100))
    tk27 = float(itemprc + ((itemprc * 14.5) / 100))
    tk28 = float(itemprc + ((itemprc * 15) / 100))
    tk29 = float(itemprc + ((itemprc * 15.5) / 100))
    tk30 = float(itemprc + ((itemprc * 16) / 100))
    if curprc > tk30:
        if itmprc == tk28:
            stats.update({item: tk29})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk29 < curprc < tk30:
        if itmprc == tk27:
            stats.update({item: tk28})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk28 < curprc < tk29:
        if itmprc == tk26:
            stats.update({item: tk27})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk27 < curprc < tk28:
        if itmprc == tk25:
            stats.update({item: tk26})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk26 < curprc < tk27:
        if itmprc == tk24:
            stats.update({item: tk25})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk25 < curprc < tk26:
        if itmprc == tk23:
            stats.update({item: tk24})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk24 < curprc < tk25:
        if itmprc == tk22:
            stats.update({item: tk23})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk23 < curprc < tk24:
        if itmprc == tk21:
            stats.update({item: tk22})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk22 < curprc < tk23:
        if itmprc == tk20:
            stats.update({item: tk21})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk21 < curprc < tk22:
        if itmprc == tk19:
            stats.update({item: tk20})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk20 < curprc < tk21:
        if itmprc == tk18:
            stats.update({item: tk19})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk19 < curprc < tk20:
        if itmprc == tk17:
            stats.update({item: tk18})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk18 < curprc < tk19:
        if itmprc == tk16:
            stats.update({item: tk17})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk17 < curprc < tk18:
        if itmprc == tk15:
            stats.update({item: tk16})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk16 < curprc < tk17:
        if itmprc == tk14:
            stats.update({item: tk15})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk15 < curprc < tk16:
        if itmprc == tk13:
            stats.update({item: tk14})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk14 < curprc < tk15:
        if itmprc == tk12:
            stats.update({item: tk13})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk13 < curprc < tk14:
        if itmprc == tk11:
            stats.update({item: tk12})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk12 < curprc < tk13:
        if itmprc == tk10:
            stats.update({item: tk11})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk11 < curprc < tk12:
        if itmprc == tk9:
            stats.update({item: tk10})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk10 < curprc < tk11:
        if itmprc == tk8:
            stats.update({item: tk9})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk9 < curprc < tk10:
        if itmprc == tk7:
            stats.update({item: tk8})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk8 < curprc < tk9:
        if itmprc == tk6:
            stats.update({item: tk7})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk7 < curprc < tk8:
        if itmprc == tk5:
            stats.update({item: tk6})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk6 < curprc < tk7:
        if itmprc == tk4:
            stats.update({item: tk5})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk5 < curprc < tk6:
        if itmprc >= tk3:
            stats.update({item: tk4})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk4 < curprc < tk5:
        if itmprc == tk2:
            stats.update({item: tk3})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk3 < curprc < tk4:
        if itmprc == tk1:
            stats.update({item: tk2})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk2 < curprc < tk3:
        if itmprc == itemprc:
            stats.update({item: tk1})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif tk1 < curprc < tk2:
        if itmprc == sl:
            stats.update({item: itemprc})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    elif sl < curprc < tk1:
        if itmprc == itemprc:
            stats.update({item: sl})
            with open(prcfle, 'w') as outfile:
                json.dump(stats, outfile)
    print(sl,itemprc,tk1,tk2,tk3,tk4,curprc)
    print(data)


def coins():
    coin = client.get_exchange_info()
    sf = pd.DataFrame.from_dict(coin['symbols'], orient='columns')
    sy = sf[sf.quoteAsset.eq('BTC')]
    sy = sy[sy.status.eq('TRADING')]
    return sy

def btcbal():
    btcj = client.get_asset_balance(asset='USDT')
    btc = btcj['free']
    return btc

def candles(items, intv):
    candles = np.array(client.get_klines(symbol=items, interval=intv, limit=300))
    df = pd.DataFrame(candles.reshape(-1, 12), dtype=float, columns=('Opentime',
                                                                     'Open',
                                                                     'High',
                                                                     'Low',
                                                                     'Close',
                                                                     'Volume',
                                                                     'Close time',
                                                                     'Quote asset volume',
                                                                     'Number of trades',
                                                                     'Taker buy base asset volume',
                                                                     'Taker buy quote asset volume',
                                                                     'Ignore'))
    df['datetime'] = pd.to_datetime(df['Opentime'], unit='ms')
    df = df.assign(Opentime = df['datetime'])
    return df




if __name__ == '__main__':
    master = '/mnt/binance/input/inputparam/BTCUSDT.txt'
    with open(master) as json_file:
        data = json.load(json_file)
    begin_time = datetime.datetime.now()
    for item in data.keys():
        if item == 'BTCUSDT':
            stc_win = data[item][0][0]
            stc_slo = data[item][0][1]
            atr_win = data[item][0][2]
            vpt_win = data[item][0][3]
            vpt_slo = data[item][0][4]
            a1 = data[item][0][5]
            a2 = data[item][0][6]
            a3 = data[item][0][7]
            a4 = data[item][0][8]
            a5 = data[item][0][9]
            a6 = data[item][0][10]
            precision = data[item][1][0]
            tickers = client.get_ticker()
            dayd = pd.DataFrame.from_dict(tickers, orient='columns')
            odrbok = client.get_orderbook_tickers()
            ob = pd.DataFrame.from_dict(odrbok, orient='columns')
            usebtc = float(btcbal())
            basset = item[3:]
            asset = item[:3]
            df = candles(item, intv=Client.KLINE_INTERVAL_5MINUTE)
            df['high'] = df['High']
            df['low'] = df['Low']
            df['open'] = df['Open']
            df['close'] = df['Close']
            df['volume'] = df['Volume']
            df['vpt'] = TA.VPT(ohlc=df)
            atro = Analyse(high=df['High'], close=df['Close'], low=df['Low'], volume=df['Volume'], vpt=df['vpt']).atr_ind(atr_win=atr_win)
            stco = Analyse(high=df['High'], close=df['Close'], low=df['Low'], volume=df['Volume'], vpt=df['vpt']).stcyc(stc_win=stc_win, stc_slo=stc_slo)
            vptmao = Analyse(high=df['High'], close=df['Close'], low=df['Low'], volume=df['Volume'], vpt=df['vpt']).mavpt(mawin=vpt_win, vptsl=vpt_slo)
            chan = chan_ind()
            df['celg'] = chan[0]
            df['cest'] = chan[1]
            df = pd.concat([df['datetime'], df['High'], df['Low'], df['Close'],
                            df['Volume'], stco['stc'], stco['stcslo'], df['celg'], df['cest'], df['vpt'], vptmao['vptma'], vptmao['vptslo']], axis=1)
            row = df.tail(1)
            abal = client.get_asset_balance(asset=asset)
            if a1 < float(row['stc']) < a2 and float(row['stcslo']) > a3 and float(row['vpt']) > float(row['vptma']) and float(row['vptslo']) > 0 and float(row['celg']) < float(row['Low']):
                for day in dayd.iterrows():
                    if day[1]['symbol'] == item:
                        if usebtc > 10:
                            for obk in ob.iterrows():
                                if obk[1]['symbol'] == item:
                                    askprc = ("{:.8f}".format(float(obk[1]['askPrice'])))
                                    askqty = float(obk[1]['askQty'])
                                    qty = float(usebtc-5)/float(askprc)
                                    ot = 1
                                    while ot == 1:
                                        try:
                                            order = client.create_order(
                                                symbol=item,
                                                side=SIDE_BUY,
                                                type=ORDER_TYPE_MARKET,
                                                quantity=(("{:."+str(precision)+"f}").format(float(qty))))
                                            buyid = order['orderId']
                                            buyst = order['status']
                                            buyprc = order['fills'][0]['price']
                                            if order['price']:
                                                ot = 0
                                                btcusdt = {}
                                                curprcallbtc = client.get_all_tickers()
                                                for i in curprcallbtc:
                                                    if i['symbol'] == "BTCUSDT":
                                                        curprcbtc = float(i['price'])
                                                btcusdt.update({"BTCUSDT": curprcbtc})
                                                with open(prcfle, 'w') as outfile:
                                                    json.dump(btcusdt, outfile)
                                        except BinanceAPIException as e:
                                            time.sleep(5)
            if abal != None:
                abal = float(abal['free'])
                if abal > 0.01:
                    qty = (("{:."+str(precision)+"f}").format(float(abal)))
                    quty = float(qty) - 0.0001
                    takeprft(item, prcfle)
                    with open(prcfle) as jsonfile:
                        data = json.load(jsonfile)
                    itmprc = float(data[item])
                    curprcall = client.get_all_tickers()
                    for i in curprcall:
                        if i['symbol'] == item:
                            curprc = float(i['price'])
                    if a4 < float(row['stc']) < a5 and float(row['stcslo']) < a6 and float(row['celg']) > float(
                            row['Low']):
                        ot = 1
                        while ot == 1:
                            try:
                                order = client.create_order(
                                    symbol=item,
                                    side=SIDE_SELL,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=(("{:."+str(precision)+"f}").format(float(quty))))
                                sellid = order['orderId']
                                sellst = order['status']
                                if order['price']:
                                    ot = 0
                                    btcusdt = {}
                                    curprcallbtc = client.get_all_tickers()
                                    for i in curprcallbtc:
                                        if i['symbol'] == "BTCUSDT":
                                            curprcbtc = float(i['price'])
                                    btcusdt.update({"BTCUSDT": curprcbtc})
                                    with open(prcfle, 'w') as outfile:
                                        json.dump(btcusdt, outfile)
                            except BinanceAPIException as e:
                                time.sleep(5)
                    elif float(curprc) < float(itmprc):
                        ot = 1
                        while ot == 1:
                            try:
                                order = client.create_order(
                                    symbol=item,
                                    side=SIDE_SELL,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=(("{:."+str(precision)+"f}").format(float(quty))))
                                buyid = order['orderId']
                                buyst = order['status']
                                if order['price']:
                                    ot = 0
                                    btcusdt = {}
                                    curprcallbtc = client.get_all_tickers()
                                    for i in curprcallbtc:
                                        if i['symbol'] == "BTCUSDT":
                                            curprcbtc = float(i['price'])
                                    btcusdt.update({"BTCUSDT": curprcbtc})
                                    with open(prcfle, 'w') as outfile:
                                        json.dump(btcusdt, outfile)
                                    time.sleep(1800)
                            except BinanceAPIException as e:
                                time.sleep(5)
