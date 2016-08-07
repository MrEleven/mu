#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2016-08-07
# Author: Master Yumi
# Email : yumi@meishixing.com

from config import db_executer

class ReplyDao(object):
    def get_reply(self, keyword=""):
        if keyword == None or keyword.strip() == "":
            return ""
        sql = "select content from reply where keyword = %s limit 1"
        n = db_executer.execute(sql, keyword)
        if not n:
            return ""
        data = db_executer.fetchall()
        return data[0][0]


reply_dao = ReplyDao()
