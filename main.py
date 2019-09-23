import os,sys,schedule,time,threading
from data.var import *
from core.crawl import *
from core.verify import *
import sqlite3,json
from flask import Flask,Response
from core.check import *
import datetime

app = Flask(__name__)
sys.path.append(os.path.abspath('../async-proxy'))
conn = sqlite3.connect('data/proxy.db', check_same_thread=False)
print("[*] 数据库连接成功")

def getip(Q,conn):
    sql = conn.cursor()
    while True:
        time.sleep(5)
        waitlist = [Q.get() for i in range(100) if not Q.empty()]
        if not waitlist:
            continue
        vaild = verify.run(waitlist)
        iplist = [ip[0] for ip in sql.execute("SELECT * FROM PROXY").fetchall()]
        for ip in vaild:
            "[*] 没有则插入，有则更新"
            if ip['ip'] not in iplist:
                print("[*] IP :",ip['ip'])
                sql.execute("""INSERT OR IGNORE INTO PROXY(IP,PORT,TYPE,TIME,DELAY,ANONYMOUS) VALUES \
                ('{_ip}',{port},'{_type}','{_time}','{delay}','{anonymous}');""".format(_ip=ip['ip'],\
                port=int(ip['port']), _type=ip['type'], _time=str(ip['time']), delay=ip['delay'], anonymous=ip['anonymous']))
            else:
                sql.execute("""UPDATE PROXY SET TIME='%s' WHERE IP='%s';""" % (str(ip['time']),ip['ip']))
                sql.execute("""UPDATE PROXY SET DELAY=%d WHERE IP='%s';"""%(ip['delay'],ip['ip']))
        conn.commit()

@app.route("/http")
def gethttpproxy():
    sql = conn.cursor()
    sql.execute("SELECT * FROM PROXY WHERE TYPE = 'http';")
    result = sql.fetchall()
    return Response(json.dumps([{
            'ip':ip[0],
            'port':ip[1],
            'type':ip[2],
            'time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(ip[3]))),
            'delay':ip[4],
            'anonymous':ip[5]
    } for ip in result], ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))\
        ,mimetype='application/json')

@app.route("/https")
def gethttpsproxy():
    sql = conn.cursor()
    sql.execute("SELECT * FROM PROXY WHERE TYPE = 'https';")
    result = sql.fetchall()
    return Response(json.dumps([{
        'ip': ip[0],
        'port':ip[1],
        'type':ip[2],
        'time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(ip[3]))),
        'delay':ip[4],
        'anonymous':ip[5]
    } for ip in result], ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))\
        ,mimetype='application/json')
    
@app.route("/all")
def getallproxy():
    sql = conn.cursor()
    sql.execute('SELECT * FROM PROXY;')
    result = sql.fetchall()
    return Response(json.dumps([{
        'ip': ip[0],
        'port':ip[1],
        'type':ip[2],
        'time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(ip[3]))),
        'delay':ip[4],
        'anonymous':ip[5]
    } for ip in result], ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))\
        ,mimetype='application/json')

def aftermin(count):
    return (datetime.datetime.now()+datetime.timedelta(minutes=count)).strftime("%H:%M")

if __name__ == '__main__':
    glo = Global()
    sql = conn.cursor()
    """
    # 创建表
    sql.execute('''CREATE TABLE PROXY
       (IP CHAR(20) PRIMARY KEY  NOT NULL,
       PORT         INT          NOT NULL,
       TYPE        CHAR(10)      NOT NULL,
       TIME        CHAR(20)      NOT NULL,
       DELAY        INT          NOT NULL,
       ANONYMOUS   BOOLEAN       NOT NULL
       );''')
    """
    # sql.execute("delete from PROXY;")
    # print("[*] 数据库清空完毕")
    conn.commit()
    

    t = threading.Thread(target=getip, args=(glo.pre, conn))
    t.start()
    print("[*] 后台验证开启")
    schedule.every().day.at(aftermin(1)).do(crawl.xici.run, glo.pre)
    schedule.every(4).hours.do(crawl.nima.run, glo.pre)
    schedule.every(15).minutes.do(crawl.freeip.run, glo.pre)
    schedule.every().day.at(aftermin(5)).do(crawl.ssip.run, glo.pre)
    schedule.every(10).minutes.do(crawl.quanwang.run, glo.pre)
    schedule.every().hour.do(crawl.superfast.run, glo.pre)
    schedule.every(3).hours.do(crawl.iphai.run, glo.pre)

    #时间超过1800秒的重新跑，一分钟校验一次
    _time = 1800
    schedule.every(1).minutes.do(checktime, glo.pre,conn,_time)
    def back():
        while True:
            schedule.run_pending()
            time.sleep(1)
    t = threading.Thread(target=back)
    t.start()
    app.run(port=5000, debug=True, host='127.0.0.1', use_reloader=False)
