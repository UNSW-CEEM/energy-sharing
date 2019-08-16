# reformats .csv file timeseries from legacy format used for morePVs to format used by energy_sharing model


import pandas as pd
f1 = 'C:\\Users\\z5044992\\Documents\\python\\energy-sharing\\Flask\\application\\modelling\\data\\shared\\solar\\C_max_pv.csv'


def reformat_ts(ts):
    nts = ts.split(' ')[0].split('-')[2] + '/' + ts.split(' ')[0].split('-')[1]+ '/' + ts.split(' ')[0].split('-')[0] + ' '+ ts.split(' ')[1].split(':')[0] + ':' + ts.split(' ')[1].split(':')[1]
    return nts


def reformat_csv(f):
    df= pd.read_csv(f)
    df['nts'] = df['timestamp'].apply(lambda x: reformat_ts(x))
    df1 = df[['nts','pv']]
    df1.columns = ['timestamp', 'pv']
    df1.set_index('timestamp', inplace=True)
    df1.to_csv(f)

if __name__ == "__main__":
    reformat_csv(f1)