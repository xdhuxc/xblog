#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from app import create_app
from app import db
from app.models import User
from app.models import Role
from flask_script import Manager
from flask_script import Shell
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
import unittest


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """
    manager.command 修饰器让自定义命令变得简单，修饰的函数名就是命令名，函数的文档字符会显示在帮助消息中
    test()函数的函数体中调用了unittest包提供的测试运行函数。
    :return:
    """
    # tests 为要测试的模块名或测试用例目录
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def initdb():
    """
    以命令方式初始化数据库
    :return:
    """
    db.create_all()


if __name__ == '__main__':
    manager.run()
