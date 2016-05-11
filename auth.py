# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud

APPID = '123'
# 填写应用的 APPID

APPKEY = '123'
# 填写应用的 APPKEY

MASTERKEY = '123'
# 填写应用的 MASTERKEY

leancloud.init(APPID,APPKEY,master_key=MASTERKEY)