#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import flash
from flask import request
from flask_login import login_required
from flask_login import current_user
from flask import current_app

from . import main
from .. import db
from ..models import User
from ..models import Role
from ..models import Permission
from ..models import Post
from .forms import PostForm
from .forms import EditProfileForm
from .forms import EditProfileAdminForm
from ..decorators import admin_required

"""
在蓝本中，Flask会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。
命名空间就是蓝本的名字，即Blueprint构造函数的第一个参数，所以视图函数index()注册的端点名是main.index，其URL使用url_for('main.index')获取。
url_for()函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如url_for('.index')，在这种写法中，命名空间是当前请求所在的蓝本。
这意味着同一蓝本中的重定向可以使用简写形式，但是跨蓝本的重定向必须使用带有命名空间的端点名。
"""


# 路由修饰器由蓝本提供
@main.route('/', methods=['GET', 'POST'])
def index():
    """
    处理博客文章的首页路由
    :return:
    """
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        """
        变量current_user由Flask-Login提供，和所有的上下文变量一样，也是通过线程内的代理对象实现。
        这个对象的表现类似用户对象，但实际上却是一个轻度包装，包含真正的用户对象，数据库需要真正的用户对象，因此要调用_get_current_object()方法
        """
        post = Post(post_title=form.post_title.data, post_body=form.post_body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    """
    渲染的页数从请求的查询字符串（request.args）中获取，如果没有明确指定，则默认渲染第一页。
    参数type=int保证参数无法转换成整数时，返回默认值。
    """
    page = request.args.get('page', 1, type=int)
    """
    为了显示某页中的记录，要把all()换成Flask-SQLAlchemy提供的paginate()方法。
    页数是paginate()方法的第一个参数，也是唯一必需的参数。
    可选参数per_page用来指定每页显示的记录数量，如果没有指定，则默认显示20条记录。
    可选参数error_out，当其设为True（默认值）时，如果请求的页数超出了范围，则返回404错误
                    当其设为False时，页数超出范围时会返回一个空列表。
    """
    pagination = Post.query.order_by(Post.post_timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/user/<user_name>')
def user(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        abort(404)
    # User.posts 返回的是查询对象，因此可在其上调用过滤器
    posts = user.posts.order_by(Post.post_timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


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


@main.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(user_id):
    """
    管理员的资料编辑路由
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    form = EditProfileAdminForm(user)
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
