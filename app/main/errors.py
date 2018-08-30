#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import jsonify
from . import main

"""
如果使用errorhandler修饰器，那么只有蓝本中的错误才能触发处理程序。要想注册程序全局的错误处理程序，必须使用app_errorhandler。
"""


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '禁止访问。'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """
    浏览器一般不限制响应的格式，但是需要为只接受JSON格式而不接受HTML格式的客户端生成JSON格式响应
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '找不到请求的页面。'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '服务器内部错误。'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
