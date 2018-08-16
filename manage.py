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

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()