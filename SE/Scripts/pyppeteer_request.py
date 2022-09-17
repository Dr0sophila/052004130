import asyncio
from pyppeteer import launch

launch_args = [
    "--no-sandbox",  # 非沙盒模式
    "--disable-infobars",  # 隐藏信息栏
    # 设置UA
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.97 Safari/537.36 ",
    "--log-level=3",  # 日志等级
]


async def init_browser(headless=False):
    return await launch({'headless': headless,
                         'args': launch_args,
                         'userDataDir': './userData',
                         'dumpio': True,
                         'ignoreHTTPSErrors ': True})


# 防WebDriver检测
async def prevent_web_driver_check(page):
    if page is not None:
        # 隐藏webDriver特征
        await page.evaluateOnNewDocument("""() => {
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined })}
        """)
        # 某些站点会为了检测浏览器而调用js修改结果
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'lang uages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')


# 新建页面
async def init_page(browser):
    page = await browser.newPage()
    await page.setViewport({'width': 1960, 'height': 1080})  # 设置页面宽高
    await page.setJavaScriptEnabled(True)
    await prevent_web_driver_check(page)
    return page


async def req(page, url, timeout=60):
    await page.goto(url, options={'timeout': int(timeout * 1000)})
    print(await page.content())


def request_data(url):
    cur_browser = asyncio.get_event_loop().run_until_complete(init_browser())
    cur_page = asyncio.get_event_loop().run_until_complete(init_page(cur_browser))
    asyncio.get_event_loop().run_until_complete(req(cur_page, url))


request_data('http://www.nhc.gov.cn/xcs/yqtb/202209/f690ecf985cd445282110c57906c8578.shtml')
