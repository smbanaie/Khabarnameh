#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import UIModule

__author__ = 'ReS4'

# from WebApplication.handlers.base import *
# from WebApplication.classes.auth.login import LoginMethod

from WebApplication.classes.permission_system import *


class Sidebar(UIModule):
    def make_urls_and_activation(self, ls):
        if type(ls) == list:
            for i in ls:
                if i['url'] != "#":
                    try:
                        i['url'] = self.handler.reverse_url(i['url'])
                    except:
                        i['url'] = "#"

                if self.handler.__class__.__name__ in i['handlers']:
                    i['activation'] = True
        else:
            if ls['url'] != "#":
                try:
                    ls['url'] = self.handler.reverse_url(ls['url'])
                except:
                    ls['url'] = "#"

            if self.handler.__class__.__name__ in ls['handlers']:
                ls['activation'] = True

        return ls

    def render(self, role="PRINCIPAL", activation=None):
        _perms = self.handler.session.get("sidebar_menu")
        for i in _perms:
            if self.handler.__class__.__name__ in i['handlers']:
                i['activation'] = True
            for j in i['child']:
                if self.handler.__class__.__name__ in j['handlers']:
                    j['activation'] = True
        # for i in range(len(_perms)):
        #     _perms[i] = self.make_urls_and_activation(_perms[i])
        #     if _perms[i]['child']:
        #         _perms[i]['child'] = self.make_urls_and_activation(_perms[i]['child'])


        # # if menu and m2:
        # #
        # #     for i in m2:
        # #         if i['url'] != "#":
        # #             try:
        # #                 i['url'] = self.handler.reverse_url(i['url'])
        # #             except:
        # #                 i['url'] = "#"
        # #
        # #         if self.handler.__class__.__name__ in i['handlers']:
        # #             i['active'] = True
        # #
        # # print(m2)
        # mm = [i['name'] for i in _perms]
        # ls = []
        # for i in [i for i in _perms if not i['parent']]:
        #     ls.append(
        #         {
        #             "name": i['name'],
        #             "url": self.handler.url(i['url']) if i['url'] != "#" else "#",
        #             "activation": True if self.handler.__class__.__name__ in i['handlers'] else False,
        #             "title": i['title'],
        #             "child": []
        #
        #         }
        #     )
        #
        # for i in [i for i in _perms if i['parent']]:
        #     for z in range(len(ls)):
        #         if ls[z]['name'] == i['parent']:
        #             if i['name'] in mm:
        #                 ls[z]['child'].append(
        #                     {
        #                         "name": i['name'],
        #                         "url": self.handler.url(i['url']) if i['url'] != "#" else "#",
        #                         "activation": True if self.handler.__class__.__name__ in i['handlers'] else False,
        #                         "title": i['title'],
        #                         "child": []
        #                     }
        #                 )
        #
        # ls2 = []
        # try:
        #     for i in ls:
        #         if i['child']:
        #             if i['url'] == "#":
        #                 ls2.append(i)
        #         elif i['name'] in mm:
        #             ls2.append(i)
        # except:
        #     pass
        #
        # ls = ls2
        return self.render_string("modules/sidebar/sidebar.html", _tree=_perms, activation=activation)

    def embedded_javascript(self):
        return '''$("li[data-id="+$("a.active").attr("data-id")+"]").addClass("active");'''
