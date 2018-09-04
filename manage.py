#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import get_variables

# 加载环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    get_variables(dotenv_path)

charset = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(charset)

cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    """
    函数coverage.coverage()用于启动覆盖检测引擎。
    branch=True选项开启分支覆盖分析，除了跟踪哪行代码已经执行外，还要检查每个条件语句的True分支和False分支是否都执行了。
    include选项用来限制程序包中文件的分析范围，只对这些文件中的代码进行覆盖检查。
    如果不指定include选项，虚拟环境中安装的全部扩展和测试代码都会包含进覆盖报告中，给报告添加很多杂项。
    """
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()


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
@click.option('--coverage/--no-coverage', default=False)
def test(coverage):
    """
    运行单元测试用例
    :param coverage:
    :return:
    """
    """
    manager.command 修饰器让自定义命令变得简单，修饰的函数名就是命令名，函数的文档字符会显示在帮助消息中
    test()函数的函数体中调用了unittest包提供的测试运行函数。
    """
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    # tests 为要测试的模块名或测试用例目录
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('代码覆盖总结：'.decode(charset))
        cov.report()
        covdir = os.path.join(basedir, 'tmp\coverage')
        cov.html_report(directory=covdir)
        print('HTML版本：file:\\\\%s\index.html'.decode(charset) % covdir)
        cov.erase()


@manager.command
def initdb():
    """
    以命令方式初始化数据库
    :return:
    """
    db.create_all()


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
