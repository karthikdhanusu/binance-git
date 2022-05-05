import pandas as pd
import ta.trend as tr
import ta.volatility as tv
import numpy as np
from finta import TA
import datetime
import ast
import os
import shutil

csvfile = '/binance/gatherdata/src/mastertech/techmaster.txt'
arr = os.listdir('/mnt/binance/gatherdata/')
dirName = '/mnt/binance/output/'

def trendline(data, order=1):
    coeffs = np.polyfit(data.index.values, data, order)
    slope = coeffs[-2]
    return slope


class Analyse:

    def __init__(self, high, low, close, volume, vpt):
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.vpt = vpt

    def mavpt(self):
        indicator_mavpt = tr.SMAIndicator(self.vpt, window=mawin)
        df['vptma'] = indicator_mavpt.sma_indicator()
        df['vptslo'] = self.vpt.rolling(vptslo, min_periods=vptslo, axis=0).apply(lambda x: trendline(data=x))
        return df[['vptma', 'vptslo']]

    def atr_ind(self):
        indicator_atr = tv.AverageTrueRange(self.high, self.low, self.close, window=atrwindow)
        df['atr'] = indicator_atr.average_true_range()
        return df['atr']

    def stcyc(self):
        indicator_stc = tr.STCIndicator(self.close, window_slow=50, window_fast=23, cycle=10, smooth1=stcwindow,
                                        smooth2=stcwindow)
        df['stc'] = indicator_stc.stc()
        df['stcslo'] = df['stc'].rolling(stcslope, min_periods=stcslope, axis=0).apply(lambda x: trendline(data=x))
        return df[['stc', 'stcslo']]


def chan_ind():
    df['Highh'] = df['High'].rolling(22, min_periods=22, axis=0).apply(lambda x: x.max())
    df['Lowl'] = df['Low'].rolling(22, min_periods=22, axis=0).apply(lambda x: x.min())
    celg = df['Highh'] - (atro * 3)
    cest = df['Lowl'] + (atro * 3)
    return celg, cest

def getFiles(dirName):
    listOfFile = os.listdir(dirName)
    completeFileList = list()
    for file in listOfFile:
        completePath = os.path.join(dirName, file)
        if os.path.isdir(completePath):
            completeFileList = completeFileList + getFiles(completePath)
        else:
            completeFileList.append(completePath)

    return completeFileList

if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    items = ['ATOMBTC','LINKBTC','MATICBTC']
    with open(csvfile) as f:
        p = f.readline()
    b = ast.literal_eval(p)
    a = np.array(b)
    for filename in arr:
        item = filename.split('_')[0][:-4]
        if not os.path.exists(dirName + str(item)):
            os.makedirs(dirName+str(item))
        listOfFiles = getFiles(dirName + str(item))
        if item in items:
            for h in a:
                df = pd.read_csv("/mnt/binance/gatherdata/" + filename, sep=',')
                df['datetime'] = pd.to_datetime(df['Open time'], unit='ms')
                rowlen = len(df['datetime'])
                df['high'] = df['High']
                df['low'] = df['Low']
                df['open'] = df['Open']
                df['close'] = df['Close']
                df['volume'] = df['Volume']
                atrwindow = h[0]
                stcwindow = h[1]
                stcslope = h[2]
                mawin = h[3]
                vptslo = h[4]
                output = filename.split('_')[0] + '_stc' + str(stcwindow) + str(stcslope) + '_CH22' + str(
                    atrwindow) + '_vpt' + str(mawin) + '_vptsl' + str(vptslo) + '.csv'
                res = any(str(output) in s for s in listOfFiles)
                #print(res)
                if res == True:
                    pass
                elif res == False:
                    df = pd.read_csv("/mnt/binance/gatherdata/" + filename, sep=',')
                    df['datetime'] = pd.to_datetime(df['Open time'], unit='ms')
                    rowlen = len(df['datetime'])
                    df['high'] = df['High']
                    df['low'] = df['Low']
                    df['open'] = df['Open']
                    df['close'] = df['Close']
                    df['volume'] = df['Volume']
                    atrwindow = h[0]
                    stcwindow = h[1]
                    stcslope = h[2]
                    mawin = h[3]
                    vptslo = h[4]
                    output = filename.split('_')[0] + '_stc' + str(stcwindow) + str(stcslope) + '_CH22' + str(
                        atrwindow) + '_vpt' + str(mawin) + '_vptsl' + str(vptslo) + '.csv'
                    df['vfi'] = TA.VFI(ohlc=df)
                    df['vpt'] = TA.VPT(ohlc=df)
                    atro = Analyse(high=df['High'], close=df['Close'], low=df['Low'], volume=df['Volume'],
                            vpt=df['vpt']).atr_ind()
                    stco = Analyse(high=df['High'], close=df['Close'], low=df['Low'], volume=df['Volume'],
                            vpt=df['vpt']).stcyc()
                    vptmao = Analyse(high=df['High'], close=df['Close'], low=df['Low'], volume=df['Volume'],
                                vpt=df['vpt']).mavpt()
                    chan = chan_ind()
                    df['celg'] = chan[0]
                    df['cest'] = chan[1]
                    df = pd.concat(
                            [df['datetime'], df['Open'], df['High'], df['Low'], df['Close'], df['Volume'], stco['stc'],
                            stco['stcslo'],df['celg'], df['cest'],df['vpt'], vptmao['vptma'], vptmao['vptslo']], axis=1)
                    for i in range(1, 26):
                        if not os.path.exists("/mnt/binance/output/" + str(item) + "/" + str(i)):
                            os.makedirs("/mnt/binance/output/" + str(item) + "/" + str(i))
                    for i in range(1, 26):
                        list1 = os.listdir("/mnt/binance/output/" + str(item) + "/" + str(i))
                        if len(list1) < 20:
                            if not os.path.exists("/mnt/binance/output/" + str(item) + "/" + str(i) + "/" + output):
                                df.to_csv("/mnt/binance/output/" + str(item) + "/" + str(i) + "/" + output)
                                print(output)
                                i = 1
                                break
                            else:
                                pass
                #movetoshare(item)
                #os.remove('/mnt/binance/gatherdata/'+filename)


