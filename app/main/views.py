#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import flash
from flask_login import login_required
from flask_login import current_user

from . import main
from .. import db
from ..models import User
from ..models import Role
from .forms import NameForm
from .forms import EditProfileForm
from .forms import EditProfileAdminForm
from ..decorators import admin_required


# 路由修饰器由蓝本提供
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        """
        在蓝本中，Flask会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。
        命名空间就是蓝本的名字，即Blueprint构造函数的第一个参数，所以视图函数index()注册的端点名是main.index，其URL使用url_for('main.index')获取。
        url_for()函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如url_for('.index')，在这种写法中，命名空间是当前请求所在的蓝本。
        这意味着同一蓝本中的重定向可以使用简写形式，但是跨蓝本的重定向必须使用带有命名空间的端点名。
        
        """
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/user/<user_name>')
def user(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    显示时，应该从数据库中查询出已有内容，显示在页面，等待用户修改。
    :return:
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.user_real_name = form.user_real_name.data
        current_user.user_location = form.user_location.data
        current_user.user_description = form.user_description.data
        db.session.add(current_user)
        db.session.commit()
        flash('你的资料已经更新。')
        return redirect(url_for('main.user', user_name=current_user.user_name))
    user = User.query.filter_by(user_name=current_user.user_name).first()
    form.user_real_name.data = user.user_real_name
    form.user_location.data = user.user_location
    form.user_description.data = user.user_description
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """
    管理员的资料编辑路由
    :param id:
    :return:
    """
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm
    if form.validate_on_submit():
        user.user_name = form.user_name.data
        user.user_email = form.user_email.data
        user.confirmed = form.confirmed.data
        user.user_role = Role.query.get(form.user_role.data)
        user.user_real_name = form.user_real_name.data
        user.user_location = form.user_location.data
        user.user_description = form.user_description.data
        db.session.add(user)
        db.session.commit()
        flash('用户信息已经更新。')
        return redirect(url_for('main.user', user_name=user.user_name))
    form.user_email.data = user.user_email
    form.user_name.data = user.user_name
    form.confirmed.data = user.confirmed
    form.user_role.data = user.role_id
    form.user_real_name.data = user.user_real_name
    form.user_location.data = user.user_location
    form.user_description.data = user.user_description
    return render_template('edit_profile.html', form=form, user=user)
