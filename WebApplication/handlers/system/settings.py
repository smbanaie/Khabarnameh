#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from WebApplication.classes.auth_role import ScopeTree

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SystemSettingsSubDomainHandler(WebBaseHandler):
    # @gen.coroutine
    # @authentication()
    def get(self):
        self.data['title'] = "مدیریت ساب دامین ها"

        self.data['sub_domains'] = SysSubDomain().get_all()
        self.render('base/system/settings/sub_domain.html', **self.data)

    # @gen.coroutine
    # @authentication()
    def post(self):
        _method = self.get_argument("method", None)

        if _method == "save":
            site_id = self.get_argument("site_id", None)
            sub_domain = self.get_argument("sub_domain", None)
            if site_id and sub_domain:
                if SysSubDomain(site_id=site_id, sub_domain=sub_domain).add_sub_domain():
                    self.set_flash("msg", "اطلاعات با موفقیت ثبت شد.")
                else:
                    self.set_flash("msg", "خطا در ثبت اطلاعات. مجدداً تلاش کنید.")
            else:
                self.set_flash("msg", "اطلاعات ارسال شده نادرست است.")

            self.redirect(self.url("system_settings_subdomain"))
            return

        elif _method == "delete":
            try:
                cid = int(self.get_argument("cid", None))
                if cid:
                    if SysSubDomain(_id=cid).delete_sub():
                        self.write({"status": True})
                        return
                    self.write({"status": False})
                else:
                    self.write({"status": False})
                return
            except:
                self.write({"status": False})

        elif _method == "update":
            try:
                cid = int(self.get_argument("cid", None))
                site_id = self.get_argument("site_id", None)
                sub_domain = self.get_argument("sub_domain", None)

                if site_id == "" or sub_domain == "":
                    self.write({"status": False})
                    return

                if cid and site_id and sub_domain:
                    SysSubDomain(_id=cid, site_id=site_id, sub_domain=sub_domain).update_sub()
                    self.write({"status": True})
            except:
                self.write({"status": False})
        else:
            self.write({"status": ":)"})


class SystemSettingsNotificationHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "مدیریت اعلان خبرها"

        self.data['types'] = SysNotificationByType().get_all()
        self.render('base/system/settings/notification.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        vals = json.loads(self.get_argument("vals", '[]'))
        for i in vals:
            SysNotificationByType(_id=i['id'], status=i['val'])._update()

        self.redirect(self.url("system_settings_notification"))
