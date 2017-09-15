#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

__author__ = 'ReS4'

from WebApplication.handlers.base import *
# from WebApplication.classes.permission_system import *


class SystemPermissionsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "مجوزهای دسترسی"
        self.data['help_id'] = "12"
        self.render('base/system/permissions/permissions.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):

        _username = self.get_argument("username", None)
        if _username:

            u = SysUsers.is_exist(user_name=_username, system=self.current_system)
            if u:
                if u['id'] == self.current_user:
                    self.write({"status": False, "error": "شما امکان ویرایش مجوزهای دسترسی خود را ندارید."})
                    return

                p = SysPermissions(user=u['id'], system=self.current_system).get_all_perms()
                self.write(
                    {
                        "status": True,
                        "tree": SystemPermissions(u['id'], self.current_system).get_all_user_permissions(p),
                        "user": u
                    }
                )
            else:
                self.write({"status": False})

    @gen.coroutine
    @authentication()
    def post(self):
        username = self.get_argument("username", None)
        permissions = self.get_argument("permissions", None)

        if permissions:
            try:
                permissions = json.loads(permissions)
            except:
                permissions = []
        else:
            permissions = []

        u = SysUsers.is_exist(user_name=username, system=self.current_system)

        if u:
            if permissions:
                if "0" in permissions:
                    permissions.remove("0")

            if SysPermissions(user=u['id'], system=self.current_system).add_user_permission(permissions):
                self.write({"status": True})
            else:
                self.write({"status": False})

