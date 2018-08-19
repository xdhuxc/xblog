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
    user_email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me login')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    # 第一个参数是在页面显示的字符
    user_email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    user_name = StringField('User Name', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
        0, 'User Name must have two letters,numbers dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_user_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_user_name(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('User Name already in use.')