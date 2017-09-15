# !/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options, define

from WebApplication.ui_modules import base_ui_module
from WebApplication.url import url_patterns

from shared_connection import SharedConnection

import os

__author__ = 'ReS4'

sh_connection = SharedConnection()

define("port", default=sh_connection.web['port'], help="run on the given port", type=int)


class WebSystemApplication(tornado.web.Application):
    def __init__(self):
        handlers = url_patterns
        settings = dict(
            debug=True,
            autoreload=False,
            cookie_secret=sh_connection.global_config['cookie_secret'],
            xsrf_cookies=True,
            login_url=sh_connection.global_config['login_url'],
            logout_url=sh_connection.global_config['logout_url'],
            template_path=os.path.join(os.path.dirname(__file__), "WebApplication/template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules=base_ui_module,
            **{
                'pycket': {
                    'engine': 'redis',
                    'storage': {
                        'host': sh_connection.global_config['redis']['host'],
                        'port': sh_connection.global_config['redis']['port'],
                        'password': sh_connection.global_config['redis']['password'],
                        'db_sessions': sh_connection.global_config['redis']['db_sessions'],
                        'db_notifications': sh_connection.global_config['redis']['db_notifications'],
                        'max_connections': 2 ** 31,
                    },
                    'cookies': {
                        'expires_days': 0.34,
                        # 'domain': sh_connection.domain,
                    },
                },
            }
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WebSystemApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
