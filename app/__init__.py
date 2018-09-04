#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_sslify import SSLify
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()

"""
LoginManager对象的session_protection属性可以设为None，'basic'或'strong'，以提供不同的安全等级防止用户会话遭串改
设为'strong'时，Flask-Login会记录客户端IP地址和浏览器的用户代理信息，如果发现异动，就退出用户。
"""
login_manager.session_protection = 'strong'
# login_view 属性设置登录页面的端点，登录路由在蓝本auth中定义，因此要在前面加上蓝本auth的名字
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """
    延迟创建程序实例，把创建过程移到可显式调用的工厂函数中

    这种方法不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例。
    :param config_name:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if app.config['SSL_ENABLE']:
        sslify = SSLify(app)

    # 路由和自定义错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    """
    如果使用了url_prefix这个参数，注册后蓝本中定义的所有路由都会加上指定的前缀，即这个示例中的/auth
    例如，/login路由会注册成/auth/login。在开发Web服务器中，完整的URL就变成了http://127.0.0.1:5000/auth/login
    """
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

