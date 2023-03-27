# -*- coding: gbk -*-
import pandas as pd


def select():
    # 不同企业相同药品
    smpy = pd.read_csv('企业1\\不同企业相同药品按季度.csv')
    smpyy = pd.read_csv('企业1\\不同企业相同药品按年.csv')
    c1 = smpy.copy()
    c1['count'] = 1
    d = c1.groupby(['药品名称', '年份']).sum().reset_index()[['药品名称', '年份', 'count']]
    d = d[d['count']>=3][['药品名称', '年份']]
    spmyn = pd.merge(smpy, d, on=['药品名称', '年份'], how='inner')
    spmyn.to_csv('企业1\\企业2\\不同企业相同药品按季度.csv', index=False, encoding='utf-8-sig')
    spmyyn = pd.merge(smpyy, d, on=['药品名称', '年份'], how='inner')
    spmyyn.to_csv('企业1\\企业2\\不同企业相同药品按年.csv', index=False, encoding='utf-8-sig')


    # 相同企业
    samepy = pd.read_csv('企业1\\相同企业按季度.csv')
    samepyy = pd.read_csv('企业1\\相同企业按年.csv')
    c2 = samepy.copy()
    c2['count'] = 1
    dd = c2.groupby(['企业名称', '年份']).sum().reset_index()[['企业名称', '年份', 'count']]
    dd = dd[dd['count']>=3][['企业名称', '年份']]
    spmyn = pd.merge(samepy, dd, on=['企业名称', '年份'], how='inner')
    spmyn.to_csv('企业1\\企业2\\相同企业按季度.csv', index=False, encoding='utf-8-sig')
    spmyyn = pd.merge(samepyy, dd, on=['企业名称', '年份'], how='inner')
    spmyyn.to_csv('企业1\\企业2\\相同企业按年.csv', index=False, encoding='utf-8-sig')

    samepmy = pd.read_csv('企业1\\相同企业相同药品按季度.csv')
    samepmyy = pd.read_csv('企业1\\相同企业相同药品按年.csv')
    c3 = samepmy.copy()
    c3['count'] = 1
    ddd = c3.groupby(['药品名称', '企业名称', '年份']).sum().reset_index()[['药品名称', '企业名称', '年份', 'count']]
    ddd = ddd[ddd['count'] >= 3][['药品名称', '企业名称', '年份']]
    spmyn = pd.merge(samepmy, ddd, on=['药品名称', '企业名称', '年份'], how='inner')
    spmyn.to_csv('企业1\\企业2\\相同企业相同药品按季度.csv', index=False, encoding='utf-8-sig')
    spmyyn = pd.merge(samepmyy, ddd, on=['药品名称', '企业名称', '年份'], how='inner')
    spmyyn.to_csv('企业1\\企业2\\相同企业相同药品按年.csv', index=False, encoding='utf-8-sig')
