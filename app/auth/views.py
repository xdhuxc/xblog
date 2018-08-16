#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from . import auth


@auth.route('/login')
def login():
    """

    :return:
    """

    """
    为render_template()指定的模板文件保存在auth目录中，这个目录必须在app/template中创建，因为flask认为模板的路径是相对于程序模板目录而言的
    """
    return render_template('auth/login.html')