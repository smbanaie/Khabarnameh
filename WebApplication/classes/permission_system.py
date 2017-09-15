#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

perms = []
last_id = 0
last_parent = 0


def new_perms(name=None, ls=None, url="#", title="", parent=None):
    global last_id, last_parent

    if not ls:
        ls = []

    last_id += 1
    # if not is_child:
    #     last_parent = last_id

    perms.append(
        {
            "id": last_id,
            "name": name,
            "handlers": ls,
            "url": url,
            "title": title,
            "parent": parent
        }
    )


#
# from WebApplication.db_models.table_models import *
#
#
# def new_perms(name=None, ls=None, url="#", title="", default=True, parent=None):
#     System_permissions().insert(
#         name=name,
#         title=title,
#         handlers=json.dumps(ls),
#         url=url,
#         default=default,
#         parent=parent,
#         perm_order=0
#     ).execute()

#
# new_perms("dashboard", ["SystemDashboard"], "system_dashboard", "داشبورد", parent=None)
#
# new_perms(name="news", title="مدیریت خبرها", parent=None)
# new_perms("news::add", ["SystemAddNews"], "system_add_news", "افزودن خبر جدید", parent="news")
# new_perms("news::management", ["SystemNewsManagement", "SystemNewsEdit"], "system_news_management", "مدیریت خبرها",
#           parent="news")
# new_perms("news::pending", [], "#", "خبرهای در انتظار تائید", parent="news")
#
# new_perms(name="collections", title="مجموعه ها", parent=None)
# new_perms("collections::management", ["SystemCollections", "SystemCollectionsAction"], "system_collections",
#           "مدیریت مجموعه ها", parent="collections")
# new_perms("collections::default_collections", ["SystemCollectionRoles"], "system_collections_roles",
#           "مجموعه های پیش فرض هر نقش", parent="collections")
#
# new_perms(name="roles", title="نقش ها", parent=None)
# new_perms("roles::management", ["SystemRoles"], "system_roles", "مدیریت نقش های سیستم", parent="roles")
#
# new_perms(name="users", title="مدیریت کاربران", parent=None)
# new_perms("users::add", ["SystemUmAddUsers"], "system_um_add_users", "افزودن کاربران جدید", parent="users")
# new_perms("users::management", ["SystemUmAUsersList"], "system_um_users_list", "لیست کاربران", parent="users")
#
# new_perms(name="user_roles", title="مدیریت نقش های کاربران", parent=None)
# new_perms("user_roles::management", ["SystemUserRolesManagement"], "system_user_management_roles",
#           "مدیریت نقش های کاربر", parent="user_roles")
# new_perms("user_roles::editors", ["SystemURmEditorManagement"], "system_urm_editors", "تعریف ویرایشگر",
#           parent="user_roles")
# new_perms("user_roles::permissions", ["SystemPermissions"], "system_permissions", "مجوز های دسترسی",
#           parent="user_roles")
#
# new_perms("slider_images", ["SystemSliderImages"], "system_slider_images", "مدیریت تصاویر اسلایدر", parent=None)
# new_perms("help", ["SystemHelp"], "system_help", "راهنمای سیستم", parent=None)

#
# class MenuTree:
#     def __init__(self, selected_perms=None, system=None):
#         self.selected_perms = selected_perms if selected_perms else []
#         self.system = system
#
#     def get_js_tree(self):
#         tree = [
#             {
#                 'id': "0", 'parent': "#",
#                 'text': "سیستم مدیریت مجوز ها", 'state': {'selected': False}, 'icon': 'fa fa-comments-o'
#             }
#         ]
#
#         for child in perms:
#             selected = True if child['name'] in self.selected_perms else False
#             tree.append({
#                 'id': child['name'], 'parent': child['parent'] if child['parent'] else "0",
#                 'text': child['title'], 'state': {'selected': selected}, 'icon': 'fa fa-comments-o'
#             })
#         return json.dumps(tree)
#

class PermsId:
    def __init__(self):
        pass

    def get_ids(self):
        return [child['name'] for child in perms]

    def get_dict(self):
        d = dict()
        for child in perms:
            for i in child['handlers']:
                d[i] = child['name']
        return d
