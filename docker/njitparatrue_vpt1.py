import pandas as pd
from numba import config, cuda, jit, njit, threading_layer, set_num_threads, prange
from numpy import load
import numpy as np
from timeit import default_timer as timer
import os, shutil

files = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
arr = os.listdir('/mnt/binance/output/')
arr1 =  os.listdir('/mnt/binance/gatherdata/')
npydata = 'pairsmastereven.npy'

@njit(parallel=True, fastmath=True)
def logic(a, df_open, df_high, df_low, df_close, df_stc, df_stcslo, df_celg, df_cest, df_vpt, df_vptma, df_vptslo):
    row = np.zeros(shape=(len(a),11))
    for j in prange(len(a)):
        b = a[j]
        a1 = b[0]
        a2 = b[1]
        a3 = b[2]
        a4 = b[3]
        a5 = b[4]
        a6 = b[5]
        rows = 0
        p = 0
        l = 0
        btc = 0.1
        buyq = 0
        sl = 0
        for i in prange(len(df_open)):
            if a1 < df_stc[i] < a2 and df_stcslo[i] > a3 and df_celg[i] < df_low[i]  and df_vpt[i] > df_vptma[i] and df_vptslo[i] > 0 and btc > 0: #
                buyq = float(btc / df_close[i])
                btclose = df_close[i]
                btc1 = btc
                btc = 0
                sl = float(df_close[i]-((df_close[i]*2)/100))
            elif buyq > 0:
                if a4 < df_stc[i] < a5 and df_stcslo[i] < a6 and df_celg[i] > df_low[i]:
                    btc = float(buyq * df_close[i])
                    stclose = float(df_close[i])
                    pl = stclose - btclose
                    sellq = buyq
                    buyq = 0
                    rows += 1
                    if stclose > btclose:
                        p+=1
                    elif stclose < btclose:
                        l+=1
            if rows > 5 :
                pp = ((p/rows)*100)
        if p > 0:
            row[j,0] = a1
            row[j,1] = a2
            row[j,2] = a3
            row[j,3] = a4
            row[j,4] = a5
            row[j,5] = a6
            row[j,6] = p
            row[j,7] = l
            row[j,8] = pp
            row[j,9] = sellq
            row[j,10] = btc
            p = 0
            buyq = 0
            l = 0
            pp = 0
            btc1 = 0
    return row


if __name__ == '__main__':
     set_num_threads(31)
     for item in arr:
         for i in files:
             if os.path.exists('/mnt/binance/output/'+str(item)+'/'+str(i)) and len(os.listdir('/mnt/binance/output/'+str(item)+'/'+str(i))) <= 20:
                 inputfilelist = os.listdir('/mnt/binance/output/'+str(item)+'/'+str(i))
                 for j in range(len(os.listdir('/mnt/binance/output/'+str(item)+'/'+str(i)))):
                     for filename in inputfilelist:
                         output = filename.split('.')[0]+ '_master.csv'
                         if not os.path.exists('/mnt/binance/output/' + str(item) + '/finalcsv/'+str(output)):
                             df = pd.read_csv('/mnt/binance/output/'+str(item)+'/'+str(i)+'/'+filename, sep=',')
                             for col in df.columns:
                                 if col == 'pl':
                                     df[col].values[:] = 0
                             df_datetime = df['datetime'].to_numpy()
                             df_open = df['Open'].to_numpy(dtype=float)
                             df_high = df['High'].to_numpy(dtype=float)
                             df_low = df['Low'].to_numpy(dtype=float)
                             df_close = df['Close'].to_numpy(dtype=float)
                             df_stc = df['stc'].to_numpy(dtype=float)
                             df_stcslo = df['stcslo'].to_numpy(dtype=float)
                             df_celg = df['celg'].to_numpy(dtype=float)
                             df_cest = df['cest'].to_numpy(dtype=float)
                             df_vpt = df['vpt'].to_numpy(dtype=float)
                             df_vptma = df['vptma'].to_numpy(dtype=float)
                             df_vptslo = df['vptslo'].to_numpy(dtype=float)
                             a = load('/mnt/binance/input/'+npydata)
                             start = timer()
                             f = logic(a, df_open, df_high, df_low, df_close, df_stc, df_stcslo, df_celg, df_cest, df_vpt, df_vptma, df_vptslo)
                             f = f[~np.all(f == 0, axis=1)]
                             df = pd.DataFrame(f, columns=('a1','a2','a3','a4','a5','a6','p','l','pp','buyq', 'btc'))
                             if os.path.exists('/mnt/binance/output/' + str(item) + '/finalcsv'):
                                 df.to_csv('/mnt/binance/output/' + str(item) + '/finalcsv/' + output)
                                 print(output, " with GPU: ", timer() - start)
                             elif not os.path.exists('/mnt/binance/output/' + str(item) + '/finalcsv'):
                                 os.makedirs('/mnt/binance/output/' + str(item) + '/finalcsv')
                                 df.to_csv('/mnt/binance/output/' + str(item) + '/finalcsv/' + output)
                                 print(output, " with GPU: ", timer() - start)

     

     '''try:
         os.makedirs('H:\\binance\\output\\' + str(item) + '\\finalcsv')
         shutil.move(os.path.join('C:\\binance\\output\\' + str(item) + '\\finalcsv\\', output),
                     'H:\\binance\\output\\' + str(item) + '\\finalcsv\\')
         os.remove('H:\\binance\\output\\'+str(item)+'\\'+str(i)+'\\'+filename)
     except OSError:
         shutil.move(os.path.join('C:\\binance\\output\\' + str(item) + '\\finalcsv\\', output),
                     'H:\\binance\\output\\' + str(item) + '\\finalcsv\\')
         os.remove('H:\\binance\\output\\' + str(item) + '\\' + str(i) + '\\' + filename)'''
