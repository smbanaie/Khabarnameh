#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import HTTPError

from WebApplication.handlers.base import *


class IndexHandler(WebBaseHandler):
    @gen.coroutine
    def get(self):
        if self.current_user is not None:
            self.redirect(self.reverse_url('system_dashboard'))
            return

        self.data['title'] = "سیستم جامع اطلاع رسانی"
        self.data['systems'] = SysSystem.get_all(True)
        self.render('base/index/index.html', **self.data)
        # pass


class DownloadAppHandler(WebBaseHandler):
    @gen.coroutine
    def get(self, system_id):

        self.data['system_id'] = system_id
        _sys = SysSystem(_id=system_id).get_one()
        if _sys:
            if SysSystemPlans(system=system_id).get_one()['id'] >= 3:
                self.set_header('Content-Disposition', 'attachment; filename=%s_bamadrese.apk' % _sys['id'])
                file_name = os.path.join(sh.web['static_address'], "android", "files", "%s.apk" % _sys['id'])
            else:
                self.set_header('Content-Disposition', 'attachment; filename=bamadrese.apk')
                file_name = os.path.join(sh.web['static_address'], "android", "files", "bamadrese.apk")
        else:
            self.set_header('Content-Disposition', 'attachment; filename=bamadrese.apk')
            file_name = os.path.join(sh.web['static_address'], "android", "files", "bamadrese.apk")

        self.set_header('Content-Type', 'application/force-download')
        try:
            with open(file_name, "rb") as f:
                try:
                    while True:
                        _buffer = f.read()
                        if _buffer:
                            self.write(_buffer)
                        else:
                            f.close()
                            self.finish()
                            return
                except:
                    raise HTTPError(404)
            raise HTTPError(500)
        except:
            raise HTTPError(404)