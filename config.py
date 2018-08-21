#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 得到当前文件的上一级目录
basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['DEV_DATABASE_URL'] = 'mysql://root:19940423@localhost/xblog'

"""
wanghuanand@sohu.com
smtp.sohu.com
Wanghuan1994
"""

class Config:
    """
    Config类作为配置类的基类，其中配置通用信息，在其子类中分别定义专用配置。
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xdhuxc'
    # 将其设为True时，每次请求结束后都会自动提交数据库中的变动。
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    # 邮箱配置
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER') or 'wanghuanand@sohu.com'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.sohu.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'wanghuanand')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'Wanghuan1994')

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev-data.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test-data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod-data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
