# Proxy-crawler

- Proxy-crawler是一个基于flask,sqlite3,aiohttp,asyncio的自动爬取免费代理脚本。脚本从公开的网站爬取一些免费的代理，并重新校验他们的延时等。该代码中有一小部分使用了Proxy_Pool的代码（全网代理），因为有点难度:(。脚本中使用了异步，实际上并没有什么用处（没有requests方便），仅仅为了学习异步、爬虫等。由于是学习代码，代码中可能存在一些错误，希望指出错误，感谢:)。代码运行一段时候后，存活的代理数一般在60-300之间（跟代理的网站测试有关）。

- 本代码仅为学习使用

# Prepare
- 仅支持python>=3.6

# Usage
- pip install requirements.txt
- python3 main.py

# FROM

- 西刺代理
- 泥马代理
- 免费ip
- 快代理
- 66代理
- ip海
- 全网代理

# API
在python3启动脚本后，访问http://127.0.0.1:5000/all 获取所有代理，http://127.0.0.1:5000/http 获取http代理，http://127.0.0.1:5000/https 获取https代理。若有其他查询需求，可在main.py文件里自行修改

# Purpose
- 练习python，简单的使用异步、flask等
- 爬取代理做成API，在枚举目录时绕过一些访问限制
