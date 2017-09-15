#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SuggestionsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['subsystems'] = []
        self.data['title'] = "انتقادات و پیشنهادات"
        if self.current_plan_id==1:
            self.data['sub_id']=0
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            ls_s=[dict(
                name="همه ",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems']=ls_s
            self.data['suggestion'] = SysSuggestions(system=self.current_system).get_all_p4()
        else:
            self.data['suggestion'] = SysSuggestions(system=self.current_system).get_all()
        self.data['total_count'] = 0
        self.render('base/system/suggestions/suggestions.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self, *args, **kwargs):
        _id = self.get_argument("_id", None)
        if _id:
            method = self.get_argument("method", None)
            ss = SysSuggestions(_id=_id, system=self.current_system)
            if self.current_plan_id==1:
                ps=ss.get_one_p4()
                if ps:
                    if method == "get":
                        try:
                            read_by = json.loads(ps['read_by'])
                        except Exception, e:
                            read_by = []

                        if self.data['full_name'] not in read_by:
                            read_by.append(self.data['full_name'])
                        # ps.update(read_by=json.dumps(read_by), status=SysSuggestions.Read)
                        SysSuggestions(_id=_id).update_p4()
                        self.write({"status": True, "text": ps['text'], "read_by": " - ".join(read_by)})
                    elif method == "delete":
                        SysSuggestions(_id=_id).delete_p4()
                        self.write({"status": True})
                else:
                    self.write({"status": False})
            else:
                ps = ss.get_one()
                if ps:
                    if method == "get":
                        try:
                            read_by = json.loads(ps['read_by'])
                        except:
                            read_by = []

                        if self.data['full_name'] not in read_by:
                            read_by.append(self.data['full_name'])
                        ss.update(read_by=json.dumps(read_by), status=SysSuggestions.Read)

                        self.write({"status": True, "text": ps['text'], "read_by": " - ".join(read_by)})
                    elif method == "delete":
                        ss.update(status=SysSuggestions.Delete)
                        self.write({"status": True})
                else:
                    self.write({"status": False})
        else:
            self.write({"status": False})

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):
        self.data['title'] = "انتقادات و پیشنهادات"
        search= self.get_argument("search",None)
        if search == "search":
            subsystem = self.get_argument("subsystem",None)
            if subsystem == "all":
                self.redirect(self.url("system_suggestions"))
                return
            self.data['suggestion'] = SysSuggestions(system=subsystem).get_all_p4()
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            ls_s=[dict(
                name="همه ",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems']=ls_s
            self.data['sub_id']= subsystem
            self.render('base/system/suggestions/suggestions.html', **self.data)

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

        data = SysSuggestions(system=self.current_system)
        data = data.get_all(dt['page'])
        self.finish(
            {
                "data": data,
                "status": True if data else False,
                "more": True if len(data) == 12 else False
            }
        )
