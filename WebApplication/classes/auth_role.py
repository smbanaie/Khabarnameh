#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ReS4'

import json
from WebApplication.db_models.models.base_model import *


class ScopeTree:
    def __init__(self, parent=None, system=None):
        self.root = parent
        self.system = system

    def __get_root(self):
        return SysCollections.get_parent(system=self.system)

    def get_js_tree(self, selected_scopes=None):
        try:
            if not selected_scopes:
                selected_scopes = []
            root = self.__get_root()
            if not root:
                SysCollections(system=self.system, name="مجموعه های سیستم", parent=None).insert_one()
                root = self.__get_root()

            selected = True if root.id in selected_scopes else False
            children = SysCollections(left_node=root.left_node, right_node=root.right_node,
                                      system=self.system).get_children()
            tree = [
                {
                    'id': str(int(root.id)),
                    'parent': "#",
                    'text': root.name,
                    'state': {'selected': selected, 'disabled': True},
                    'icon': 'fa fa-comment-o'
                }
            ]
            for child in children:
                selected = True if child.id in selected_scopes else False
                parent_col_p4 = SysCollections(_id=int(child.id)).get_parent_col_p4_id()
                if parent_col_p4:
                    tree.append({
                        'id': str(int(child.id)), 'parent': str(int(child.parent)),
                        'text': child.name, 'state': {'selected': selected}, 'icon': 'fa fa-user colorRed'
                    })
                else:
                    tree.append({
                        'id': str(int(child.id)), 'parent': str(int(child.parent)),
                        'text': child.name, 'state': {'selected': selected}, 'icon': 'fa fa-comments-o colorBlue'
                    })
            return json.dumps(tree)
        except Exception, e:
            pass


    def get_js_tree_default(self,cid=None, selected_scopes=None):
        try:
            if not selected_scopes:
                selected_scopes = []
            root = self.__get_root()
            if not root:
                SysCollections(system=self.system, name="مجموعه های سیستم", parent=None).insert_one()
                root = self.__get_root()

            selected = True if root.id in selected_scopes else False
            children = SysCollections(left_node=root.left_node, right_node=root.right_node,
                                      system=self.system).get_children()
            tree = [
                {
                    'id': str(int(root.id)),
                    'parent': "#",
                    'text': root.name,
                    'state': {'selected': selected, 'disabled': True},
                    'icon': 'fa fa-comment-o'
                }
            ]
            for child in children:
                if child.id in cid:
                    selected = True if child.id in selected_scopes else False
                    parent_col_p4 = SysCollections(_id=int(child.id)).get_parent_col_p4_id()
                    if parent_col_p4:
                        tree.append({
                            'id': str(int(child.id)), 'parent': str(int(child.parent)),
                            'text': child.name, 'state': {'selected': selected}, 'icon': 'fa fa-user colorRed'
                        })
                    else:
                        tree.append({
                            'id': str(int(child.id)), 'parent': str(int(child.parent)),
                            'text': child.name, 'state': {'selected': selected}, 'icon': 'fa fa-comments-o colorBlue'
                        })
            return json.dumps(tree)
        except Exception, e:
            pass


    def get_js_tree1(self, selected_scopes=None):
        try:
            if not selected_scopes:
                selected_scopes = []
            root = self.__get_root()
            if not root:
                SysCollections(system=self.system, name="مجموعه های سیستم", parent=None).insert_one()
                root = self.__get_root()

            selected = True if root.id in selected_scopes else False
            children = SysCollections(left_node=root.left_node, right_node=root.right_node,
                                      system=self.system).get_children()
            tree = [
                {
                    'id': str(int(root.id)),
                    'parent': "#",
                    'text': root.name,
                    'state': {'selected': selected, 'disabled': True},
                    'icon': 'fa fa-comment-o'
                }
            ]
            for child in children:
                selected = True if child.id in selected_scopes else False
                parent_col_p4 = SysCollections(_id=int(child.id)).get_parent_col_p4_id()
                count_user = User_collections.select().where(User_collections.collection == child.id).count()
                count_news = News_collections.select().where(News_collections.collection == child.id).count()
                if count_news > 0:
                    count_news = str(count_news)
                    child.name = u"{} - {} خبر".format(child.name, count_news)
                if count_user > 0:
                    count_user = str(count_user)
                    child.name = u"{} - {} کاربر".format(child.name, count_user)

                if parent_col_p4:
                    tree.append({
                        'id': str(int(child.id)), 'parent': str(int(child.parent)),
                        'text': child.name, 'state': {'selected': selected}, 'icon': 'fa fa-user colorRed'
                    })
                else:
                    tree.append({
                        'id': str(int(child.id)), 'parent': str(int(child.parent)),
                        'text': child.name, 'state': {'selected': selected}, 'icon': 'fa fa-comments-o colorBlue'
                    })
            return json.dumps(tree)
        except Exception, e:
            pass
