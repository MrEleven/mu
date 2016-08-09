#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-07-21
# Author: Master Yumi
# Email : yumi@meishixing.com

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
import os, json
import hashlib
import xmltodict
from service.reply_service import reply_service

from tornado.options import define, options
define("port", default=8866, help="run on the given port", type=int)

TOKEN = "449801285f551ec67ec8358e4b05dbb5"


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        signature = self.get_argument("signature")
        params = [timestamp, nonce, TOKEN]
        params.sort()
        sign = hashlib.sha1("".join(params)).hexdigest()
        if sign == signature:
            self.write(echostr)
        else:
            print "validate failed"

    def post(self):
        message = self.request.body
        message_info = xmltodict.parse(message).get("xml", "{}")
        my_name = message_info.get("ToUserName", "")
        user_name = message_info.get("FromUserName", "")
        msg_tyep = message_info.get("MsgType", "")
        msg_content = message_info.get("Content", "")
        msg_id = message_info.get("MsgId", "")
        if msg_tyep != "text":
            self.write("success")
            return
        reply_msg = reply_service.get_reply_msg(user_name, my_name, msg_content)
        self.write(reply_msg)
        
class ManageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("manage.html", result={})

class ListHandler(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument("keyword", "")
        reply_list = reply_service.get_reply_list(keyword=keyword)
        result = json.dumps(reply_list)
        self.write(result)

class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        replyid = int(self.get_argument("replyid", 0))
        keyword = self.get_argument("keyword", "")
        content = self.get_argument("content", "")
        if not all([replyid, keyword, content]):
            return
        return reply_service.update_reply(replyid, keyword, content)

class DeleteHandler(tornado.web.RequestHandler):
    def post(self):
        replyid = int(self.get_argument("replyid", 0))
        if not replyid:
            return
        return reply_service.delete_reply(replyid)

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        keyword = self.get_argument("keyword", "")
        content = self.get_argument("content", "")
        if not all([keyword, content]):
            return
        return reply_service.add_reply(keyword, content)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/index", IndexHandler), (r"/", ManageHandler),
                  (r"/list", ListHandler), (r"/add", AddHandler),
                  (r"/delete", DeleteHandler), (r"/update", UpdateHandler)],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
