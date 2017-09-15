#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ReS4'


import mandrill
import os
# from setting import Setting
from tornado import template

from shared_connection import SharedConnection
ssss = SharedConnection()

class R_Mail():
    def __init__(self, from_address='admin@bamardese.ir', from_name='BaMadrese :)', subject='Active Profile',
                 tag_list=['BaMadrese'], to=[{'email': 'reza.s4t4n@yahoo.com', 'name': 'Reza S4T4N', 'type': 'to'}]):
        self.from_address = from_address
        self.from_name = from_name
        self.html = ''
        self.subject = subject
        self.tag_list = tag_list
        self.to = to
        # self.active_code = active_code

    def send(self):
        try:
            mandrill_client = mandrill.Mandrill('cSI3xgSvdLGaWy6Z8mtO5Q')

            message = {
             'auto_html': True,
             'auto_text': False,
             'bcc_address': self.from_address,
             'from_email': self.from_address,
             'from_name': self.from_name,

             'headers': {'Reply-To': 'noreply@foodlist.ir'},
             'html': self.html,

             'important': True,
             'inline_css': None,
             'merge': True,
             # 'merge_vars': [{'rcpt': 'recipient.email@example.com',
             #                 'vars': [{'content': 'merge2 content', 'name': 'merge2'}]}],
             'metadata': {'website': 'www.foodlist.ir'},
             'preserve_recipients': False,
             # 'recipient_metadata': [{'rcpt': 'reza.s4t4n@gmail.com',
             #                         'values': {'user_id': 123456}}],
             'return_path_domain': None,
             'signing_domain': None,

             'subject': self.subject,
             'tags': self.tag_list,
             'text': '',
             'to': self.to,
             'track_clicks': None,
             'track_opens': None,
             'tracking_domain': None,
             'url_strip_qs': None,
             'view_content_link': None}

            result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
            return result
        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            pass

    def render_html(self, template_name, **kwargs):
        try:
            av_dir = os.path.join(ssss.web['template_address'], "email_form/")

            if not os.path.exists(av_dir):
                os.makedirs(av_dir)

            tmp = av_dir + template_name

            f = open(tmp).read()
            t = template.Template(f)

            self.html = t.generate(**kwargs)
        except Exception, e:
            pass



# #
# m = R_Mail()
# m.from_name = 'BaMadrese'
# m.from_address = 'reza@foodlist.com'
# m.to = [
#         {'email': 'omid.m_1990@yahoo.com','name': 'Reza S4T4N','type': 'to'}
#     ]
# # m.html = u"<p style='color:red'>سلام عزیزم</p>"
# # m.send()
#
#
# m.render_html("active_mail.html",active_code='123145')
#
# m.send()




# emails = ['zaaferani.arta@gmail.com']
# i = 0
# m = R_Mail()
# m.from_name = '{0} {1}'.format('حسن', 'زعفرانی')
# m.from_address = 'user-invite@foodlist.ir'
# m.subject = 'دعوت به سایت فودلیست'
#
# ls = []
# for email in emails:
#     ls.append({'email': email, 'name': '', 'type': 'to'})
#     i += 1
#
# m.to = ls
# m.make_html(
#     "user_invite.html",
#     link='http://www.foodlist.ir/userRegister/invite/{0}'.format(1),
#     name=m.from_name
# )
# if i != 0:
#     m.send()
#     print('ok')