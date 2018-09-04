#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import SMTPHandler

# 得到当前文件的上一级目录
basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['DEV_DATABASE_URL'] = 'mysql://root:19940423@localhost/xblog'
os.environ['CHARSET'] = 'utf-8'
os.environ['FLASKY_ADMIN'] = 'wanghuanand@sohu.com'


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
    # 数据库相关配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 将其设为True时，每次请求结束后都会自动提交数据库中的变动。
    SQLALCHEMY_RECORD_QUERIES = True  # 启用记录查询统计数字功能

    FLASKY_DB_QUERY_TIMEOUT = 0.5  # 设置缓慢查询的阈值为0.5秒。
    FLASKY_POSTS_PER_PAGE = os.environ.get('FLASKY_POSTS_PER_PAGE') or 10
    FLASKY_FOLLOWERS_PER_PAGE = os.environ.get('FLASKY_FOLLOWERS_PER_PAGE') or 10
    FLASKY_COMMENTS_PER_PAGE = os.environ.get('FLASKY_COMMENTS_PER_PAGE') or 10
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'wanghuanand@sohu.com'

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
    # 在测试配置中禁用CSRF保护
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test-data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod-data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # 把错误通过电子邮件发送给管理员
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.FLASKY_MAIL_SENDER,
                toaddrs=[cls.FLASKY_ADMIN],
                subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' 程序错误',
                credentials=credentials,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
