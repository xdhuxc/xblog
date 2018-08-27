#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
import hashlib

from markdown import markdown
import bleach
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask import request
from . import db
from . import login_manager

charset = os.environ.get('CHARSET') or 'utf-8'
reload(sys)
sys.setdefaultencoding(charset)


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, index=True)
    user_real_name = db.Column(db.String(64), comment='用户真实姓名')
    user_location = db.Column(db.String(120), comment='用户所在地')
    user_description = db.Column(db.Text(), comment='用户的自我介绍')
    register_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='注册日期')
    last_access_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='最后访问日期')
    user_email = db.Column(db.String(64), unique=True, index=True, comment='用户邮箱')
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    confirmed = db.Column(db.Boolean, default=False, comment='是否已确认该邮箱')
    gravatar_hash = db.Column(db.String(32), comment='电子邮件地址的MD5散列值')
    """
    lazy属性设置为dynamic，关系属性不会直接返回记录，而是返回查询对象，所以在执行查询之前还可以添加额外的过滤器。
    """
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        # 调用基类的构造函数
        super(User, self).__init__(**kwargs)
        # 如果创建基类对象后还没有定义角色，则根据电子邮箱地址决定将其设为管理员还是默认角色
        if self.role is None:
            if self.user_email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(role_name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # 添加用户的电子邮件地址MD5散列值，用于生成用户图像。
        if self.user_email is not None and self.gravatar_hash is None:
            self.gravatar_hash = hashlib.md5(self.user_email.encode(charset)).hexdigest()

    def ping(self):
        """
        每次收到用户的请求时都要调用ping()方法
        :return:
        """
        self.last_access_date = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

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
        if data.get('change_email') != self.user_id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        # 查看数据库中是否已经有该email
        if self.query.filter_by(user_email=new_email).first() is not None:
            return False
        self.user_email = new_email
        self.gravatar_hash = hashlib.md5(self.user_email.encode(charset)).hexdigest()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        generated_hash = self.gravatar_hash or hashlib.md5(self.user_email.encode(charset)).hexdigest()
        return '{url}/{generated_hash}?s={size}&d={default}&r={rating}'.format(
            url=url, generated_hash=generated_hash, size=size, default=default, rating=rating)

    """
    %r 调用 repr() 函数打印字符串，repr() 函数返回的字符串是加上了转义序列，是直接书写的字符串的形式。
    %s 调用 str() 函数打印字符串，str()函数返回原始字符串。
    """
    def __repr__(self):
        return '%r' % {'User': (self.user_id, self.user_name, self.user_email, self.user_real_name,
                                self.user_location, self.user_description, self.confirmed)}


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

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        """
        检查一个角色是否拥有某个权限，将当前对象的权限值整数的二进制与传入的权限值二进制进行&操作，然后再判断与传入值是否相等
        :param perm:
        :return:
        """
        return self.permissions & perm == perm

    def add_permission(self, perm):
        """
        为角色添加权限
        :param perm:
        :return:
        """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """
        取消角色的权限
        :param perm:
        :return:
        """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    @staticmethod
    def insert_roles():
        # 定义角色User，Moderator，Administrator，匿名角色不需要在数据库中表示出来，该角色的含义就是不在数据库中的用户
        roles = {
            'User': [Permission.FOLLOW | Permission.COMMENT | Permission.WRITE],
            'Moderator': [Permission.FOLLOW | Permission.COMMENT | Permission.WRITE | Permission.MODERATE],
            'Administrator': [Permission.FOLLOW | Permission.COMMENT | Permission.WRITE
                              | Permission.MODERATE | Permission.ADMIN],
        }
        default_role = 'User'
        """
        通过角色名查找现有的角色，然后再进行更新。只有当数据库中没有某个角色时才会创建新角色对象。
        """
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.role_name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '%r' % {'Role': (self.role_id, self.role_name, self.default, self.permissions, self.users)}


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='博客ID')
    post_title = db.Column(db.String(120), unique=True, index=True, comment='博客标题')
    post_body = db.Column(db.Text, comment='博客正文')
    post_timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='博客撰写时间')
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), comment='博客作者')
    post_body_html = db.Column(db.Text, comment='博客文章的HTML代码')

    @staticmethod
    def on_changed_body(target, value, old_value, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquota', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.post_body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags,
            strip=True))

    def __repr__(self):
        return '%r' % {'Post': (self.post_id, self.post_title, self.post_body, self.post_timestamp,
                       self.author, self.post_body_html)}


"""
on_changed_body()函数注册在post_body字段上，是SQLAlchemy “set”事件的监听程序，这意味着
只要这个类实例的post_body字段设置了新值，函数就会自动被调用。
"""
db.event.listen(Post.post_body, 'set', Post.on_changed_body)
