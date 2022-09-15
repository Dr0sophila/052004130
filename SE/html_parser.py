import re


class Parser:
    @staticmethod
    def parse(paragraph, china, province_list):  # This paragraph is mainly about new cases.

        # 日期
        date = re.findall(r"(\d+月\d+日)", paragraph[0])[0]

        # 中国大陆每日本土新增确诊人数
        domestic_new_diagnosis = re.findall(r"本土\D?\D?(\d*)例（", paragraph[0])[0]

        #         print("中国大陆每日本土新增确诊人数:",domestic_new_diagnosis)
        china.update_diagnosis(date, domestic_new_diagnosis)

        domestic_diagnosis_province_list = re.findall(r"本土\D?\D?\d*例(（.*?）)", paragraph[0])[0]
        domestic_diagnosis_province = re.findall(r"[，；（]([^均其]\D+)(\d+)例", domestic_diagnosis_province_list)

        for province in domestic_diagnosis_province:
            try:
                province_list[province[0]].update_diagnosis(date, province[1])
            except:
                print(paragraph)
        # 中国大陆每日本土新增无症状人数
        domestic_new_asymptomatic = re.findall(r"本土\D?\D?(\d*)例（", paragraph[1])[0]
        #         print("中国大陆每日本土新增无症状人数:",domestic_new_asymptomatic)
        if domestic_new_asymptomatic == '':
            print("domestic_new_asymptomatic", date)
        china.update_asymptomatic(date, domestic_new_asymptomatic)

        domestic_asymptomatic_province_list = re.findall(r"本土\D?\D?\d+例(（.*?）)", paragraph[1])[0]
        domestic_asymptomatic_province = re.findall(r"[，；（]([^均其]\D+)(\d+)例", domestic_asymptomatic_province_list)

        for province in domestic_asymptomatic_province:
            #             print(province,date,domestic_asymptomatic_province_num[index])
            try:
                province_list[province[0]].update_asymptomatic(date, province[1])
            except:
                print(paragraph)
