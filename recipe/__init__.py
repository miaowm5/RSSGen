#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

recipe_list = []
hide_list = []
base_list = {}

for file in os.listdir(os.path.dirname(__file__)):
    if not file.endswith('.py'): continue
    if file.startswith('__'): continue
    name = os.path.splitext(file)[0]
    try:
        recipe = (__import__("recipe." + name, fromlist='*')).recipe
        if name.endswith("hide"): hide_list.append(recipe)
        elif name.endswith("base"): base_list[name] = recipe
        else: recipe_list.append(recipe)
    except Exception as e: print("%s import failed : %s" % (name, e))
