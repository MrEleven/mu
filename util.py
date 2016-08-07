#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2016-08-07
# Author: Master Yumi
# Email : yumi@meishixing.com

def to_utf8(text):
    if isinstance(text, unicode):
        return text.encode("utf8")
    return str(text)
