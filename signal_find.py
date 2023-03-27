# -*- coding: gb2312 -*-

import pandas as pd
import numpy as np
import data_prod_name as dpn


def med_fl(s):
    s1 = ['注射用', '吸入用', '吸入', ' ', '-']
    for i in s1:
        s = s.replace(i, '')

    s2 = ['控释片', '注射液', '滴眼液', '滴丸', '复合包装', '分散片', '片', '气雾剂', '注射剂',
          '软胶囊',  '胶囊', '分散', '颗粒', '糖浆', '胶囊', '干混悬剂', '肠溶', '肠溶液',
          '肠溶缓释', '泡腾', '含', '搽剂', '滴眼液', '咀嚼', '注射用无菌粉末', '合剂',
          '氯化钠', '缓释', '贴膏', '混悬液', '凝胶', '肠溶', '口服溶液', '口崩', '透皮贴剂',
          '口腔崩解', '溶液', '贴', '滴鼻剂', '软膏', '浸膏', '乳状', '针', '口服', '无',
          '喷雾剂', '雾化剂', '雾化液', '浸液', '粉剂', '营养', '乳剂', '洗剂', '滴耳液'
          '洗液', '葡萄糖', '酚', '阴道栓', '电解质散', '含漱液', '止痛膏', '粉雾剂',
          '冲剂', '眼用', '眼膏', 'J', '口腔粘贴', '阴道', '栓', '酯', '冷敷', '浓',
          '滴剂', '肠溶微', '贴剂', '乳胶剂', '丸', '喷剂', '粉吸入剂', '吸入粉雾剂',
          '滴耳液']
    for i in s2:
        if i in s:
            s = s.rstrip(i)
    return s


if __name__ == '__main__':
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    # 对齐这两个参数的默认设置都是False
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    med = pd.read_excel('药品.xlsx')
    med['药品'] = med['药品名称'].apply(med_fl)

    _ = pd.read_excel('../../企业信息.xlsx', sheet_name='Sheet1')
    df_w = pd.DataFrame()
    df_w[['producer', 'producer_id']] = _[['名单名(药监局)', 'id']].copy()
    df_w = dpn.data_p_name(df_w)
    pro = df_w['producer'].unique()

    l1 = med['药品'].unique()
    hhu = 1
    while(hhu):
        ch1 = int(input('请选择信号检测算法：\n'
                        '1.加权Bagging\n'
                        '2.经典Bagging\n'
                        '3.加权BCPNN\n'
                        '4.经典BCPNN\n'
                        '5.加权MHRA\n'
                        '6.经典MHRA\n'
                        '7.加权PRR\n'
                        '8.经典PRR\n'
                        '9.加权ROR\n'
                        '10.经典ROR\n'
                        '11.加权YuleQ\n'
                        '12.经典YuleQ\n'))
        if ch1 == 1:
            df = pd.read_csv('加权Bagging信号.csv', encoding='utf-8-sig')
        elif ch1 == 2:
            df = pd.read_csv('经典Bagging信号.csv', encoding='utf-8-sig')
        elif ch1 == 3:
            df = pd.read_csv('加权BCPNN信号.csv', encoding='utf-8-sig')
        elif ch1 == 4:
            df = pd.read_csv('经典BCPNN信号.csv', encoding='utf-8-sig')
        elif ch1 == 5:
            df = pd.read_csv('加权MHRA信号.csv', encoding='utf-8-sig')
        elif ch1 == 6:
            df = pd.read_csv('经典MHRA信号.csv', encoding='utf-8-sig')
        elif ch1 == 7:
            df = pd.read_csv('加权PRR信号.csv', encoding='utf-8-sig')
        elif ch1 == 8:
            df = pd.read_csv('经典PRR信号.csv', encoding='utf-8-sig')
        elif ch1 == 9:
            df = pd.read_csv('加权ROR信号.csv', encoding='utf-8-sig')
        elif ch1 == 10:
            df = pd.read_csv('经典ROR信号.csv', encoding='utf-8-sig')
        elif ch1 == 11:
            df = pd.read_csv('加权YuleQ信号.csv', encoding='utf-8-sig')
        elif ch1 == 12:
            df = pd.read_csv('经典YuleQ信号.csv', encoding='utf-8-sig')
        else:
            print('选择错误！\n')
            continue
        print('--------可选择的药品------\n')
        jjj = df[df['药品名称'].isin(l1)]['药品名称'].unique()
        mff = med[med['药品'].isin(jjj)]['药品名称'].unique()
        print(mff)
        ch_med = input('请输入药品名：')
        ch_med = med_fl(ch_med)
        end_data = df[df['药品名称'] == ch_med].copy()
        end_data.drop_duplicates(subset=['药品名称', '不良反应id'], inplace=True, keep='first')
        sp = 1
        while(sp):
            ch2 = input('展示所有不良反应（0）/新的不良反应（1）：')
            if ch2 == '0':
                end_data_all = end_data[['药品名称', '不良反应名称']]
                if end_data_all.shape[0] == 0:
                    print('未从数据库中检测到该药品的不良反应！\n')
                else:
                    print('所有不良反应:\n')
                    print('共检测到不良反应', end_data_all.shape[0], '个。\n')
                    print(end_data_all)
            else:
                end_data_new = end_data[end_data['是否新信号'] == 1][['药品名称', '不良反应名称',
                                                                 '年份', '季度']].rename(columns={
                    '年份': '首次检出年份', '季度': '首次检出季度'})
                if end_data_new.shape[0] == 0:
                    print('未从数据库中检测到该药品的不良反应！\n')
                else:
                    print('新的不良反应:\n')
                    print('共检测到新的不良反应', end_data_new.shape[0], '个。\n')
                    print(end_data_new)
            ch3 = input('重新展示1/重新查询0/退出（else）：')
            if ch3 == '0':
                sp = 0

        dh = input('是（1）否（0）继续查询：')
        if dh == '0':
            break

