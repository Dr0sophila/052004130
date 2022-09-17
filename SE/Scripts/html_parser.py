import re

from Scripts.info_list import province_names


class Parser:
    @staticmethod
    def parse(paragraph, china, province_list):  # This paragraph is mainly about new cases.

        # 日期
        date = re.findall(r"(\d+月\d+日)", paragraph[0])[0]

        # 中国大陆每日本土新增确诊人数
        domestic_new_diagnosis = re.findall(r"本土\D?\D?(\d*)例（", paragraph[0])
        if len(domestic_new_diagnosis) > 0:
            china.update_diagnosis(date, domestic_new_diagnosis[0])
        else:
            china.update_diagnosis(date, "0")

        domestic_diagnosis_province_list = re.findall(r"本土\D?\D?\d*例(（.*?）)", paragraph[0])
        if len(domestic_diagnosis_province_list) > 0:
            domestic_diagnosis_province = re.findall(r"[，；（](\D\D\D?)(\d+)例", domestic_diagnosis_province_list[0])

            for province in domestic_diagnosis_province:
                if province[0] in province_names:
                    province_list[province[0]].update_diagnosis(date, province[1])

        # 中国大陆每日本土新增无症状人数
        domestic_new_asymptomatic = re.findall(r"本土\D?\D?(\d*)例（", paragraph[1])
        if len(domestic_new_asymptomatic) > 0:
            china.update_asymptomatic(date, domestic_new_asymptomatic[0])
        else:
            china.update_asymptomatic(date, "0")

        domestic_asymptomatic_province_list = re.findall(r"本土\D?\D?\d+例(（.*?）)", paragraph[1])
        if len(domestic_asymptomatic_province_list) > 0:
            domestic_asymptomatic_province = re.findall(r"[，；（](\D\D\D?)(\d+)例", domestic_asymptomatic_province_list[0])

            for province in domestic_asymptomatic_province:
                if province[0] in province_names:
                    province_list[province[0]].update_asymptomatic(date, province[1])

        # 港澳台确诊病例
        hk_new_diagnosis = re.findall(r"香港特别行政区(\d+)例", paragraph[2])
        mc_new_diagnosis = re.findall(r"澳门特别行政区(\d+)例", paragraph[2])
        tw_new_diagnosis = re.findall(r"台湾地区(\d+)例", paragraph[2])

        province_list["香港"].update_asymptomatic(date, hk_new_diagnosis[0])
        province_list["澳门"].update_asymptomatic(date, mc_new_diagnosis[0])
        province_list["台湾"].update_asymptomatic(date, tw_new_diagnosis[0])