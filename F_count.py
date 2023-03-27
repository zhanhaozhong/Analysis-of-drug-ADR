# -*- coding: gb2312 -*-
import pandas as pd
import numpy as np


def count_other(dff, year, method='adr_date_month'):
    ob = pd.DataFrame()
    dff = dff[dff['adr_date_year'].isin(year)].copy()

    dff['adr_date_year'] = dff['adr_date_year'].apply(int)
    dff[method] = dff[method].apply(int)
    temp = sorted(dff[method].unique())
    for i in temp:
        df = dff[dff[method] <= i][['generic_name', 'meddra_id']].copy()
        df['knn'] = 1
        hhu = df[['generic_name', 'meddra_id', 'knn']].copy()
        gg = hhu.groupby(['generic_name', 'meddra_id']).sum().reset_index()
        gg = gg[gg['knn'] > 3]
        del gg['knn']
        del df['knn']
        df = pd.merge(gg, df, on=['generic_name', 'meddra_id'])

        df['a'] = df['b'] = df['c'] = df['d'] = 1
        grouped1 = df.groupby(['generic_name', 'meddra_id']).sum().reset_index()[['generic_name',
                                                                                  'meddra_id',
                                                                                  'a']]
        grouped2 = df.groupby('generic_name').sum().reset_index()[['generic_name', 'b']]
        grouped3 = df.groupby('meddra_id').sum().reset_index()[['meddra_id', 'c']]
        end_1 = pd.merge(grouped1, grouped2, on='generic_name')
        end_1 = pd.merge(end_1, grouped3, on='meddra_id')
        end_1['n'] = end_1['a'].sum()
        end_1['b'] = end_1['b'] - end_1['a']
        end_1['c'] = end_1['c'] - end_1['a']
        end_1['d'] = end_1['n'] - end_1['b'] - end_1['a'] - end_1['c']
        t_i = str(i)
        if len(t_i) > 4:
            end_1['adr_date_year'] = int(t_i[:4])
            end_1['adr_date_quarter'] = int(t_i[4])
        else:
            end_1[method] = int(i)
            end_1['adr_date_quarter'] = 0
        ob = pd.concat([ob, end_1], axis=0, ignore_index=True)

    med_name = dff[['generic_name', 'meddra_id', 'name', 'is_new',
                    'adr_date_year']].drop_duplicates(subset=['generic_name',
                                                              'meddra_id', 'is_new',
                                                              'adr_date_year'],
                                                      keep='first')
    ob = pd.merge(ob, med_name, on=['adr_date_year', 'generic_name', 'meddra_id'], how='left')[[
        'generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year', 'adr_date_quarter',
        'a', 'b', 'c', 'd', 'n']]
    ob = ob.sort_values(by=['generic_name', 'meddra_id', 'adr_date_year'],
                        ascending=[True, True, True]).fillna(method='ffill')

    return ob


def count_other_se(dff, year, method='adr_date_month'):
    ob = pd.DataFrame()
    dff = dff[dff['adr_date_year'].isin(year)].copy()
    dff['adr_date_year'] = dff['adr_date_year'].apply(int)
    dff[method] = dff[method].apply(int)
    temp = sorted(dff[method].unique())
    for i in temp:
        df = dff[dff[method] <= i][['generic_name', 'meddra_id',
                                    'end_weight']].copy()

        df['knn'] = 1
        hhu = df[['generic_name', 'meddra_id', 'knn']].copy()
        gg = hhu.groupby(['generic_name', 'meddra_id']).sum().reset_index()
        gg = gg[gg['knn'] > 3]
        del gg['knn']
        del df['knn']
        df = pd.merge(gg, df, on=['generic_name', 'meddra_id'])

        grouped1 = df.groupby(['generic_name', 'meddra_id']).sum().reset_index()
        grouped1 = grouped1[['generic_name', 'meddra_id', 'end_weight']]
        grouped1.rename(columns={'end_weight': 'a'}, inplace=True)

        grouped2 = df[['generic_name', 'end_weight']]. \
            groupby(['generic_name']).sum().reset_index()
        grouped2 = grouped2[['generic_name', 'end_weight']]
        grouped2.rename(columns={'end_weight': 'b'}, inplace=True)

        grouped3 = df.groupby(['meddra_id']).sum().reset_index()
        grouped3 = grouped3[['meddra_id', 'end_weight']]
        grouped3.rename(columns={'end_weight': 'c'}, inplace=True)

        end_1 = pd.merge(grouped1, grouped2, on='generic_name')
        end_1 = pd.merge(end_1, grouped3, on='meddra_id')
        end_1['n'] = end_1['a'].sum()
        end_1['b'] = end_1['b'] - end_1['a']
        end_1['c'] = end_1['c'] - end_1['a']
        end_1['d'] = end_1['n'] - end_1['b'] - end_1['a'] - end_1['c']
        t_i = str(i)
        if len(t_i) > 4:
            end_1['adr_date_year'] = int(t_i[:4])
            end_1['adr_date_quarter'] = int(t_i[4])
        else:
            end_1[method] = int(i)
            end_1['adr_date_quarter'] = 0
        ob = pd.concat([ob, end_1], axis=0, ignore_index=True)

    med_name = dff[['generic_name', 'meddra_id', 'name', 'is_new',
                    'adr_date_year']].drop_duplicates(subset=['generic_name',
                                                              'meddra_id', 'is_new',
                                                              'adr_date_year'],
                                                      keep='first')
    ob = pd.merge(ob, med_name, on=['adr_date_year', 'generic_name', 'meddra_id'], how='left')[[
        'generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year', 'adr_date_quarter',
        'a', 'b', 'c', 'd', 'n']]
    ob = ob.sort_values(by=['generic_name', 'meddra_id', 'adr_date_year'],
                        ascending=[True, True, True]).fillna(method='ffill')

    return ob
