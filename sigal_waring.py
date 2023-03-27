# -*- coding: gb2312 -*-
import pandas as pd
import numpy as np

def First():
    df = pd.read_csv('BCPNN�����Ȩ.csv', encoding='utf-8-sig')
    # df = pd.read_csv('BCPNN�������.csv', encoding='utf-8-sig')
    df1 = df[(df['adr_date_year'] == 2019) & (df['adr_date_quarter'] == 4)].copy()
    df2 = df[['generic_name', 'meddra_id', 'name', 'adr_date_year', 'adr_date_quarter', 'BCPNN_signal']].copy()
    mmm = zip(list(df1['generic_name'].values), list(df1['meddra_id'].values))

    ending = pd.DataFrame()
    dddd = 0
    for i in mmm:
        end_1 = df2[(df2['generic_name'] == i[0]) & (df2['meddra_id'] == i[1])]
        num = 0
        for j in range(10000):
            try:
                s = end_1.iloc[j, :]
                if s['BCPNN_signal'] >= 2:
                    num += 1
                    if num >= 5:
                        # ending = pd.DataFrame()
                        ending.loc[dddd, 'generic_name'] = s['generic_name']
                        ending.loc[dddd, 'meddra_id'] = s['meddra_id']
                        ending.loc[dddd, 'name'] = s['name']
                        ending.loc[dddd, 'waring_time'] = str(s['adr_date_year']) + str(s['adr_date_quarter'])
                        dddd += 1
                        break
            except:
                break
        ending.to_csv('AFBCPNNԤ��.csv', encoding='utf-8-sig', index=False)


def Second():
    df1 = pd.read_csv('AFBCPNNԤ��.csv', encoding='utf-8-sig').rename(
        columns={'generic_name': 'ҩƷ����', 'name': '������Ӧ', 'waring_time': 'Ԥ��ʱ��'})
    df2 = pd.read_csv('�źż������Ȩ.csv', encoding='utf-8-sig')
    df2 = df2[df2['�㷨']=='BCPNN']
    del df2['�㷨']
    df2['Ԥ��ʱ��'] = df2['���'].astype(str)+df2['����'].astype(str)
    df2['Ԥ��ʱ��'] = df2['Ԥ��ʱ��'].astype(int)
    # df2 = df2[df2['�µ��źŸ���']>0]
    df2 = df2[['ҩƷ����', '��֪�ź�', 'Ԥ��ʱ��']]
    df3 = pd.merge(df1, df2, on=['ҩƷ����', 'Ԥ��ʱ��'])
    df3['s'] = None
    n = df3.shape[0]
    for i in range(n):
        a = df3.loc[i, '������Ӧ']
        b = df3.loc[i, '��֪�ź�']
        if a not in b:
            df3.loc[i, 's'] = 1
    df3 = df3[df3['s']==1]
    del df3['s'], df3['��֪�ź�']
    ending = df3.sort_values(by=['ҩƷ����','������Ӧ', 'Ԥ��ʱ��'], axis=0, ascending=True)
    ending.drop_duplicates(keep='first', inplace=True)

    ending.to_csv('Ԥ���ź�.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    First()
    Second()
