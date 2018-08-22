#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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
from .forms import ChangePasswordForm
from .forms import PasswordResetRequestForm
from .forms import PasswordResetForm
from .forms import ChangeEmailForm
from ..models import User
from .. import db
from ..email import send_email
from flask_login import current_user

import os

charset = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
# 设置编解码时默认的字符集，需要和文件的编码字符集一致，不设置的话，在windows下，默认为：ASCII
sys.setdefaultencoding(charset)


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
    """
    用户注册后，将新用户添加到数据库后，发送确认电子邮件，并重定向到index.html
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_email=form.user_email.data,
                    user_name=form.user_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.user_email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # 调用Flask-Login中的logout_user()函数，删除并重设用户会话
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    """
    同时满足以下三个条件时，before_app_request处理程序会拦截请求：
    1）用户已经登录（current_user.is_authenticated()必须返回True）
    2）用户的账户还未确认
    3）请求的端点（使用request.endpoint获取）不在auth蓝本中。访问认证路由要获取权限，因为这些路由的作用是让用户确认账户或执行其他账户管理操作
    如果请求满足以上3个条件，则会被重定向到/auth/unconfirmed路由，显示一个确认账户相关信息的页面。
    :return:
    """
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.user_email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    修改密码，修改成功后跳转至首页
    :return:
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已经修改！')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误！')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    # 如果不是一个匿名用户，返回首页
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # 查询用户信息
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user:
            # 生成 token
            token = user.generate_confirmation_token()
            # 发送重置密码的确认邮件
            send_email(user.user_email, '重置密码', 'auth/email/reset_password', user=user, token=token)
            flash('重置密码的邮件已经发送至你的邮箱 %s' % user.user_email)
            # 跳转首页？登录页？（其实在同一个页面）
            return redirect(url_for('auth.login'))
    # 使用GET请求第一次访问时，渲染重置密码的表单
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('你的密码已经重置。')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        # 判断密码是否合法
        if current_user.verify_password(form.password.data):
            new_email = form.user_email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '确认邮箱地址', 'auth/email/change_email', user=current_user, token=token)
            flash('确认新邮箱的邮件已发送至 %s' % new_email)
            return redirect(url_for('main.index'))
        else:
            flash('不合法的邮箱或密码。')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('你的电子邮箱地址已经更改，请重新登录。')
    else:
        flash('请求错误。')
    logout()
    return redirect(url_for('main.index'))



"""
@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
"""

