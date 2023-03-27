# -*- coding: gb2312 -*-

import sqlalchemy as sqla
import pandas as pd
import time
import data_med_fliter as dmf
import F_count
import signal_test
import jxing_fliter as jf
import data_get
import med_score
import numpy as np


def quater_one(x):
    x = str(x)
    x = x[:4]
    return x


def quater_two(x):
    x = str(x)
    x = x[4]
    return x


def im_data():
    start = time.time()
    db = sqla.create_engine('sqlite:///adr.db')
    print(db.engine.table_names())
    s = pd.read_sql('select adr.*,report_raw.* from adr left '
                    'join report_raw on adr.report_id=report_raw.id ', db)

    fy_name = pd.read_sql('select meddra.* from meddra ', db)
    end = time.time()
    print('从数据库中读取数据耗时：', end - start, 's')
    return s, fy_name


def medscore(df, table, method=0):
    # if method == 0:
    test_0 = df[['generic_name', 'adr_date_quarter',
                 'delivery_way', 'serious_adr_level']].copy()
    temp1 = test_0['generic_name'].copy()
    temp2 = temp1.value_counts()
    a1 = set(temp2[temp2 >= 6].index.values)
    del temp1, temp2
    dddd = test_0['adr_date_quarter'].unique()
    end_df = pd.DataFrame()
    start = time.time()
    for i in dddd:
        test = test_0[test_0['adr_date_quarter'] <= i].copy()
        # test = test_0[test_0['adr_date_quarter'] == i].copy()
        cod = med_score.Med_score(test, a1)
        cod['adr_date_year'] = i[0:4]
        cod['adr_date_quarter'] = i[4]
        end_df = pd.concat([end_df, cod], axis=0, ignore_index=True)
    end = time.time()
    end_df.rename(columns={'generic_name': '药品名称',
                           'level_score': '药品评估值',
                           'report_numbers': '报告数',
                           'serious_adr_level': '不良反应严重程度等级',
                           'adr_date_year': '年份',
                           'adr_date_quarter': '季度'},
                  inplace=True)
    end_df = pd.merge(end_df, table, how='inner', on=['药品名称', '年份', '季度'])[
        ['药品名称', '药品评估值', '报告数', '不良反应严重程度等级', '年份', '季度',
         '一般报告数', '严重报告数']]

    ending = end_df.sort_values(by=['年份', '季度'], axis=0, ascending=True)
    ending.to_csv('药品质量/分季度药品质量.csv', encoding='utf-8-sig', index=False)
    print('药品评级耗时:', end - start, 's')
    return end_df
    # elif method == 1:
    #     test = df[['generic_name', 'adr_date_year',
    #                'delivery_way', 'serious_adr_level']].copy()
    #     start = time.time()
    #     cod = med_score.Med_score(test)
    #     end = time.time()
    #     cod.rename(columns={
    #         'generic_name': '药品名称',
    #         'level_score': '药品评估值',
    #         'report_numbers': '报告数',
    #         'serious_adr_level': '不良反应严重程度等级'}, inplace=True)
    #     cod = pd.merge(cod, table, how='outer', on=['药品名称', '年份', '季度'])[
    #         ['药品名称', '药品评估值', '报告数', '不良反应严重程度等级', '年份', '季度',
    #          '一般报告数', '严重报告数']]
    #     cod.to_csv('药品质量/总数据库药品质量.csv', encoding='utf-8-sig', index=0)
    #     print('药品评级耗时:', end - start, 's')
    #     return cod
    # else:
    #     test_0 = df[['generic_name', 'adr_date_year',
    #                  'delivery_way', 'serious_adr_level']].copy()
    #     dddd = test_0['adr_date_year'].unique()
    #     end_df = pd.DataFrame()
    #     start = time.time()
    #     for i in dddd:
    #         test = test_0[test_0['adr_date_year'] <= i].copy()
    #         cod = med_score.Med_score(test)
    #         cod['adr_date_year'] = i
    #         end_df = pd.concat([end_df, cod], axis=0, ignore_index=True)
    #     # end_df.rename()
    #     end = time.time()
    #     end_df.rename(columns={'generic_name': '药品名称',
    #                            'level_score': '药品评估值',
    #                            'report_numbers': '报告数',
    #                            'serious_adr_level': '不良反应严重程度等级',
    #                            'adr_date_year': '年份'},
    #                   inplace=True)
    #     table.drop_duplicates(['药品名称', '年份'], keep='last', inplace=True)
    #     end_df = pd.merge(end_df, table, how='inner', on=['药品名称', '年份', ])[
    #         ['药品名称', '药品评估值', '报告数', '不良反应严重程度等级', '年份',
    #          '一般报告数', '严重报告数']]
    #     end_df.to_csv('药品质量/按年份药品质量00.csv', encoding='utf-8-sig', index=0)
    #     print('药品评级耗时:', end - start, 's')
    #     return end_df


def ready_data():
    s, fyname = im_data()
    new_colname = list(s.columns)
    new_colname[5] = 'drop'
    s.columns = new_colname
    s.drop(['drop'], axis=1, inplace=True)
    s = s[['id', 'report_id', 'meddra_id', 'name', 'code', 'gender',
           'age', 'is_new', 'severity', 'serious_adr', 'suspect_or_blend',
           'drug_sn', 'generic_name', 'potion_form', 'producer', 'delivery_way',
           'duration_start_date', 'duration_end_date', 'adr_date',
           'adr_result', 'sequelae', 'death_date', 'cause_of_death',
           'whether_disappear_after_stop', 'whether_same_after_medication',
           'effect_on_disease', 'reportor_evaluation', 'reporting_unit_evaluation',
           'reportor_profession', 'reporting_unit_name', 'report_source',
           'district_evaluation', 'city_evaluation', 'province_evaluation',
           'nation_evaluation']]
    s.rename(columns={'generic_name': 'm_firstname'}, inplace=True)

    name = pd.read_excel('药品名称映射表.xlsx', sheet_name='Sheet1')
    ds1 = pd.merge(s, name, on='m_firstname').dropna(subset=['generic_name']).copy()

    ds = dmf.adr_level(ds1).copy()


    del ds1
    year = ['2014', '2015', '2016', '2017', '2018', '2019']  # 选择年份数据
    start = time.time()
    df = data_get.data_get(ds, year)
    end = time.time()
    print('获取使用数据耗时：', end - start, 's')
    fyname.rename(columns={'id': 'meddra_id'}, inplace=True)
    del fyname['created_at'], fyname['updated_at'], df['name']
    df = pd.merge(df, fyname, on=['meddra_id'], how='inner')

    return df


def m_s_count(df):
    sl = list(df.columns)
    sl[8] = 'now_used'
    df.columns = sl
    df = df[['now_used', 'generic_name', 'adr_date_quarter']].rename(columns={
        'now_used': 'severity'}).copy()
    df['ap'] = 1
    dddd = sorted(df['adr_date_quarter'].unique())
    ending = pd.DataFrame()
    for i in dddd:
        dg = df[df['adr_date_quarter'] <= i].copy()
        grouped1 = dg.groupby(['generic_name', 'severity']).sum().reset_index()[['generic_name', 'severity', 'ap']]
        grouped1['adr_date_quarter'] = i
        ending = pd.concat([ending, grouped1], axis=0, ignore_index=True)

    table = pd.pivot_table(ending, values='ap', index=['adr_date_quarter', 'generic_name'],
                           columns=['severity'], fill_value=0, aggfunc=np.sum).reset_index()
    table['年份'] = table['adr_date_quarter'].apply(quater_one)
    table['季度'] = table['adr_date_quarter'].apply(quater_two)
    table.rename(columns={
        'generic_name': '药品名称', '一般': '一般报告数', '严重': '严重报告数'}, inplace=True)
    return table


def signal_num(df):
    df['num'] = 1
    df1 = df[df['是否新信号'] == 1]
    df2 = df[df['是否新信号'] == 0]
    grouped1 = df2.groupby(['算法', '时间', '药品名称'])['不良反应名称']. \
        apply(lambda x: x.str.cat(sep=',')).reset_index().rename(columns={
        '不良反应名称': '已知信号'})
    grouped1['已知信号个数'] = df2.groupby(['算法', '时间', '药品名称']). \
        sum().reset_index()['num']
    # grouped1.to_csv('经典信号已知.csv', index=0, encoding='utf-8-sig')
    grouped2 = df1.groupby(['算法', '时间', '药品名称'])['不良反应名称']. \
        apply(lambda x: x.str.cat(sep=',')).reset_index().rename(columns={
        '不良反应名称': '新的信号'})
    grouped2['新的信号个数'] = df1.groupby(['算法', '时间', '药品名称']). \
        sum().reset_index()['num']

    enddf = pd.merge(grouped1, grouped2, on=['算法', '时间', '药品名称'], how='outer')
    enddf['新的信号个数'].fillna(0, inplace=True)
    ss = enddf['时间'].str.split('年', expand=True)
    cf = ss[1].str.split('季度', expand=True)[0]
    enddf['年份'] = ss[0]
    enddf['季度'] = cf

    return enddf


def signal_find(ob, ss):
    start = time.time()
    df11, _ = signal_test.mhraaaaaaaa(ob, ss)
    df2, _ = signal_test.bllll(ob, ss)
    df3, _ = signal_test.prrrr(ob, ss)
    df4, _ = signal_test.rorrrrr(ob, ss)
    df5, _ = signal_test.qqqqqqqqq(ob, ss)

    _, df1 = signal_test.mhraaaaaaaa(ob, ss)
    _, df1 = signal_test.bllll(df1, ss)
    _, df1 = signal_test.prrrr(df1, ss)
    _, df1 = signal_test.rorrrrr(df1, ss)
    _, df1 = signal_test.qqqqqqqqq(df1, ss)
    df6, _ = signal_test.Bagging(df1, ss)
    end = time.time()
    df_01 = pd.concat([df11, df2, df3, df4, df5, df6], axis=0, ignore_index=True)
    print('信号检测耗时：', end - start, 's')
    df_01 = df_01[['药品名称', '不良反应id', '不良反应名称', '是否新信号',
                   '时间', '算法']]
    jieguo = signal_num(df_01)  # 信号检测结果
    return jieguo


if __name__ == '__main__':
    year = ['2014', '2015', '2016', '2017', '2018', '2019']
    df = ready_data()

    s = 1
    while s != 0:
        ot = int(input('请选择(0退出，1药品评价季度，2药品评价ALL，3药品评价年，4信号检测)：\n'))
        if 1<=ot<=3:
            table = m_s_count(df)
            # table.to_excel('aaa.xlsx', sheet_name='Sheet1')
            medscore_0 = medscore(df, table, method=0)  # 按季度计算药品质量

        elif ot == 4:  # 构造四格表，检测信号
            dfg = jf.find_new(df)
            menthod_0 = 'adr_date_quarter'
            ss = int(input('选择四格表（0-经典, 1-加权）：\n'))
            if ss == 0:  # 经典结果
                start = time.time()
                ob = F_count.count_other(dfg, year, menthod_0)  # 普通四格表
                end = time.time()
                print('药品不良反应四格表构造耗时：', end - start, 's')
                resulted = signal_find(ob, ss)
                #resulted.to_csv('信号检测结果经典.csv', encoding='utf-8-sig', index=False)
                resulted.to_excel('信号检测结果经典.xlsx', sheet_name='Sheet1')
            else:
                start = time.time()
                df11 = dmf.report_weight(dfg)  # 报告权重
                ob = F_count.count_other_se(df11, year, menthod_0)
                end = time.time()
                print('药品不良反应四格表构造耗时：', end - start, 's')
                resulted = signal_find(ob, ss)
                #resulted.to_csv('信号检测结果加权.csv', encoding='utf-8-sig', index=False)
                resulted.to_excel('信号检测结果加权.xlsx', sheet_name='Sheet1')
        elif ot == 0:
            s = 0
