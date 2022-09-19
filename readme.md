[magical-psy/052004130 (github.com)](https://github.com/magical-psy/052004130)



# 一、PSP表格 



| PSP2.1                                  | Personal Software Process Stages       | 预估耗时（分钟） | 实际耗时（分钟） |
| --------------------------------------- | -------------------------------------- | ---------------- | ---------------- |
| Planning                                | 计划                                   | 30               | 60               |
| · Estimate                              | · 估计这个任务需要多少时间             | 1690             | 2730             |
| Development                             | 开发                                   | 720              | 1040             |
| · Analysis                              | · 需求分析 (包括学习新技术)            | 60               | 30               |
| · Design Spec                           | · 生成设计文档                         | 30               | 60               |
| · Design Review                         | · 设计复审 (和同事审核设计文档)        | 30               | 80               |
| · Coding Standard                       | · 代码规范 (为目前的开发制定合适的规范 | 60               | 60               |
| · Design                                | · 具体设计                             | 60               | 100              |
| · Coding                                | · 具体编码                             | 360              | 720              |
| · Code Review                           | · 代码复审                             | 60               | 100              |
| · Test                                  | · 测试（自我测试，修改代码，提交修改） | 80               | 160              |
| Reporting                               | 报告                                   | 100              | 130              |
| · Test Report                           | · 测试报告                             | 60               | 80               |
| · Size Measurement                      | · 计算工作量                           | 20               | 30               |
| · Postmortem & Process Improvement Plan | · 事后总结, 并提出过程改进计划         | 60               | 80               |
|                                         | 合计                                   | 1690             | 2730             |



# 二、任务要求的实现

 ## (3.1)项目设计与技术栈。从阅读完题目到完成作业，这一次的任务被你拆分成了几个环节？你分 别通过什么渠道、使用什么方式方法完成了各个环节？列出你完成本次任务所使用的技术栈。

### 任务环节：

>
>
>1.编写爬虫，爬取数据
>
>2.分析数据，预测疫情发展（挖掘每日热点）
>
>3.编写前端网页（数据可视化大屏）
>
>

1.爬虫技术栈python ：

| 任务      | 使用的库                            |
| --------- | ----------------------------------- |
| 请求      | aiohttp                             |
| 解析html  | BeautifulSoup用lxml(时需要另外安装) |
| 异步/协程 | asyncio                             |
| 提取信息  | re正则匹配                          |

2.分析数据，预测疫情发展（挖掘每日热点）python(jupyter notebook):

| 任务     | 使用库      |
| -------- | ----------- |
| 数据处理 | pandas      |
| 画图     | matplotlib  |
| 建立模型 | statsmodels |
| 使用模型 | ARIMA       |

3.编写前端网页（数据可视化大屏）html/python:

| 任务           | 方法                                                         |
| -------------- | ------------------------------------------------------------ |
| 制作图标       | pyechart/matplotlib(直接生成的图片只能说有点丑)              |
| 数据可视化大屏 | 写了个html把我所有的组件都缝合进来                           |
| 项目部署       | 使用flusk完成/(在请求图片时会出现bug，应该是应为没有转成二进制文件) |
| 挖掘信息       | 嵌入了我之前写的notebook                                     |

## (3.2)爬虫与数据处理。

**爬虫流程**：

1.从官网爬取所有通报的url

官网的每一页数据的url都有规律，只要在一串格式化的路径后加个连续的后缀就行了

2.逐个请求url列表，从中取出每个通报页的url

3.解析html,用关键词正则匹配得到数据并贮存

**亮点：**

使用协程爬虫非常快，爬两百个数据实际只需5秒左右

**代码分析**：

update——data.py:

~~~python
def get_homepage_url() -> list[str]
#根据命名规则生成不同的页面url

async def request_url(homepage_url, url_list):
#通过请求主页url申请获得通报页面url并解析
    
def get_urls() -> list[str]:
#异步调用request_url生成通报页面url列表
    
async def get_data(url, china_total, province_list):
#请求拥抱页面并解析   
 
def update(china_total, province_list):
#异步调用请求页面并写入数据
~~~

info_list.py

~~~python
class ChinaTotal:
#有两个函数update_diagnosis()，update_asymptomatic()更新数据
    
class Province:
#有两个函数update_diagnosis()，update_asymptomatic()更新数据

def create_province_list() -> dict[str, Province]:
#生成32个省+兵团的数据列表
~~~



html_parser.py

~~~python
class Parser
def parse(paragraph, china, province_list):
#解析传回的字符串列表，并写入数据
#字符串列表有三个元素对应确诊，无症状和港澳台数据
~~~



## (3.3)数据统计接口部分的性能改进。记录在数据统计接口的性能上所花费的时间，描述你改进的 思路，并展示一张性能分析图

消耗最大的函数是update_data()用来请求网页并更新数据

优化方法：

* 1.优化正则表达式
* 2.使用协程，异步执行网络请求
* 因为请求过快经常被服务器拉黑，所以没请求1/1的数据主动停止1秒

![性能分析](https://github.com/magical-psy/052004130/blob/master/blog/%E6%80%A7%E8%83%BD%E5%88%86%E6%9E%90.PNG)

## (3.4)每日热点的实现思路。简要介绍实现该功能的算法原理，可给出必要的步骤流程图、数学公 式推导和核心代码实现，并简要谈谈所采用算法的优缺点与可能的改进方案。

**ARIMA模型**

**ARIMA模型**，差分整合移动平均自回归模型，又称整合移动平均自回归模型（移动也可称作滑动），是时间序列预测分析方法之一。ARIMA(p，d，q)中，AR是“自回归”，p为自回归项数；MA为“滑动平均”，q为滑动平均项数，d为使之成为平稳序列所做的差分次数（阶数）。“差分”一词虽未出现在ARIMA的英文名称中，却是关键步骤。

三个参数:p,d,q。
p--代表预测模型中采用的时序数据本身的滞后数(lags) ,也叫做AR/Auto-Regressive项
d--代表时序数据需要进行几阶差分化，才是稳定的，也叫Integrated项。
q--代表预测模型中采用的预测误差的滞后数(lags)，也叫做MA/Moving Average项

![fom](https://github.com/magical-psy/052004130/blob/master/blog/fom.PNG)

建立模型，根据之间的数据预测后一天的数据，如果出现较大偏差，则发生了一些突然状况。

**可以改进的方能**

模型尚待完善，现在的模型拟合度太低。





## (3.5)数据可视化界面的展示。在博客中介绍数据可视化界面的组件和设计的思路。

使用pyechart生成动态图标可以用中国地图直观地展示跟个省份效果如图

![可视化效果](https://github.com/magical-psy/052004130/blob/master/blog/%E5%8F%AF%E8%A7%86%E5%8C%96%E6%95%88%E6%9E%9C.PNG)

最终展示



![结果](https://github.com/magical-psy/052004130/blob/master/blog/%E7%BB%93%E6%9E%9C.jpeg)

## 三、心得体会 

这次作业没想到花最多时间的居然是前端，而且最后也没有做出好看的前端来
技术栈比较浅，vue,css啥的都不会用，只能用python生成页面。
实在不知道怎么做html了，最后就用frame标签把几个组件缝合在了一起。

用协程异步爬取数据时逻辑比较混乱，花了好多时间才理清。

爬取数据时尝试使用了pyppeteer，但是效果不好，改为使用aiohttp，做了一些反爬措施，爬取速度和成功率比较高

最后发现需要疫情新闻的时候就很暴力地直接嵌入html了~~（最直接有效啊？）~~
