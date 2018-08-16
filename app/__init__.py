#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config
from .main import main as main_blueprint
from .auth import auth as auth_blueprint

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
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

    # 路由和自定义错误页面
    app.register_blueprint(main_blueprint)
    """
    如果使用了url_prefix这个参数，注册后蓝本中定义的所有路由都会加上指定的前缀，即这个示例中的/auth
    例如，/login路由会注册成/auth/login。在开发Web服务器中，完整的URL就变成了http://127.0.0.1:5000/auth/login
    """
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

