import asyncio
import time
import aiohttp
from lxml import etree
from data.var import *
import random
from functools import reduce

class crawl:
    @staticmethod
    async def get(url, analyze, Q):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5, headers=headers) as resp:
                    await asyncio.sleep(random.randint(1, 3))
                    assert resp.status == 200
                    r = await resp.text()
                    for res in analyze(r):
                        Q.put(res)
        except asyncio.TimeoutError:
            print("[*] Timeout!")
        except AssertionError:
            print("[*] Status code :", resp.status)

    @staticmethod
    def runloop(tasks,SIZE,_time):
        for i in range(0, len(tasks), SIZE):
            time.sleep(_time)
            task = tasks[i:i+SIZE]
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(task))

    "[*] 尼玛代理，更新较快(但是最近好像不更新了...)"
    class nima:
        @staticmethod
        def run(Q):
            print("[*] 泥马代理爬取")
            def analyze(html):
                html = etree.HTML(html)
                return [{'ip': html.xpath("/html/body/div/div[1]/div/\
                    table/tbody/tr[%i]/td[1]" % i)[0].text.split(":")[0],
                    'port': html.xpath("/html/body/div/div[1]/div/\
                    table/tbody/tr[%i]/td[1]" % i)[0].text.split(":")[1],
                    'type': 'https' if 'https' in html.xpath("\
                    /html/body/div/div[1]/div/table/tbody/\
                    tr[%i]/td[2]" % i)[0].text.lower() else 'http'}
                    for i in range(1,51) if html is not None]

            urls = ["http://www.nimadaili.com/putong/",
                "http://www.nimadaili.com/http/",
                "http://www.nimadaili.com/https/",
                "http://www.nimadaili.com/gaoni/"]
            tasks = [crawl.get(url+str(page)+"/",analyze,Q) for url in urls for page in range(1, 16)]
            crawl.runloop(tasks,2,0.5)
    
    "[*] 西刺代理，量不是很大"
    class xici:
        @staticmethod
        def run(Q):
            print("[*] 西刺代理爬取")
            def analyze(html):
                html = etree.HTML(html)
                return [{'ip': html.xpath("/html/body/div[1]/div[2]/table/tr[%d]/td[2]" % i)[0].text,
                        'port':html.xpath("/html/body/div[1]/div[2]/table/tr[%d]/td[3]" % i)[0].text,
                        'type':html.xpath("/html/body/div[1]/div[2]/table/tr[%d]/td[6]" % i)[0].text.lower()
                        } for i in range(2, 102)]

            urls =["https://www.xicidaili.com/nn/",
                "https://www.xicidaili.com/nt/",
                "https://www.xicidaili.com/wn/",
                "https://www.xicidaili.com/wt/"]
            tasks = [crawl.get(url+str(page)+"/", analyze, Q)
                     for url in urls for page in range(1, 4)]
            crawl.runloop(tasks, 1, 3)
    
    "[*] 量小，更新快，一天多次"
    class freeip:
        @staticmethod
        def run(Q):
            print("[*] FreeIP爬取")
            def analyze(html):
                html = etree.HTML(html)
                return [{'ip': html.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[%d]/td[2]" % i)[0].text,
                    'port':html.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[%d]/td[3]" % i)[0].text,
                    'type':html.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[%d]/td[5]" % i)[0].text.lower()
                    } for i in range(1, 16) 
                    if html.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr[%d]/td[2]" % i) != []]

            url = "http://ip.jiangxianli.com/"
            tasks = [crawl.get(url + "?page="+ str(page),analyze, Q) for page in range(1,4)]
            crawl.runloop(tasks, 1, 1)
    
    "[*] 较好，一天多次"
    class superfast:
        @staticmethod
        def run(Q):
            print("[*] 快代理爬取")
            def analyze(html):
                html = etree.HTML(html)
                return [{'ip': html.xpath('/html/body/div[3]/div/div/div[2]/div/table/tbody/tr[%d]/td[1]' % i)[0].text,
                        'port':html.xpath('/html/body/div[3]/div/div/div[2]/div/table/tbody/tr[%d]/td[2]' % i)[0].text,
                        'type':html.xpath('/html/body/div[3]/div/div/div[2]/div/table/tbody/tr[%d]/td[4]' % i)[0].text.lower()
                         } for i in range(1, 21) 
                        if html.xpath('/html/body/div[3]/div/div/div[2]/div/table/tbody/tr[%d]/td[1]' % i) != []]
            url = "http://www.superfastip.com/welcome/freeip/"
            tasks = [crawl.get(url + "%d" % page,analyze, Q) for page in range(1,11)]
            crawl.runloop(tasks,1,1)

    "[*] 更新慢，量多"
    class ssip:
        @staticmethod
        def run(Q):
            print("[*] 66ip代理爬取")
            def analyze(html):
                html = etree.HTML(html)
                result = [
                    {'ip': html.xpath('/html/body/div[4]/div/div/div/\
                        div[2]/div/table/tr[%d]/td[1]' % i)[0].text,
                    'port': html.xpath('/html/body/div[4]/div/div/div/\
                        div[2]/div/table/tr[%d]/td[2]' % i)[0].text,
                    'type': 'unknown'
                    }  for i in range(2,151) 
                    if (html.xpath('/html/body/div[4]/div/div/div/div[2]/\
                        div/table/tr[%d]/td[2]' % i) != [])]
                run_function = lambda x, y: x if y in x else x + [y]
                return reduce(run_function, [[], ] + result)
                
            urls = ["http://www.66ip.cn/areaindex_%d/1.html" % i for i in range(1,35)]
            tasks = [crawl.get(url, analyze, Q) for url in urls]
            crawl.runloop(tasks, 1, 1)

    "[*] 更新慢"
    class iphai:
        @staticmethod
        def run(Q):
            print("[*] IP海代理爬取")
            def analyze(html):
                html = etree.HTML(html)
                return [{
                    'ip':html.xpath("/html/body/div[2]/div[2]/table/tr[%d]/td[1]" % i)[0].text.strip("\n").strip(" "),
                    'port':html.xpath("/html/body/div[2]/div[2]/table/tr[%d]/td[2]" % i)[0].text.strip("\n").strip(" "),
                    'type':html.xpath("/html/body/div[2]/div[2]/table/tr[%d]/td[4]" % i)[0].text.strip("\n").strip(" ")
                    } for i in range(2, 1000) if html.xpath("/html/body/div[2]/div[2]/table/tr[%d]/td[1]" % i) !=[]]
            urls = ["http://www.iphai.com/free/ng",
                    "http://www.iphai.com/free/np",
                    "http://www.iphai.com/free/wg",
                    "http://www.iphai.com/free/wp"]
            tasks = [crawl.get(url,analyze, Q) for url in urls]
            crawl.runloop(tasks, 1, 1)
                        
    "[*] 量少，15分钟一次"
    class quanwang:
        @staticmethod
        def run(Q):
            """
            [*]过程比较复杂，直接在Proxy_Pool的代码上加了一点
            """
            print("[*] 全网代理")
            def analyze(html):
                html = etree.HTML(html)
                proxylist = html.xpath('//td[@class="ip"]')
                xpath_str = """.//*[not(contains(@style, 'display: none'))
                and not(contains(@style, 'display:none'))
                and not(contains(@class, 'port'))
                ]/text()
                """
                result = []
                for each_proxy in proxylist:
                    try:
                        ip_addr = ''.join(each_proxy.xpath(xpath_str))
                        port = 0
                        for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                            "/attribute::class")[0].replace("port ", ""):
                            port *= 10
                            port += (ord(_) - ord('A'))
                        port /= 8
                        _type = html.xpath(
                            '/html/body/section[2]/div/div[2]/div/div/\
                            div/table/tbody/tr[%d]/td[3]/a'
                            % proxylist.index(each_proxy))[0].text
                        result.append({
                            'ip':ip_addr,
                            'port':int(port),
                            'type':_type
                        })
                    except:
                        pass
                return result
            url = "http://www.goubanjia.com/"
            tasks = [crawl.get(url, analyze, Q)]
            crawl.runloop(tasks, 1, 1)
