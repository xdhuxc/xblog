#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from app import create_app
from app import db
from app.models import User
from app.models import Role
from flask import url_for

import unittest


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # Flask 测试客户端对象
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        """
        默认情况下，get_data()得到的响应主体是一个字节数组，传入参数as_text=True后得到的是一个更易于处理的Unicode字符串。
        """
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # 注册新账户
        response = self.client.post(url_for('auth.register'), data={
            'user_email': 'wanghuan@189.com',
            'user_name': 'yztc',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertTrue(response.status_code == 302)

        # 使用新注册的账户登录
        """
        指定了参数follow_redirects=True，让测试客户端和浏览器一样，自动向重定向的URL发起GET请求。
        指定了这个参数后，返回的不是302状态码，而是请求重定向的URL返回的响应。
        """
        response = self.client.post(url_for('auth.login'), data={
            'user_email': 'wanghuan@189.com',
            'password': 'cat'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hello,\s+yztc!', data))
        self.assertTrue('You have not confirmed your account yet' in data)

        # 发送确认令牌
        user = User.query.filter_by(user_email='wanghuan@189.com').first_or_404()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('你已经确认过你的邮件地址了!' in data)

        # 退出
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('你已经退出登录。' in data)
