#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import api
from ..models import Post
from ..models import Comment
from .. import db
from flask import request
from flask import current_app
from flask import url_for
from flask import jsonify
from flask import g


@api.route('/comments/<int:comment_id>')
def get_comment(comment_id):
    """
    获取一篇评论
    :param comment_id:
    :return:
    """
    comment = Comment.query.get_or_404(comment_id)
    return jsonify(comment.to_json())


@api.route('/comments/', methods=['GET'])
def get_comments():
    """
    获取某篇博客的所有评论
    :param post_id:
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.comment_timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments', page=page+1)
    return jsonify({
        'comments': [comment.to_json for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_post_comment(post_id):
    """
    创建一个评论
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json, 201, {'Location': url_for('api.get_comment', comment_id=comment.comment_id)})


@api.route('/posts/<int:post_id>/comments')
def get_post_comments(post_id):
    """
    查询一篇博客文章中的所有评论
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.comment_timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('app.get_post_comments', post_id=post_id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('app.get_post_comments', post_id=post_id, page=page+1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
