#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import pymysql

# 處理與資料庫連線的各種動作
class DbConn:
    batch_size = 100	# 批次處理的大小
    count = 0			# 批次處理的個數

    ip
    usr
    pw
    dbname
    chset = "utf8"
    socket = "/tmp/mysql.sock"
#dbcollat utf8_general_ci

    def __init__(self):
        self.con = None
        self.cur = None

    # 從檔案設定連線資料
    def loadParam(self, path):
        config = configparser.ConfigParser()
        config.read(path)

        self.ip = config.get("DatabaseSection", "ip")
        self.usr = config.get("DatabaseSection", "usr")
        self.pw = config.get("DatabaseSection", "pw")
        self.dbname = config.get("DatabaseSection", "dbname")
        self.chset = config.get("DatabaseSection", "charset")

    # 設定連線資料
    def setConn(self, ip, usr, pw, dbname):
        self.ip = ip
        self.usr = usr
        self.pw = pw
        self.dbname = dbname

    # 設定批次處理的大小
    def setBatchSize(self, size):
        self.batch_size = size

    # 與資料庫連線
    def connect(self):
        self.con = pymysql.connect(host=self.ip, unix_socket=self.socket, user=self.usr, passwd=self.pw, db=self.dbname, charset=self.chset)
        self.cur = self.con.cursor()

    # 寫入資料庫
    def update(self, sql):
        self.cur.execute(sql)

        self.count = (self.count + 1) % self.batch_size
        if self.count == 0:
            self.con.commit()

    # commit
    def commit(self):
        self.con.commit()

    # 搜尋資料庫
    def select(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 關閉連線
    def close(self):
        try:
            if self.cur != None:
                self.cur.close()
            if self.con != None:
                self.con.close()
        except Exception as e:
            print(e)
