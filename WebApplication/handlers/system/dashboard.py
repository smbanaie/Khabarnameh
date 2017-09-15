#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from WebApplication.classes.MailClass import R_Mail

__author__ = 'ReS4'

import datetime

from WebApplication.classes.functions import upload_photo
from WebApplication.handlers.base import *


class SystemDashboardHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['request'] = []
        self.data['title'] = "داشبورد"
        self.data['help_id'] = "1"
        sys = SysSystem(_id=self.current_system).get_one()
        self.data['system'] = sys
        # self.data['status_mail'] = sys['status_mail']

        self.data['new_msg'] = SysMessages(system=self.current_system).get_new_messages_count()
        self.data['new_suggestions'] = SysSuggestions(system=self.current_system).get_new_count()
        self.data['new_news_comment'] = SysNewsComments(system=self.current_system).new_news_comment_count()

        a = self.data['system']['date_obj'] + datetime.timedelta(days=365)
        self.data['system']['reg_date'] = to_jalali(a)

        m = datetime.datetime.now()
        self.data['last_visit'] = SysNewsVisit(system=self.current_system).last_visit()[0:10]
        self.render('base/system/dashboard/dashboard.html', **self.data)


class SystemHelpHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self, _id):
        try:
            _id = int(_id)
        except:
            _id = 1

        self.data['hid'] = _id
        self.data['title'] = "راهنمای سیستم"
        self.render('base/system/dashboard/help.html', **self.data)
