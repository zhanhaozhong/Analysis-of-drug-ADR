# -*- coding: gbk -*-
import pandas as pd


def select():
    # ��ͬ��ҵ��ͬҩƷ
    smpy = pd.read_csv('��ҵ1\\��ͬ��ҵ��ͬҩƷ������.csv')
    smpyy = pd.read_csv('��ҵ1\\��ͬ��ҵ��ͬҩƷ����.csv')
    c1 = smpy.copy()
    c1['count'] = 1
    d = c1.groupby(['ҩƷ����', '���']).sum().reset_index()[['ҩƷ����', '���', 'count']]
    d = d[d['count']>=3][['ҩƷ����', '���']]
    spmyn = pd.merge(smpy, d, on=['ҩƷ����', '���'], how='inner')
    spmyn.to_csv('��ҵ1\\��ҵ2\\��ͬ��ҵ��ͬҩƷ������.csv', index=False, encoding='utf-8-sig')
    spmyyn = pd.merge(smpyy, d, on=['ҩƷ����', '���'], how='inner')
    spmyyn.to_csv('��ҵ1\\��ҵ2\\��ͬ��ҵ��ͬҩƷ����.csv', index=False, encoding='utf-8-sig')


    # ��ͬ��ҵ
    samepy = pd.read_csv('��ҵ1\\��ͬ��ҵ������.csv')
    samepyy = pd.read_csv('��ҵ1\\��ͬ��ҵ����.csv')
    c2 = samepy.copy()
    c2['count'] = 1
    dd = c2.groupby(['��ҵ����', '���']).sum().reset_index()[['��ҵ����', '���', 'count']]
    dd = dd[dd['count']>=3][['��ҵ����', '���']]
    spmyn = pd.merge(samepy, dd, on=['��ҵ����', '���'], how='inner')
    spmyn.to_csv('��ҵ1\\��ҵ2\\��ͬ��ҵ������.csv', index=False, encoding='utf-8-sig')
    spmyyn = pd.merge(samepyy, dd, on=['��ҵ����', '���'], how='inner')
    spmyyn.to_csv('��ҵ1\\��ҵ2\\��ͬ��ҵ����.csv', index=False, encoding='utf-8-sig')

    samepmy = pd.read_csv('��ҵ1\\��ͬ��ҵ��ͬҩƷ������.csv')
    samepmyy = pd.read_csv('��ҵ1\\��ͬ��ҵ��ͬҩƷ����.csv')
    c3 = samepmy.copy()
    c3['count'] = 1
    ddd = c3.groupby(['ҩƷ����', '��ҵ����', '���']).sum().reset_index()[['ҩƷ����', '��ҵ����', '���', 'count']]
    ddd = ddd[ddd['count'] >= 3][['ҩƷ����', '��ҵ����', '���']]
    spmyn = pd.merge(samepmy, ddd, on=['ҩƷ����', '��ҵ����', '���'], how='inner')
    spmyn.to_csv('��ҵ1\\��ҵ2\\��ͬ��ҵ��ͬҩƷ������.csv', index=False, encoding='utf-8-sig')
    spmyyn = pd.merge(samepmyy, ddd, on=['ҩƷ����', '��ҵ����', '���'], how='inner')
    spmyyn.to_csv('��ҵ1\\��ҵ2\\��ͬ��ҵ��ͬҩƷ����.csv', index=False, encoding='utf-8-sig')
