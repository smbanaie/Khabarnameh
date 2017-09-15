#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import UIModule

__author__ = 'ReS4'


class Footer(UIModule):
    def render(self):
        return self.render_string("modules/footer/footer.html")


class Analytics(UIModule):
    def render(self):
        return self.render_string("modules/analytics/piwik.html")
