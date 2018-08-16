#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 得到当前文件的上一级目录
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Config类作为配置类的基类，其中配置通用信息，在其子类中分别定义专用配置。
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xdhuxc'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_USERNAME = os.environ.get('FLASKY_MAIL_USERNAME') | 'xdhuxc@163.com'
    FLASKY_MAIL_SERVER = 'smtp.163.com'
    FLASKY_MAIL_PASSWORD = 'xdhuxc'
    FLASKY_MAIL_PORT = 25
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URL = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev-data.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test-data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod-data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}