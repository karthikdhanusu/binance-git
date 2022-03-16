import pandas as pd
import os

if __name__ == '__main__':
    lists = ['BTCUSDT']
    dict1 = {}
    for i in lists:
        if len(os.listdir('/mnt/binance/output/'+str(i)+'/finalcsv')) == 500:
            arr = os.listdir('/mnt/binance/output/'+str(i)+'/finalcsv')
            if 'running.lck' not in arr:
                with open('/mnt/binance/output/'+str(i)+'/finalcsv/running.lck', 'w') as f:
                    f.write('process running!')
                    f.close()
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
                c = {i : [stc_win,stc_slo,atr_win,vpt_win,vpt_slo,int(b['a1'].values),int(b['a2'].values),int(b['a3'].values),int(b['a4'].values),int(b['a5'].values),int(b['a6'].values),int(b['pp'].values),int(b['buyq'].values),int(b['btc'].values)]}
                #print(list(c.keys())[0])
            else:
                pass
        if not os.path.exists('/mnt/binance/input/inputparam'):
            os.makedirs('/mnt/binance/input/inputparam')
        with open('/mnt/binance/input/inputparam/'+str(i)+'.txt', 'w') as f:
            f.write(str(c))

