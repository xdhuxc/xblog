#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from base64 import b64encode
import json

from app import create_app
from app import db
from app.models import Role
from app.models import User
from flask import url_for

CHARSET = os.environ.get('CHARSET') or 'utf-8'


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, user_name, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (user_name + ':' + password).encode(CHARSET)).decode(CHARSET),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get(url_for('api.get_posts'), content_type='application/json')
        self.assertTrue(response.status_code == 401)

    def test_posts(self):
        # 添加一个用户
        r = Role.query.filter_by(role_name='User').first_or_404()
        self.assertIsNotNone(r)
        u = User(user_email='xdhuxc@123.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # 写一篇文章
        response = self.client.post(
            url_for('api.new_post'),
            headers=self.get_api_headers('xdhuxc@123.com', 'cat'),
            data=json.dumps({'post_body': 'body of the *blog* post'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # 获取刚发布的文章
        response = self.client.get(
            url, headers=self.get_api_headers('xdhuxc@123.com', 'cat')
        )
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode(CHARSET))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['post_body'] == 'body of the *blog* post')
        self.assertTrue(json_response['post_body_html'] == '<p>body of the <em>blog</em> post</p>')
