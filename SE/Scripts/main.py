import info_list
import update_data
import write_data
import show_graphs




def main():
    province_list = info_list.create_province_list()
    china_total = info_list.ChinaTotal()
    update_data.update(china_total, province_list)

    diagnosis, asymptomatic = write_data.write(china_total, province_list)

    show_graphs.show_data("每日确诊", diagnosis)
    show_graphs.show_data("每日无症状", asymptomatic)


if __name__ == '__main__':
    main()
