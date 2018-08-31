#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import AnonymousUser
from ..models import User
from .errors import unauthorized
from .errors import forbidden
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """
    支持令牌的验证回调
    :param email_or_token:
    :param password:
    :return:
    """
    # 如果电子邮件地址或认证令牌为空，则为匿名用户
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    # 如果密码为空，则假定email_or_token提供的是令牌，按照令牌方式认证
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    # 如果这两个参数都不为空，则使用常规的电子邮件地址和密码进行认证
    user = User.query.filter_by(user_email=email_or_token).first_or_404()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    """
    Flask-HTTPAuth错误处理程序
    :return:
    """
    return unauthorized('非法的认证')


@api.before_request
@auth.login_required
def before_request():
    """
    由于api蓝本中的所有路由都要使用相同的方式进行保护，所以可以在before_request处理程序中使用一次login_required修饰器，
    应用到整个蓝本，从而api蓝本中的所有路由都能进行自动认证。
    :return:
    """
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('未确认的账户')


@api.route('/token')
def get_token():
    """
    生成认证令牌，由于这个路由也在蓝本中，所以添加到before_request处理程序上的认证机制也会用在这个路由上。
    :return:
    """
    # 为了避免客户端使用旧令牌申请新令牌，要在视图函数中检查g.token_used变量的值。
    if g.current_user.is_anonymous() or g.token_used:
        return unauthorized('非法的认证。')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})
