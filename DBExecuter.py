#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2016-09-21
# Author: Master Yumi
# Email : yumi@meishixing.com

import MySQLdb

class DBExecuter(object):
    conn = None
    cursor = None
    host = ""
    user = ""
    port = ""
    passwd = ""
    db = ""
    charset = ""

    def __init__(self, host, user, port, passwd, db, charset="utf8"):
        self.host = host
        self.user = user
        self.port = port
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self._reconnect()

    def connect(self):
        return self._reconnect()

    def _reconnect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, port=self.port, passwd=self.passwd, db=self.db, charset=self.charset)
        self.conn.autocommit(1)
        self.cursor = self.conn.cursor()
        return self.conn

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self._reconnect()
            self.cursor.execute(sql)

    def fetchall(self):
        return self.cursor.fetchall()
