#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from . import main
from .forms import NameForm


# 路由修饰器由蓝本提供
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        """
        在蓝本中，Flask会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。
        命名空间就是蓝本的名字，即Blueprint构造函数的第一个参数，所以视图函数index()注册的端点名是main.index，其URL使用url_for('main.index')获取。
        url_for()函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如url_for('.index')，在这种写法中，命名空间是当前请求所在的蓝本。
        这意味着同一蓝本中的重定向可以使用简写形式，但是跨蓝本的重定向必须使用带有命名空间的端点名。
        
        """

        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())