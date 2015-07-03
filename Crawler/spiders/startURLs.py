# coding=utf8

import MySQLdb


class GetStartURLs:
    def __init__(self):
        self.stock_id = []
        conn = MySQLdb.connect(host='localhost', user='root', passwd='passw0rd', db='thomas')
        cursor = conn.cursor()
        cursor.execute('select stock_id from stock limit 1')
        results = cursor.fetchall()
        for stockId in results:
            self.stock_id.append(stockId[0][:6])
