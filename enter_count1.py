import pandas as pd
import numpy as np


def Q_ic(A, B, C, D):
    # IC = np.log2((a * (a + b + c + d)) / ((a + b) * (a + c)))
    N = A + B + C + D
    c0 = A
    c1 = A + B
    c2 = A + C
    lamda = 0.1
    alpha = beta = 0.1
    delta = yita = 0.2
    r = lamda * (N + delta) * (N + yita) / ((c1 + alpha) * (c2 + beta))
    IC = np.log2((c0 + lamda) * (N + alpha) * (N + beta) / ((N + r) * (c1 + alpha) * (c2 + beta)))
    return IC


def Four_table(df, stype):
    np.seterr(divide='ignore', invalid='ignore')
    df = df[['producer', 'generic_name', '剂型', stype, '权重']].copy()
    df['a'] = df['b'] = df['c'] = df['d'] = df['权重']
    # df['a'] = df['b'] = df['c'] = df['d'] = 1
    df = df[df['权重'] != 0]
    s = ['口服', '注射', '外用', '其他']
    ending2 = pd.DataFrame()
    temp = df[stype].unique()
    for k in s:  # 选择剂型
        for i in temp:  # 选择季度
            dfs = df[df['剂型'] == k]
            df_1 = dfs[dfs[stype] == i].copy()
            # 计算 a
            grouped1 = df_1.groupby(['producer', 'generic_name', stype]) \
                .sum().reset_index()[['producer', 'generic_name', stype, 'a']]
            # 计算 a+c
            grouped2 = df_1.groupby(['generic_name']).sum(). \
                reset_index()[['generic_name', 'b']]

            # 计算 a+b
            grouped3 = df_1.groupby(['producer']).sum(). \
                reset_index()[['producer', 'c']]

            # a+b、a+c 贴入原始带a值的表格
            end_1 = pd.merge(grouped1, grouped3, on=['producer'])
            end_1 = pd.merge(end_1, grouped2, on=['generic_name'])

            # 计算最终四格表的a|b|c|d|n
            # end_1['n'] = df.shape[0]

            end_1['n'] = df_1['权重'].sum()
            end_1['b'] = (end_1['b'] - end_1['a'])
            end_1['c'] = (end_1['c'] - end_1['a'])
            # end_1['b'] = (end_1['b'] - end_1['a'])*end_1['权重']
            # end_1['c'] = (end_1['c'] - end_1['a'])*end_1['权重']
            end_1['d'] = end_1['n'] - end_1['b'] - end_1['a'] - end_1['c']
            # 加入一列(时间)
            end_1[stype] = i

            # Dataframe的值转为numpy数组存储，方便计算
            a = np.array(end_1['a'].values, dtype=float)
            b = np.array(end_1['b'].values, dtype=float)
            c = np.array(end_1['c'].values, dtype=float)
            d = np.array(end_1['d'].values, dtype=float)
            # 计算IC值，返回一列数据
            IC = Q_ic(a, b, c, d)
            # IC值贴入四格表 企业名称|药品名称|年份/季度|a|b|c|d|n|IC
            end_1['IC'] = IC
            # 选择给定企业
            # end_1 = end_1[end_1['producer'].isin(df_weight['producer'].values)]
            # 各个企业权重贴入四格表，重新计算IC值
            # end_1 = pd.merge(end_1, df_weight, on='producer')
            # end_1['IC'] = end_1['IC'] * end_1['weight']
            # 求每个企业所有IC的均值，命名为IC_mean_1
            mean = end_1.groupby(['producer']).agg('mean').\
                reset_index()[['producer', 'IC']]. \
                rename(columns={'IC': 'IC_mean_1'})
            # 各个企业IC均值贴入四格表
            end_1 = pd.merge(end_1, mean, on='producer')

            # 去掉企业名称的重复项，每个企业数据只保留一行
            end_2 = end_1.drop_duplicates(subset=['producer'], keep='first').copy()
            # 计算所有企业IC均值的(均值、标准差)
            end_2['IC_mean'] = end_2['IC_mean_1'].mean()
            end_2['IC_std'] = end_2['IC_mean_1'].std()
            end_2['IC_std'].fillna(0, inplace=True)
            # 计算第一预警值
            end_2['mean + 0.5*sigma'] = end_2['IC_mean'] + 0.5 * end_2['IC_std']
            # 计算第二预警值
            end_2['mean + sigma'] = end_2['IC_mean'] + end_2['IC_std']
            # 降序排列
            # end_1.sort_values('IC', ascending=False, inplace=True)
            end_2.sort_values('IC_mean_1', ascending=False, inplace=True)
            hhu = str(i)
            end_2['年份'] = hhu[0:4]
            if len(hhu)>4:
                end_2['季度'] = hhu[4]
            else:
                end_2['季度'] = 0
            # 不同时间、季度的结果拼接为一个表格
            # ending1 = pd.concat([ending1, end_1], axis=0, ignore_index=True)
            end_2['剂型'] = k

            ending2 = pd.concat([ending2, end_2], axis=0, ignore_index=True)

    ending2['s1'] = ending2['mean + 0.5*sigma'] - ending2['IC_mean_1']
    ending2['s2'] = ending2['mean + sigma'] - ending2['IC_mean_1']
    ending2['预警等级'] = '良好'
    ending2.loc[ending2['s2'] < 0, '预警等级'] = '二级'
    ending2.loc[(ending2['s2'] >= 0) & (ending2['s1'] < 0), '预警等级'] = '一级'

    ending2 = ending2[['producer', '剂型', '年份', '季度',
                       'IC_mean_1', 'mean + 0.5*sigma', 'mean + sigma',
                       '预警等级']].rename(columns={'producer': '企业名称',
                                                'mean + 0.5*sigma': '第一预警线',
                                                'mean + sigma': '第二预警线',
                                                'IC_mean_1': '预警值'})
    if stype == 'adr_date_year':
        ending2.to_csv('企业1/企业2/不同企业按年.csv', index=0, encoding='utf-8-sig')
        return ending2
    else:
        ending2.to_csv('企业1/企业2/不同企业按季度.csv', index=0, encoding='utf-8-sig')
        return ending2


def med_enter(df, stype):
    np.seterr(divide='ignore', invalid='ignore')
    df = df[['producer', 'generic_name', '剂型', stype, '权重']].copy()
    df['a'] = df['b'] = df['c'] = df['d'] = df['权重']
    df = df[df['权重'] != 0]
    ending1 = pd.DataFrame()
    temp = df[stype].unique()
    for i in temp:  # 选择时间
        df_1 = df[df[stype] == i].copy()
        # 计算a
        grouped1 = df_1.groupby(['producer', 'generic_name', stype]) \
            .sum().reset_index()[['producer', 'generic_name', stype, 'a']]
        # 计算a+c
        grouped2 = df_1.groupby(['generic_name']).sum(). \
            reset_index()[['generic_name', 'c']]
        # 计算a+b
        grouped3 = df_1.groupby(['producer']).sum(). \
            reset_index()[['producer', 'b']]

        # a+b、a+c 贴入原始带a值的表格
        end_1 = pd.merge(grouped1, grouped3, on=['producer'])
        end_1 = pd.merge(end_1, grouped2, on=['generic_name'])
        # 计算最终四格表的a|b|c|d|n
        end_1['n'] = df_1['权重'].sum()
        end_1['b'] = (end_1['b'] - end_1['a'])
        end_1['c'] = (end_1['c'] - end_1['a'])
        end_1['d'] = end_1['n'] - end_1['b'] - end_1['a'] - end_1['c']
        # 加入一列(时间)
        end_1[stype] = i
        # Dataframe的值转为numpy数组存储，方便计算
        a = np.array(end_1['a'].values, dtype=float)
        b = np.array(end_1['b'].values, dtype=float)
        c = np.array(end_1['c'].values, dtype=float)
        d = np.array(end_1['d'].values, dtype=float)
        # 计算IC值，返回一列数据
        IC = Q_ic(a, b, c, d)
        # IC值贴入四格表 企业名称|药品名称|年份/季度|a|b|c|d|n|IC
        end_1['IC'] = IC
        # 选择给定企业
        # end_1 = end_1[end_1['producer'].isin(df_weight['producer'].values)]
        # 各个企业权重贴入四格表，重新计算IC值
        # end_1 = pd.merge(end_1, df_weight, on='producer')
        # end_1['IC'] = end_1['IC'] * end_1['weight']
        # 求每个企业所有IC的均值，命名为IC_mean_1
        mean = end_1.groupby(['generic_name']).agg('mean'). \
            reset_index()[['generic_name', 'IC']]. \
            rename(columns={'IC': 'IC_mean'})
        # 各个企业IC均值贴入四格表
        end_1 = pd.merge(end_1, mean, on='generic_name')
        std = end_1.groupby(['generic_name']).agg('std'). \
            reset_index()[['generic_name', 'IC']]. \
            rename(columns={'IC': 'IC_std'}).fillna(0)
        end_1 = pd.merge(end_1, std, on='generic_name')

        end_1['mean + 0.5*sigma'] = end_1['IC_mean'] + 0.5 * end_1['IC_std']
        # 计算第二预警值
        end_1['mean + sigma'] = end_1['IC_mean'] + end_1['IC_std']
        # 降序排列
        end_1.sort_values('IC', ascending=False, inplace=True)
        # 不同时间、季度的结果拼接为一个表格
        hhu = str(i)
        end_1['年份'] = hhu[0:4]
        if len(hhu)>4:
            end_1['季度'] = hhu[4]
        else:
            end_1['季度'] = 0
        ending1 = pd.concat([ending1, end_1], axis=0, ignore_index=True)

    ending1['s1'] = ending1['mean + 0.5*sigma'] - ending1['IC']
    ending1['s2'] = ending1['mean + sigma'] - ending1['IC']
    ending1['预警等级'] = '良好'
    ending1.loc[ending1['s2'] < 0, '预警等级'] = '二级'
    ending1.loc[(ending1['s2'] >= 0) & (ending1['s1'] < 0), '预警等级'] = '一级'
    # 选择输出列
    ending1 = ending1[['generic_name', 'producer', '年份', '季度',
                       'IC', 'mean + 0.5*sigma', 'mean + sigma', '预警等级']].\
        rename(columns={'producer': '企业名称',
                        'generic_name': '药品名称', 'IC': '预警值',
                        'mean + 0.5*sigma': '第一预警线',
                        'mean + sigma': '第二预警线'
    })
    if stype == 'adr_date_year':
        ending1.to_csv('企业1/不同企业相同药品按年.csv', index=0, encoding='utf-8-sig')
        return ending1
    else:
        ending1.to_csv('企业1/不同企业相同药品按季度.csv', index=0, encoding='utf-8-sig')
        return ending1



def enter_med(df, stype):
    np.seterr(divide='ignore', invalid='ignore')
    df = df[['producer', 'generic_name', '剂型', stype, '权重']].copy()
    df['a'] = df['b'] = df['c'] = df['d'] = df['权重']
    df = df[df['权重']!=0]
    ending2 = pd.DataFrame()
    temp = df[stype].unique()
    for i in temp:  # 选择季度
        df_1 = df[df[stype] == i].copy()
        # 计算a
        grouped1 = df_1.groupby(['producer', 'generic_name', stype]) \
            .count().reset_index()[['producer', 'generic_name', stype, 'a']]
        # 计算a+c
        grouped2 = df_1.groupby(['generic_name']).sum(). \
            reset_index()[['generic_name', 'c']]
        # 计算a+b
        grouped3 = df_1.groupby(['producer']).sum(). \
            reset_index()[['producer', 'b']]

        # a+b、a+c 贴入原始带a值的表格
        end_1 = pd.merge(grouped1, grouped3, on=['producer'])
        end_1 = pd.merge(end_1, grouped2, on=['generic_name'])
        # 计算最终四格表的a|b|c|d|n
        end_1['n'] = df_1['权重'].sum()
        end_1['b'] = (end_1['b'] - end_1['a'])
        end_1['c'] = (end_1['c'] - end_1['a'])
        end_1['d'] = end_1['n'] - end_1['b'] - end_1['a'] - end_1['c']
        # 加入一列(时间)
        end_1[stype] = i
        # Dataframe的值转为numpy数组存储，方便计算
        a = np.array(end_1['a'].values, dtype=float)
        b = np.array(end_1['b'].values, dtype=float)
        c = np.array(end_1['c'].values, dtype=float)
        d = np.array(end_1['d'].values, dtype=float)
        # 计算IC值，返回一列数据
        IC = Q_ic(a, b, c, d)
        # IC值贴入四格表 企业名称|药品名称|年份/季度|a|b|c|d|n|IC
        end_1['IC'] = IC
        # 选择给定企业
        # end_1 = end_1[end_1['producer'].isin(df_weight['producer'].values)]
        # 各个企业权重贴入四格表，重新计算IC值
        # end_1 = pd.merge(end_1, df_weight, on='producer')
        # end_1['IC'] = end_1['IC'] * end_1['weight']
        end_1.sort_values('IC', ascending=False, inplace=True)
        hhu = str(i)
        end_1['年份'] = hhu[0:4]
        if len(hhu) > 4:
            end_1['季度'] = hhu[4]
        else:
            end_1['季度'] = 0
        # 不同时间、季度的结果拼接为一个表格
        ending2 = pd.concat([ending2, end_1], axis=0, ignore_index=True)

    # 求每个企业所有IC的均值，命名为IC_mean_1
    mean = ending2.groupby(['producer', 'generic_name']).agg('mean'). \
        reset_index()[['producer', 'generic_name', 'IC']]. \
        rename(columns={'IC': 'IC_mean'})
    std = ending2.groupby(['producer', 'generic_name']).agg('std'). \
        reset_index()[['producer', 'generic_name', 'IC']]. \
        rename(columns={'IC': 'IC_std'})
    # 各个企业IC均值贴入四格表
    end_1 = pd.merge(ending2, mean, on=['producer', 'generic_name'])
    end_1 = pd.merge(end_1, std, on=['producer', 'generic_name'])
    end_1.fillna(0, inplace=True)
    # 计算第一预警值
    end_1['mean + 0.5*sigma'] = end_1['IC_mean'] + 0.5 * end_1['IC_std']
    # 计算第二预警值
    end_1['mean + sigma'] = end_1['IC_mean'] + end_1['IC_std']
    end_1['s1'] = end_1['mean + 0.5*sigma'] - end_1['IC']
    end_1['s2'] = end_1['mean + sigma'] - end_1['IC']
    end_1['预警等级'] = '良好'
    end_1.loc[end_1['s2'] < 0, '预警等级'] = '二级'
    end_1.loc[(end_1['s2'] >= 0) & (end_1['s1'] < 0), '预警等级'] = '一级'
    end_1 = end_1[['producer', 'generic_name', '年份',
                   '季度', 'IC', 'mean + 0.5*sigma', 'mean + sigma',
                   '预警等级']].rename(columns={'producer': '企业名称',
                                            'generic_name': '药品名称',
                                            'mean + 0.5*sigma': '第一预警线',
                                            'mean + sigma': '第二预警线',
                                            'IC': '预警值'})
    if stype == 'adr_date_year':
        end_1.to_csv('企业1/相同企业相同药品按年.csv', index=0, encoding='utf-8-sig')
        return end_1
    else:
        end_1.to_csv('企业1/相同企业相同药品按季度.csv', index=0, encoding='utf-8-sig')
        return end_1



def same_enter_med(df, stype):
    np.seterr(divide='ignore', invalid='ignore')
    df = df[['producer', 'generic_name', '剂型', stype, '权重']].copy()
    df['a'] = df['b'] = df['c'] = df['d'] = df['权重']
    df = df[df['权重'] != 0]
    ending2 = pd.DataFrame()
    temp = df[stype].unique()
    for i in temp:  # 选择季度
        df_1 = df[df[stype] == i].copy()
        # 计算a
        grouped1 = df_1.groupby(['producer', 'generic_name', stype]) \
            .sum().reset_index()[['producer', 'generic_name', stype, 'a']]
        # 计算a+c
        grouped2 = df_1.groupby(['generic_name']).sum(). \
            reset_index()[['generic_name', 'c']]
        # 计算a+b
        grouped3 = df_1.groupby(['producer']).sum(). \
            reset_index()[['producer', 'b']]

        # a+b、a+c 贴入原始带a值的表格
        end_1 = pd.merge(grouped1, grouped3, on=['producer'])
        end_1 = pd.merge(end_1, grouped2, on=['generic_name'])
        # 计算最终四格表的a|b|c|d|n
        end_1['n'] = df_1['权重'].sum()
        end_1['b'] = (end_1['b'] - end_1['a'])
        end_1['c'] = (end_1['c'] - end_1['a'])
        end_1['d'] = end_1['n'] - end_1['b'] - end_1['a'] - end_1['c']
        # 加入一列(时间)
        end_1[stype] = i
        # Dataframe的值转为numpy数组存储，方便计算
        a = np.array(end_1['a'].values, dtype=float)
        b = np.array(end_1['b'].values, dtype=float)
        c = np.array(end_1['c'].values, dtype=float)
        d = np.array(end_1['d'].values, dtype=float)
        # 计算IC值，返回一列数据
        IC = Q_ic(a, b, c, d)
        # IC值贴入四格表 企业名称|药品名称|年份/季度|a|b|c|d|n|IC
        end_1['IC'] = IC
        # 选择给定企业
        # end_1 = end_1[end_1['producer'].isin(df_weight['producer'].values)]
        # 各个企业权重贴入四格表，重新计算IC值
        # end_1 = pd.merge(end_1, df_weight, on='producer')
        # end_1['IC'] = end_1['IC'] * end_1['weight']
        # 求每个企业所有IC的均值，命名为IC_mean_1
        mean = end_1.groupby(['producer']).agg('mean').\
            reset_index()[['producer', 'IC']]. \
            rename(columns={'IC': 'IC_mean_1'})
        # 各个企业IC均值贴入四格表
        end_1 = pd.merge(end_1, mean, on='producer')
        # 去掉企业名称的重复项，每个企业数据只保留一行
        end_2 = end_1.drop_duplicates(subset=['producer'], keep='first').copy()
        hhu = str(i)
        end_2['年份'] = hhu[0:4]
        if len(hhu) > 4:
            end_2['季度'] = hhu[4]
        else:
            end_2['季度'] = 0
        # 不同时间、季度的结果拼接为一个表格
        ending2 = pd.concat([ending2, end_2], axis=0, ignore_index=True)

    mean = ending2.groupby('producer').agg('mean'). \
        reset_index()[['producer', 'IC_mean_1']]. \
        rename(columns={'IC_mean_1': 'IC_mean'})
    std = ending2.groupby('producer').agg('std'). \
        reset_index()[['producer', 'IC_mean_1']]. \
        rename(columns={'IC_mean_1': 'IC_std'})
    end_1 = pd.merge(ending2, mean, on='producer')
    end_1 = pd.merge(end_1, std, on='producer')
    end_1.fillna(0, inplace=True)

    end_1['mean + 0.5*sigma'] = end_1['IC_mean'] + 0.5 * end_1['IC_std']
    end_1['mean + sigma'] = end_1['IC_mean'] + end_1['IC_std']

    end_1['s1'] = end_1['mean + 0.5*sigma'] - end_1['IC_mean_1']
    end_1['s2'] = end_1['mean + sigma'] - end_1['IC_mean_1']
    end_1['预警等级'] = '良好'
    end_1.loc[end_1['s2'] < 0, '预警等级'] = '二级'
    end_1.loc[(end_1['s2'] >= 0) & (end_1['s1'] < 0), '预警等级'] = '一级'
    end_1 = end_1[['producer', '年份', '季度',
                   'IC_mean_1', 'mean + 0.5*sigma', 'mean + sigma',
                   '预警等级']].rename(columns={'producer': '企业名称',
                                            'mean + 0.5*sigma': '第一预警线',
                                            'mean + sigma': '第二预警线',
                                            'IC_mean_1': '预警值'})
    if stype == 'adr_date_year':
        end_1.to_csv('企业1/相同企业按年.csv', index=0, encoding='utf-8-sig')
    else:
        end_1.to_csv('企业1/相同企业按季度.csv', index=0, encoding='utf-8-sig')
    return end_1

