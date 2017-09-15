#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WebApplication.classes.gcm import GCM

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SendMessagesHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "ارسال پیام جدید"
        self.data['help_id'] = "2"
        self.data['users'] = SysUsers(system=self.current_system).get_all(not_paginate=True)
        self.data['subsystems'] = []
        if self.current_plan_id == 1:
            try:
                ls = []
                for i in self.data['users']:
                    ls.append(i)
                x = SysUsers(system=self.current_system).get_all_users_subsystem()
                for i in x:
                    ls.append(i)
                self.data['users'] = ls
            except:
                pass
            ls_s = [dict(
                name="همه کاربران",
                id="all"
            )]
            x = SysSystem().get_all_sub_system(self.current_system)
            for i in x:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
        ls_col = SysCollections().get_all(self.current_system)
        ls_col.insert(0, dict(
            name="همه مجموعه ها",
            id="all"
        ))
        self.data['collections_sys'] = ls_col
        self.render('base/system/messages/send_message.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        dt = {}
        self.check_sent_value("text", dt, "text", "متن پیام را وارد کنید.")
        self.check_sent_value("receivers", dt, "receivers", nullable=True, default="[]")

        try:
            dt['receivers'] = map(int, json.loads(dt['receivers']))
            if not dt['receivers']:
                self.errors.append("گیرندگان پیام را مشخص کنید.")
        except:
            self.errors.append("گیرندگان پیام را مشخص کنید.")

        if not self.errors:
            z = SysMessages(
                system=self.current_system,
                text=dt['text'],
                msg_type=SysMessages.SystemToUser,
                status=SysMessages.Sent,
                type=SysMessages.TypeSMS
            )
            if z.send_many(dt['receivers']):
                GCM(
                    message_type=2,
                    registration_ids=SysGcmUsers(user=dt['receivers']).get_all_users_reg_id(),
                    title=u"پیام جدید",
                    content=u"{}...".format(dt['text'][0:23]) if len(dt['text']) >= 25 else dt['text'],
                    system_id=self.current_system
                ).send_massage()
                self.set_flash("msg", "پیام با موفقیت ارسال شد.")
            else:
                self.add_error("خطا در ارسال پیام. مجدداً تلاش نمایید.")
        else:
            for i in self.errors:
                self.add_error(i)

        self.redirect(self.reverse_url("system_messages_send_new"))

    @gen.coroutine
    @authentication()
    def put(self):
        col_id = self.get_argument("col_id", None)
        ls_u = SysUsers().get_all_by_collection(col_id)
        self.finish({'status': True if ls_u else False, 'users_col': ls_u})


class ReceivedMessagesHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['subsystems'] = []
        self.data['sub_id'] = 0
        self.data['title'] = "پیام های دریافت شده"
        if self.current_plan_id == 1:
            self.data['new_messages'] = SysMessages(system=self.current_system,
                                                    type=SysMessages.TypeSMS).get_all_for_system_p4(count=15,
                                                                                                    only_new=True)
            self.data['messages'] = SysMessages(system=self.current_system,
                                                type=SysMessages.TypeSMS).get_all_for_system_p4(count=15)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            x = SysSystem().get_all_sub_system(self.current_system)
            for i in x:
                ls_s.append(i)
            self.data['subsystems'] = ls_s

        else:
            self.data['new_messages'] = SysMessages(system=self.current_system,
                                                    type=SysMessages.TypeSMS).get_all_for_system(count=15,
                                                                                                 only_new=True)
            self.data['messages'] = SysMessages(system=self.current_system,
                                                type=SysMessages.TypeSMS).get_all_for_system(count=15)
        self.data['help_id'] = "2"
        self.render('base/system/messages/received_messages.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self, *args, **kwargs):
        _id = self.get_argument("_id", None)
        if _id:
            method = self.get_argument("method", None)
            if self.current_plan_id == 1:
                if method == "get":
                    system = SysMessages(_id=_id, system=self.current_system, type=SysMessages.TypeSMS).get_system()
                    ss = SysMessages(_id=_id, system=system['system'], type=SysMessages.TypeSMS)
                    ps = ss.get_one()
                    if ps:
                        if ps['status'] == SysMessages.Sent:
                            ss.update(status=SysMessages.Viewed)
                        ss.user = ps['user']['id']
                        ss.update_all_messages_from_user_p4(self.current_system)
                        ss.system = system['system_user']
                        h = ss.get_one_with_parent_p4(self.current_system)

                        xx = [
                            dict(
                                id=i['id'],
                                dir="pull-right" if i['msg_type'] == SysMessages.UserToSystem else "pull-left",
                                text=i['text'],
                                date=i['date']
                            ) for i in h
                            ]
                        self.write(
                            {
                                "status": True,
                                "ls": xx,
                                "user": ps['user'],
                            }
                        )

                    else:
                        self.write({"status": False})
                elif method == "delete":
                    system = SysMessages(_id=_id, system=self.current_system, type=SysMessages.TypeSMS).get_system()
                    p = SysMessages(_id=_id, system=system['system'], type=SysMessages.TypeSMS).delete_msg_p4()
                    if p:
                        self.write({"status": True})
                    else:
                        self.write({"status": False})
                elif method == "reply":
                    try:
                        _id = int(_id)
                    except:
                        self.write({"status": False})
                        return
                    txt = self.get_argument("text", None)
                    if txt and txt != '':
                        system = SysUsers(_id=_id, system=self.current_system).get_system()
                        if system:
                            if SysMessages(system=self.current_system, user=_id, text=txt, status=SysMessages.Sent,
                                           msg_type=SysMessages.SystemToUser, type=SysMessages.TypeSMS).send():
                                GCM(
                                    message_type=2,
                                    registration_ids=SysGcmUsers(user=[_id]).get_all_users_reg_id(),
                                    title=u"پیام جدید",
                                    content=u"{}...".format(txt[0:23]) if len(txt) >= 25 else txt,
                                    system_id=system
                                ).send_massage()
                                self.write({"status": True})
                            else:
                                self.write({"status": False})
                        else:
                            self.write({"status": False})

                    else:
                        self.write({"status": False})
                else:
                    self.write({"status": False})

            else:

                if method == "get":
                    ss = SysMessages(_id=_id, system=self.current_system, type=SysMessages.TypeSMS)
                    ps = ss.get_one()
                    if ps:
                        if ps['status'] == SysMessages.Sent:
                            ss.update(status=SysMessages.Viewed)
                        ss.user = ps['user']['id']
                        ss.update_all_messages_from_user()
                        h = ss.get_one_with_parent()
                        xx = [
                            dict(
                                id=i['id'],
                                dir="pull-right" if i['msg_type'] == SysMessages.UserToSystem else "pull-left",
                                text=i['text'],
                                date=i['date']
                            ) for i in h
                            ]
                        self.write(
                            {
                                "status": True,
                                "ls": xx,
                                "user": ps['user'],
                            }
                        )

                    else:
                        self.write({"status": False})
                elif method == "delete":
                    ss = SysMessages(_id=_id, system=self.current_system, type=SysMessages.TypeSMS)
                    ps = ss.get_one()
                    if ps:
                        ss.update(status=SysMessages.Deleted)
                        self.write({"status": True})
                    else:
                        self.write({"status": False})
                elif method == "reply":
                    try:
                        _id = int(_id)
                    except:
                        self.write({"status": False})
                        return
                    txt = self.get_argument("text", None)
                    if txt and txt != '':
                        u = SysUsers.is_exist(user_id=_id, system=self.current_system)
                        if u:
                            if SysMessages(system=self.current_system, user=_id, text=txt, status=SysMessages.Sent,
                                           msg_type=SysMessages.SystemToUser, type=SysMessages.TypeSMS).send():
                                GCM(
                                    message_type=2,
                                    registration_ids=SysGcmUsers(user=[_id]).get_all_users_reg_id(),
                                    title=u"پیام جدید",
                                    content=u"{}...".format(txt[0:23]) if len(txt) >= 25 else txt,
                                    system_id=self.current_system
                                ).send_massage()
                                self.write({"status": True})
                            else:
                                self.write({"status": False})
                        else:
                            self.write({"status": False})

                    else:
                        self.write({"status": False})
                else:
                    self.write({"status": False})



        else:
            self.write({"status": False})

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):

        search = self.get_argument("search", None)
        if search == "search":
            subsystem = self.get_argument("subsystem", None)
            if subsystem == "all":
                self.redirect(self.url("system_messages_received"))
                return
            self.data['title'] = "پیام های دریافت شده"
            self.data['new_messages'] = SysMessages(system=subsystem, type=SysMessages.TypeSMS).get_all_for_system(
                count=15, only_new=True)
            self.data['messages'] = SysMessages(system=subsystem, type=SysMessages.TypeSMS).get_all_for_system(count=15)
            x = SysSystem().get_all_sub_system(self.current_system)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            for i in x:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['help_id'] = "2"
            self.data['sub_id'] = subsystem
            self.render('base/system/messages/received_messages.html', **self.data)
        else:
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

            data = SysMessages(system=self.current_system, type=SysMessages.TypeSMS).get_all_for_system(dt['page'],
                                                                                                        count=15)

            self.finish(
                {
                    "data": data,
                    "status": True if data else False,
                    "more": True if len(data) == 15 else False
                }
            )


class SentMessagesHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['subsystems'] = []
        self.data['sub_id'] = 0
        self.data['title'] = "پیام های ارسال شده"
        if self.current_plan_id == 1:
            self.data['messages'] = SysMessages(system=self.current_system,
                                                type=SysMessages.TypeSMS).get_all_sent_for_system_p4(count=15)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            x = SysSystem().get_all_sub_system(self.current_system)
            for i in x:
                ls_s.append(i)
            self.data['subsystems'] = ls_s

        else:
            self.data['messages'] = SysMessages(system=self.current_system,
                                                type=SysMessages.TypeSMS).get_all_sent_for_system(count=15)
        self.render('base/system/messages/sent_messages.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):

        search = self.get_argument("search", None)
        if search == "search":
            subsystem = self.get_argument("subsystem", None)
            if subsystem == "all":
                self.redirect(self.url("system_messages_sent"))
                return
            self.data['title'] = "پیام های ارسال شده"
            self.data['messages'] = SysMessages(system=subsystem, type=SysMessages.TypeSMS).get_all_sent_for_system(
                count=15)
            x = SysSystem().get_all_sub_system(self.current_system)
            ls_s = [dict(
                name="همه پیام ها",
                id="all"
            )]
            for i in x:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['help_id'] = "2"
            self.data['sub_id'] = subsystem
            self.render('base/system/messages/sent_messages.html', **self.data)
        else:
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

            data = SysMessages(system=self.current_system, type=SysMessages.TypeSMS).get_all_sent_for_system_p4(
                dt['page'], count=15)
            self.finish(
                {
                    "data": data,
                    "status": True if data else False,
                    "more": True if len(data) == 15 else False
                }
            )
