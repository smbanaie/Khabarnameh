#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from WebApplication.classes.auth_role import ScopeTree

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SystemRolesHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "گروه های کاربری سیستم"

        self.data['roles'] = SysRoles(system=self.current_system).get_all()
        self.data['help_id'] = "10"
        self.render('base/system/roles/roles.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        _method = self.get_argument("method", None)

        if _method == "save":
            _name = self.get_argument("role_name", None)
            if _name:
                if SysRoles(title=_name, system=self.current_system).add_role():
                    self.set_flash("msg", "اطلاعات با موفقیت ثبت شد.")
                else:
                    self.set_flash("msg", "خطا در ثبت اطلاعات. مجدداً تلاش کنید.")
            else:
                self.set_flash("msg", "اطلاعات ارسال شده نادرست است.")

            self.redirect(self.url("system_roles"))
            return

        elif _method == "delete":
            try:
                cid = int(self.get_argument("cid", None))
                if cid:
                    for i in SysRoles(system=self.current_system).get_all():
                        if cid == i['id']:
                            if i['name'] not in ["ADMIN", "USER", "EDITOR", "GUEST"]:
                                SysRoles(_id=cid, system=self.current_system).delete_role()
                                self.write({"status": True})
                                return
                            else:
                                self.write({"status": False})
                                return

                    self.write({"status": False})
                    return
                else:
                    self.write({"status": False})
                    return
            except:
                self.write({"status": False})

        elif _method == "update":
            try:
                cid = int(self.get_argument("cid", None))
                _name = self.get_argument("_val", None)

                if _name == "":
                    self.write({"status": False})
                    return

                if cid and _name:
                    for i in SysRoles(system=self.current_system).get_all():
                        if cid == i['id']:
                            SysRoles(_id=cid, title=_name, system=self.current_system).update_role()
                            self.write({"status": True})
            except:
                self.write({"status": False})
        else:
            self.write({"status": ":)"})


class SystemCollectionRolesHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "مجموعه های مجاز هر نقش"

        self.data['roles'] = SysRoles(system=self.current_system).get_all()
        # del (self.data['roles'][0])
        self.data['help_id'] = "7"
        self.render('base/system/roles/default_collections.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):
        _id = self.get_argument("role_id")
        cid = SysCollectionRoles.get_all_ids(_id, True)
        tree = ScopeTree(system=self.current_system).get_js_tree(cid)
        if _id:
            self.write({"status": True, "tree": tree})

    @gen.coroutine
    @authentication()
    def post(self):

        role = self.get_argument("role_id", None)
        collections = self.get_argument("collections", None)
        if collections:
            try:
                collections = json.loads(collections)
            except:
                collections = []

        if role and collections:
            if SysCollectionRoles.add_role_collections(role, collections):
                self.write({"status": True})
            else:
                self.write({"status": False})


class SystemDefaultCollectionRolesHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "مجموعه های پیش فرض هر نقش"

        self.data['roles'] = SysRoles(system=self.current_system).get_all()
        # del (self.data['roles'][0])
        self.data['help_id'] = "7"
        self.render('base/system/roles/assumtion_collections.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):
        _id = self.get_argument("role_id")
        cid = SysCollectionRoles.get_all_ids(_id, True)
        cid_default = SysCollectionRoles.get_all_ids2(_id)
        tree_default = ScopeTree(system=self.current_system).get_js_tree_default(cid,cid_default)
        if _id:
            self.write({"status": True, "tree": tree_default})

    @gen.coroutine
    @authentication()
    def post(self):

        role = self.get_argument("role_id", None)
        collections = self.get_argument("collections", None)
        if collections:
            try:
                collections = json.loads(collections)
            except:
                collections = []

        if role and collections:
            if SysCollectionRoles.change_defualt_collections(role, collections):
                self.write({"status": True})
            else:
                self.write({"status": False})
