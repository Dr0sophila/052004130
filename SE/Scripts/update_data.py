import re
import sys
import time
import aiohttp
from bs4 import BeautifulSoup
import asyncio
import html_parser

DAYS = 240  # 爬取天数（可修改）

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "insert_cookie=91349450; yfx_c_g_u_id_10006654=_ck22091016193310257145017533795; security_session_verify=4a5f3c112034b72078057eea47fcaab3; yfx_f_l_v_t_10006654=f_t_1662797973027__r_t_1662797973027__v_t_1662805227140__r_c_0; sVoELocvxVW0T=53SSEnbWQ1KLqqqDkxXvQlGlOu07WnJuOYrSsW5EtgwKgj5D0Vt6iQqjE7rnnDzdgq2xCGr.pyCDEMlvFY_yDPsJ1M0y2SJR3ovaPvNEoUQ8tQI6F94YYZG4Nn3zaQcuVRVFff6PvW60UcyPWLKQe._BxYMUqdo_TEcNz3L5if8puCPac1SbewqhMiZNZTpeaOqRzW65todn.2Qv0oO3c5QCjbvIw_2fd.6h6ERwOb40qeTZC0oFfCfOnqP7VHKZxCT0UCjwlVjLpR7loQAD68yCliRcoeFqxedL53xPuVeMKwppJQY0G021evAQx5_Tq65Hz4LDpvZdCNsy07lOGn9",
    "Host": "www.nhc.gov.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
}


# 根据命名规则生成不同的页面url
def get_homepage_url() -> list[str]:
    base_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd'
    homepage_url_list = [base_url + ".shtml"]
    for i in range(2, DAYS//24+1):
        homepage_url_list.append(base_url + "_%d.shtml" % i)
    # for url in homepage_url_list:
    #     print(url)
    return homepage_url_list


# 通过请求主页url申请获得通报页面url并解析
async def request_url(homepage_url, url_list):
    async with aiohttp.ClientSession() as session:
        async with session.get(homepage_url, headers=headers) as res:
            homepage_soup_res = await res.text()
            homepage_soup = BeautifulSoup(homepage_soup_res, "lxml")
            for url in homepage_soup.findAll('li'):
                for a in url.findAll("a"):
                    url_list.append("http://www.nhc.gov.cn" + a.attrs["href"])


# 异步调用request_url生成通报页面url列表
def get_urls() -> list[str]:
    start_time = time.time()
    url_list = []

    tasks = [asyncio.ensure_future(request_url(url, url_list)) for url in get_homepage_url()]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))

    print('url ', time.time() - start_time, ' seconds')
    return url_list


# 请求拥抱页面并解析
async def get_data(url, china_total, province_list):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            res = await res.text()
            soup = BeautifulSoup(res, "lxml")
            paragraph = []
            count = 0
            for i in soup.findAll("p"):
                if re.search(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例\d+例", i.text) is not None:
                    paragraph.append(i.text)
                    count += 1
                elif re.search(r"31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者\d+例", i.text) is not None:
                    paragraph.append(i.text)
                    count += 1
                elif re.search(r"累计收到港澳台地区通报确诊病例", i.text) is not None:
                    paragraph.append(i.text)
                    count += 1
            if count == 3:
                try:
                    html_parser.Parser.parse(paragraph, china_total, province_list)
                except:
                    print(sys.exc_info())
                    print("error! fail to parse", url)

            else:
                print("error!! count = ", count)
                print(url)
                print(paragraph)


# 异步调用请求页面并写入数据
def update(china_total, province_list):
    start_time = time.time()
    urls = get_urls()[0:DAYS]
    tasks1 = [asyncio.ensure_future(get_data(url, china_total, province_list)) for url in urls[:DAYS // 3]]
    tasks2 = [asyncio.ensure_future(get_data(url, china_total, province_list)) for url in urls[DAYS // 3:DAYS // 3 * 2]]
    tasks3 = [asyncio.ensure_future(get_data(url, china_total, province_list)) for url in urls[DAYS // 3 * 2:]]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks1))
    time.sleep(1)
    loop.run_until_complete(asyncio.gather(*tasks2))
    time.sleep(1)
    loop.run_until_complete(asyncio.gather(*tasks3))
    loop.close()
    print('page+parse time ', time.time() - start_time, ' seconds')
