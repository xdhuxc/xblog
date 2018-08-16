#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, index=True)
    user_email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

    """
    %r 调用 repr() 函数打印字符串，repr() 函数返回的字符串是加上了转义序列，是直接书写的字符串的形式。
    %s 调用 str() 函数打印字符串，str()函数返回原始字符串。

    """
    def __repr__(self):
        return '<User %r>' % self.user_name

    """
    python内置的@property装饰器负责把一个方法变成属性调用。
    把一个getter方法变成属性，只需要加上@property就可以了
    可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性
    """
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    """
    @password.setter负责把一个setter方法变成属性赋值
    """
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        接收密码作为参数，将其传给Werkzeug提供的check_password_hash()函数，和存储在User模型中的密码散列值进行比对。
        如果这个方法返回True，就表明密码是正确的。
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    """
    类变量 __tablename__ 定义在数据库中使用的表名
    如果没有定义__tablename__，flask-SQLAlchemy会使用一个默认的名字，但是默认的表名没有遵守使用复数形式进行命名的约定。
    """
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.role_name
