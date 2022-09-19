import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

table = pd.read_excel('../data.xlsx', sheet_name="每日确诊")
table1 = pd.read_excel('../data.xlsx', sheet_name="每日无症状")

date = table.iloc[:, 0].values.tolist()[:10]
confirm = table.iloc[:, 1].values.tolist()[:10]
asymptomatic = table1.iloc[:, 1].values.tolist()[:10]
print(type(date))
c = (
    Bar()
        .add_xaxis(
        date
    )

        .add_yaxis("每日确诊", confirm)
        .add_yaxis("每日无症状",asymptomatic)
        .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="近十日全国疫情统计"),
    )
        .render("../templates/bar.html")
)
