import info_list
import update_data
import write_data
import show_graphs
from Scripts.asymptomaticmap import asymptomatic_map
from Scripts.confirmedmap import confirm_map


def main():
    province_list = info_list.create_province_list()  # 创建省列表储存数据
    china_total = info_list.ChinaTotal()  # 创建全国数据实例
    update_data.update(china_total, province_list)  # 更新数据

    diagnosis, asymptomatic = write_data.write(china_total, province_list)  # 写入html

    show_graphs.show_data("每日确诊", diagnosis, "confirm")  # 用图标展示数据
    show_graphs.show_data("每日无症状", asymptomatic, "asymptomatic")  # 用图标展示数据

    asymptomatic_map()
    confirm_map()

if __name__ == '__main__':
    main()
