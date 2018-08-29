#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import Regexp
from wtforms.validators import EqualTo
from wtforms import ValidationError

from ..models import User


class LoginForm(FlaskForm):
    """
    用户登录表单
    """
    user_email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    # 第一个参数是在页面显示的字符
    user_email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    user_name = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
        0, 'User Name must have two letters,numbers dots or underscores')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码必须一致。')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')


    """
    这个表单中还有两个自定义的验证函数，以方法的形式实现。
    如果表单类中定义了以validate_开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用。
    """
    def validate_user_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError('该邮件地址已经被注册。')

    def validate_user_name(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('该用户名已经被使用。')


class ChangePasswordForm(FlaskForm):
    """
    更新密码的表单
    """
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='两次输入的密码必须一致。')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('更改密码')


class PasswordResetRequestForm(FlaskForm):
    """
    重置密码请求表单
    """
    user_email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
    """
    重置密码表单
    """
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='两次输入的密码不一致。')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')


class ChangeEmailForm(FlaskForm):
    user_email = StringField('新电子邮件地址', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('更改电子邮箱')

    @staticmethod
    def validate_user_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError('该邮箱已经注册。')