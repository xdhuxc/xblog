#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

# 通过实例化一个Blueprint类对象可以创建蓝本。
# 这个构造函数有两个必须指定的参数：蓝本的名字和蓝本所在的包或模块，和程序一样，大多数情况下第二个参数使用Python的__name__变量即可。
main = Blueprint('main', __name__)

# 导入这两个模块就能把路由和错误处理程序与蓝本关联起来
# 注意，这些模块在 app/main/__init__.py脚本的末尾导入，这是为了避免循环导入依赖，因为在views.py和errors.py中还要导入蓝本main
from . import views
from . import errors