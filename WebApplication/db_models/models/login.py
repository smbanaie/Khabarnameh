#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string

__author__ = 'ReS4'

import re
import hashlib
from WebApplication.db_models.models.base_model import *
from WebApplication.classes.permissions.permissions import SystemPermissions, SidebarMenu


# noinspection PyBroadException
class LoginMethod:
    def __init__(self, username, password, system_id, handler):
        self.username = username
        self.password = password
        self.system_id = system_id

        self.user_object = object
        self.user_roles = []
        self.user_permissions = []
        self.sidebar_menu = []
        self.plan_id = None

        self.handler = handler

    @staticmethod
    def mk_pass(password):
        ps = hashlib.md5()
        ps.update(password)
        _hash = ps.hexdigest()
        ps = hashlib.sha1()
        ps.update(password)
        _hash += ps.hexdigest()[:20:-1]
        _hash = _hash[::-1]
        ps = hashlib.new('ripemd160')
        ps.update(_hash)
        return ps.hexdigest()[2:39]

    def check(self):
        try:
            u = SysUsers(username=self.username, system=self.system_id).get_one()

            if u['password'] == LoginMethod.mk_pass(self.password) and u['status'] == "active":
                self.user_object = u

                role_cur = User_roles().select().where(User_roles.user == u['id']).execute()
                self.user_roles = [item.role.name for item in role_cur]

                sp = SystemPermissions(u['id'], self.system_id)
                self.user_permissions = sp.get_all()
                # self.plan_id = u['user_group']['id']

                self.sidebar_menu = SidebarMenu(sp.names, self.system_id, self.handler).menu

                return True
        except Exception, err:
            print ("login check", err)
            pass
        return False

    def check2(self):
        try:
            u = SysUsers(username=self.username, system=self.system_id).get_one()

            if u['status'] == "active":
                self.user_object = u

                role_cur = User_roles().select().where(User_roles.user == u['id']).execute()
                self.user_roles = [item.role.name for item in role_cur]

                sp = SystemPermissions(u['id'], self.system_id)
                self.user_permissions = sp.get_all()
                # self.plan_id = u['user_group']['id']

                self.sidebar_menu = SidebarMenu(sp.names, self.system_id, self.handler).menu

                return True
        except Exception, err:
            # print err
            pass
        return False
