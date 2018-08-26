#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models import User
from app.models import Role
from app import create_app
from app import db


if __name__ == '__main__':
    app = create_app('default')
    app.app_context().push()

    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.user_email == app.config['FLASKY_ADMIN']:
                user.role = Role.query.filter_by(role_name='Administrator').first()
                db.session.add(user)
                db.session.commit()
            else:
                user.role = Role.query.filter_by(default=True).first()
                db.session.add(user)
                db.session.commit()
