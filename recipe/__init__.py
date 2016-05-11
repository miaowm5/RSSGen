#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

recipe_list = []

for file in os.listdir(os.path.dirname(__file__)):
    if not file.endswith('.py'): continue
    if file.startswith('__') or file.endswith("base.py"): continue
    name = os.path.splitext(file)[0]
    try:
        recipe = __import__("recipe." + name, fromlist='*')
        recipe_list.append(recipe.recipe)
    except Exception as e: print("%s import failed : %s" % (name, e))
