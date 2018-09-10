#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import click
from app import create_app
from app import db
from app.models import User
from app.models import Role
from app.models import Post
from app.models import Comment
from app.models import Permission
from flask_script import Manager
from flask_script import Shell
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_migrate import upgrade


charset = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(charset)


# 获取当前文件所在目录
basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Comment=Comment, Permission=Permission)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    """
    以命令方式初始化数据库
    :return:
    """
    db.create_all()


@manager.command
def dropdb():
    """
    以命令方式初始化数据库
    :return:
    """
    db.drop_all()


@manager.command
def profile(length=25):
    """
    在请求分析器的监视下运行程序
    :param length:
    :return:
    """
    profile_dir = os.path.join(basedir, 'tmp\profile')
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length])
    app.run()


@manager.command
def deploy():
    """
    运行部署命令
    :return:
    """
    # 把数据库迁移到最新修订版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()
    # 所有用户都关注自己
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()
