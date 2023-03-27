# -*- coding: gb2312 -*-

import pandas as pd
import numpy as np
import data_prod_name as dpn


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
    # ��ʾ������
    pd.set_option('display.max_columns', None)
    # ��ʾ������
    pd.set_option('display.max_rows', None)
    # ����value����ʾ����Ϊ100��Ĭ��Ϊ50
    pd.set_option('max_colwidth', 100)
    # ����������������Ĭ�����ö���False
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
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
            df = pd.read_csv('��ȨBagging�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 2:
            df = pd.read_csv('����Bagging�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 3:
            df = pd.read_csv('��ȨBCPNN�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 4:
            df = pd.read_csv('����BCPNN�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 5:
            df = pd.read_csv('��ȨMHRA�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 6:
            df = pd.read_csv('����MHRA�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 7:
            df = pd.read_csv('��ȨPRR�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 8:
            df = pd.read_csv('����PRR�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 9:
            df = pd.read_csv('��ȨROR�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 10:
            df = pd.read_csv('����ROR�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 11:
            df = pd.read_csv('��ȨYuleQ�ź�.csv', encoding='utf-8-sig')
        elif ch1 == 12:
            df = pd.read_csv('����YuleQ�ź�.csv', encoding='utf-8-sig')
        else:
            print('ѡ�����\n')
            continue
        print('--------��ѡ���ҩƷ------\n')
        jjj = df[df['ҩƷ����'].isin(l1)]['ҩƷ����'].unique()
        mff = med[med['ҩƷ'].isin(jjj)]['ҩƷ����'].unique()
        print(mff)
        ch_med = input('������ҩƷ����')
        ch_med = med_fl(ch_med)
        end_data = df[df['ҩƷ����'] == ch_med].copy()
        end_data.drop_duplicates(subset=['ҩƷ����', '������Ӧid'], inplace=True, keep='first')
        sp = 1
        while(sp):
            ch2 = input('չʾ���в�����Ӧ��0��/�µĲ�����Ӧ��1����')
            if ch2 == '0':
                end_data_all = end_data[['ҩƷ����', '������Ӧ����']]
                if end_data_all.shape[0] == 0:
                    print('δ�����ݿ��м�⵽��ҩƷ�Ĳ�����Ӧ��\n')
                else:
                    print('���в�����Ӧ:\n')
                    print('����⵽������Ӧ', end_data_all.shape[0], '����\n')
                    print(end_data_all)
            else:
                end_data_new = end_data[end_data['�Ƿ����ź�'] == 1][['ҩƷ����', '������Ӧ����',
                                                                 '���', '����']].rename(columns={
                    '���': '�״μ�����', '����': '�״μ������'})
                if end_data_new.shape[0] == 0:
                    print('δ�����ݿ��м�⵽��ҩƷ�Ĳ�����Ӧ��\n')
                else:
                    print('�µĲ�����Ӧ:\n')
                    print('����⵽�µĲ�����Ӧ', end_data_new.shape[0], '����\n')
                    print(end_data_new)
            ch3 = input('����չʾ1/���²�ѯ0/�˳���else����')
            if ch3 == '0':
                sp = 0

        dh = input('�ǣ�1����0��������ѯ��')
        if dh == '0':
            break

