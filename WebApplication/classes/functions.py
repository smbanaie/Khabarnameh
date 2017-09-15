#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os
import random
import urllib2
import khayyam
import time
from WebApplication.classes.img import R_imgResizer
from shared_connection import SharedConnection

__author__ = 'ReS4'

s2 = SharedConnection()


def upload_file(handler, name='avatar', folder='avatars', extensions=None, default='',
                audio_name=None, index=0, max_size=15000):
    if not extensions:
        extensions = ['.mp3', '.amr', '.wma', '.mp4', '.3gp', '.pdf', '.doc', '.docx', '.pptx', '.zip']
    if name not in handler.request.files or len(handler.request.files[name][index]['body']) > (max_size * 1024):
        return default

    try:
        audio = handler.request.files[name][index]
        extension = os.path.splitext(audio['filename'])[-1].lower()
        upload_folder = os.path.join(s2.applications_root, 'static', 'upload', folder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        if extension in extensions:
            audio_name = str(audio_name) if audio_name is not None else str(
                random.randint(1155551918949, 91555519189459))
            audio_name += extension
            full_name = os.path.join(upload_folder, audio_name)
            output = open(full_name, 'wb')
            output.write(audio['body'])
            output.close()
            return audio_name
        else:
            return default
    except Exception as e:
        print e.message
        return default


def upload_photo(handler, name='avatar', folder='avatars', max_width=0, max_height=0, extensions=None, default='',
                 photo_name=None, index=0, max_size=3000):
    if not extensions:
        extensions = ['.jpg', '.png', '.gif', '.bmp', '.jpeg']
    if name not in handler.request.files or len(handler.request.files[name][index]['body']) > (max_size * 1024):
        return default

    try:
        pic = handler.request.files[name][index]
        extension = os.path.splitext(pic['filename'])[-1].lower()
        upload_folder = os.path.join(s2.applications_root, 'static', 'upload', folder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        if extension in extensions:
            photo_name = str(photo_name) if photo_name is not None else str(
                random.randint(1155551918949, 91555519189459))
            photo_name += extension
            full_name = os.path.join(upload_folder, photo_name)
            output = open(full_name, 'wb')
            output.write(pic['body'])
            output.close()

            if max_width != 0 and max_height != 0:
                s = R_imgResizer(os.path.join(upload_folder, photo_name))
                prefix = str(max_width) + 'x' + str(max_height) + '_'
                s.only_resize(max_width, max_height, prefix, upload_folder, quality=85, structure="JPEG")
                prefix = '1152x768_'
                s.only_resize(1400, 1100, prefix, upload_folder, quality=75, structure="JPEG")

                # os.remove(os.path.join(upload_folder, photo_name))
            else:
                prefix = ''

            return photo_name
        else:
            return default
    except Exception as e:
        print e.message
        return default


def upload_photo_by_url(url, name='avatar', folder='avatars', max_width=0, max_height=0, extensions=None, default='',
                        photo_name=None, max_size=3000):
    try:
        if not extensions:
            extensions = ['.jpg', '.png', '.gif', '.bmp', '.jpeg']

        photo = urllib2.build_opener().open(url)
        try:
            pic = photo.read()
            extension = os.path.splitext(url)[-1].lower()
            upload_folder = os.path.join(s2.applications_root, 'static', 'upload', folder)
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            if extension in extensions:
                photo_name = str(photo_name) if photo_name is not None else str(
                    random.randint(1155551918949, 91555519189459))
                photo_name = photo_name + extension
                full_name = os.path.join(upload_folder, photo_name)
                output = open(full_name, 'wb')
                output.write(pic)
                output.close()

                if max_width != 0 and max_height != 0:
                    s = R_imgResizer(os.path.join(upload_folder, photo_name))
                    prefix = str(max_width) + 'x' + str(max_height) + '_'
                    s.only_resize(max_width, max_height, prefix, upload_folder, quality=85, structure="JPEG")
                    prefix = '1152x768_'
                    s.only_resize(1420, 1100, prefix, upload_folder, quality=75, structure="JPEG")
                    # os.remove(os.path.join(upload_folder, photo_name))
                else:
                    prefix = ''
                return photo_name
            else:
                return default
        except Exception, e:
            print e, "        read and upload img "
            return False
    except Exception, e:
        print e, "    open img from url"
        return False


def to_jalali(date, _format="%Y/%m/%d"):
    return khayyam.JalaliDatetime(date).strftime(_format)


def to_time(_time):
    x = time.strptime(str(_time), "%H:%M:00")
    h = x.tm_hour if x.tm_hour >= 10 else "0%s" % x.tm_hour
    m = x.tm_min if x.tm_min >= 10 else "0%s" % x.tm_min
    return "{}:{}".format(h, m)


def rand_string(count=5):
    ps = hashlib.new('ripemd160')
    ps.update("Reza")
    chars = "t1abcg3deafg5hij2yz12ap34xum56b7d8b9j0w" + ps.hexdigest().lower()
    ret = ""
    for i in range(count):
        ret += chars[random.randint(0, 78)]
    return ret


from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ' '.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def read_xlsx(fname):
    import zipfile
    from xml.etree.ElementTree import iterparse

    z = zipfile.ZipFile(fname)
    strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    rows = []
    row = {}
    value = ''
    for e, el in iterparse(z.open('xl/worksheets/sheet1.xml')):
        if el.tag.endswith('}v'):  # <v>84</v>
            value = el.text
        if el.tag.endswith('}c'):  # <c r="A3" t="s"><v>84</v></c>
            if el.attrib.get('t') == 's':
                value = strings[int(value)]
            letter = el.attrib['r']  # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]
            row[letter] = value
            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    return rows
