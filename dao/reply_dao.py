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
        sql = "select content from reply where keyword = %s order by id desc limit 1"
        n = db_executer.execute(sql, keyword)
        if not n:
            return ""
        data = db_executer.fetchall()
        return data[0][0]

    def get_reply_list(self, keyword=""):
        sql = "select id, keyword, content from reply "
        if keyword:
            sql = sql + " where keyword like '%" + keyword + "%'"
        sql = sql + " order by id desc"
        n = db_executer.execute(sql)
        if not n:
            return []
        data = db_executer.fetchall()
        return data

    def add_reply(self, keyword, content):
        if not keyword or not content:
            return None
        sql = "insert into reply (keyword, content) values (%s, %s);"
        db_executer.execute(sql, (keyword, content))

    def update_reply(self, replyid, keyword, content):
        sql = "update reply set keyword = %s, content = %s where id = %s"
        db_executer.execute(sql, (keyword, content, replyid))

    def delete_reply(self, replyid):
        sql = "delete from reply where id = %s"
        db_executer.execute(sql, replyid)
    
reply_dao = ReplyDao()
