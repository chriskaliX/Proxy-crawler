import time
def checktime(Q, conn, _time):
    print("[*] 定时校验开始")
    sql = conn.cursor()
    sql.execute('SELECT * FROM PROXY;')
    iplist = sql.fetchall()
    backlist = []
    for ip in iplist:
        if (int(time.time())-int(ip[3])) > _time:
            print("[*] 时间超时:",ip)
            backlist.append(ip)
            sql.execute("DELETE FROM PROXY WHERE IP='%s';" % ip[0])
    conn.commit()
    for i in backlist:
        _in = {
            'ip':i[0],
            'port':str(i[1]),
            'type':i[2],
            'time':i[3]
        }
        Q.put(_in)
