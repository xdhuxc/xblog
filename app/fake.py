#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User
from .models import Post


def users(count=100):
    """
    生成虚拟用户
    :param count: 生成的虚拟账户数量
    :return:
    """
    fake = Faker()
    i = 0
    while i < count:
        u = User(user_name=fake.email(),
                 user_email=fake.user_name(),
                 password='password',
                 confirmed=True,
                 user_real_name=fake.name(),
                 user_location=fake.city(),
                 user_description=fake.text(),
                 last_access_date=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    """
    生成的虚拟博客文章数量
    :param count:
    :return:
    """
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(post_title=fake.text(),
                 post_body=fake.text(),
                 post_timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()
