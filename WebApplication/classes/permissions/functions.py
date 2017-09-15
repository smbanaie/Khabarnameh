#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ReS4'

import json

last_id = 0
last_parent = 0


class Sections:
    Admin = "ADMIN"
    Plan1 = "Plan1"
    Plan2 = "Plan2"
    Plan3 = "Plan3"
    Plan4 = "Plan4"

    def __init__(self):
        pass


class UserGroups:
    Admin = 1
    Doctor = 2
    Clerk = 3
    Patient = 4

    def __init__(self):
        pass


def make_perms(_list, name=None, group=None, title="", section=None, ls=None, url="#", is_default=None, icon=None, parent=None):
    global last_id, last_parent

    if not ls:
        ls = []

    last_id += 1
    # if not is_child:
    #     last_parent = last_id
    _list.append(
        {
            "id": last_id,
            "name": name,
            "user_group": group,
            "persian_name": title,
            "section": section,
            "handlers": ls,
            "url": url,
            "is_default": is_default,
            "icon": icon,
            "parent": parent
        }
    )
