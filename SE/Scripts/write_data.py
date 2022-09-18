import re

import pandas as pd

import info_list


def write(china_total, province_list):
    calendar_list = china_total.daily_diagnosis.keys()
    calendar = []
    for day in calendar_list:
        calendar.append(day)

    daily_diagnosis = pd.DataFrame(columns=['大陆总计'] + [*info_list.province_names], index=[*calendar])

    for key in province_list.keys():
        for date in province_list[key].daily_diagnosis:
            daily_diagnosis.loc[date, key] = province_list[key].daily_diagnosis[date]

    for key in china_total.daily_diagnosis.keys():
        daily_diagnosis.loc[key, '大陆总计'] = china_total.daily_diagnosis[key]

        days = re.findall(r"2022/(\d+)/(\d+)", key)
        index = 100 * (int(days[0][0])) + int(days[0][1])
        daily_diagnosis.loc[key, 'index'] = index

    daily_diagnosis.fillna(0, inplace=True)

    # 第二张表

    daily_asymptomatic = pd.DataFrame(columns=['大陆总计'] + [*info_list.province_names], index=[*calendar])
    for key in province_list.keys():
        for date in province_list[key].daily_asymptomatic:
            daily_asymptomatic.loc[date, key] = province_list[key].daily_asymptomatic[date]

    for key in china_total.daily_asymptomatic.keys():
        daily_asymptomatic.loc[key, '大陆总计'] = china_total.daily_asymptomatic[key]

        days = re.findall(r"2022/(\d+)/(\d+)", key)
        index = 100 * (int(days[0][0])) + int(days[0][1])
        daily_asymptomatic.loc[key, 'index'] = index

    daily_asymptomatic.fillna(0, inplace=True)

    # daily_asymptomatic.to_csv("daily_asymptomatic.csv",encoding='GBK')
    # daily_asymptomatic.to_excel("daily_asymptomatic.xlsx",encoding='GBK',sheet_name="daily_asymptomatic")
    daily_diagnosis.sort_values(by="index", ascending=False, inplace=True)
    daily_asymptomatic.sort_values(by="index", ascending=False, inplace=True)

    daily_diagnosis.drop('index', axis=1, inplace=True)
    daily_asymptomatic.drop('index', axis=1, inplace=True)

    buffer = daily_diagnosis.iloc[:, 33:]
    buffer = buffer.diff(periods=-1)

    daily_diagnosis = daily_diagnosis.drop(['香港', "澳门", "台湾"], axis=1)
    daily_diagnosis = pd.concat([daily_diagnosis, buffer], axis=1)
    daily_diagnosis.index.names = ['日期']

    daily_asymptomatic = daily_asymptomatic.drop(['香港', "澳门", "台湾"], axis=1)
    daily_asymptomatic.index.names = ['日期']
    with pd.ExcelWriter('./data.xlsx') as writer:
        daily_diagnosis.to_excel(writer, sheet_name='每日确诊', index=True)
        daily_asymptomatic.to_excel(writer, sheet_name='每日无症状', index=True)
    return daily_diagnosis, daily_asymptomatic
