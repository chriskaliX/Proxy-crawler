import datetime
import asyncio
import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType
import requests
import os
import queue
import threading
import traceback
import sys
import time
import data.var
sys.path.append(os.path.abspath('../async-proxy'))

class verify:
    @staticmethod
    def run():
        async def Check(ip):
            if not ip['ip']:
                return False
            if (ip['type'].lower() == "http") or (ip['type'].lower() == "https"):
                typelist = [ip['type'].lower()]
            elif (ip['type'] == 'unknown') or (ip['type'] == ""):
                typelist = ["https","http"]
            
            for _type in typelist:
                proxy = _type + "://" +ip['ip'] + ":" + str(ip['port'])
                connector = ProxyConnector.from_url(proxy)
                try:
                    start = time.time()
                    async with aiohttp.ClientSession(connector=connector) as session:
                        async with session.get("%s://httpbin.org/get" % _type, timeout=5) as resp:
                            r = await resp.json()
                            iplist = r['origin'].split(",")
                            for i in range(len(iplist)):
                                iplist[i] = iplist[i].strip(" ")
                            iplist = list(set(iplist))
                            ip["anonymous"] = True if len(iplist) == 1 else False
                            assert (ip['ip'] in r['origin'])
                    end = time.time()
                    delay = int(round((end - start),3)*1000)
                    ip['type'] = _type
                    ip['time'] = int(end)
                    ip['delay'] = delay
                    return ip
                except:
                    pass
            return False

        async def GetValidProxyPool(iplist):
            validProxyList = list()
            # SIZE = 10
            # for i in range(0, iplist.qsize, SIZE):
            # for i in range(iplist.qsize):
            coroList = [asyncio.ensure_future(Check(ip)) for ip in iplist.queue]
            for f in asyncio.as_completed(coroList):
                proxy = await f
                if proxy:
                    validProxyList.append(proxy)
            return validProxyList

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        validProxyList = loop.run_until_complete(GetValidProxyPool(data.var.pre))
        return validProxyList
