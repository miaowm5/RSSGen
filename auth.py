# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud

APPID = '123'
# 填写应用的 APPID

APPKEY = '123'
# 填写应用的 APPKEY

MASTERKEY = '123'
# 填写应用的 MASTERKEY

HEROKUAPP = r''
# 应用的 heroku 版网址（可不填）

leancloud.init(APPID,APPKEY,master_key=MASTERKEY)