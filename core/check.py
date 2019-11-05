import time
import data.var
def checktime(conn, _time):
    print("[*] 定时校验开始")

    # 查询所有数据库中的数据
    sql = conn.cursor()
    sql.execute('SELECT * FROM PROXY;')
    iplist = sql.fetchall()

    # 得到IP队列,删除超时IP
    backlist = []
    for ip in iplist:
        if (int(time.time())-int(ip[3])) > _time:
            print("[*] 时间超时:",ip)
            backlist.append(ip)
            sql.execute("DELETE FROM PROXY WHERE IP='%s';" % ip[0])
    conn.commit()

    # 插入至全局队列里
    for i in backlist:
        data.var.pre.put({
            'ip': i[0],
            'port': str(i[1]),
            'type': i[2],
            'time': i[3]
        })