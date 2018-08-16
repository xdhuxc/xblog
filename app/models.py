#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

    """
    %r 调用 repr() 函数打印字符串，repr() 函数返回的字符串是加上了转义序列，是直接书写的字符串的形式。
    %s 调用 str() 函数打印字符串，str()函数返回原始字符串。
    """
    def __repr__(self):
        return '<User %r>' % self.user_name


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
