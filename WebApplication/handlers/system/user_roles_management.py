#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WebApplication.classes.auth_role import ScopeTree

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SystemUserRolesManagementHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):

        self.data['subsystems'] = False
        if self.current_plan_id == 1:
            self.data['sub_id'] = 0
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            sys.insert(0, dict(name="سامانه اصلی", id="all"))
            self.data['subsystems'] = sys
        self.data['title'] = "مدیریت نقش های کاربر"
        self.data['help_id'] = "11"
        self.render('base/system/user_roles_management/user_management.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):

        _username = self.get_argument("username", None)
        sys_id = self.get_argument("sys_id", "all")
        if sys_id == "all":
            sys_id = self.current_system
        if _username:
            u = SysUsers.is_exist(user_name=_username, system=self.current_system)
            if u:
                r = map(int, SysUserRoles.get_all(u['id']))
                self.write(
                    {
                        "status": True,
                        "tree": SysRoles(system=sys_id).get_js_tree(r),
                        "user": u
                    }
                )
            else:
                self.write({"status": False})
        else:
            self.write({"status": False})

    @gen.coroutine
    @authentication()
    def post(self):
        username = self.get_argument("username", None)
        roles = self.get_argument("roles", None)
        sys_id = self.get_argument("sys_id", "all")
        if sys_id == "all":
            sys_id = self.current_system
        if roles:
            try:
                roles = json.loads(roles)
            except:
                roles = []

        u = SysUsers.is_exist(user_name=username, system=self.current_system)
        editor_role = SysRoles(system=self.current_system, name="EDITOR").get_one_by_name()
        if u and roles:
            if "0" in roles:
                roles.remove("0")

            if SysUserRoles().add_user_roles_2(u['id'], roles, sys_id):
                if str(editor_role['id']) in roles:
                    SysEditorsSetting(
                        user=u['id'],
                        edit_news=SysEditorsSetting.Disable,
                        direct_publish=SysEditorsSetting.No
                    ).add_setting()
                else:
                    SysEditorsSetting(user=u['id']).delete_setting()

                self.write({"status": True})
            else:
                self.write({"status": False})


class SystemURmEditorManagementHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "تعریف نویسنده"
        self.data['help_id'] = "13"
        self.render('base/system/user_roles_management/editors.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):

        _username = self.get_argument("username", None)
        if _username:

            u = SysUsers.is_exist(user_name=_username, system=self.current_system)
            if u:
                r = SysUserRoles.is_editor(u['id'])
                if r:
                    ec = SysEditorsCollections.get_all(u['id'])
                    es = SysEditorsSetting(user=u['id']).get_one()
                    self.write(
                        {
                            "status": True,
                            "tree": ScopeTree(system=self.current_system).get_js_tree(ec),
                            "settings": es,
                            "user": u
                        }
                    )
            else:
                self.write({"status": False})

    @gen.coroutine
    @authentication()
    def post(self):
        username = self.get_argument("username", None)
        collections = self.get_argument("collections", None)
        edit_news = self.get_argument("e1", None)
        direct_publish = self.get_argument("e2", None)

        if edit_news == "all":
            edit_news = SysEditorsSetting.All
        elif edit_news == "own":
            edit_news = SysEditorsSetting.Own
        elif edit_news == "disable":
            edit_news = SysEditorsSetting.Disable
        else:
            edit_news = SysEditorsSetting.Disable

        if direct_publish == "yes":
            direct_publish = SysEditorsSetting.Yes
        else:
            direct_publish = SysEditorsSetting.No

        try:
            collections = json.loads(collections)
        except:
            collections = ["0"]

        u = SysUsers.is_exist(user_name=username, system=self.current_system)

        if u and collections:
            if "0" in collections:
                collections.remove("0")

            if SysEditorsCollections.add_editors_collection(u['id'], collections):

                if SysEditorsSetting(
                        user=u['id'],
                        edit_news=edit_news,
                        direct_publish=direct_publish
                ).update_setting():
                    self.write({"status": True})
                else:
                    self.write({"status": False})
            else:
                self.write({"status": False})
