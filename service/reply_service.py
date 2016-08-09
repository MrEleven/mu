#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2016-08-07
# Author: Master Yumi
# Email : yumi@meishixing.com

from dao.reply_dao import reply_dao
import time
from util import to_utf8

class ReplyService(object):
    def get_reply_info(self, user_msg=""):
        if user_msg == None or user_msg.strip() == "":
            return ""
        content = reply_dao.get_reply(user_msg)
        return content

    def get_reply_msg(self, to_user, from_user, user_msg):
        content = self.get_reply_info(user_msg)
        if not content:
            content = "八戒，师傅被黑山老妖抓走啦！木木等等就肥来，回复你！"
        reply_template = """<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>"""
        create_time = int(time.time())
        return reply_template % (to_utf8(to_user), to_utf8(from_user), to_utf8(create_time), to_utf8(content))

    def get_reply_list(self, keyword=""):
        data = reply_dao.get_reply_list(keyword)
        result = []
        for d in data:
            reply_info = {"replyid": d[0], "keyword": d[1], "content": d[2]}
            result.append(reply_info)
        return result

    def add_reply(self, keyword, content):
        return reply_dao.add_reply(keyword, content)

    def delete_reply(self, replyid):
        return reply_dao.delete_reply(replyid)

    def update_reply(self, replyid, keyword, content):
        return reply_dao.update_reply(replyid, keyword, content)
    
reply_service = ReplyService()
        
