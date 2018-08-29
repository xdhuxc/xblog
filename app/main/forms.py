#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import Regexp
from flask_pagedown.fields import PageDownField

from ..models import Role
from ..models import User


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


class EditProfileAdminForm(FlaskForm):
    user_email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
    user_name = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名必须以字母开头，且包含字母、数字、‘.’或者下划线。')])
    confirmed = BooleanField('是否已认证')
    # 使用coerce=int参数，其作用是保证这个字段的data属性值是整数
    user_role = SelectField('角色', coerce=int)
    user_real_name = StringField('真实姓名', validators=[Length(0, 64)])
    user_location = StringField('所在地', validators=[Length(0, 64)])
    user_description = TextAreaField('自我介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.user_role.choices = [(role.role_id, role.role_name) for role in Role.query.order_by(Role.role_name).all()]
        self.user = user

    def validate_user_email(self, field):
        """
        首先要检查字段的值是否发生了变化，如果有变化，就要保证新值不和其他用户的相应字段值重复；
        如果字段值没有变化，则应该跳过验证。
        :param field:
        :return:
        """
        if field.data != self.user.user_email and User.query.filter_by(user_email=field.data).first():
            raise ValidationError('该邮箱已经被注册。')

    def validate_user_name(self, field):
        if field.data != self.user.user_name and User.query.filter_by(user_name=field.data).first():
            raise ValidationError('该用户名已经被使用。')


class PostForm(FlaskForm):
    """
    博客表单
    """
    post_title = StringField('标题',
                             validators=[DataRequired(), Length(5, 120, message='标题必须填写并且须多于10个字符。')])
    post_body = PageDownField('正文', validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    """
    评论表单
    """
    comment_body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('提交')