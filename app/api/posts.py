#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import api
from .errors import forbidden
from ..models import Post
from ..models import Permission
from ..decorators import permission_required
from flask import request
from flask import g
from flask import jsonify
from flask import url_for
from flask import current_app
from .. import db


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    """
    文章资源POST请求处理程序
    :return:
    """
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json(), 201, {'Location': url_for('api.get_post', post_id=post.post_id, _external=True)})


@api.route('/posts/', methods=['GET'])
def get_posts():
    """
    实现查询所有博客文章的资源端点，采用分页方式实现
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:post_id>')
def get_post(post_id):
    """
    查找某篇博客文章
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_json())


@api.route('/posts/<int:post_id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(post_id):
    """
    编辑修改某篇文章
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    # 作者和管理员可以修改博客内容
    if g.current_user != post.author and not g.current_user.can(Permission.ADMIN):
        return forbidden('权限不足，无法操作。')
    post.post_title = request.json.get('post_title', post.post_title)
    post.post_body = request.json.get('post_body', post.post_body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json)




