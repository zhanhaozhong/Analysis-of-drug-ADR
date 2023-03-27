import numpy as np
import pandas as pd


def Bcpnn(A, B, C, D):
    N = A + B + C + D
    c0 = A
    c1 = A + B
    c2 = A + C
    lamda = 1
    alpha = beta = 1
    delta = yita = 2
    r = lamda * (N + delta) * (N + yita) / ((c1 + alpha) * (c2 + beta))
    E = np.log2((c0 + lamda) * (N + alpha) * (N + beta) / ((N + r) * (c1 + alpha) * (c2 + beta)))
    V = ((N - c0 + r - lamda) / ((c0 + lamda) * (1 + N + lamda)) + (N - c1 + delta - alpha) / (
            (c1 + alpha) * (1 + N + delta)) + (N - c2 + yita - beta) / ((c1 + beta) * (1 + N + yita))) / (
                np.log(2) * np.log(2))
    IC = E
    SD = np.sqrt(V)
    moba = IC - 2 * SD
    up = IC + 2 * SD
    down = moba

    return IC, SD, up, down


def PRR(A, B, C, D):
    prr = (A / (A + B)) / (C / (C + D))
    se = np.sqrt(1 / A - 1 / (A + B) + 1 / C - 1 / (C + D))

    return prr, se


def ROR(a, b, c, d):
    ror = (a * d) / (b * c)
    se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)

    return ror, se


def Q_value(a, b, c, d):
    q = (a * d - b * c) / (a * d + b * c)
    se = 1 / 2 * (1 - q ** 2) * np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)

    return q, se


def MHRA(A, B, C, D):
    prr = (A / (A + B)) / (C / (C + D))
    Ma = prr
    N = A + B + C + D
    fz = np.abs(A * B - B * C)
    x_2 = (N * ((fz - N / 2) ** 2)) / ((A + B) * (A + C) * (C + D) * (B + D))
    return Ma, x_2


def qqqqqqqqq(ob, ss=0):
    v_ = ob.copy()
    v = v_.loc[v_['c'] > 0]
    Q, SE = Q_value(v['a'], v['b'], v['c'], v['d'])
    v_.loc[v_['c'] > 0, 'Q_value_q'] = Q
    v_.loc[v_['c'] > 0, 'Q_value_SE'] = SE
    v_['Q_value_sigmal'] = v_['Q_value_q'] - 1.96 * v_['Q_value_SE']
    v_['Q_value_signal'] = 0
    v_.loc[(v_['Q_value_sigmal'] > 0) & (v_['a'] > 3), 'Q_value_signal'] = 1
    vv = v_[['generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year',
             'adr_date_quarter', 'a', 'b', 'c', 'd', 'n', 'Q_value_q',
             'Q_value_SE', 'Q_value_signal']]
    if ss == 0:
        vv.to_csv('Q结果经典.csv', encoding='utf-8-sig', index=0)
    else:
        vv.to_csv('Q结果加权.csv', encoding='utf-8-sig', index=0)
    vv = vv[(vv['a'] > 3) & (vv['Q_value_signal'] > 0)][['generic_name',
                                                         'meddra_id', 'name',
                                                         'is_new', 'adr_date_year',
                                                         'adr_date_quarter', ]].copy()
    vv = vv.rename(columns={'generic_name': '药品名称',
                            'meddra_id': '不良反应id',
                            'name': '不良反应名称',
                            'is_new': '是否新信号',
                            'adr_date_year': '年份',
                            'adr_date_quarter': '季度'})
    vv['s1'] = '年'
    vv['s2'] = '季度'
    vv['时间'] = vv['年份'].apply(str) + vv['s1'] + \
               vv['季度'].apply(str) + vv['s2']
    vv['算法'] = 'Q_value'
    new = vv[vv['是否新信号'] == 1].copy()
    new = new[['药品名称', '不良反应id', '不良反应名称', '年份', '季度']]. \
        drop_duplicates(subset=['药品名称', '不良反应id'], keep='first')
    group = vv.groupby(['药品名称', '年份', '季度']).count().reset_index()[['药品名称',
                                                                    '年份', '季度',
                                                                    '不良反应名称']]. \
        rename(columns={'不良反应名称': '不良反应数'})
    if ss == 0:
        vv.to_csv('信号检测/信号检测/经典YuleQ信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/经典YuleQ法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/经典YuleQ法.csv', index=0, encoding='utf-8-sig')
    else:
        vv.to_csv('信号检测/信号检测/加权YuleQ信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/加权YuleQ法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/加权YuleQ法.csv', index=0, encoding='utf-8-sig')

    return vv, v_


def rorrrrr(ob, ss=0):
    v_ = ob.copy()
    v = v_.loc[v_['c'] > 0]
    Ror, SE = ROR(v['a'], v['b'], v['c'], v['d'])
    v_.loc[v_['c'] > 0, 'ROR_ror'] = Ror
    v_.loc[v_['c'] > 0, 'ROR_SE'] = SE
    v_['ROR_sigmal'] = v_['ROR_ror'] - 1.96 * v_['ROR_SE']
    v_['ROR_signal'] = 0
    v_.loc[(v_['a'] > 3) & (v_['ROR_sigmal'] > 1) & (v_['ROR_sigmal'] <= 50), 'ROR_signal'] = 1
    v_.loc[(v_['a'] > 3) & (v_['ROR_sigmal'] > 50) & (v_['ROR_sigmal'] < 1000), 'ROR_signal'] = 2
    v_.loc[(v_['ROR_sigmal'] >= 1000) & (v_['a'] > 3), 'ROR_signal'] = 3
    vv = v_[['generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year',
             'adr_date_quarter', 'a', 'b', 'c', 'd', 'n', 'ROR_ror',
             'ROR_SE', 'ROR_signal']]
    if ss == 0:
        vv.to_csv('ROR结果经典.csv', encoding='utf-8-sig', index=0)
    else:
        vv.to_csv('ROR结果加权.csv', encoding='utf-8-sig', index=0)
    vv = vv[(vv['a'] > 3) & (vv['ROR_signal'] > 0)][['generic_name',
                                                     'meddra_id', 'name',
                                                     'is_new', 'adr_date_year',
                                                     'adr_date_quarter', ]].copy()
    vv = vv.rename(columns={'generic_name': '药品名称',
                            'meddra_id': '不良反应id',
                            'name': '不良反应名称',
                            'is_new': '是否新信号',
                            'adr_date_year': '年份',
                            'adr_date_quarter': '季度'})
    vv['s1'] = '年'
    vv['s2'] = '季度'
    vv['时间'] = vv['年份'].apply(str) + vv['s1'] + \
               vv['季度'].apply(str) + vv['s2']
    vv['算法'] = 'ROR'
    new = vv[vv['是否新信号'] == 1].copy()
    new = new[['药品名称', '不良反应id', '不良反应名称', '年份', '季度']]. \
        drop_duplicates(subset=['药品名称', '不良反应id'], keep='first')
    group = vv.groupby(['药品名称', '年份', '季度']).count().reset_index()[['药品名称',
                                                                    '年份', '季度',
                                                                    '不良反应名称']]. \
        rename(columns={'不良反应名称': '不良反应数'})
    if ss == 0:
        vv.to_csv('信号检测/信号检测/经典ROR信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/经典ROR法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/经典ROR法.csv', index=0, encoding='utf-8-sig')
    else:
        vv.to_csv('信号检测/信号检测/加权ROR信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/加权ROR法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/加权ROR法.csv', index=0, encoding='utf-8-sig')

    return vv, v_


def prrrr(ob, ss=0):
    v_ = ob.copy()
    v = v_.loc[v_['c'] > 0]
    Prr, SE = PRR(v['a'], v['b'], v['c'], v['d'])
    v_.loc[v_['c'] > 0, 'PRR_prr'] = Prr
    v_.loc[v_['c'] > 0, 'PRR_SE'] = SE
    v_['PRR_sigmal'] = v_['PRR_prr'] - 1.96 * v_['PRR_SE']
    v_['PRR_signal'] = 0
    v_.loc[(v_['a'] > 3) & (v_['PRR_sigmal'] > 1) & (v_['PRR_sigmal'] <= 50), 'PRR_signal'] = 1
    v_.loc[(v_['a'] > 3) & (v_['PRR_sigmal'] > 50) & (v_['PRR_sigmal'] < 1000), 'PRR_signal'] = 2
    v_.loc[(v_['PRR_sigmal'] >= 1000) & (v_['a'] > 3), 'PRR_signal'] = 3
    vv = v_[['generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year',
             'adr_date_quarter', 'a', 'b', 'c', 'd', 'n', 'PRR_prr',
             'PRR_SE', 'PRR_signal']]
    if ss == 0:
        vv.to_csv('PRR结果经典.csv', encoding='utf-8-sig', index=0)
    else:
        vv.to_csv('PRR结果加权.csv', encoding='utf-8-sig', index=0)
    vv = vv[(vv['a'] > 3) & (vv['PRR_signal'] > 0)][['generic_name',
                                                     'meddra_id', 'name',
                                                     'is_new', 'adr_date_year',
                                                     'adr_date_quarter', ]].copy()
    vv = vv.rename(columns={'generic_name': '药品名称',
                            'meddra_id': '不良反应id',
                            'name': '不良反应名称',
                            'is_new': '是否新信号',
                            'adr_date_year': '年份',
                            'adr_date_quarter': '季度'})
    vv['s1'] = '年'
    vv['s2'] = '季度'
    vv['时间'] = vv['年份'].apply(str) + vv['s1'] + \
               vv['季度'].apply(str) + vv['s2']
    vv['算法'] = 'PRR'
    new = vv[vv['是否新信号'] == 1].copy()
    new = new[['药品名称', '不良反应id', '不良反应名称', '年份', '季度']]. \
        drop_duplicates(subset=['药品名称', '不良反应id'], keep='first')
    group = vv.groupby(['药品名称', '年份', '季度']).count().reset_index()[['药品名称',
                                                                    '年份', '季度',
                                                                    '不良反应名称']]. \
        rename(columns={'不良反应名称': '不良反应数'})
    if ss == 0:
        vv.to_csv('信号检测/信号检测/经典PRR信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/经典PRR法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/经典PRR法.csv', index=0, encoding='utf-8-sig')
    else:
        vv.to_csv('信号检测/信号检测/加权PRR信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/加权PRR法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/加权PRR法.csv', index=0, encoding='utf-8-sig')

    # return v_
    return vv, v_


def mhraaaaaaaa(ob, ss=0):
    v_ = ob.copy()
    v = v_.loc[v_['c'] > 0]
    Ma, x_2 = MHRA(v['a'], v['b'], v['c'], v['d'])
    v_.loc[v_['c'] > 0, 'MHRA_prr'] = Ma
    v_.loc[v_['c'] > 0, 'MHRA_x2'] = x_2
    v_['MHRA_signal'] = 0
    v_.loc[(v_['a'] > 3) & (v_['MHRA_prr'] > 2) & (v_['MHRA_x2'] > 4) & (v_['MHRA_x2'] < 100), 'MHRA_signal'] = 1
    v_.loc[(v_['a'] > 3) & (v_['MHRA_prr'] > 2) & (v_['MHRA_x2'] >= 100) & (v_['MHRA_x2'] < 1000), 'MHRA_signal'] = 2
    v_.loc[(v_['a'] > 3) & (v_['MHRA_prr'] > 2) & (v_['MHRA_x2'] >= 1000), 'MHRA_signal'] = 3
    vv = v_[['generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year',
             'adr_date_quarter', 'a', 'b', 'c', 'd', 'n', 'MHRA_prr',
             'MHRA_x2', 'MHRA_signal']]
    if ss == 0:
        vv.to_csv('MHRA结果经典.csv', encoding='utf-8-sig', index=0)
    else:
        vv.to_csv('MHRA结果加权.csv', encoding='utf-8-sig', index=0)
    vv = vv[(vv['a'] > 3) & (vv['MHRA_signal'] > 0)][['generic_name',
                                                      'meddra_id', 'name',
                                                      'is_new', 'adr_date_year',
                                                      'adr_date_quarter']].copy()
    vv = vv.rename(columns={'generic_name': '药品名称',
                            'meddra_id': '不良反应id',
                            'name': '不良反应名称',
                            'is_new': '是否新信号',
                            'adr_date_year': '年份',
                            'adr_date_quarter': '季度'})
    vv['s1'] = '年'
    vv['s2'] = '季度'
    vv['时间'] = vv['年份'].apply(str) + vv['s1'] + \
               vv['季度'].apply(str) + vv['s2']
    vv['算法'] = 'MHRA'
    new = vv[vv['是否新信号'] == 1].copy()
    new = new[['药品名称', '不良反应id', '不良反应名称', '年份', '季度']]. \
        drop_duplicates(subset=['药品名称', '不良反应id'], keep='first')
    group = vv.groupby(['药品名称', '年份', '季度']).count().reset_index()[['药品名称',
                                                                    '年份', '季度',
                                                                    '不良反应名称']]. \
        rename(columns={'不良反应名称': '不良反应数'})
    if ss == 0:
        vv.to_csv('信号检测/信号检测/经典MHRA信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/经典MHRA信号.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/经典MHRA法.csv', index=0, encoding='utf-8-sig')
    else:
        vv.to_csv('信号检测/信号检测/加权MHRA信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/加权MHRA信号.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/加权MHRA法.csv', index=0, encoding='utf-8-sig')
    return vv, v_


def bllll(ob, ss=0):
    v = ob.copy()
    ic, se, up0, down0 = Bcpnn(v['a'], v['b'], v['c'], v['d'])
    v['BCPNN_IC'] = ic
    v['BCPNN_IC上限'] = up0
    v['BCPNN_IC下限'] = down0
    v['BCPNN_signal'] = 0
    v.loc[(0 < v['BCPNN_IC下限']) & (v['BCPNN_IC下限'] <= 1.5), 'BCPNN_signal'] = 1
    v.loc[(1.5 < v['BCPNN_IC下限']) & (v['BCPNN_IC下限'] <= 3), 'BCPNN_signal'] = 2
    v.loc[v['BCPNN_IC下限'] > 3, 'BCPNN_signal'] = 3
    vv = v[['generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year',
            'adr_date_quarter', 'a', 'b', 'c', 'd', 'n', 'BCPNN_IC',
            'BCPNN_IC上限', 'BCPNN_IC下限', 'BCPNN_signal']]
    if ss == 0:
        vv.to_csv('BCPNN结果经典.csv', encoding='utf-8-sig', index=0)
    else:
        vv.to_csv('BCPNN结果加权.csv', encoding='utf-8-sig', index=0)
    vv = vv[(vv['a'] > 3) & (vv['BCPNN_signal'] > 0)][['generic_name',
                                                       'meddra_id', 'name',
                                                       'is_new', 'adr_date_year',
                                                       'adr_date_quarter', ]].copy()
    vv = vv.rename(columns={'generic_name': '药品名称',
                            'meddra_id': '不良反应id',
                            'name': '不良反应名称',
                            'is_new': '是否新信号',
                            'adr_date_year': '年份',
                            'adr_date_quarter': '季度'})
    vv['s1'] = '年'
    vv['s2'] = '季度'
    vv['时间'] = vv['年份'].apply(str) + vv['s1'] + \
               vv['季度'].apply(str) + vv['s2']
    vv['算法'] = 'BCPNN'
    new = vv[vv['是否新信号'] == 1].copy()
    new = new[['药品名称', '不良反应id', '不良反应名称', '年份', '季度']]. \
        drop_duplicates(subset=['药品名称', '不良反应id'], keep='first')
    group = vv.groupby(['药品名称', '年份', '季度']).count().reset_index()[['药品名称',
                                                                    '年份', '季度',
                                                                    '不良反应名称']]. \
        rename(columns={'不良反应名称': '不良反应数'})
    if ss == 0:
        vv.to_csv('信号检测/信号检测/经典BCPNN信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/经典BCPNN法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/经典BCPNN法.csv', index=0, encoding='utf-8-sig')
    else:
        vv.to_csv('信号检测/信号检测/加权BCPNN信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/加权BCPNN法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/加权BCPNN法.csv', index=0, encoding='utf-8-sig')

    return vv, v


def Bagging(oob, ss=0):
    s = ['BCPNN_signal', 'MHRA_signal', 'PRR_signal', 'ROR_signal', 'Q_value_signal']
    v = oob[s].copy()
    s = v[v == 0].fillna(1)
    v['Bagging'] = s.sum(axis=1)
    ob = oob.copy()
    ob['Bagging_signal'] = 0
    ob.loc[(v['Bagging'] >= 4) & (ob['a'] > 3), 'Bagging_signal'] = 1
    vv = ob[['generic_name', 'meddra_id', 'name', 'is_new', 'adr_date_year',
             'adr_date_quarter', 'a', 'b', 'c', 'd', 'n', 'Bagging_signal']]
    if ss == 0:
        vv.to_csv('Bagging结果经典.csv', encoding='utf-8-sig', index=0)
    else:
        vv.to_csv('Bagging结果加权.csv', encoding='utf-8-sig', index=0)
    vv = vv[(vv['a'] > 3) & (vv['Bagging_signal'] > 0)][['generic_name',
                                                         'meddra_id', 'name',
                                                         'is_new', 'adr_date_year',
                                                         'adr_date_quarter']].copy()
    vv = vv.rename(columns={'generic_name': '药品名称',
                            'meddra_id': '不良反应id',
                            'name': '不良反应名称',
                            'is_new': '是否新信号',
                            'adr_date_year': '年份',
                            'adr_date_quarter': '季度'})
    vv['s1'] = '年'
    vv['s2'] = '季度'
    vv['时间'] = vv['年份'].apply(str) + vv['s1'] + \
               vv['季度'].apply(str) + vv['s2']
    vv['算法'] = 'Bagging'
    new = vv[vv['是否新信号'] == 1].copy()
    new = new[['药品名称', '不良反应id', '不良反应名称', '年份', '季度']]. \
        drop_duplicates(subset=['药品名称', '不良反应id'], keep='first')
    group = vv.groupby(['药品名称', '年份', '季度']).count().reset_index()[['药品名称',
                                                                    '年份', '季度',
                                                                    '不良反应名称']]. \
        rename(columns={'不良反应名称': '不良反应数'})
    if ss == 0:
        vv.to_csv('信号检测/信号检测/经典Bagging信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/经典Bagging法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/经典Bagging法.csv', index=0, encoding='utf-8-sig')
    else:
        vv.to_csv('信号检测/信号检测/加权Bagging信号.csv', index=0, encoding='utf-8-sig')
        new.to_csv('信号检测/新的信号/加权Bagging法.csv', index=0, encoding='utf-8-sig')
        group.to_csv('信号检测/不良反应计数/加权Bagging法.csv', index=0, encoding='utf-8-sig')
    return vv, ob
