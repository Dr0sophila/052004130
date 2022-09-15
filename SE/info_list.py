class ChinaTotal:

    def __init__(self):
        self.daily_diagnosis = {}
        self.daily_asymptomatic = {}

    def update_diagnosis(self, date, num):
        self.daily_diagnosis[date] = int(num)

    def update_asymptomatic(self, date, num):
        self.daily_asymptomatic[date] = int(num)


class Province:

    def __init__(self, name):
        self.name = name
        self.daily_diagnosis = {}
        self.daily_asymptomatic = {}

    def update_diagnosis(self, date, num):
        self.daily_diagnosis[date] = int(num)

    def update_asymptomatic(self, date, num):
        self.daily_asymptomatic[date] = int(num)


province_names = ["河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "海南", "四川",
                  "贵州", "云南", "陕西", "甘肃", "青海", "内蒙古", "广西", "西藏", "宁夏", "新疆", "北京", "天津", "上海", "重庆", "兵团", "香港", "澳门",
                  "台湾"]


def create_province_list() -> dict[str, Province]:
    province_list = {}
    for province in province_names:
        province_list[province] = Province(province)
    return province_list
