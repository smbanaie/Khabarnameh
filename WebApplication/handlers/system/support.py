#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WebApplication.classes.functions import upload_photo

__author__ = 'Kamal'

import random
from WebApplication.handlers.base import *


class SendNewTicketHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "ارسال درخواست"
        self.render('base/system/support/new_ticket.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        d = {}
        self.check_sent_value("topic", d, "c1", "عنوان را وارد کنید.")
        self.check_sent_value("full_text", d, "c2", "متن اصلی را وارد کنید")
        full_text = strip_tags(d['c2'])
        file_name = upload_photo(self, 'attachment', 'tickets', extensions= ['.jpg', '.png', '.gif', '.bmp', '.jpeg', '.zip', '.rar'])
        if not self.errors:
            x = SysTickets(system_id=self.current_system,status="sent", topic=d['c1'], priority=self.get_argument('priority', None)).send()
            z = SysSubticket(tickets_id=x, file= file_name, user_id=self.current_user, type="s2a", text=full_text).send_subticket()
            if z:

                self.set_flash("msg", "پیام با موفقیت ارسال شد.")
            else:
                self.add_error("خطا در ارسال پیام. مجدداً تلاش نمایید.")
        self.redirect(self.reverse_url("system_support_send_new_ticket"))


class MyTicketsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "درخواست های پشتیبانی من"
        self.data['tickets'] = SysTickets(system_id=self.current_system).get_all()
        self.render('base/system/support/my_tickets.html', **self.data)

class MyTicketsShowHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self, _id):
        t1 = SysTickets(system_id=self.current_system, _id=_id)
        t = t1.is_exist()
        if t:

            s = SysSubticket(tickets_id=t['id']).get_all()
            self.data['title'] = "درخواست های پشتیبانی من"
            self.data['ticket'] = t
            self.data['subtikets'] = s
            self.render('base/system/support/my_subtickets.html', **self.data)
            pass
        else:
            pass

    @gen.coroutine
    @authentication()
    def post(self,_id):
        d = {}
        self.check_sent_value("full_text", d, "c2", "متن اصلی را وارد کنید")
        file_name = upload_photo(self, 'attachment', 'tickets', extensions= ['.jpg', '.png', '.gif', '.bmp', '.jpeg', '.zip', '.rar'])
        if not self.errors:
            full_text = strip_tags(d['c2'])
            z = SysSubticket(tickets_id=_id, file=file_name, user_id=self.current_user, type="s2a", text=full_text).send_subticket()
            s1 = SysTickets(system_id=self.current_system, _id=_id)
            s1.change_status("sent")
            if z:
                self.set_flash("msg", "پیام با موفقیت ارسال شد.")
            else:
                self.add_error("خطا در ارسال پیام. مجدداً تلاش نمایید.")
        self.redirect(self.reverse_url("system_support_my_tickets_show_by_id",_id ))
