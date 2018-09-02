#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import api
from ..models import User
from ..models import Post
from flask import jsonify
from flask import request
from flask import current_app
from flask import url_for


@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    查询一个用户
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())


@api.route('/users/<int:user_id>/posts/', methods=['GET'])
def get_user_posts(user_id):
    """
    获取一个用户发布的所有博客文章
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.post_timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', user_id=user_id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', user_id=user_id, page=page+1)

    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:user_id>/timeline', methods=['GET'])
def get_followed_posts(user_id):
    """
    一个用户所关注用户发布的文章
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.post_timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_followed_posts', user_id=user_id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_followed_posts', user_id=user_id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
