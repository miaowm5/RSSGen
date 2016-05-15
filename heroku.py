# !/usr/bin/env python
# -*- coding:utf-8 -*-

import wsgi, os
wsgi.app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))