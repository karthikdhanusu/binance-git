from binance.client import Client
import pandas as pd
import os
import shutil
import json

if __name__ == '__main__':
    lists = ['SOLBTC','BNBBTC']
    presicion = 0
    for i in lists:
        client = Client('IbcuXBijlP4zgX4LBkD0YlDvFsj1IvvLcat7PuhtmwxkgXmpCi9iGaKC7EHNLbR6',
                        'HdDVKCVKZGon5iNVY9cSwL2OPBMh22Y2QvMu68tr1ApublkPw6cd1RjbENX5hi6m',
                        {"verify": True, "timeout": 20})
        info = client.get_symbol_info(str(i))
        dict1 = {}
        for j in info:
            if j == 'filters':
                if (float(info[j][2]['stepSize']) * 1) == 0:
                    presicion = 0
                elif (float(info[j][2]['stepSize']) * 10) == 1:
                    presicion = 1
                elif (float(info[j][2]['stepSize']) * 100) == 1:
                    presicion = 2
                elif (float(info[j][2]['stepSize']) * 1000) == 1:
                    presicion = 3
                elif (float(info[j][2]['stepSize']) * 10000) == 1:
                    presicion = 4
                elif (float(info[j][2]['stepSize']) * 100000) == 1:
                    presicion = 5
                elif (float(info[j][2]['stepSize']) * 1000000) == 1:
                    presicion = 6
                elif (float(info[j][2]['stepSize']) * 10000000) == 1:
                    presicion = 7
                elif (float(info[j][2]['stepSize']) * 100000000) == 1:
                    presicion = 8
        if len(os.listdir('/mnt/binance/output/'+str(i)+'/finalcsv')) <= 500:
            arr = os.listdir('/mnt/binance/output/'+str(i)+'/finalcsv')
            for filename in arr:
                df = pd.read_csv('/mnt/binance/output/'+str(i)+'/finalcsv/'+filename, sep=',')
                max_val = df['buyq'].max()
                dict1.update({filename:max_val})
            a = list(dict1.keys())[list(dict1.values()).index(max(dict1.values()))]
            df = pd.read_csv('/mnt/binance/output/' + str(i) + '/finalcsv/' + a, sep=',')
            b = df[df['buyq'] == df['buyq'].max()]
            splits = a.split('_')
            stc_win = (splits[1][3:])[:1]
            stc_slo = (splits[1][3:])[1:]
            atr_win = (splits[2][4:])
            vpt_win = (splits[3][3:])
            vpt_slo = (splits[4][5:])
            c = {i : [[int(stc_win),int(stc_slo),int(atr_win),int(vpt_win),int(vpt_slo),int(b['a1'].values),int(b['a2'].values),int(b['a3'].values),int(b['a4'].values),int(b['a5'].values),int(b['a6'].values)],[int(presicion)]]}
        if not os.path.exists('/mnt/binance/input/inputparam'):
            os.makedirs('/mnt/binance/input/inputparam')
        with open('/mnt/binance/input/inputparam/'+str(i)+'.txt', 'w') as f:
            f.write(str(json.dumps(c)))
        with open('/mnt/binance/input/prcfile/'+str(i)+'.txt', 'w') as f:
            f.write(str('{"'+str(i)+'":0}'))
        #try:
        #    shutil.rmtree('/mnt/binance/output/'+str(i))
        #except:
        #    pass

