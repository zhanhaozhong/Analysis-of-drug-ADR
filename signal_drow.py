# -*- coding: gb2312 -*-

import pandas as pd
import numpy as np
import data_prod_name as dpn
import matplotlib.pyplot as plt


def drow_0(x_1, y, med=''):
    names = x_1
    x = range(1, len(x_1) + 1)
    plt.plot(x, y, marker='o', mec='green', mfc='w', zorder=1)
    plt.title(med+'������Ӧ����')
    plt.xticks(x, names, rotation=35)
    plt.xlabel(u"ʱ��")
    plt.ylabel(u"������Ӧ��")  # Y���ǩ
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.grid(True)
    plt.show()


def med_fl(s):
    s1 = ['ע����', '������', '����', ' ', '-']
    for i in s1:
        s = s.replace(i, '')

    s2 = ['����Ƭ', 'ע��Һ', '����Һ', '����', '���ϰ�װ', '��ɢƬ', 'Ƭ', '�����', 'ע���',
          '����',  '����', '��ɢ', '����', '�ǽ�', '����', '�ɻ�����', '����', '����Һ',
          '���ܻ���', '����', '��', '���', '����Һ', '�׽�', 'ע�����޾���ĩ', '�ϼ�',
          '�Ȼ���', '����', '����', '����Һ', '����', '����', '�ڷ���Һ', '�ڱ�', '͸Ƥ����',
          '��ǻ����', '��Һ', '��', '�αǼ�', '���', '����', '��״', '��', '�ڷ�', '��',
          '�����', '����', '��Һ', '��Һ', '�ۼ�', 'Ӫ��', '���', 'ϴ��', '�ζ�Һ'
          'ϴҺ', '������', '��', '����˨', '�����ɢ', '����Һ', 'ֹʹ��', '�����',
          '���', '����', '�۸�', 'J', '��ǻճ��', '����', '˨', '��', '���', 'Ũ',
          '�μ�', '����΢', '����', '�齺��', '��', '���', '�������', '��������',
          '�ζ�Һ']
    for i in s2:
        if i in s:
            s = s.rstrip(i)
    return s


if __name__ == '__main__':
    med = pd.read_excel('ҩƷ.xlsx')
    med['ҩƷ'] = med['ҩƷ����'].apply(med_fl)

    _ = pd.read_excel('../../��ҵ��Ϣ.xlsx', sheet_name='Sheet1')
    df_w = pd.DataFrame()
    df_w[['producer', 'producer_id']] = _[['������(ҩ���)', 'id']].copy()
    df_w = dpn.data_p_name(df_w)
    pro = df_w['producer'].unique()

    l1 = med['ҩƷ'].unique()

    hhu = 1
    while(hhu):
        ch1 = int(input('��ѡ���źż���㷨��\n'
                        '1.��ȨBagging\n'
                        '2.����Bagging\n'
                        '3.��ȨBCPNN\n'
                        '4.����BCPNN\n'
                        '5.��ȨMHRA\n'
                        '6.����MHRA\n'
                        '7.��ȨPRR\n'
                        '8.����PRR\n'
                        '9.��ȨROR\n'
                        '10.����ROR\n'
                        '11.��ȨYuleQ\n'
                        '12.����YuleQ\n'))
        if ch1 == 1:
            df = pd.read_csv('��ȨBagging��.csv', encoding='utf-8-sig')
        elif ch1 == 2:
            df = pd.read_csv('����Bagging��.csv', encoding='utf-8-sig')
        elif ch1 == 3:
            df = pd.read_csv('��ȨBCPNN��.csv', encoding='utf-8-sig')
        elif ch1 == 4:
            df = pd.read_csv('����BCPNN��.csv', encoding='utf-8-sig')
        elif ch1 == 5:
            df = pd.read_csv('��ȨMHRA��.csv', encoding='utf-8-sig')
        elif ch1 == 6:
            df = pd.read_csv('����MHRA��.csv', encoding='utf-8-sig')
        elif ch1 == 7:
            df = pd.read_csv('��ȨPRR��.csv', encoding='utf-8-sig')
        elif ch1 == 8:
            df = pd.read_csv('����PRR��.csv', encoding='utf-8-sig')
        elif ch1 == 9:
            df = pd.read_csv('��ȨROR��.csv', encoding='utf-8-sig')
        elif ch1 == 10:
            df = pd.read_csv('����ROR��.csv', encoding='utf-8-sig')
        elif ch1 == 11:
            df = pd.read_csv('��ȨYuleQ��.csv', encoding='utf-8-sig')
        elif ch1 == 12:
            df = pd.read_csv('����YuleQ��.csv', encoding='utf-8-sig')
        else:
            print('ѡ�����\n')
            continue
        print('--------��ѡ���ҩƷ------\n')
        jjj = df[df['ҩƷ����'].isin(l1)]['ҩƷ����'].unique()
        mff = med[med['ҩƷ'].isin(jjj)]['ҩƷ����'].unique()
        print(mff)
        ch_med = input('������ҩƷ����')
        ch_med = med_fl(ch_med)
        end_data = df[df['ҩƷ����'] == ch_med]
        end_data = end_data.sort_values(['���', '����'])
        end_data['s1'] = '���'
        end_data['s2'] = '����'
        end_data['ʱ��'] = end_data['���'].apply(str) + end_data['s1']\
                         + end_data['����'].apply(str) + end_data['s2']
        x = end_data['ʱ��'].values
        y = end_data['������Ӧ��'].values
        drow_0(x, y, ch_med)
        end_data = end_data[['ҩƷ����', '���', '����', '������Ӧ��']]
        print(end_data)
        dh = input('�ǣ�1����0��������')
        if dh == '0':
            break

