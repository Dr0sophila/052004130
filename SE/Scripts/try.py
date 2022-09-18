import re

date = re.findall(r"2022/(\d+)/(\d+)", "2022/3/27")[0]
print(date)#2020/3/27