# -*- coding: gbk -*-
import pandas as pd
import sqlalchemy as sqla
import numpy as np
import time

import jxing_fliter as jf
import enter_count1
import data_get
import en_select

def f1(x):
    _ = ['*', '?', '？', '-', '—', ',', '：', ':', '、']
    x = x.replace('【', '（')
    x = x.replace('】', '）')
    x = x.replace('(', '（')
    x = x.replace(')', '）')
    for i in _:
        x = x.replace(i, '')
    x = x.strip()
    return x


def money_change(x):
    if x == '元人民币':
        return 1
    if x == '港元':
        return 0.8425
    if x == '日元':
        return 0.0627
    if x == '欧元':
        return 7.9143
    if x == '美元':
        return 6.5301
    return x


def del_h(x):
    if x == '-':
        return ''
    return x


if __name__ == '__main__':
    db = sqla.create_engine('sqlite:///adr.db')
    print(db.engine.table_names())

    # 读取数据，企业名称清洗，赋权
    df1 = pd.read_sql('select * from report_raw', db)
    df1.drop_duplicates(['code', 'producer', 'gender', 'birthday', 'age',
                         'generic_name', 'adr_name'], keep='first', inplace=True)
    df1['producer'] = df1['producer'].apply(f1)
    df1.dropna(subset=['producer'], inplace=True)
    df1.rename(columns={'producer': '名单名'}, inplace=True)

    # df1 = dmf.enterprise_medname(df1)
    df1.rename(columns={'generic_name': 'm_firstname'}, inplace=True)
    name = pd.read_excel('药品名称映射表.xlsx', sheet_name='Sheet1')
    df1 = pd.merge(df1, name, on='m_firstname').dropna(subset=['generic_name']).copy()

    df2 = pd.read_excel('企业名称映射.xlsx', sheet_name='Sheet1')
    df2['权重'] = round(df2['权重'], 4)
    df = pd.merge(df1, df2, on='名单名', how='inner')

    # 获取指定年份数据
    year = ['2014', '2015', '2016', '2017', '2018', '2019']
    df = data_get.data_get(df, year)
    #
    #
    # breakpoint()
    # 剂型清洗
    df = jf.jixing(df)

    for i in ['adr_date_year', 'adr_date_quarter']:
        enter_count1.Four_table(df, i)
        enter_count1.med_enter(df, i)
        enter_count1.enter_med(df, i)
        enter_count1.same_enter_med(df, i)

    en_select.select()

