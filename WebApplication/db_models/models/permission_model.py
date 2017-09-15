#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
from WebApplication.classes.functions import strip_tags, to_jalali

from WebApplication.db_models.table_models import *


class SysSystemPermissions:
    def __init__(self, _name=None, title=None, handlers=None, url=None, default=None, icon=None, parent=None,
                 perm_order=None, *args, **kwargs):

        self.name = _name
        self.title = title
        self.handlers = handlers
        self.url = url
        self.default = default
        self.icon = icon
        self.parent = parent
        self.perm_order = perm_order

    @staticmethod
    def get_all():
        try:
            r = System_permissions().select()
            ls = []
            for i in r:
                ls.append(
                    dict(
                        name=i.name,
                        title=i.title,
                        handlers=i.handlers,
                        url=i.url,
                        default=i.default,
                        icon=i.icon,
                        parent=i.parent,
                        perm_order=i.perm_order
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_one(self):
        try:
            i = System_permissions().get(System_permissions.name == self.name)
            if i:
                return dict(
                    name=i.name,
                    title=i.title,
                    handlers=i.handlers,
                    url=i.url,
                    default=i.default,
                    icon=i.icon,
                    parent=i.parent,
                    perm_order=i.perm_order
                )
            else:
                return False
        except Exception, e:
            return {}


class SysSystemPlans:
    def __init__(self, _id=None, system=None, plan=None):

        self.id = _id
        self.system = system
        self.plan = plan

    def insert(self):
        try:
            m = System_plans().insert(system=self.system, plan=self.plan).execute()
            if m:
                return m
            else:
                return False
        except:
            return False

    def get_one(self):
        try:
            m = System_plans().get(System_plans.system == self.system)
            if m:
                return dict(id=m.plan.id, name=m.plan.plan_name, type=m.plan.plan_type, price=m.plan.price)
        except:
            return {}


class SysPlanPermissions:
    def __init__(self, _id=None, plan=None, permission=None):
        self.id = _id
        self.permission = permission
        self.plan = plan

    def get_all_perm_id(self):
        try:
            m = Plan_permissions().select().where(Plan_permissions.plan == self.plan)
            ls = []
            for i in m:
                ls.append(i.permission.name)
            if m:
                return
        except:
            return []

    def get_all_perms_by_plan(self):
        try:
            m = Plan_permissions().select(
                System_permissions.name,
                System_permissions.title,
                System_permissions.handlers,
                System_permissions.url,
                System_permissions.default,
                System_permissions.icon,
                System_permissions.parent,
                System_permissions.perm_order
            ).order_by(SQL("perm_order")).join(
                System_permissions, JOIN_INNER, on=(System_permissions.name == Plan_permissions.permission)
            ).where(Plan_permissions.plan == self.plan).naive()
            ls = []
            for i in m:
                ls.append(
                    dict(
                        name=i.name,
                        title=i.title,
                        handlers=i.handlers,
                        url=i.url,
                        default=i.default,
                        icon=i.icon,
                        parent=i.parent,
                        perm_order=i.perm_order
                    )
                )
            return ls
        except Exception, e:
            print("permission get_all_by_plan", e)
            return []


class SysPermissions:
    def __init__(self, _id=None, system=None, user=None, perm_name=None, *args, **kwargs):
        self.id = _id
        self.system = system
        self.user = user
        self.perm_name = perm_name

    def add_user_permission(self, perms=None):
        if not perms:
            perms = []

        if perms:
            row_dicts = ({'perm_name': nm, 'user': self.user, 'system': self.system} for nm in perms)
            try:
                if SysPermissions.__delete_all_perms(self):
                    if Permissions().insert_many(row_dicts).execute():
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception, e:
                return False
        elif not perms:
            if SysPermissions.__delete_all_perms(self):
                return True
            else:
                return False
        else:
            return False

    def get_all_perms(self):
        try:
            p = Permissions().select().where(Permissions.user == self.user, Permissions.system == self.system).execute()
            return [dict(
                id=i.id,
                perm_name=i.perm_name.name
            ) for i in p]

        except Exception, e:
            print("permission get_all", e)
            return []

    def __delete_all_perms(self):
        try:
            Permissions().delete().where(Permissions.user == self.user, Permissions.system == self.system).execute()
            return True
        except:
            return False


class SysPlans:
    def __init__(self, _id=None, plan_name=None, plan_type=None, price=None):
        self.id = _id
        self.plan_name = plan_name
        self.plan_type = plan_type
        self.price = price

    def get_one(self):
        try:
            p = Plans().get(id=self.id, plan_type="public")
            if p:
                return dict(id=p.id, plan_name=p.plan_name, plan_type=p.plan_type, price=p.price)
        except:
            return {}


class SysPlanFeatures:
    def __init__(self, _id=None, plan=None, max_users=None, active_days=None, sub_system=None):
        self.id = _id
        self.plan = plan
        self.max_users = max_users
        self.active_days = active_days
        self.sub_system = sub_system

    def get_one(self):
        try:
            p = Plan_features().get(Plan_features.plan == self.plan)
            if p:
                return dict(id=p.id, max_users=p.max_users, active_days=p.active_days, sub_system=p.sub_system)
        except:
            return {}


class SysSystemPlanFeatures:
    def __init__(self, _id=None, system=None, max_users=None, active_days=None, sub_system=None):
        self.id = _id
        self.system = system
        self.max_users = max_users
        self.active_days = active_days
        self.sub_system = sub_system

    def insert(self):
        try:
            p = System_plan_features().insert(
                system=self.system,
                max_users=self.max_users,
                active_days=self.active_days,
                sub_system=self.sub_system
            ).execute()

            if p:
                return True
            else:
                return False
        except:
            return False

    def copy_plan_features(self, plan):
        z = SysPlanFeatures(plan=plan).get_one()
        self.max_users = z['max_users']
        self.active_days = z['active_days']
        self.sub_system = z['sub_system']
        h = self.insert()
        if h:
            return h
        else:
            return False

    def get_one(self):
        try:
            p = System_plan_features().get(System_plan_features.system == self.system)
            if p:
                return dict(id=p.id, max_users=p.max_users, active_days=p.active_days, sub_system=p.sub_system)
        except:
            return {}
