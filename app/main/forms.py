#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """
    用户资料编辑表单
    此表单中的所有字段都是可选的，因此长度验证函数允许长度为零。
    """
    user_real_name = StringField('真实姓名', validators=[Length(0, 64)])
    user_location = StringField('地址', validators=[Length(0, 150)])
    user_description = TextAreaField('自我介绍')
    submit = SubmitField('提交')
