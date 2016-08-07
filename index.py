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
import os
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


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/index", IndexHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
