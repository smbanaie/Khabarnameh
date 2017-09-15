#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WebApplication.classes.auth_role import ScopeTree
from WebApplication.classes.functions import upload_photo

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SystemCollectionsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['subsystems'] = False
        if self.current_plan_id == 1:
            self.data['sub_id'] = 0
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            sys.insert(0, dict(name="سامانه اصلی", id="all"))
            self.data['subsystems'] = sys
        self.data['title'] = "مدیریت مجموعه ها"
        self.data['help_id'] = "6"
        self.data['js_tree'] = ScopeTree(system=self.current_system).get_js_tree1()
        self.render('base/system/collections/collections.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        try:
            sys_id = self.get_argument("pid", "all")
            if sys_id == "all":
                sys_id = self.current_system
            js_tree = ScopeTree(system=sys_id).get_js_tree1()
            self.write({
                'status': True,
                'js_tree': js_tree,
            })
        except Exception, e:
            self.write({'status': False})


class SystemCollectionsActionHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self, action=None, _id=None):
        # self.data['plan'] = self.current_plan_id
        if action and action == "Add":
            parent_col_p4 = SysCollections(_id=_id).get_parent_col_p4_id()
            if parent_col_p4:
                self.set_flash("msg","این مجموعه را مدیر کل اضافه نموده و شما اجازه افزون زیرمجموعه به آن را ندارید.")
                self.redirect(self.url("system_collections"))
                return
            else:
                self.data['title'] = "افزودن مجموعه جدید"
                pr = SysCollections(system=self.current_system, _id=_id).get_one()
                self.data['parent'] = pr
                if pr:
                    self.render('base/system/collections/collections_add.html', **self.data)
                else:
                    self.redirect(self.url("system_collections"))

        elif action and action == "Edit":
            # parent_col_p4 = SysCollections(_id=_id).get_parent_col_p4_id()
            # if parent_col_p4:
            #     self.set_flash("msg", "این مجموعه را مدیر کل اضافه نموده و شما اجازه ویرایش این مجموعه را ندارید.")
            #     self.redirect(self.url("system_collections"))
            #     return
            if SysCollections(_id=_id, system=self.current_system).get_system():
                self.data['title'] = "ویرایش مجموعه"
                pr = SysCollections(system=self.current_system, _id=_id).get_one()
                self.data['parent'] = pr
                self.data['parents'] = SysCollections.get_all(self.current_system)
                self.data['children'] = SysCollections(
                    system=self.current_system,
                    left_node=pr['left_node'],
                    right_node=pr['right_node']
                ).get_children_id()

                if pr:
                    self.render('base/system/collections/collections_edit.html', **self.data)
                else:
                    self.redirect(self.url("system_collections"))
            else:
                self.redirect(self.url("system_collections"))

        elif action and action == "ShowUsers":
            self.data['title'] = "لیست کاربران مجموعه"
            self.data['subsystems'] = []
            self.data['search'] = False
            self.data['users'] = SysUserCollections(_id=_id).get_all_user_col(system=self.current_system)
            self.data['help_id'] = "8"
            self.render('base/system/users_management/users_list.html', **self.data)

        else:
            self.redirect(self.url("system_collections"))

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):
        _method = self.get_argument("method", None)
        # self.data['plan'] = self.current_plan_id

        if _method == "add":
            coll_name = self.get_argument("coll_name", None)
            parent = self.get_argument("parent", None)
            coll_img = ""
            try:
                coll_img = upload_photo(self, 'coll_img', "collection_pic", max_width=500, max_height=450, default=None,
                                        max_size=10000)
            except Exception, e:
                pass
            if coll_name and parent:
                if self.current_plan_id == 1:
                    systems = SysSystem(_id=self.current_system).get_children()
                    systems.insert(0, dict(child_id=self.current_system))

                    parent_col_p4 = None
                    old_parent_col_p4 = None
                    for i in systems:
                        if i['child_id'] != self.current_system:
                            parent = SysCollections(system=i['child_id'], parent_col_p4=old_parent_col_p4).get_sub_col()
                            if not parent:
                                parent = SysCollections(system=i['child_id']).get_rood_id()
                        z = SysCollections(system=i['child_id'], parent=parent, parent_col_p4=parent_col_p4,
                                           name=coll_name, coll_img=coll_img).add_collection()
                        if i['child_id'] == self.current_system:
                            parent_col_p4 = z
                            h = SysCollections(_id=z, system=i['child_id']).get_one()
                            old_parent_col_p4 = h["parent"]
                else:
                    SysCollections(system=self.current_system, parent=parent, name=coll_name, coll_img=coll_img,
                                   ).add_collection()
                self.set_flash("msg", "مجموعه با موفقیت اضافه شد.")
            self.redirect(self.url("system_collections"))

        elif _method == "edit":
            _id = self.get_argument("_id", None)
            coll_name = self.get_argument("coll_name", None)
            parent = self.get_argument("parent", None)
            coll_img = ""
            try:
                coll_img1 = upload_photo(self, 'coll_img', "collection_pic", max_width=500, max_height=450,
                                         default=None,
                                         max_size=10000)
                if coll_img1:
                    coll_img = coll_img1
                else:
                    coll_img = SysCollections(_id=_id).get_image_id()
            except Exception, e:
                pass
            if coll_name and parent:
                if self.current_plan_id == 1:
                    systems = SysSystem(_id=self.current_system).get_children()
                    systems.insert(0, dict(child_id=self.current_system))
                    cid = _id
                    for i in systems:
                        if i['child_id'] != self.current_system:

                            _id = SysCollections(system=i['child_id'], parent_col_p4=cid).get_sub_col()
                        SysCollections(
                            _id=_id,
                            system=i['child_id'],
                            name=coll_name,
                            coll_img=coll_img
                        ).edit_collection_p4()
                    self.set_flash("msg", "ویرایش مجموعه با موفقیت انجام شد.")

                else:
                    # parent_col_p4 = SysCollections(_id=_id).get_parent_col_p4_id()
                    # if parent_col_p4:
                    #     self.set_flash("msg",
                    #                    "این مجموعه را مدیر کل اضافه نموده و شما اجازه ویرایش این مجموعه را ندارید.")
                    # else:
                    SysCollections(
                        _id=_id,
                        system=self.current_system,
                        parent=parent,
                        name=coll_name
                    ).edit_collection()
                    self.set_flash("msg", "ویرایش مجموعه با موفقیت انجام شد.")
            self.redirect(self.url("system_collections"))

        elif _method == "delete":
            try:
                cid = int(self.get_argument("id", None))
                if cid and cid != 1:
                    for i in SysCollections.get_all(self.current_system):
                        if cid == i['id']:
                            if not SysNewsCollections(collection=cid).get_count_by_collection_id():
                                if self.current_plan_id == 1:
                                    systems = SysSystem(_id=self.current_system).get_children()
                                    systems.insert(0, dict(child_id=self.current_system))
                                    cid1 = cid
                                    for i in systems:
                                        if i['child_id'] != self.current_system:
                                            cid = SysCollections(system=i['child_id'], parent_col_p4=cid1).get_sub_col()
                                        if SysCollections(_id=cid, system=i['child_id']).delete_collection():
                                            self.set_flash("msg", "مجموعه با موفقیت حذف شد.")
                                        else:
                                            self.set_flash("msg", "مجموعه ای که دارای فرزند میباشد را نمیتوان حذف کرد.")

                                else:
                                    parent_col_p4 = SysCollections(_id=cid).get_parent_col_p4_id()
                                    if parent_col_p4:
                                        self.set_flash("msg",
                                                       "این مجموعه را مدیر کل اضافه نموده و شما اجازه حذف این مجموعه را ندارید.")
                                    else:
                                        if SysCollections(_id=cid, system=self.current_system).delete_collection():
                                            self.set_flash("msg", "مجموعه با موفقیت حذف شد.")
                                        else:
                                            self.set_flash("msg", "مجموعه ای که دارای فرزند میباشد را نمیتوان حذف کرد.")
                            else:
                                self.set_flash("msg", "مجموعه ای که دارای خبر میباشد را نمیتوان حذف کرد.")
                self.write({"status": True, "js_tree": ScopeTree(system=self.current_system).get_js_tree1()})

            except:
                self.write({"status": False})
