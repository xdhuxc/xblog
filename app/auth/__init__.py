#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

"""
与用户认证系统相关的路由可在auth蓝本中定义。对于不同的程序功能，要使用不同的蓝本，保持代码整齐有序。
"""
auth = Blueprint('auth', __name__)

from . import views