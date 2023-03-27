# -*- coding: gb2312 -*-

import pandas as pd
import numpy as np
import data_prod_name as dpn
import matplotlib.pyplot as plt


def drow_0(x_1, y, med=''):
    names = x_1
    x = range(1, len(x_1) + 1)
    plt.plot(x, y, marker='o', mec='green', mfc='w', zorder=1)
    plt.title(med+'不良反应计数')
    plt.xticks(x, names, rotation=35)
    plt.xlabel(u"时间")
    plt.ylabel(u"不良反应数")  # Y轴标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.grid(True)
    plt.show()


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
            df = pd.read_csv('加权Bagging法.csv', encoding='utf-8-sig')
        elif ch1 == 2:
            df = pd.read_csv('经典Bagging法.csv', encoding='utf-8-sig')
        elif ch1 == 3:
            df = pd.read_csv('加权BCPNN法.csv', encoding='utf-8-sig')
        elif ch1 == 4:
            df = pd.read_csv('经典BCPNN法.csv', encoding='utf-8-sig')
        elif ch1 == 5:
            df = pd.read_csv('加权MHRA法.csv', encoding='utf-8-sig')
        elif ch1 == 6:
            df = pd.read_csv('经典MHRA法.csv', encoding='utf-8-sig')
        elif ch1 == 7:
            df = pd.read_csv('加权PRR法.csv', encoding='utf-8-sig')
        elif ch1 == 8:
            df = pd.read_csv('经典PRR法.csv', encoding='utf-8-sig')
        elif ch1 == 9:
            df = pd.read_csv('加权ROR法.csv', encoding='utf-8-sig')
        elif ch1 == 10:
            df = pd.read_csv('经典ROR法.csv', encoding='utf-8-sig')
        elif ch1 == 11:
            df = pd.read_csv('加权YuleQ法.csv', encoding='utf-8-sig')
        elif ch1 == 12:
            df = pd.read_csv('经典YuleQ法.csv', encoding='utf-8-sig')
        else:
            print('选择错误！\n')
            continue
        print('--------可选择的药品------\n')
        jjj = df[df['药品名称'].isin(l1)]['药品名称'].unique()
        mff = med[med['药品'].isin(jjj)]['药品名称'].unique()
        print(mff)
        ch_med = input('请输入药品名：')
        ch_med = med_fl(ch_med)
        end_data = df[df['药品名称'] == ch_med]
        end_data = end_data.sort_values(['年份', '季度'])
        end_data['s1'] = '年第'
        end_data['s2'] = '季度'
        end_data['时间'] = end_data['年份'].apply(str) + end_data['s1']\
                         + end_data['季度'].apply(str) + end_data['s2']
        x = end_data['时间'].values
        y = end_data['不良反应数'].values
        drow_0(x, y, ch_med)
        end_data = end_data[['药品名称', '年份', '季度', '不良反应数']]
        print(end_data)
        dh = input('是（1）否（0）继续：')
        if dh == '0':
            break

