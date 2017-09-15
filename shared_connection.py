#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__author__ = 'ReS4'


class SharedConnection:
    def __init__(self):
        self.applications_root = os.path.join(os.path.dirname(__file__), "")
        self.domain = '.localhost'

        self.mobile_redis = {
            'host': '127.0.0.1', 'port': 6379, 'db': 4, 'password': "1234567890 0987654321foo"
        }

        self.mobile_settings = {
            'port': 8851,
            "mandrill_api_key": 'mmwmS-pWBLPYohHlZkTzOQ',
            "GOOGLE_API_KEY": "AIzaSyCiKl9f_PcBZvD-UKibJz-Jt_RVvTV_rfU",
            "GOOGLE_API_URL": "https://android.googleapis.com/gcm/send"
        }

        self.SESSION_TIME = 2592000

        self.web = {
            'port': 8850,
            'server_ip': '127.0.0.1',
            'server_path': os.path.join(self.applications_root, 'WebApplication/'),
            'mysql': {
                'host': '127.0.0.1',
                'db': 'asemaneh_db',
                # 'user': 'root',
                'user': 'asemaneh_user',
                # 'password': '',
                'password': 'W5URfc2qLcBJSwDt',
                'port': 3306,
            },
            'redis': {
                'password': '1234567890 0987654321foo',
            },
            'template_address': os.path.join(os.path.dirname(__file__), "WebApplication", "template"),
            'static_address': os.path.join(os.path.dirname(__file__), "static"),
        }

        self.auth = {
            'mysql': {
                'host': '127.0.0.1',
                'db': 'asemaneh_db',
                # 'user': 'root',
                'user': 'asemaneh_user',
                # 'password': '',
                'password': 'W5URfc2qLcBJSwDt',
                'port': 3306,
            }
        }

        self.global_config = {
            'cookie_secret': "po#Y6A95j6ssv7*&3ez3n6dwsal",
            'login_url': 'http://{0}:{1}/login'.format(self.web['server_ip'], self.web['port']),
            'logout_url': 'http://{0}:{1}/logout'.format(self.web['server_ip'], self.web['port']),
            'redis': {
                'host': '127.0.0.1',
                'port': 6379,
                'password': "1234567890 0987654321foo",
                'db_sessions': 8,
                'db_notifications': 9,
            },
        }
