#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask_login import login_required
from flask_login import login_user

from . import auth
from .forms import LoginForm
from ..models import User


@auth.route('/login')
def login():
    """

    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    # 当请求类型是GET时，视图函数直接渲染模板，显示表单。
    return render_template('auth/login.html', form=form)

    """
    为render_template()指定的模板文件保存在auth目录中，这个目录必须在app/template中创建，因为flask认为模板的路径是相对于程序模板目录而言的
    """
    return render_template('auth/login.html', form=form)

"""
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
"""

