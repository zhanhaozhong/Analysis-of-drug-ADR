def change_type(x):
    if x < 10:
        x = '0' + str(x)
    else:
        x = str(x)
    return x


def data_get(ds, year):
    _ = ds['adr_date'].str.split('-', expand=True).rename(columns={0: 'adr_date_year',
                                                                   1: 'adr_date_month',
                                                                   2: 'adr_date_day'})
    ds[['adr_date_year', 'adr_date_month', 'adr_date_day']] = \
        _[['adr_date_year', 'adr_date_month', 'adr_date_day']]
    df = ds[ds['adr_date_year'].isin(year)].copy()
    df['adr_date_month'] = df['adr_date_month'].apply(int)
    # df['adr_date_year'] = df['adr_date_year'].apply(int)
    df['adr_date_quarter'] = '1'  # 1表示第一季度
    df['adr_date_midyear'] = '1'  # 1表示下半年，0表示上半年
    df.loc[df['adr_date_month'] <= 6, 'adr_date_midyear'] = '0'
    df.loc[(3 < df['adr_date_month']) & (df['adr_date_month'] <= 6), 'adr_date_quarter'] \
        = '2'
    df.loc[(6 < df['adr_date_month']) & (df['adr_date_month'] <= 9), 'adr_date_quarter'] \
        = '3'
    df.loc[(9 < df['adr_date_month']) & (df['adr_date_month'] <= 12), 'adr_date_quarter'] \
        = '4'
    df['adr_date_midyear'] = df['adr_date_year'] + df['adr_date_midyear']
    df['adr_date_quarter'] = df['adr_date_year'] + df['adr_date_quarter']
    df['adr_date_month'] = df['adr_date_year'] + df['adr_date_month'].apply(change_type)

    return df