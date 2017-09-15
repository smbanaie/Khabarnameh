#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ReS4'

from WebApplication.handlers.base import *


class ShowCommentsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['subsystems'] = []
        self.data['title'] = "نظرات خبرها"

        ls = []
        ls1 = []
        if self.current_plan_id != 1:
            self.data['new_comments'] = SysNewsComments(system=self.current_system).get_all(count=1000, only_new=True)
            self.data['comments'] = SysNewsComments(system=self.current_system).get_all(count=15, only_new=False)
            x = [i['news_id']['id'] for i in SysNews_admin_p4(system_id=self.current_system).get_admin_news()]

            if x:
                y = self.data['new_comments']
                z = self.data['comments']
                ls = []
                ls1 = []
                for i in y:
                    if i['news']['id'] not in x:
                        ls.append(i)
                self.data['new_comments'] = ls
                for i in z:
                    if i['news']['id'] not in x:
                        ls1.append(i)
                self.data['comments'] = ls1
                self.data['new_comments'] = ls
        else:
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            sub_sys = [ss['id'] for ss in sys]
            sub_sys.append(self.current_system)
            for i in sub_sys:
                a = SysNewsComments(system=i).get_all(count=1000, only_new=True)
                b = SysNewsComments(system=i).get_all(count=15, only_new=False)
                for i in a:
                    ls.append(i)
                for i in b:
                    ls1.append(i)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['new_comments'] = ls
            self.data['comments'] = ls1
        self.data['sub_id'] = 0
        self.render('base/system/comments/comments.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):
        self.data['title'] = "نظرات خبرها"
        search = self.get_argument("search", None)
        if search == "search":
            subsystem = self.get_argument("subsystem", None)
            if subsystem == "all":
                self.redirect(self.url("system_comments"))
                return
            self.data['new_comments'] = SysNewsComments(system=subsystem).get_all(count=1000, only_new=True)
            self.data['comments'] = SysNewsComments(system=subsystem).get_all(count=15, only_new=False)
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['sub_id'] = subsystem
            self.render('base/system/comments/comments.html', **self.data)
        _id = self.get_argument("_id", None)
        if _id:
            method = self.get_argument("method", None)
            if self.current_plan_id == 1:
                if method == "delete":
                    ss = SysNewsComments(_id=_id, system=self.current_system)
                    ps = ss.get_one_p4()
                    if ps:
                        ss.delete_by_id_p4()
                        self.write({"status": True})
                    else:
                        self.write({"status": False})
                elif method == "accept":
                    ss = SysNewsComments(_id=_id, system=self.current_system)
                    ps = ss.get_one_p4()
                    if ps:
                        ss.update_p4(confirmed="yes")
                        self.write({"status": True})
                    else:
                        self.write({"status": False})
                else:
                    self.write({"status": False})

            else:
                if method == "delete":
                    ss = SysNewsComments(_id=_id, system=self.current_system)
                    ps = ss.get_one()
                    if ps:
                        ss.delete_by_id()
                        self.write({"status": True})
                    else:
                        self.write({"status": False})
                elif method == "accept":
                    ss = SysNewsComments(_id=_id, system=self.current_system)
                    ps = ss.get_one()
                    if ps:
                        ss.update(confirmed="yes")
                        self.write({"status": True})
                    else:
                        self.write({"status": False})
                else:
                    self.write({"status": False})

        else:
            self.write({"status": False})

    @gen.coroutine
    @authentication()
    def put(self, *args, **kwargs):
        dt = dict()

        def chk(val, default):
            z = self.get_argument(val, default)
            if z:
                if z != '':
                    dt[val] = z
                else:
                    dt[val] = None
            else:
                dt[val] = None

        chk("page", 1)

        if dt['page']:
            try:
                dt['page'] = int(dt['page'])
            except:
                dt['page'] = 1

        data = SysNewsComments(system=self.current_system).get_all(page=dt['page'], count=15)
        self.finish(
            {
                "data": data,
                "status": True if data else False,
                "more": True if len(data) == 15 else False
            }
        )
