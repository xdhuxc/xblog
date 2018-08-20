#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from . import auth
from .forms import LoginForm
from .forms import RegistrationForm
from ..models import User
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """

    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            """
            用户访问未授权的URL时会显示登录表单，Flask-Login会把原地址保存在查询字符串的next参数中，这个参数可从request.args字典中读取
            如果查询字符串中没有next参数，则重定向到首页。
            """
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    # 当请求类型是GET时，视图函数直接渲染模板，显示表单。
    return render_template('auth/login.html', form=form)

    """
    为render_template()指定的模板文件保存在auth目录中，这个目录必须在app/template中创建，因为flask认为模板的路径是相对于程序模板目录而言的
    """
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_email=form.user_email.data,
                    user_name=form.user_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # 调用Flask-Login中的logout_user()函数，删除并重设用户会话
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

"""
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
"""

