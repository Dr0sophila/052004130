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

    daily_diagnosis.fillna(0, inplace=True)
    # daily_diagnosis.to_csv("daily_diagnosis.csv",encoding='GBK')
    # daily_diagnosis.to_excel("daily_asymptomatic.xlsx",encoding='GBK',sheet_name="daily_diagnosis")

    daily_asymptomatic = pd.DataFrame(columns=['大陆总计'] + [*info_list.province_names], index=[*calendar])
    for key in province_list.keys():
        for date in province_list[key].daily_asymptomatic:
            daily_asymptomatic.loc[date, key] = province_list[key].daily_asymptomatic[date]

    for key in china_total.daily_asymptomatic.keys():
        daily_asymptomatic.loc[key, '大陆总计'] = china_total.daily_asymptomatic[key]

    daily_asymptomatic.fillna(0, inplace=True)
    # daily_asymptomatic.to_csv("daily_asymptomatic.csv",encoding='GBK')
    # daily_asymptomatic.to_excel("daily_asymptomatic.xlsx",encoding='GBK',sheet_name="daily_asymptomatic")

    with pd.ExcelWriter('1.xlsx') as writer:
        daily_diagnosis.to_excel(writer, sheet_name='每日确诊', index=True)
        daily_asymptomatic.to_excel(writer, sheet_name='每日无症状', index=True)
    return daily_diagnosis, daily_asymptomatic
