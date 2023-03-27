import pandas as pd
import time
import re


def s_left(x):
    _ = ['20', 'L', 'X', '拜', '']
    for i in _:
        x = x.lstrip(i)
    return x


def s_mid_1(x):
    _ = [' ', '[消栓]', '()', ' ', '250ml:12.5g', '10%', '0.25g','0.25', '0.5g',
         '500ml', '3克/支', '10mg', '4.2mg', 'ong', 'z20033183', '5ml:1g',
         'GS 12.5ml',
         '0.9GNS', '0.03%', 'CREAM', '口服乳', '口服补液盐', '8.4mg', '4.2mg',
         '0.9100ml/瓶', '8.5%', '70/30', '18种', '注射永', '30%', '2.0g', '815267',
         '50mg', '：', '注射液安平', '氧化钠', '80mg：2ml*1支', '1.5g*1瓶', '18A',
         '100ML*0.5G', '10ML*10支', '氯化纳', '4:1', '400mg50片', '15mg*10片',
         '10g/50ml/瓶', '阿斯利康制药有限公司', '/福爱康', '/聚荣', '/鹿顶丹', 'AZD9291',
         ' 0.15', '2.5g *10袋', '毫升', '？', '关节部位疼痛酸麻肿胀', '5mg/支', '笔芯',
         '*0.9%', '1.0（达力舒）', '补及液', '补给液', '1.0g', '*27', '*654-2',
         '1g/支', '10g*20袋', '32g/ml', '100ml:0.3g', '100ml:0.2g', '2ml，0.1g',
         '250ml:2.25g', '.9', '.', 'ml:1g', '250ml', '10ml', '10％', '1.2g', ':0g',
         'bom', '缓释颗粒剂', '－', '25', '/100ml：0.3g/袋（针剂）', '0.3', '0.5',
         '12g', '', '注射用', '吸入用', '通用名称', '0.9', '吸入', '100ug', ':', '~',
         '=-', '-', '冻干粉针', '9AA', '[江苏恒瑞]', '盐水', '双释放肠溶胶囊', '*1'
         , '0.75g', '注射用无菌粉末', '复合包装', '5ml:1g', '1.0g', '复方南星药业有限公司',
         '5ml:1g', '04g*30s', '2g', '30mg', '1ml', '20ml', '300u', '201406211',
         '1g', '100ml', '20mg', '100mg', 'GS1ml', '1.0', '0.125g *6袋', '40/0.9%',
         '颈部疼痛酸麻肿胀', '肩部疼痛酸麻肿胀', '国药准字H19994088', '29', '/甲红',
         '30#', '{2}', '（跌打损伤型', '0.15', 'JH-A', '绿化难', '(预混', '注射样',
         '眼用凝', '/会康', 'SAVOLITIIB', 'savolitinib', '2mg', '0.4', 'abemaciclib',
         ]
    for i in _:
        x = x.replace(i, '')
    return x


def s_mid_2(x):
    # 包含“*%氯化钠*”或“*生理盐水*”，统一成“氯化钠注射液”
    if x == 'L－门冬氨酸氨氯地平片':
        return '门冬氨酸氨氯地平'
    re_1 = re.compile('生理盐水|氯化钠$')
    x = re_1.sub('氯化钠注射液', x)
    # 去掉名称前“*‘
    re_2 = re.compile('^\*')
    x = re_2.sub('', x)
    # “5*葡萄糖*”统一为“葡萄糖”
    re_3 = re.compile('5葡萄糖|5%葡萄糖')
    x = re_3.sub('葡萄糖', x)
    # 去掉空格
    x = x.replace(' ', '')
    if x == '999':
        return '999感冒灵'
    # 去掉“片”，“胶囊”，“分散片”，“丸”，“注射剂”，“注射液”，“糖浆”，“软胶囊”，“干混悬剂”，“肠溶片”，“肠溶液”，“肠溶胶囊”，“肠溶缓释”，“泡腾”，“口服液”，“颗粒”，“气雾剂”，“乳膏”，“鼻喷雾剂”，“搽剂”，“滴眼液”，“咀嚼片”，“控释片”，“喷鼻剂”，“含片”，“注射用无菌粉末”，“滴丸”，“合剂”，“喷剂”，“粉雾剂”，“粉吸入剂”，“吸入粉雾剂”，“滴耳液”(位于名称末尾)
    re_4 = re.compile('喉片|片|解毒胶囊|胶囊|分散片|胶丸|丸|软化乳膏|注射剂|混合注射液|'
                      '混悬凝胶|鼻用喷雾剂|雾化混悬液|肠溶胶南|合计|葡萄颗粒|口颊|片剂|'
                      '混和注射液|注射液|糖浆|外用溶液剂|阴道软胶|冷疗贴|阴道膨胀栓|'
                      '口含滴丸|外用溶液|灌肠剂|缓释植入剂|冲洗液|脐贴|吸入溶液剂|酏剂|'
                      '软胶囊|混悬滴剂|干混悬剂|肠溶片|肠溶液|肠溶胶囊|肠溶缓释|干混剂'
                      '|泡腾|口服液|颗粒|气雾剂|乳膏|鼻喷雾剂|搽剂|滴眼液|咀嚼片|口腔贴'
                      '|控释片|喷鼻剂|含片|注射用无菌粉末|滴丸|合剂|喷剂|粉雾剂|缓释|'
                      '粉吸入剂|吸入粉雾剂|滴耳液|栓剂|口服溶液剂|注射汀液|滴鼻液|混悬剂|'
                      '针剂|雾化溶液|口服冻干粉|发用洗剂|溶液剂|鼻用吸入剂|冻干粉|注射粉剂$')
    x = re_4.sub('', x)
    # 去掉名称中括号内的内容（包括括号）
    re_5 = re.compile('(\(|（).+(\)|）)')
    x = re_5.sub('', x)

    # 去掉“.药品名”的“.”
    re_6 = re.compile('^\.')
    x = re_6.sub('', x)
    _1 = ['白蛋白结合型紫杉醇', '冰黄肤乐软膏', '丙胺酰-L-谷氨酰胺',
          '单唾液四己酸神经节苷脂钠', '青霉素Ｖ钾', '碳酸钙维D3元素',
          '碳酸钙D3', '云南白药创可贴', '“明通”治伤风', '罗汉果茶',
          '板蓝根茶', 'A阿司匹林', '氯化钠:225g', '克霉唑栓；克霉唑阴道膨胀',
          'VC银翘', '=-谷氨酰胺呱仑酸钠', '=-门冬氨酸氨氯地平', '%甘露醇',
          '%静脉用脂肪乳', '中长链脂肪乳', '(复方氨基酸', '(盐酸莫西沙星',
          '；甲泼尼龙琥珀酸钠', '10g头孢噻肟钠', '30%静脉用脂肪乳',
          '阿莫西林克拉维酸', '阿莫西林舒巴坦钠', '阿莫西林舒巴坦匹',
          '阿莫西林克拉维酸钾钾', '复发氨基酸', '()', '20AA', '藿香正气水',
          '氯化钠注射', '50', '蒙脱石散剂', '灭菌水', '（）',
          '葡萄糖注射', '庆大霉素普鲁卡因B12', '曲安奈德益康唑膏',
          '曲克芦丁脑蛋白水解物', '乳酸左氧氟沙星沙星', '碳酸钙维生素D3', '每支',
          '维生素E乳', '乳剂TPFT', '明通治上风', '双唑泰栓；双唑泰阴道膨胀栓',
          '阴道膨胀', '头孢夫', '制霉菌素', '制霉素', '亚胺培南/西司他汀', '不详',
          '青霉素G', '12种', '十二种复合维生素', '12', '味D2磷酸氢钙',
          '六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄六味地黄',
          '左氧氟沙星盐', '碳酸钙d3', '说明书', '复合12种维生素', '引道', '复方对乙酰氨基酚（',
          '葡萄糖氯化钠射液注', '氯化钠', 'wc', 'N', '/辰欣', '甲泼尼龙琥珀酸钠(',
          '左氧200ml', '5G', '氯氯雷他定雷他氯雷他定', '无锡市中医医院消肿膏',
          '无锡市中医医院肃肺', '注盐酸川芎嗪射用盐酸川芎嗪', '头孢呋辛之', '莫西沙星注射',
          '盐酸莫西沙星氯化钠(拜复', '葡萄糖5/瓶', '/混合重组人胰岛素',
          '门冬胰岛素30(诺和锐30特充', '824VE', 'PolymyxinBforinjection'
          , '混合唐电解质', '感冒灵(', '复方氢溴酸东莨菪碱贴膏)', '肠溶胶蘘', '18aav',
          '15hbc', '(18AAV', '18AAV', '【18AA]ML', '折射也', '注射夜',
          '复方氨基酸注射', '复方磺胺甲基噁唑', '５％ＧＳ葡萄糖100G', '葡萄糖100毫升',
          '葡萄糖0毫升', '3克克林霉素磷酸酯', '氟沙星)', '组合包装脂溶性维生素/水溶性维生素',
          '左氧氟沙星/100ml：03g/袋', '门冬氨酸鸟氨酸门冬氨酸鸟氨酸', '口服溶',
          '君欣(乳酸左氧氟沙', '甲甲甲磺酸左氧磺酸左氧', '左氧氟沙星注射', '射用头孢唑肟钠',
          '六味地黄/道君', '*头孢地qin', '头孢呋辛na', '水溶性维生素/脂溶性维生素',
          '甲硝唑vb6', '盐城左氧氟沙星', '脂溶性维生素/水溶性维生素',
          '盐酸坦索罗安斯泰来制药有限公司辛', '盐酸左氧氟沙星/', '脂溶性维生素II/水溶性维生素',
          '盐酸莫西杀星', '碳酸钙-维生素D3元素', '克林霉素磷酸脂1', '18AA',
          '脂溶性维生素/水溶性维生素组合', '脂溶性维生素Ⅱ/水', '脂溶性维生素/水溶性维生素复方',
          '艾塞那肽微球（', '3氧氟沙星', '30/70混合重组人胰岛素', '5氨基水杨酸', '%中/长链脂肪乳',
          '4替硝唑', '乳酸左氧氟沙星星', '丙氨酰L谷氨酰胺', '中/长链脂肪乳E', '丹参川芎嗪丹参川芎嗪',
          '丹参滴注', '%盐酸利多卡因', '%中长链脂肪乳', '%左氧氟沙星']
    _2 = ['白蛋白紫杉醇', '冰黄软膏', '丙氨酰谷氨酰胺', '单唾液酸四己糖神经节苷脂钠',
          '青霉素V钾', '碳酸钙-维生素D3', '碳酸钙-维生素D3', '云南白药',
          '明通治伤风', '罗汉果', '板蓝根', '阿司匹林', '氯化钠', '克霉唑栓',
          '维C银翘', '谷氨酰胺呱仑酸钠', '门冬氨酸氨氯地平', '甘露醇',
          '脂肪乳', '中长链脂肪乳', '复方氨基酸', '盐酸莫西沙星', '甲泼尼龙琥珀酸钠',
          '头孢噻肟钠', '脂肪乳', '阿莫西林克拉维酸钾', '阿莫西林舒巴坦',
          '阿莫西林舒巴坦', '阿莫西林克拉维酸钾', '复方氨基酸', '', '',
          '藿香正气', '', '', '蒙脱石散', '灭菌注射', '', '',
          '庆大霉素普鲁卡因维B12', '曲安奈德益康唑', '曲克芦丁蛋白水解物',
          '乳酸左氧氟沙星', '碳酸钙-维生素D3', '', '维生素E', '',
          '明通治伤风', '双唑泰', '阴道膨胀', '头孢呋辛', '', '',
          '亚胺培南西司他丁', '', '青霉素', '', '复合维生素', '',
          '维D2磷酸氢钙', '六味地黄', '左氧氟沙星', '碳酸钙-维生素D3', '', '复合维生素',
          '', '复方对乙酰氨基酚', '', '', '', '', '', '甲泼尼龙琥珀酸钠',
          '左氧氟沙星', '', '氯雷他定', '消肿膏', '肃肺', '盐酸川芎嗪',
          '头孢呋辛酯', '莫西沙星', '盐酸莫西沙星', '', '混合重组人胰岛素',
          '门冬胰岛素', '', '', '混合糖电解质', '感冒灵', '复方氢溴酸东莨菪碱', '', '',
          '', '', '', '', '', '', '复方氨基酸', '复方磺胺甲噁唑', '', '',
          '', '克林霉素磷酸酯', '左氧氟沙星', '脂溶性维生素/水溶性维生素组合包装',
          '左氧氟沙星', '门冬氨酸鸟氨酸', '', '乳酸左氧氟沙星', '甲磺酸左氧氟沙星',
          '左氧氟沙星', '头孢唑肟钠', '六味地黄', '*头孢地嗪', '头孢呋辛钠',
          '脂溶性维生素/水溶性维生素组合包装', '甲硝唑', '盐酸左氧氟沙星',
          '脂溶性维生素/水溶性维生素组合包装', '盐酸坦索罗辛', '盐酸左氧氟沙星',
          '脂溶性维生素/水溶性维生素组合包装', '盐酸莫西沙星', '碳酸钙-维生素D3',
          '克林霉素磷酸脂', '', '脂溶性维生素/水溶性维生素组合包装', '脂溶性维生素Ⅱ',
          '脂溶性维生素/水溶性维生素组合包装', '艾塞那肽微球', '氧氟沙星',
          '30%常规重组人胰岛素和70%PH重组人胰岛素', '氨基水杨酸', '中/长链脂肪乳',
          '替硝唑', '乳酸左氧氟沙星', '丙氨酰谷氨酰胺', '中/长链脂肪乳', '丹参川芎嗪',
          '丹参', '盐酸利多卡因', '中/长链脂肪乳', '左氧氟沙星']
    for i in range(len(_1)):
        x = x.replace(_1[i], _2[i])
    return x


def s_right(x):
    if x == '30常规重组人胰岛素和70PH重组人胰岛素':
        return '30%常规重组人胰岛素和70%PH重组人胰岛素'
    if x == '30常规重组人胰岛素和':
        return '30%常规重组人胰岛素和70%PH重组人胰岛素'
    if x == '30常规重组人胰岛素和70PH重组人胰岛素混合注射':
        return '30%常规重组人胰岛素和70%PH重组人胰岛素'
    if x == '7030混合人胰岛素':
        return '30%常规重组人胰岛素和70%PH重组人胰岛素'
    _ = ['氯化钠', '缓释', '贴膏', '混悬液', '凝胶', '肠溶', '口服溶液', '口崩', '透皮贴剂',
         '口腔崩解', '溶液', '贴', '滴鼻剂', '软膏', '浸膏', '乳状', '针', '口服', '无',
         '喷雾剂', '雾化剂', '雾化液', '浸液', '粉剂', '营养', '乳剂', '洗剂',
         '洗液', '葡萄糖', '阴道栓', '电解质散', '含漱液', '止痛膏', '40',
         '冲剂', '眼用', '眼膏', 'J', '口腔粘贴', '阴道', '栓', '冷敷', '浓',
         '滴剂', '肠溶微', '贴剂', '乳胶剂', '葡葡糖', '%', '100', '200/05',
         '', '', '氯化钠100ml02g',
         '130/04', '30', '甘露醇', '无菌粉末', '氯化钠注', '<加立信>', '075g/支',
         '[消栓]', '2ml40mg', '氯化钠100ml03g', '40氨基酸', '20', '液',
         '[17]葡萄糖[11]', '[C824Ve]', 'C824Ve', 'C824Ve()', '粉针075g',
         'C6～24', '/支', '（）', '()', 'C824Ve（）', 'S', '涂剂', 'Ⅱ',
         'Ⅰ', 'II', '30R', 'Ⅲ', 'III', '补给', '粒', '脂质体', '舌下',
         '胶蘘', '‘', '/']
    if x == '复方':
        x = '复方甘露醇'
    for i in _:
        if i in x:
            x = x.rstrip(i)
    return x


def data_f(s):
    start = time.time()
    s.dropna(subset=['generic_name'], inplace=True)
    s['generic_name'] = s['generic_name'].apply(s_mid_1)
    s['generic_name'] = s['generic_name'].apply(s_mid_2)
    s['generic_name'] = s['generic_name'].apply(s_left)
    s['generic_name'] = s['generic_name'].apply(s_right)
    end = time.time()
    s.drop_duplicates(['code', 'meddra_id', 'gender', 'age', 'suspect_or_blend',
                       'generic_name'], keep='first')
    print('数据清洗(药品名称)耗时：', end - start, 's')
    s = s[~s['generic_name'].isin([''])]
    return s


def enterprise_medname(s):
    s.dropna(subset=['generic_name'], inplace=True)
    s['generic_name'] = s['generic_name'].apply(s_mid_1)
    s['generic_name'] = s['generic_name'].apply(s_mid_2)
    s['generic_name'] = s['generic_name'].apply(s_left)
    s['generic_name'] = s['generic_name'].apply(s_right)
    s = s[~s['generic_name'].isin([''])]
    return s


def t(x):
    if '导致死亡' in x:
        x = 6
    elif '危及生命' in x:
        x = 5
    elif ('导致显著的或永久的人体伤残或器官功能的损伤' in x) or ('致癌、致畸、致出生缺陷' in x):
        x = 4
    elif ('导致其他重要医学事件' in x) or ('导致住院或住院时间延长' in x):
        x = 3
    elif x == '-':
        x = 3
    return x


def adr_level(df):
    start = time.time()
    df['serious_adr_level'] = df['serious_adr'].apply(t)
    df.loc[df['adr_result'] == '死亡', 'serious_adr_level'] = 6
    df.loc[(df['severity'].iloc[:, 1] == '一般') & (df['adr_result'] == '痊愈'), 'serious_adr_level'] = 1
    df.loc[(df['severity'].iloc[:, 1] == '一般') & (df['adr_result'] != '痊愈'), 'serious_adr_level'] = 2
    end = time.time()
    print('不良反应严重程度等级评估耗时：', end - start, 's')
    return df

#赋值部分
def report_weight(df):
    df['new_weight'] = 0
    df.loc[df['is_new'] == 1, 'new_weight'] = 0.925
    df.loc[df['is_new'] == 0, 'new_weight'] = 0

    df['whether_disappear_after_stop'].fillna('不明')
    df['whether_same_after_medication'].fillna('不明')

    df['use_med_weight'] = 0
    df.loc[(df['whether_disappear_after_stop'] == '否')
           & (df['whether_same_after_medication'] == '否'),
           'use_med_weight'] = 0.2
    df.loc[((df['whether_disappear_after_stop'] == '不明') |
            (df['whether_disappear_after_stop'] == '未停量或未减量'))
           & ((df['whether_same_after_medication'] == '不明') |
              (df['whether_same_after_medication'] == '未再使用')),
           'use_med_weight'] = 0.5
    df.loc[(df['whether_disappear_after_stop'] == '是')
           & (df['whether_same_after_medication'] == '否'),
           'use_med_weight'] = 0.6
    df.loc[(df['whether_disappear_after_stop'] == '否')
           & (df['whether_same_after_medication'] == '是'),
           'use_med_weight'] = 0.6
    df.loc[(df['whether_disappear_after_stop'] == '是')
           & (df['whether_same_after_medication'] == '是'),
           'use_med_weight'] = 0.975
    df.loc[((df['whether_disappear_after_stop'] == '不明') |
            (df['whether_disappear_after_stop'] == '未停量或未减量'))
           & (df['whether_same_after_medication'] == '是'),
           'use_med_weight'] = 0.8
    df.loc[(df['whether_disappear_after_stop'] == '是')
           & ((df['whether_same_after_medication'] == '不明') |
              (df['whether_same_after_medication'] == '未再使用')),
           'use_med_weight'] = 0.8
    df.loc[((df['whether_disappear_after_stop'] == '不明') |
            (df['whether_disappear_after_stop'] == '未停量或未减量'))
           & (df['whether_same_after_medication'] == '否'),
           'use_med_weight'] = 0.4
    df.loc[(df['whether_disappear_after_stop'] == '否')
           & ((df['whether_same_after_medication'] == '不明') |
              (df['whether_same_after_medication'] == '未再使用')),
           'use_med_weight'] = 0.4

    df['report_weight'] = 0
    df.loc[df['reportor_evaluation'] == '可能无关', 'report_weight'] = 0.2
    df.loc[df['reportor_evaluation'] == '肯定', 'report_weight'] = 0.925
    df.loc[df['reportor_evaluation'] == '很可能', 'report_weight'] = 0.825
    df.loc[df['reportor_evaluation'] == '可能', 'report_weight'] = 0.7
    df.loc[(df['reportor_evaluation'] == '待评价') |
           (df['reportor_evaluation'] == '无法评价'),
           'report_weight'] = 0.5

    df['t_weight'] = 0
    df.loc[df['reporting_unit_evaluation'] == '可能无关', 't_weight'] = 0.2
    df.loc[df['reporting_unit_evaluation'] == '肯定', 't_weight'] = 0.925
    df.loc[df['reporting_unit_evaluation'] == '很可能', 't_weight'] = 0.825
    df.loc[df['reporting_unit_evaluation'] == '可能', 't_weight'] = 0.7
    df.loc[(df['reporting_unit_evaluation'] == '待评价') |
           (df['reporting_unit_evaluation'] == '无法评价'),
           't_weight'] = 0.5

    df['level_weight'] = 0
    df.loc[df['serious_adr_level'] == 1, 'level_weight'] = 1 / 6
    df.loc[df['serious_adr_level'] == 2, 'level_weight'] = 2 / 6
    df.loc[df['serious_adr_level'] == 3, 'level_weight'] = 3 / 6
    df.loc[df['serious_adr_level'] == 4, 'level_weight'] = 4 / 6
    df.loc[df['serious_adr_level'] == 5, 'level_weight'] = 6 / 6
    df.loc[df['serious_adr_level'] == 6, 'level_weight'] = 7 / 6

    df['end_weight'] = df['level_weight'] * 0.15 + df['t_weight'] * 0.5 + \
                       df['report_weight'] * 0.5 + df['use_med_weight'] * 0.3 + \
                       df['new_weight'] * 0.05
#(New_weight)报告类型――新的、
# (level_weight)ADR严重 程度、
# (use_med_weight)停药减药以及再用药表现、
# (report_weight)报告人评价
# (t_weight)报告人单位评价
    return df
