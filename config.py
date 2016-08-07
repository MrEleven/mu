#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2016-08-07
# Author: Master Yumi
# Email : yumi@meishixing.com

import MySQLdb

db_conn = MySQLdb.connect(host="121.40.236.133", user="eleven", port=3306, passwd="password", db="mumushuoka", charset="utf8")
db_executer = db_conn.cursor()
