#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web

import functools
from tornado import gen

from pycket.session import SessionMixin
from pycket.notification import NotificationMixin
from WebApplication.classes.permission_system import *

from WebApplication.db_models.models.base_model import *


# from WebApplication.db_models.models.permission_model import *
from WebApplication.classes.permissions.permissions import *

s = SharedConnection()


def authentication():
    def f(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):
            if not self.is_authenticated():
                self.redirect(self.reverse_url("index"))
                return
            try:
                # if PermsId().get_dict()[self.__class__.__name__] not in self.get_user_permissions():
                if self.__class__.__name__ not in self.get_user_permissions():
                    self.render(s.web['template_address'] + "/base/notifications/access_denied.html")
                    return
            except Exception, e:
                pass

            return func(self, *args, **kwargs)

        return func_wrapper

    return f


# noinspection PyBroadException
class Base1Handler(tornado.web.RequestHandler, SessionMixin, NotificationMixin):
    def __init__(self, application, request, **kwargs):
        super(Base1Handler, self).__init__(application, request, **kwargs)

        self.namespace = ''
        self.role = ''
        self.scope = ''

    def get_current_user(self):
        return self.session.get('current_user')

    @property
    def current_system(self):
        return self.session.get('current_system')

    @property
    def current_plan_id(self):
        return self.session.get('current_plan')['id']

    def get_user_roles(self):
        return self.session.get('user_roles')

    def get_user_permissions(self):
        return self.session.get('user_permissions')

    def set_flash(self, name, value):
        self.notifications.set(name, value)

    def get_flash(self, name):
        return self.notifications.get(name)

    def add_error(self, message):
        error_list = self.session.get('error_list')
        if error_list is None:
            error_list = []
        error_list.append(message)
        self.session.set('error_list', error_list)

    def get_errors(self):
        error_list = self.session.get('error_list')
        self.session.delete('error_list')
        return error_list

    def has_error(self):
        return True if self.session.get('error_list') is not None else False

    def is_authenticated(self):
        if self.get_current_user() is not None:
            return True
        return False


class WebBaseHandler(Base1Handler):
    def __init__(self, application, request, **kwargs):
        super(WebBaseHandler, self).__init__(application, request, **kwargs)
        web_db.connect()

        self.data = dict(
            title="",
            user=object,
            active_tab=None,
            system_id=self.current_system,
            system_name=self.session.get("current_system_name"),
            system_pname=self.session.get("full_current_system")['pname'] if self.session.get(
                "full_current_system") else '',
            full_system=self.session.get("full_current_system") if self.session.get("full_current_system") else None,
            url=self.url,
            help_id=1
        )
        try:
            f = self.session.get("full_current_user")
            self.data['full_name'] = u"{} {}".format(f['first_name'], f['last_name'])
        except:
            self.data['full_name'] = ""
        self.errors = []

    def on_finish(self):
        # try:
        #     __user_agent = self.request.headers['User-Agent']
        # except:
        #     __user_agent = ''
        #
        # x_real_ip = self.request.headers.get("X-Forwarded-For")
        # remote_ip = self.request.remote_ip if not x_real_ip else x_real_ip
        #
        # try:
        #     SysSystemLog(
        #         system=self.current_system,
        #         user=self.current_user,
        #         request_type="WEB",
        #         device_id="",
        #         handler=self.__class__.__name__,
        #         link=self.request.uri,
        #         ip=remote_ip,
        #         user_agent=__user_agent
        #     ).add_log()
        # except:
        #     pass
        web_db.close()

    def url(self, url, *args):
        # args = (self.data['system_id'], self.data['system_name']) + args
        return self.reverse_url(url, *args)

    def check_sent_value(self, val, _table, _field, error_msg=None, nullable=False, default=None):
        vl = self.get_argument(val, None)
        if vl is not None:
            if not nullable:
                if vl != '':
                    _table[_field] = vl
                else:
                    if error_msg:
                        self.errors.append(error_msg)
            else:
                _table[_field] = vl if vl else default
        else:
            if error_msg:
                self.errors.append(error_msg)


def error_handler(self, status_code, **kwargs):
    if status_code == 404:
        self.render("base/notifications/404.html")
    else:
        self.render("base/notifications/error_page.html")


tornado.web.RequestHandler.write_error = error_handler
