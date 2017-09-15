#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2

import khayyam

from shared_connection import SharedConnection

__author__ = 'Ali'


class GCM:
    def __init__(self, message_type, registration_ids, title='', content='', **kwargs):
        # type = 0 => system message
        # type = 1 => notify user for new posts
        # type = 2 => notify user for new messages
        self.type = message_type
        self.title = title
        self.content = content
        self.registration_ids = registration_ids
        self.google_api_url = SharedConnection().mobile_settings["GOOGLE_API_URL"]
        self.google_api_key = "key=" + SharedConnection().mobile_settings["GOOGLE_API_KEY"]

        self.kw = kwargs

    def send_massage(self):
        message = {
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'date': str(khayyam.JalaliDatetime().now().strftime('%Y/%m/%d'))
        }
        z = {"message": message}
        if self.kw:
            z.update(**self.kw)
        params = {'registration_ids': self.registration_ids, "data": z}
        header = {'Authorization': self.google_api_key, 'Content-type': 'application/json'}
        try:
            req = urllib2.Request(self.google_api_url, data=json.dumps(params), headers=header)
            response = urllib2.urlopen(req)
            res_content = json.loads(response.read())
            return res_content['success'] > 0
        except:
            return False

# # test
# # m_type=0 => system message | m_type=1 notify user for new posts
# m_type = 0
# # reg_ids = ['APA91bEJgfO9ZleXr8iM15iDn2IiqkCNRs0JwbVCPwKa-BIp2Jb8THxzUlDr1LD47iC6Xdm6On_CheHT9lCS9-6NHOAe-2J16IzrnPkLdxF6jVzzKtQhfejuImEuz6GuJq81fVYJVTAvgbErdVk9Qujtn6A7bvvnMw']
# reg_ids = ['APA91bGMSgde9yICVCNdfRqHauif1qW-bq26-sVrLs2JrEiCN2n0e2r8aDUZbzN-Y9tUipqfRxSkvRS4QOcDnzKuJMAoAQpxmz9KXHfKugKePyIGSCuCb3rmogUvjzeW3JrTvfhjXidL']
# m_title = "اطلاعیه جدید"
# m_content = "سامانه پیام برای شما فعال شد."
# gcm = GCM(message_type=m_type, registration_ids=reg_ids, title=m_title, content=m_content)
# print gcm.send_massage()
