#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ReS4'

import json
from WebApplication.db_models.models.base_model import SysUsers
from WebApplication.db_models.models.permission_model import *


# from WebApplication.classes.permissions import doctor_perms, user_perms, clerk_perms, admin_perms

# perms = doctor_perms.doctor_perms + user_perms.user_perms + clerk_perms.clerk_perms + admin_perms.admin_perms

class MenuTree:
    def __init__(self, perms, selected_perms=None):
        self.perms = perms
        self.selected_perms = [i['perm_name'] for i in selected_perms] if selected_perms else []

    def get_js_tree(self):
        tree = [
            {
                'id': "0", 'parent': "#",
                'text': "سیستم مدیریت مجوز ها", 'state': {'selected': False}, 'icon': 'fa fa-comments-o'
            }
        ]

        # perms = SystemPermissions.get_perms(self.system)
        for child in self.perms:
            selected = True if child['name'] in self.selected_perms else False
            tree.append({
                'id': child['name'], 'parent': child['parent'] if child['parent'] else "0",
                'text': child['title'], 'state': {'selected': selected}, 'icon': 'fa fa-comments-o'
            })
        return json.dumps(tree)


class SystemPermissions:
    def __init__(self, user, system):
        self.user = user
        self.system = system

        self.__user_object = self.__get_user()
        if not self.__user_object:
            raise Exception("Cannot find the user.")

        self.names = []
        self.plan_perms = SystemPermissions.get_perms(self.system)

    def __get_user(self):
        return SysUsers(_id=self.user, system=self.system).get_one()

    def __get_user_perms(self):
        return SysPermissions(user=self.user, system=self.system).get_all_perms()

    @staticmethod
    def get_perms(system):
        return SysPlanPermissions(plan=SysSystemPlans(system=system).get_one()['id']).get_all_perms_by_plan()

    def __get_user_group_perms(self):
        d = list()
        perms = self.plan_perms
        for child in [i for i in perms if i['default']]:
            self.names.append(child['name'])
            for j in self.__nn(child['handlers']):
                d.append(j)
        return d

    def __nn(self, js):
        try:
            z = json.loads(js)
            if z:
                return z
            else:
                return []
        except:
            return []

    def get_all(self):
        # d = self.__get_user_group_perms()
        u_perm = self.__get_user_perms()

        perms = self.plan_perms
        d = []
        for i in u_perm:
            self.names.append(i['perm_name'])
            for k in [self.__nn(j['handlers']) for j in perms if j['name'] == i['perm_name']]:
                for p in k:
                    d.append(p)

        return d

    def get_all_user_permissions(self, selected_perms=None):
        if not selected_perms:
            selected_perms = []
        return MenuTree(self.plan_perms, selected_perms).get_js_tree()


class SidebarMenu:
    def __init__(self, handlers_list, system, handler):
        if type(handlers_list) == list:
            self.__handlers = handlers_list
        else:
            raise Exception("Expected a Handler list, {} given.".format(type(handlers_list)))
        self.menu = []
        self.system = system
        self.__make_menu(handler)

    def __make_menu(self, handler):
        _perms = SystemPermissions.get_perms(self.system)

        ls = []
        for i in [i for i in _perms if not i['parent']]:
            ls.append(
                {
                    "name": i['name'],
                    "url": handler.url(i['url']) if i['url'] != "#" else "#",
                    "handlers": json.loads(i['handlers']) if i['handlers'] != 'null' else [],
                    "activation": False,
                    "title": i['title'],
                    "child": []
                }
            )

        for i in [i for i in _perms if i['parent']]:
            for z in range(len(ls)):
                if ls[z]['name'] == i['parent']:
                    if i['name'] in self.__handlers:
                        ls[z]['child'].append(
                            {
                                "name": i['name'],
                                "url": handler.url(i['url']) if i['url'] != "#" else "#",
                                "handlers": json.loads(i['handlers']) if i['handlers'] != 'null' else [],
                                "activation": False,
                                "title": i['title'],
                                "child": []
                            }
                        )

        self.menu = []
        try:
            for i in ls:
                if i['child']:
                    if i['url'] == "#":
                        self.menu.append(i)
                elif i['name'] in self.__handlers:
                    self.menu.append(i)
        except:
            pass
