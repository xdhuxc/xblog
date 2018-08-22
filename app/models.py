#!/usr/bin/env python
# -*- coding: utf-8 -*-


from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from . import login_manager

import sys
import os

charset = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(charset)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, index=True)
    user_email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    # 是否已经确认该账户可使用邮箱联系
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        # 调用基类的构造函数
        super(User, self).__init__(**kwargs)
        # 如果创建基类对象后还没有定义角色，则根据电子邮箱地址决定将其设为管理员还是默认角色
        if self.role is None:
            if self.user_email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def get_id(self):
        """
        返回一个能唯一识别用户的，并能用于从 user_loader 回调中 加载用户的 unicode 。注意着 必须 是一个 unicode ——如果 ID 原本是 一个 int 或其它类型，你需要把它转换为 unicode。
        :return:
        """
        return unicode(self.user_id)

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

    def generate_confirmation_token(self, expiration=3600):
        """
        生成一个令牌，有效期默认为一小时。
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.user_id})

    def confirm(self, token):
        """
        校验令牌，如果校验通过，则把新添加的confirmed属性设为True。
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        # 检查令牌中的id是否和存储在current_user中的已登录用户匹配
        if data.get('confirm') != self.user_id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode(charset))
            print("data:" + data)
            print("data-reset:" + data.get('reset'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.user_id, 'new_email':new_email}).decode(charset)

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode(charset))
        except:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        # 查看数据库中是否已经有该email
        if self.query.filter_by(user_email=new_email).first() is not None:
            return False
        self.user_email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    """
    %r 调用 repr() 函数打印字符串，repr() 函数返回的字符串是加上了转义序列，是直接书写的字符串的形式。
    %s 调用 str() 函数打印字符串，str()函数返回原始字符串。
    """
    def __repr__(self):
        return '<User %r>' % self.user_name


# Flask-Login要求程序实现一个回调函数，使用指定的标识符加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """
    类变量 __tablename__ 定义在数据库中使用的表名
    如果没有定义__tablename__，flask-SQLAlchemy会使用一个默认的名字，但是默认的表名没有遵守使用复数形式进行命名的约定。
    """
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True)
    # 只有一个角色的default字段需要设置为True，其他都为False，用户注册时，其角色会被设置为默认角色
    default = db.Column(db.Boolean, default=False, index=True)
    # 其值是一个整数，表示位标志，各操作都对应一个位位置，能执行某项操作的角色，其位会被设为1.
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        # 定义角色User，Moderator，Administrator，匿名角色不需要在数据库中表示出来，该角色的含义就是不在数据库中的用户
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES
                          | Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        """
        通过角色名查找现有的角色，然后再进行更新。只有当数据库中没有某个角色时才会创建新角色对象。
        """
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.role_name


class Permission:
    FOLLOW = 0X01
    COMMENT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0x80


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
