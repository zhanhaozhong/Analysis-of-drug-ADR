import pandas as pd
import numpy as np
import time


def Med_score(data0, a2):
    medname = []
    medscore = []
    num = []
    a0 = data0['generic_name'].unique()
    a1 = list(set(a0)&a2)
    del a0, a2
    # a1 = ['多西他赛（注射液等）', '紫杉醇（注射液等）']
    for i in a1:
        # print('药品名称:', i)
        data = data0[data0['generic_name'] == i]
        # print('涉及报告数量:', data.shape[0])
        # if data.shape[0] < 6:
        #     continue
        # print(i, data.shape[0])
        medname.append(i)
        num.append(data.shape[0])
        grouped = data.groupby('delivery_way').count().reset_index()
        s_index = grouped.iloc[:, 0].values
        D = data.groupby(['delivery_way', 'serious_adr_level']).count().unstack().reset_index().fillna(0)
        s_num = grouped.iloc[:, 1].values
        A = pd.Series(s_num, index=s_index)
        A = A / A.sum()

        for i in D['generic_name'].columns:
            if i == 1:
                D['generic_name', i] = D['generic_name', i] * 0.01
            elif i == 2:
                D['generic_name', i] = D['generic_name', i] * 0.0352
            elif i == 3:
                D['generic_name', i] = D['generic_name', i] * 0.0754
            elif i == 4:
                D['generic_name', i] = D['generic_name', i] * 0.1507
            elif i == 5:
                D['generic_name', i] = D['generic_name', i] * 0.2764
            elif i == 6:
                D['generic_name', i] = D['generic_name', i] * 0.4523
        # for i in D['generic_name'].columns:
        #     if i == 1:
        #         D['generic_name', i] = D['generic_name', i] * (1/36)
        #     elif i == 2:
        #         D['generic_name', i] = D['generic_name', i] * (3/36)
        #     elif i == 3:
        #         D['generic_name', i] = D['generic_name', i] * (5/36)
        #     elif i == 4:
        #         D['generic_name', i] = D['generic_name', i] * (7/36)
        #     elif i == 5:
        #         D['generic_name', i] = D['generic_name', i] * (9/36)
        #     elif i == 6:
        #         D['generic_name', i] = D['generic_name', i] * (11/36)
        he = D.sum(axis=1)
        col = D['generic_name'].columns
        for i in col:
            D['generic_name', i] = D['generic_name', i] / he
        # print(D)  # D['generic_name'].values输出评价矩阵
        # print(A)
        D['generic_name', 'w'] = A.values
        for j in col[:-1]:
            for i in D.index:
                D.loc[i, ('generic_name', j)] = min(D['generic_name', j][i], D['generic_name', 'w'][i])
        # print(D)
        D = D['generic_name'][col]
        Dl = D.copy()
        Dl.index = A.index
        # print(Dl) # 评价矩阵
        # print(A) # 权重
        D = D.sum() / D.sum().sum()
        d_index = D.index
        # print(D)
        C = D.copy()
        d_left = D.copy()  # 0 * c[0] + 4 * c[1] + 10 * c[2] + 20 * c[3] + 40 * c[4] + 70 * c[5]
        d_right = D.copy()  # 4 * c[0] + 10 * c[1] + 20 * c[2] + 40 * c[3] + 70 * c[4] + 110 * c[5]
        for i in d_index:
            if i == 1:
                C[i] = D[i] * 2
                d_left[i] = d_left[i] * 0
                d_right[i] = d_right[i] * 4
            elif i == 2:
                C[i] = D[i] * 7
                d_left[i] = d_left[i] * 4
                d_right[i] = d_right[i] * 10
            elif i == 3:
                C[i] = D[i] * 15
                d_left[i] = d_left[i] * 10
                d_right[i] = d_right[i] * 20
            elif i == 4:
                C[i] = D[i] * 30
                d_left[i] = d_left[i] * 20
                d_right[i] = d_right[i] * 40
            elif i == 5:
                C[i] = D[i] * 55
                d_left[i] = d_left[i] * 40
                d_right[i] = d_right[i] * 70
            elif i == 6:
                C[i] = D[i] * 90
                d_left[i] = d_left[i] * 70
                d_right[i] = d_right[i] * 110
        # for i in d_index:
        #     if i == 1:
        #         C[i] = D[i] * 0.5
        #         d_left[i] = d_left[i] * 0
        #         d_right[i] = d_right[i] * 1
        #     elif i == 2:
        #         C[i] = D[i] * 1.5
        #         d_left[i] = d_left[i] * 1
        #         d_right[i] = d_right[i] * 2
        #     elif i == 3:
        #         C[i] = D[i] * 2.5
        #         d_left[i] = d_left[i] * 2
        #         d_right[i] = d_right[i] * 3
        #     elif i == 4:
        #         C[i] = D[i] * 3.5
        #         d_left[i] = d_left[i] * 3
        #         d_right[i] = d_right[i] * 4
        #     elif i == 5:
        #         C[i] = D[i] * 4.5
        #         d_left[i] = d_left[i] * 4
        #         d_right[i] = d_right[i] * 5
        #     elif i == 6:
        #         C[i] = D[i] * 5.5
        #         d_left[i] = d_left[i] * 5
        #         d_right[i] = d_right[i] * 6

        C = C.sum()
        # print('评分值：', C)
        D1 = pd.concat([d_left, d_right], axis=1).reset_index()
        # print(D1) # 评分区间
        medscore.append(C)
        # print(A) # 给药途径权重

    end_df = pd.DataFrame()
    end_df['generic_name'] = medname
    end_df['level_score'] = medscore
    end_df['report_numbers'] = num

    if end_df.shape[0] != 0:
        end_df.loc[end_df['level_score'] <= 4, 'serious_adr_level'] = 1
        end_df.loc[(end_df['level_score'] <= 10) & (end_df['level_score'] > 4), 'serious_adr_level'] = 2
        end_df.loc[(end_df['level_score'] <= 20) & (end_df['level_score'] > 10), 'serious_adr_level'] = 3
        end_df.loc[(end_df['level_score'] <= 40) & (end_df['level_score'] > 20), 'serious_adr_level'] = 4
        end_df.loc[(end_df['level_score'] <= 70) & (end_df['level_score'] > 40), 'serious_adr_level'] = 5
        end_df.loc[end_df['level_score'] > 70, 'serious_adr_level'] = 6
        end_df.sort_values('level_score', ascending=False, inplace=True)
    # if end_df.shape[0] != 0:
    #     end_df.loc[end_df['level_score'] <= (100/6), 'serious_adr_level'] = 1
    #     end_df.loc[(end_df['level_score'] <= (200/6)) & (end_df['level_score'] > (100/6)), 'serious_adr_level'] = 2
    #     end_df.loc[(end_df['level_score'] <= (300/6)) & (end_df['level_score'] > (200/6)), 'serious_adr_level'] = 3
    #     end_df.loc[(end_df['level_score'] <= (400/6)) & (end_df['level_score'] > (300/6)), 'serious_adr_level'] = 4
    #     end_df.loc[(end_df['level_score'] <= (500/6)) & (end_df['level_score'] > (400/6)), 'serious_adr_level'] = 5
    #     end_df.loc[end_df['level_score'] > (500/6), 'serious_adr_level'] = 6
    #     end_df.sort_values('level_score', ascending=False, inplace=True)

    return end_df
