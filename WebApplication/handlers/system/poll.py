#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WebApplication.classes.gcm import GCM

__author__ = 'Nikam'
from WebApplication.db_models.models.base_model import *

from tornado import gen
from WebApplication.handlers.base import WebBaseHandler, authentication


class PollInsertHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "ایجاد نظرسنجی"
        self.data['help_id'] = "1"
        self.data['js_tree'] = []
        self.data['subsystems'] = []
        if self.current_plan_id == 1:
            self.data['subsystems'] = True
            ls_s = [dict(
                id=self.current_system,
                parent="#",
                text="همه  ",
                icon='fa fa-comment-o colorBlue'

            )]
            x = SysSystem().get_all_sub_system(self.current_system)
            for i in x:
                ls_s.append(
                    dict(
                        id=i['id'],
                        parent=self.current_system,
                        text=i['name'],
                        icon='fa fa-comment-o colorBlue'
                    )
                )
            ls_s = json.dumps(ls_s)
            self.data['js_tree'] = ls_s
        self.render('base/system/poll/insert_poll.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        try:
            item = self.get_arguments("item")
            text = self.get_argument("text", None)
            status_poll = self.get_argument("status_poll", None)
            subsystems = json.loads(self.get_argument("subsystems", '[]'))
            if self.current_plan_id == 1:
                if not subsystems:
                    self.add_error(" سیستم ها را انتخاب کنید.")
                    self.redirect(self.reverse_url("system_poll_insert"))
                    return
            if text:
                for i in item:
                    if not i:
                        self.add_error("گزینه خالی مجاز نیست.")
                        self.redirect(self.reverse_url("system_poll_insert"))
                        return
                # print( subsystems)
                if self.current_plan_id == 1:
                    ls = []
                    ls.append(int(self.current_system))
                    for i in subsystems:
                        if int(i) != self.current_system:
                            ls.append(int(i))
                    parent = 0
                    for i in ls:
                        q = SysPollQuestion(_system_id=i, _question=text, parent_question=parent).insert()
                        if i == self.current_system:
                            parent = int(q)
                        if q:
                            if status_poll:
                                u = SysPollQuestion(_id=q, _status="deactive").update_status()
                            m = SysPoolItem().insert_list_item(q, item)
                        try:
                            if not status_poll:
                                _gcm = GCM(message_type=1, registration_ids=[], system_id=i)
                                _gcm.title = u"نظرسنجی جدید"
                                gcm = SysGcmUsers().get_all_users_for_poll(i)
                                if gcm:
                                    _gcm.content = text
                                    _gcm.registration_ids = gcm
                                    _gcm.send_massage()
                        except Exception, e:
                            pass

                else:
                    q = SysPollQuestion(_system_id=self.current_system, _question=text).insert()
                    if q:
                        if status_poll:
                            u = SysPollQuestion(_id=q, _status="deactive").update_status()
                        m = SysPoolItem().insert_list_item(q, item)
                    try:
                        if not status_poll:
                            _gcm = GCM(message_type=1, registration_ids=[], system_id=self.current_system)
                            _gcm.title = u"نظرسنجی جدید"
                            gcm = SysGcmUsers().get_all_users_for_poll(self.current_system)
                            if gcm:
                                _gcm.content = text
                                _gcm.registration_ids = gcm
                                _gcm.send_massage()
                    except Exception, e:
                        pass

                if m:
                    self.set_flash('msg', "نظرسنجی با موفقیت ثبت شد.")
                    self.redirect(self.reverse_url("system_poll_insert"))
                else:
                    SysPollQuestion(q).delete()
                    self.add_error("خطا در ثبت نظرسنجی.مجددا تلاش کنید.")
                    self.redirect(self.reverse_url("system_poll_insert"))
            else:
                self.add_error("متن نظر سنجی را وارد کنید.")
                self.redirect(self.reverse_url("system_poll_insert"))
                return
        except Exception, e:
            return False


class PollResultHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['subsystems'] = False
        self.data['title'] = "نتیجه نظرسنجی"
        self.data['help_id'] = "1"
        if self.current_plan_id == 1:
            self.data['sub_id'] = 0
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            ls_s = [dict(
                name="همه  ",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['poll'] = SysPollQuestion(_system_id=self.current_system).get_all_p4()
        else:
            self.data['poll'] = SysPollQuestion(_system_id=self.current_system).get_all()
        self.render('base/system/poll/show_result_poll.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        B = False
        self.data['title'] = "نتیجه نظرسنجی"
        search = self.get_argument("search", None)
        if search == "search":
            subsystem = self.get_argument("subsystem", None)
            if subsystem == "all":
                self.redirect(self.url("system_poll_result"))
                return
            self.data['poll'] = SysPollQuestion(_system_id=subsystem).get_all_p4()
            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['sub_id'] = subsystem
            self.render('base/system/poll/show_result_poll.html', **self.data)
        try:
            _id = self.get_argument("cid", "")
            method = self.get_argument("method", "")
            if self.current_plan_id == 1:
                if method == 'show':
                    item = SysPoolItem(_question_id=_id).get_all()
                    answer = SysPollAnswer(_question_id=_id).get_all_p4()
                    _len = len(answer)
                    if _len > 0:
                        B = True
                    for i in item:
                        for j in answer:
                            if i["item"] == j["item"]["text"]:
                                i['count'] += 1
                        if _len > 0:
                            i['darsad'] = (i['count'] * 100 / _len)
                    self.write({"item": item, "bool": B})
                elif method == 'delete':
                    if SysPollQuestion(_id=_id).delete():
                        B = True
                        self.write({"status": B})
                    else:
                        self.write({"status": B})
            else:
                if method == 'show':
                    item = SysPoolItem(_question_id=_id).get_all()
                    answer = SysPollAnswer(_question_id=_id).get_all()
                    _len = len(answer)
                    if _len > 0:
                        B = True
                    for i in item:
                        for j in answer:
                            if i["id"] == j["item"]["id"]:
                                i['count'] += 1
                        if _len > 0:
                            i['darsad'] = (i['count'] * 100 / _len)
                    self.write({"item": item, "bool": B})
                elif method == 'delete':
                    if SysPollQuestion(_id=_id).delete():
                        B = True
                        self.write({"status": B})
                    else:
                        self.write({"status": B})




        except Exception, e:
            self.write({"item": "0", "bool": B})

    @gen.coroutine
    @authentication()
    def put(self, *args, **kwargs):
        m = False
        try:
            _id = self.get_argument("cid", "")
            method = self.get_argument("method", None)
            if method == 'deactive':
                m = SysPollQuestion(_id=_id, _status="deactive").update_status()
            elif method == 'active':
                m = SysPollQuestion(_id=_id, _status="active").update_status()
            self.write({"status": m})
        except Exception, e:
            self.write({"status": m})
