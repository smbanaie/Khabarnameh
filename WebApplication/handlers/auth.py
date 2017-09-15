#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from WebApplication.classes.functions import upload_photo, rand_string

__author__ = 'ReS4'

from WebApplication.handlers.base import *
from WebApplication.db_models.models.login import LoginMethod


class LoginHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        if self.current_user is not None:
            self.redirect(self.reverse_url('system_dashboard'))
            return

        self.render('base/index/index.html', **self.data)

    @gen.coroutine
    def post(self):
        if self.current_user is not None:
            self.redirect(self.reverse_url('system_dashboard'))
            return
        time_login = self.get_argument('time_login', None)
        if time_login == "first":
            username = self.get_argument('_uname', '')
            password = self.get_argument('_pass', '')
            ls_user = SysUsers(username=username).get_all_for_login()
            if len(ls_user) == 1:
                system_id = ls_user[0]['system'].id
                l = LoginMethod(username, password, system_id, self)
                if l.check():

                    if ("ADMIN" in l.user_roles) or ("EDITOR" in l.user_roles):
                        self.session.set("current_system", l.user_object['system']['id'])
                        self.session.set("current_plan", SysSystemPlans(system=l.user_object['system']['id']).get_one())
                        self.session.set("full_current_system", l.user_object['system'])
                        self.session.set("current_system_name", l.user_object['system']['name'])
                        self.session.set("current_user", l.user_object['id'])
                        self.session.set("full_current_user", l.user_object)
                        self.session.set('user_roles', l.user_roles)
                        self.session.set('user_permissions', l.user_permissions)
                        self.session.set('sidebar_menu', l.sidebar_menu)
                        self.redirect(self.url("system_dashboard"))

                    else:
                        self.add_error("نام کاربری یا رمز عبور نادرست است.")
                        self.redirect(self.reverse_url("index"))

                else:
                    self.add_error("نام کاربری یا رمز عبور نادرست است.")
                    self.redirect(self.reverse_url("index"))

            elif len(ls_user) > 1:
                password1= LoginMethod.mk_pass(password)
                user = SysUsers(username=username, password=password1).is_exist_for_login()
                if user:
                    self.session.set('un_for_login', username)
                    self.session.set('pass_for_login', password)
                    ls_sys = []
                    for i in ls_user:
                        try:
                            ls_sys.append(i['system'])
                        except Exception, e:
                            pass
                    self.data['systems'] = ls_sys
                    self.render('base/auth/login_second.html', **self.data)
                else:
                    self.add_error("نام کاربری یا رمز عبور نادرست است.")
                    self.redirect(self.reverse_url("index"))
            else:
                self.add_error("نام کاربری یا رمز عبور نادرست است.")
                self.redirect(self.reverse_url("index"))


        elif time_login == "second":
            user_name = self.session.get('un_for_login')
            password = self.session.get('pass_for_login')
            system_id = self.get_argument("system_id", None)
            l = LoginMethod(user_name, password, system_id, self)
            if l.check2():
                if ("ADMIN" in l.user_roles) or ("EDITOR" in l.user_roles):
                    self.session.delete('un_for_login')
                    self.session.delete('pass_for_login')
                    self.session.set("current_system", l.user_object['system']['id'])
                    self.session.set("current_plan", SysSystemPlans(system=l.user_object['system']['id']).get_one())
                    self.session.set("full_current_system", l.user_object['system'])
                    self.session.set("current_system_name", l.user_object['system']['name'])
                    self.session.set("current_user", l.user_object['id'])
                    self.session.set("full_current_user", l.user_object)
                    self.session.set('user_roles', l.user_roles)
                    self.session.set('user_permissions', l.user_permissions)
                    self.session.set('sidebar_menu', l.sidebar_menu)
                    self.redirect(self.url("system_dashboard"))
                else:
                    ls_user = SysUsers(username=user_name).get_all_for_login()
                    ls_sys = []
                    for i in ls_user:
                        try:
                            ls_sys.append(i['system'])
                        except Exception, e:
                            pass
                    self.data['systems'] = ls_sys
                    self.add_error("شما اجازه ورود به این سیستم را ندارید.")
                    self.render('base/auth/login_second.html', **self.data)
            else:
                self.add_error("نام کاربری یا رمز عبور نادرست است.")
                self.render('base/auth/login.html', **self.data)
        else:
            self.add_error("نام کاربری یا رمز عبور نادرست است.")
            self.render('base/auth/login.html', **self.data)
            return

# noinspection PyBroadException
class GetCitiesHandler(WebBaseHandler):
    @gen.coroutine
    def post(self):
        try:
            _id = self.get_argument("pid", "")
            ct = []

            ct = SysCity(province_id=_id).get_all()

            sorted_ls = sorted(ct, key=lambda k: k['name'], reverse=False)
            self.write({'city': sorted_ls})

        except Exception, e:
            self.write("0")


class LogoutHandler(WebBaseHandler):
    def get_post(self, *args, **kwargs):
        for i in self.session.keys():
            self.session.delete(i)
        self.redirect(self.reverse_url('index'))

    @gen.coroutine
    def get(self, *args, **kwargs):
        self.get_post(self, args, kwargs)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.get_post(self, args, kwargs)
