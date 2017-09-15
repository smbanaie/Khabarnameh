#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
from WebApplication.classes.auth_role import ScopeTree
from WebApplication.classes.functions import upload_photo, upload_file
from WebApplication.classes.gcm import GCM

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SystemAddNewsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "افزودن خبر جدید"

        tree = ScopeTree(system=self.current_system).get_js_tree()
        try:
            _tree = json.loads(tree)
        except:
            _tree = []

        ec = SysEditorsCollections.get_all(self.current_user)
        self.data['have_collection'] = True

        if "ADMIN" in self.get_user_roles():
            if ec:
                for i in range(len(_tree)):
                    if int(_tree[i]['id']) not in ec:
                        _tree[i]['state']['disabled'] = True
        elif "EDITOR" in self.get_user_roles():
            if ec:
                for i in range(len(_tree)):
                    if int(_tree[i]['id']) not in ec:
                        _tree[i]['state']['disabled'] = True
            else:
                self.data['have_collection'] = False

        if _tree:
            _tree = json.dumps(_tree)
            self.data['js_tree'] = _tree
        else:
            self.data['js_tree'] = tree
        self.data['help_id'] = "3"
        self.render('base/system/news/add_news.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):
        _error = False
        news = dict(
            system=self.current_system,
            _user=self.current_user,
            title=self.get_argument("news_title", ""),
            text=self.get_argument("full_text", None),
            _type=self.get_argument("_type", 0),
            status=SysNews.Published,
            public=1 if self.get_argument("public", 0) == "on" else 0
        )
        if "EDITOR" in self.get_user_roles():
            se = SysEditorsSetting(user=self.current_user).get_one()
            if se:
                if se['direct_publish'] == "yes":
                    news['status'] = SysNews.Published
                elif se['direct_publish'] == "no":
                    news['status'] = SysNews.Draft
            else:
                news['status'] = SysNews.Published

        for i in news:
            if news[i] is None or news[i] == "":
                _error = True
                self.add_error("تمامی موارد را به درستی وارد کنید.")

        if not _error:
            collections = json.loads(self.get_argument("collections", '[]'))
            if not collections:
                self.add_error("مجموعه ها را انتخاب کنید.")
            else:
                if self.current_plan_id == 1:
                    systems = []
                    systems.append(dict(child_id=self.current_system))
                    ls = SysSystem(_id=self.current_system).get_children()
                    for i in ls:
                        systems.append(i)

                else:
                    systems = [
                        dict(
                            child_id=self.current_system
                        )
                    ]
                pic_ls = []
                try:
                    for i in range(len(self.request.files['pic'])):
                        _pic = upload_photo(self, "pic", "news_pic", max_width=500, max_height=350, default=None,
                                            max_size=10000, index=i)
                        if _pic:
                            pic_ls.append(
                                dict(
                                    _pic=_pic
                                )
                            )

                except:
                    pass

                news_link = []
                try:
                    link_name = self.request.arguments['link_name']
                    link_address = self.request.arguments['link_address']
                    random_id = self.request.arguments['random_id']
                    for i in range(len(link_address)):
                        if link_address[i]:
                            if not link_name[i]:
                                link_name[i] = "بدون نام"

                            news_link.append(
                                dict(
                                    link_name=link_name[i],
                                    link_address=link_address[i],
                                    random_id=random_id[i],
                                )
                            )

                except Exception, e:
                    pass

                attach_file_ls = []
                file_type = None
                try:
                    x_f_n = self.get_arguments("file_name")
                    for i in range(len(self.request.files['attach_file'])):
                        attach_file = upload_file(self, "attach_file", "news_attach_file", index=i)
                        if attach_file:
                            file_type_s = attach_file.split(".")[-1]
                            if file_type_s in ["mp3", "amr", "wma"]:
                                file_type = "audio"
                            elif file_type_s in ["mp4", "3gp"]:
                                file_type = "video"
                            elif file_type_s in ["doc", "docx"]:
                                file_type = "word"
                            elif file_type_s == "pdf":
                                file_type = "pdf"
                            elif file_type_s == "pptx":
                                file_type = "powerpoint"
                            elif file_type_s == "zip":
                                file_type = "zip"

                            attach_file_ls.append(
                                dict(
                                    file_type=file_type,
                                    file_name=x_f_n[i],
                                    attach_file=attach_file
                                )
                            )
                except Exception, e:
                    pass
                try:
                    z = int(news['_type'])
                    if z in [1, 2, 3, 4, 5, 6]:
                        if z == 1:
                            news['_type'] = SysNews.TypeNews
                        elif z == 2:
                            news['_type'] = SysNews.TypeInstant
                        elif z == 3:
                            news['_type'] = SysNews.TypeImportant
                        elif z == 4:
                            news['_type'] = SysNews.TypeNotification
                        elif z == 5:
                            news['_type'] = SysNews.TypeFavorite
                        elif z == 6:
                            news['_type'] = SysNews.TypeGallery
                    else:
                        news['_type'] = SysNews.TypeNews
                except:
                    news['_type'] = SysNews.TypeNews

                collections1 = collections
                n_admin_id = ""
                for i in systems:
                    news['system'] = i['child_id']
                    n_id = SysNews(**news).add_news()
                    if i['child_id'] == self.current_system:
                        n_admin_id = n_id
                    if i['child_id'] != self.current_system:
                        SysNews_admin_p4(news_id=n_id, system_id=i['child_id']).insert(n_admin_id)
                    if n_id:
                        _tags = self.get_argument("tags", None)
                        if _tags:
                            try:
                                _tags = _tags.split(",")
                            except:
                                _tags = []

                            if _tags:
                                SysTags(system=i['child_id']).add_many(n_id, _tags)
                        if pic_ls:
                            try:
                                for j in pic_ls:
                                    SysNewsPic(news=n_id, pic_name=j['_pic'], system=i['child_id']).add_one()
                            except Exception, e:
                                pass
                        if attach_file_ls:
                            try:
                                for k in attach_file_ls:
                                    if not k['file_name']:
                                        k['file_name'] = "بدون نام"
                                    SysNewsFile(news=n_id, file_random_name=k['attach_file'], file_name=k['file_name'],
                                                file_type=k['file_type'], system=i['child_id']).add_one()
                            except Exception, e:
                                pass
                        if news_link:
                            for ln in news_link:
                                SysNewsLink(news=n_id, system=i['child_id'], link_name=ln['link_name'],
                                            link_address=ln['link_address'], random_id=ln['random_id']).add_one()

                        if self.current_system != news['system']:
                            collections = []
                            ls_col = []
                            for w in collections1:
                                try:
                                    _id = SysCollections(system=i['child_id'], parent_col_p4=w).get_sub_col()
                                    if _id:
                                        ls_col.append(_id)
                                except Exception, e:
                                    pass
                            collections = ls_col

                        _gcm = GCM(message_type=1, registration_ids=[], system_id=i['child_id'])
                        try:
                            # z = int(news['_type'])
                            if z in [1, 2, 3, 4, 5, 6]:
                                if z == 1:
                                    # news['_type'] = SysNews.TypeNews
                                    _gcm.title = u"خبر جدید"
                                elif z == 2:
                                    # news['_type'] = SysNews.TypeInstant
                                    _gcm.title = u"خبر فوری جدید"
                                elif z == 3:
                                    # news['_type'] = SysNews.TypeImportant
                                    _gcm.title = u"خبر مهم جدید"
                                elif z == 4:
                                    # news['_type'] = SysNews.TypeNotification
                                    _gcm.title = u"اطلاعیه جدید"
                                elif z == 5:
                                    # news['_type'] = SysNews.TypeFavorite
                                    _gcm.title = u"خبر برگزیده جدید"
                                elif z == 6:
                                    # news['_type'] = SysNews.TypeGallery
                                    _gcm.title = u"گالری عکس جدید"
                            else:
                                # news['_type'] = SysNews.TypeNews
                                _gcm.title = u"خبر جدید"
                        except:
                            news['_type'] = SysNews.TypeNews
                            _gcm.title = u"خبر جدید"

                        if SysNewsCollections(news=n_id).add_many(collections):
                            if SysNotificationByType(_type= news['_type']).get_one_status():
                                gcm = SysGcmUsers().get_all_users_for_news(collections)
                                if gcm:
                                    _gcm.content = news['title']
                                    _gcm.registration_ids = gcm
                                    _gcm.send_massage()
                        self.set_flash("msg", "خبر با موفقیت ثبت شد.")
                    else:
                        self.add_error("خطا در ثبت خبر. مجدداً تلاش نمایید.")
                        break

        self.redirect(self.url("system_add_news"))


class SystemNewsManagementHandler(WebBaseHandler):
    def __init__(self, application, request, **kwargs):
        super(SystemNewsManagementHandler, self).__init__(application, request, **kwargs)
        self.page_number = 1

    @gen.coroutine
    @authentication()
    def get(self, *args, **kwargs):
        self.data['title'] = "مدیریت اخبار"

        try:
            self.page_number = int(args[0])
        except:
            self.page_number = 1
            pass

        try:
            self.data['coll_id'] = int(args[1])
        except:
            self.data['coll_id'] = "all"
            pass

        try:
            self.data['sub_id'] = int(args[2])
        except:
            self.data['sub_id'] = "all"
            pass

        system = self.data['sub_id']
        collection = self.data['coll_id']
        if collection == "all" or not collection:
            collection = None
        if not system or system == "all":
            system = self.current_system

        if self.current_plan_id == 1:
            self.data['can_view_news'] = True
            sys_n = SysNews(system=system, status=SysNews.Published)
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news_p4(page=self.page_number, collection=collection)
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news_p4(page=self.page_number, collection=collection,
                                                              exp=News.user == self.current_user)
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                self.data['news'] = sys_n.get_news_p4(page=self.page_number, collection=collection)

            self.data['page_number'] = self.page_number
            ls = self.data['news']
            if self.current_system == system:
                x = [i['news_id']['id'] for i in SysNews_admin_p4().get_all(self.current_system)]
                if x:
                    y = self.data['news']
                    ls = []
                    for i in y:
                        if i['id'] not in x:
                            ls.append(i)
            self.data['total_count'] = len(ls)
            self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1

            }
            self.data['subsystems'] = SysSystem().get_all_sub_system(self.current_system)
            self.data['subsystems'].insert(0, dict(name="همه سیستم ها ", id="all"))
            coll = SysCollections().get_all(system=system)
            coll.insert(0, dict(name="همه مجموعه ها ", id="all"))
        else:
            self.data['can_view_news'] = True
            sys_n = SysNews(system=system, status=SysNews.Published)
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news(page=self.page_number, collection=collection)
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news(page=self.page_number, collection=collection,
                                                           exp=News.user == self.current_user)
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                self.data['news'] = sys_n.get_news(page=self.page_number, collection=collection)

            self.data['page_number'] = self.page_number
            # self.data['total_count'] = sys_n.get_count(collection=collection)
            x = [i['news_id']['id'] for i in SysNews_admin_p4(system_id=self.current_system).get_admin_news()]
            ls = self.data['news']
            if x:
                # self.data['total_count'] = self.data['total_count'] - len(x)
                y = self.data['news']
                ls = []
                for i in y:
                    if i['id'] not in x:
                        ls.append(i)
                        # self.data['news'] = ls
            self.data['subsystems'] = []
            self.data['total_count'] = len(ls)
            self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1
            }
            coll = SysCollections().get_all(system=self.current_system)
            coll.insert(0, dict(name="همه مجموعه ها ", id="all"))
        self.data['collections'] = coll
        del (self.data['collections'][1])
        self.data['help_id'] = "4"
        self.render('base/system/news/news.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self, *args, **kwargs):

        _method = self.get_argument("method", None)

        if _method == "delete":
            status = False
            try:
                cid = int(self.get_argument("cid", None))
                if cid:
                    if self.current_plan_id == 1:
                        n = SysNews(system=self.current_system, _id=cid)
                        get_one = False
                        if "EDITOR" in self.get_user_roles():
                            se = SysEditorsSetting(user=self.current_user).get_one()
                            if se:
                                if se['edit_news'] == "own":
                                    get_one = n.get_one_p4(News.user == self.current_user)
                                elif se['edit_news'] == "all":
                                    get_one = n.get_one_p4()
                            else:
                                self.write({"status": False})
                                return
                        else:
                            get_one = n.get_one_p4()

                        if get_one:

                            if n.delete_subnews():
                                x = SysNews_admin_p4(news_admin_id=cid).get_sub_news()
                                for i in x:
                                    SysNews(_id=i['sub_news_id']['id']).delete_subnews()
                                status = True

                    else:
                        n = SysNews(system=self.current_system, _id=cid)
                        get_one = False

                        if "EDITOR" in self.get_user_roles():
                            se = SysEditorsSetting(user=self.current_user).get_one()
                            if se:
                                if se['edit_news'] == "own":
                                    get_one = n.get_one(News.user == self.current_user)
                                elif se['edit_news'] == "all":
                                    get_one = n.get_one()
                            else:
                                self.write({"status": False})
                                return
                        else:
                            get_one = n.get_one()

                        if get_one:
                            if n.delete_news():
                                status = True

                self.write({"status": status})
            except:
                self.write({"status": status})

        else:
            self.write({"status": ":)"})

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):
        self.data['title'] = "مدیریت اخبار"
        subsystem = ""
        try:
            self.page_number = int(args[0])
        except Exception, e:
            self.page_number = 1
            pass
        coll_id = self.get_argument("coll", "all")
        if self.current_plan_id == 1:
            subsystem = self.get_argument("subsystem", "all")
            self.data['can_view_news'] = True
            sys_n = SysNews(system=self.current_system, status=SysNews.Published)
            if coll_id == "all" and subsystem == "all":
                self.redirect(self.url("system_news_management"))
                return
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news_by_search_p4(page=self.page_number, subsystem=subsystem,
                                                                        collection=coll_id)
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news_by_search_p4(page=self.page_number,
                                                                        exp=News.user == self.current_user
                                                                        , subsystem=subsystem, collection=coll_id)
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                self.data['news'] = sys_n.get_news_by_search_p4(page=self.page_number, subsystem=subsystem,
                                                                collection=coll_id)

            self.data['page_number'] = self.page_number
            coll_id1 = coll_id
            if coll_id1 == "all":
                coll_id1 = None

            subsystem1 = subsystem
            if subsystem1 == "all":
                subsystem1 = self.current_system
            self.data['total_count'] = sys_n.total_count_search_p4(sys_id=subsystem1, coll_id=coll_id1)
            ls = self.data['news']
            self.data['total_count'] = len(ls)
            if ls:
                self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1

            }
            self.data['subsystems'] = SysSystem().get_all_sub_system(self.current_system)
            self.data['subsystems'].insert(0, dict(name="همه سیستم ها ", id="all"))
            if subsystem == "all":
                subsystem = self.current_system
            self.data['collections'] = SysCollections().get_all(system=subsystem)
            self.data['collections'].insert(0, dict(name="همه مجموعه ها ", id="all"))
            del (self.data['collections'][1])

        else:
            self.data['can_view_news'] = True
            sys_n = SysNews(system=self.current_system, status=SysNews.Published)
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if coll_id == "all":
                        self.redirect(self.url("system_news_management"))
                        return
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news_by_search(page=self.page_number, collection=coll_id)
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news_by_search(page=self.page_number,
                                                                     exp=News.user == self.current_user,
                                                                     collection=coll_id)
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                if coll_id == "all":
                    self.redirect(self.url("system_news_management"))
                    return
                self.data['news'] = sys_n.get_news_by_search(page=self.page_number, collection=coll_id)
            all_news = len(self.data['news'])
            self.data['page_number'] = self.page_number
            coll_id1 = coll_id
            # if coll_id1 == "all":
            #     coll_id1 = None
            x = [i['news_id']['id'] for i in SysNews_admin_p4(system_id=self.current_system).get_admin_news()]
            if x:
                y = self.data['news']
                ls = []
                for i in y:
                    if i['id'] not in x:
                        ls.append(i)
                if ls:
                    self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            else:
                self.data['news'] = self.data['news'][(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['total_count'] = all_news
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1
            }

            self.data['subsystems'] = ""
            self.data['collections'] = SysCollections().get_all(system=self.current_system)
            self.data['collections'].insert(0, dict(name="همه مجموعه ها ", id="all"))
            del (self.data['collections'][1])
        self.data['help_id'] = "4"
        self.data['sub_id'] = subsystem
        self.data['coll_id'] = coll_id
        self.render('base/system/news/news.html', **self.data)


class SystemNewsEditHandler(WebBaseHandler):
    def __init__(self, application, request, **kwargs):
        super(SystemNewsEditHandler, self).__init__(application, request, **kwargs)
        self.get_one = {}

    def get_news_info(self, news_id):
        n = SysNews(system=self.current_system, _id=news_id)
        if self.current_plan_id == 1:
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "own":
                        self.get_one = n.get_one_p4(News.user == self.current_user)
                    elif se['edit_news'] == "all":
                        self.get_one = n.get_one_p4()
                    else:
                        self.redirect(self.url("system_news_management"))
                        return
            else:
                self.get_one = n.get_one_p4()
        else:
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "own":
                        self.get_one = n.get_one(News.user == self.current_user)
                    elif se['edit_news'] == "all":
                        self.get_one = n.get_one()
                else:
                    self.redirect(self.url("system_news_management"))
                    return
            else:
                self.get_one = n.get_one()

    @gen.coroutine
    @authentication()
    def get(self, news_id):
        self.data['title'] = "ویرایش خبر"

        if int(news_id):
            self.get_news_info(news_id)
            if self.get_one:
                system_id = self.current_system
                if self.current_plan_id == 1:
                    system_id = self.get_one['system']
                nc = SysNewsCollections(news=news_id).get_collection_id_by_news()
                tree = ScopeTree(system=system_id).get_js_tree(selected_scopes=nc)

                try:
                    _tree = json.loads(tree)
                except:
                    _tree = []

                ec = SysEditorsCollections.get_all(self.current_user)
                self.data['have_collection'] = True

                if "ADMIN" in self.get_user_roles():
                    if ec:
                        for i in range(len(_tree)):
                            if int(_tree[i]['id']) not in ec:
                                _tree[i]['state']['disabled'] = True
                elif "EDITOR" in self.get_user_roles():
                    if ec:
                        for i in range(len(_tree)):
                            if int(_tree[i]['id']) not in ec:
                                _tree[i]['state']['disabled'] = True
                    else:
                        self.data['have_collection'] = False

                if _tree:
                    _tree = json.dumps(_tree)
                    self.data['js_tree'] = _tree
                else:
                    self.data['js_tree'] = tree

                self.data['news'] = self.get_one

                self.data['tags'] = ",".join([i['tag']['name'] for i in SysNewsTag(news=news_id).get_all()])
                self.data['pics'] = SysNewsPic(news=news_id, system=system_id).get_all_dict()
                self.data['files'] = SysNewsFile(news=news_id, system=system_id).get_all_dict()
                self.data['links'] = SysNewsLink(news=news_id, system=system_id).get_all_dict()

                self.render('base/system/news/edit_news.html', **self.data)
            else:
                self.set_flash("msg", "خبر مورد نظر یافت نشد.")
                self.redirect(self.url("system_news_management"))
        else:
            self.set_flash("msg", "خبر مورد نظر یافت نشد.")
            self.redirect(self.url("system_news_management"))

    @gen.coroutine
    @authentication()
    def post(self, news_id):

        if int(news_id):
            self.get_news_info(news_id)

            if self.get_one:
                system_id = self.current_system
                if self.current_plan_id == 1:
                    system_id = self.get_one['system']

                _error = False
                news = dict(
                    _id=news_id,
                    system=system_id,
                    _user=self.get_one['user']['id'],
                    title=self.get_argument("news_title", ""),
                    text=self.get_argument("full_text", None),
                    _type=self.get_argument("_type", 0),
                    status=SysNews.Published,
                    public=1 if self.get_argument("public", 0) == "on" else 0
                )

                if "EDITOR" in self.get_user_roles():
                    se = SysEditorsSetting(user=self.current_user).get_one()
                    if se:
                        if se['direct_publish'] == "yes":
                            news['status'] = SysNews.Published
                        elif se['direct_publish'] == "no":
                            news['status'] = SysNews.Draft
                    else:
                        news['status'] = SysNews.Published

                try:

                    z = int(news['_type'])
                    if z in [1, 2, 3, 4, 5, 6]:
                        if z == 1:
                            news['_type'] = SysNews.TypeNews
                        elif z == 2:
                            news['_type'] = SysNews.TypeInstant
                        elif z == 3:
                            news['_type'] = SysNews.TypeImportant
                        elif z == 4:
                            news['_type'] = SysNews.TypeNotification
                        elif z == 5:
                            news['_type'] = SysNews.TypeFavorite
                        elif z == 6:
                            news['_type'] = SysNews.TypeGallery
                    else:
                        news['_type'] = SysNews.TypeNews
                except:
                    news['_type'] = SysNews.TypeNews

                for i in news:
                    if (news[i] is None or news[i] == ""):
                        _error = True
                        self.add_error("تمامی موارد را به درستی وارد کنید.")

                if not _error:
                    collections = json.loads(self.get_argument("collections", '[]'))
                    if not collections:
                        self.add_error("مجموعه ها را انتخاب کنید.")
                    else:
                        pic_ls = []
                        try:
                            for i in range(len(self.request.files['pic'])):
                                _pic = upload_photo(self, "pic", "news_pic", max_width=500, max_height=350,
                                                    default=None,
                                                    max_size=10000, index=i)
                                if _pic:
                                    pic_ls.append(
                                        dict(
                                            _pic=_pic
                                        )
                                    )

                        except Exception, e:
                            pass

                        news_link = []
                        try:
                            link_name = self.request.arguments['link_name']
                            link_address = self.request.arguments['link_address']
                            random_id = self.request.arguments['random_id']
                            for i in range(len(link_address)):
                                if link_address[i]:
                                    if not link_name[i]:
                                        link_name[i] = "بدون نام"

                                    news_link.append(
                                        dict(
                                            link_name=link_name[i],
                                            link_address=link_address[i],
                                            random_id=random_id[i],
                                        )
                                    )
                        except Exception, e:
                            pass

                        attach_file_ls = []
                        file_type = None
                        try:
                            x_f_n = self.get_arguments("file_name")
                            for i in range(len(self.request.files['attach_file'])):
                                attach_file = upload_file(self, "attach_file", "news_attach_file", index=i)
                                if attach_file:
                                    file_type_s = attach_file.split(".")[-1]
                                    if file_type_s in ["mp3", "amr", "wma"]:
                                        file_type = "audio"
                                    elif file_type_s in ["mp4", "3gp"]:
                                        file_type = "video"
                                    elif file_type_s in ["doc", "docx"]:
                                        file_type = "word"
                                    elif file_type_s == "pdf":
                                        file_type = "pdf"
                                    elif file_type_s == "pptx":
                                        file_type = "powerpoint"
                                    elif file_type_s == "zip":
                                        file_type = "zip"

                                    attach_file_ls.append(
                                        dict(
                                            file_type=file_type,
                                            file_name=x_f_n[i],
                                            attach_file=attach_file
                                        )
                                    )
                        except Exception, e:
                            pass

                        if self.current_plan_id == 1:
                            if system_id == self.current_system:
                                systems = []
                                systems.append(dict(child_id=self.current_system))
                                ls = SysSystem(_id=self.current_system).get_children()
                                for i in ls:
                                    systems.append(i)
                            else:
                                systems = [
                                    dict(
                                        child_id=system_id
                                    )
                                ]

                        else:
                            systems = [
                                dict(
                                    child_id=self.current_system
                                )
                            ]
                        _n_id = news_id
                        collections1 = collections

                        p = self.get_argument("deleted_image", "[]")
                        ff = self.get_argument("deleted_file", "[]")
                        lnk = self.get_argument("deleted_link", "[]")
                        try:
                            edit_news_names_file = []
                            edit_nm = self.request.arguments["edit_name_file"]
                            edit_file_id = self.request.arguments["edit_file_id"]
                        except Exception, e:
                            pass
                        try:
                            edit_news_link = []
                            edit_nm_link = self.request.arguments["edit_link_name"]
                            edit_adrs_link = self.request.arguments["edit_link_address"]
                            edit_id_link = self.request.arguments["edit_id_link"]
                        except Exception, e:
                            pass

                        try:
                            for i in range(len(edit_id_link)):
                                edit_news_link.append(
                                    dict(
                                        edit_id_link=edit_id_link[i],
                                        edit_nm_link=edit_nm_link[i],
                                        edit_adrs_link=edit_adrs_link[i]
                                    )
                                )
                        except:
                            pass
                        try:
                            for i in range(len(edit_file_id)):
                                edit_news_names_file.append(
                                    dict(
                                        edit_file_id=edit_file_id[i],
                                        new_name=edit_nm[i]
                                    )
                                )
                        except:
                            pass
                        if len(systems) > 1:
                            try:
                                p = json.loads(p)
                                if p:
                                    p = map(int, p)
                                    SysNewsPic(news=news_id, system=news['system']).delete_bash_pics_p4(p)
                            except Exception, e:
                                pass
                            try:
                                ff = json.loads(ff)
                                if ff:
                                    ff = map(int, ff)
                                    SysNewsFile(news=news_id, system=news['system']).delete_bash_files_p4(ff)
                            except Exception, e:
                                pass
                            try:
                                lnk = json.loads(lnk)
                                if lnk:
                                    lnk = map(int, lnk)
                                    SysNewsLink(news=news_id, system=news['system']).delete_links_p4(lnk)
                            except Exception, e:
                                pass

                            for i in edit_news_names_file:
                                SysNewsFile(news=news_id, system=news['system'], _id=i['edit_file_id'],
                                            file_name=i['new_name']).update_file_name_p4()

                            for l1 in edit_news_link:
                                SysNewsLink(news=news_id, system=news['system'], _id=l1['edit_id_link'],
                                            link_name=l1['edit_nm_link'],
                                            link_address=l1['edit_adrs_link']).update_link_p4()
                        else:
                            try:
                                p = json.loads(p)
                                if p:
                                    p = map(int, p)
                                    SysNewsPic(news=news_id, system=news['system']).delete_bash_pics(p, False)
                            except Exception, e:
                                pass

                            try:
                                ff = json.loads(ff)
                                if ff:
                                    ff = map(int, ff)
                                    SysNewsFile(news=news_id, system=news['system']).delete_bash_files(ff, False)
                            except Exception, e:

                                pass
                            try:
                                lnk = json.loads(lnk)
                                if lnk:
                                    lnk = map(int, lnk)
                                    SysNewsLink(news=news_id, system=news['system']).delete_links(lnk)
                            except Exception, e:
                                pass

                            for f1 in edit_news_names_file:
                                SysNewsFile(news=news_id, system=news['system'], _id=f1['edit_file_id'],
                                            file_name=f1['new_name']).update_file_name()

                            for l1 in edit_news_link:
                                SysNewsLink(news=news_id, system=news['system'], _id=l1['edit_id_link'],
                                            link_name=l1['edit_nm_link'],
                                            link_address=l1['edit_adrs_link']).update_link()

                        for i in systems:
                            try:
                                news['system'] = i['child_id']
                                if len(systems) > 1 and news['system'] != self.current_system:
                                    i = SysNews_admin_p4(news_admin_id=_n_id, system_id=news['system']).get_one()
                                    news_id = i['news_id']['id']
                                    news['_id'] = news_id
                                SysNews(**news).update_news()
                                _tags = self.get_argument("tags", None)
                                if _tags == "":
                                    SysNewsTag(news=news_id).delete_by_news_id()
                                elif _tags:
                                    try:
                                        _tags = _tags.split(",")
                                    except:
                                        _tags = []

                                    if _tags:
                                        SysNewsTag(news=news_id).delete_by_news_id()
                                        SysTags(system=news['system']).add_many(news_id, _tags)

                                if pic_ls:
                                    try:
                                        for j in pic_ls:
                                            SysNewsPic(news=news_id, pic_name=j['_pic'],
                                                       system=news['system']).add_one()
                                    except Exception, e:
                                        pass

                                if attach_file_ls:
                                    try:
                                        for k in attach_file_ls:
                                            if not k['file_name']:
                                                k['file_name'] = "بدون نام"
                                            SysNewsFile(news=news_id, file_random_name=k['attach_file'],
                                                        file_type=k['file_type'], file_name=k['file_name'],
                                                        system=news['system']).add_one()
                                    except Exception, e:
                                        pass

                                if news_link:
                                    for ln in news_link:
                                        SysNewsLink(news=news_id, system=news['system'], link_name=ln['link_name'],
                                                    link_address=ln['link_address'],
                                                    random_id=ln['random_id']).add_one()

                                if len(systems) > 1 and self.current_system != news['system']:
                                    collections = []
                                    ls_c = []
                                    for w in collections1:
                                        try:
                                            _id = SysCollections(system=news['system'], parent_col_p4=w).get_sub_col()
                                            if _id:
                                                ls_c.append(_id)
                                        except Exception, e:
                                            pass
                                    collections = ls_c

                                if SysNewsCollections(news=news_id).update_many(collections):
                                    self.set_flash("msg", "خبر با موفقیت ثبت شد.")
                                else:
                                    self.set_flash("msg", "")
                                    self.set_flash("msg",
                                                   "خطا در ثبت خبر. برای برخی از زیرسیستم ها مجموعه ای انتخاب نشده است.")
                            except Exception, e:
                                self.set_flash("msg", "")
                                self.add_error("خطا در ثبت خبر. مجدداً تلاش نمایید.")
                                pass

                self.redirect(self.url("system_news_management"))
                return

        self.set_flash("msg", "خبر مورد نظر یافت نشد.")
        self.redirect(self.url("system_news_management"))


class SystemPendingNewsHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self, page):
        self.data['title'] = "خبر های در انتظار تایید"
        try:
            self.page_number = int(page)
        except:
            self.page_number = 1

        # self.data['coll_id'] = 0
        if self.current_plan_id == 1:
            self.data['sub_id'] = "all"
            self.data['can_view_news'] = True
            sys_n = SysNews(system=self.current_system, status=SysNews.Draft)
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news_p4()
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news_p4(exp=News.user == self.current_user)
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                self.data['news'] = sys_n.get_news_p4()

            self.data['page_number'] = self.page_number
            # self.data['total_count'] = sys_n.total_count_p4()
            x = [i['news_id']['id'] for i in SysNews_admin_p4().get_all(self.current_system)]
            ls = self.data['news']
            if x:
                # r=len(x)
                # self.data['total_count']=self.data['total_count']-r
                y = self.data['news']
                ls = []
                for i in y:
                    if i['id'] not in x:
                        ls.append(i)
            self.data['total_count'] = len(ls)
            self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1

            }
            sys = SysSystem().get_all_sub_system(self.current_system)
            ls_s = [dict(
                name="همه ",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems'] = ls_s

        else:
            self.data['can_view_news'] = True
            sys_n = SysNews(system=self.current_system, status=SysNews.Draft)
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news()
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news(exp=News.user == self.current_user)
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                self.data['news'] = sys_n.get_news()

            self.data['page_number'] = self.page_number
            # self.data['total_count'] = sys_n.get_count()

            x = [i['news_id']['id'] for i in SysNews_admin_p4(system_id=self.current_system).get_admin_news()]
            ls = self.data['news']
            if x:
                # r=len(x)
                # self.data['total_count']=self.data['total_count']-r
                y = self.data['news']
                ls = []
                for i in y:
                    if i['id'] not in x:
                        ls.append(i)
                        # self.data['news'] = ls
            self.data['subsystems'] = []
            self.data['total_count'] = len(ls)
            self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1

            }
        self.data['help_id'] = "4"
        self.render('base/system/news/waiting_news.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self, page, *args, **kwargs):
        self.data['title'] = "خبر های در انتظار تایید"
        _method = self.get_argument("method", None)
        search = self.get_argument("search", None)
        if search == "search":
            try:
                self.page_number = int(page)
            except:
                self.page_number = 1
            subsystem = self.get_argument("subsystem", None)
            self.data['can_view_news'] = True
            sys_n = SysNews(system=self.current_system, status=SysNews.Draft)
            if subsystem == "all":
                self.redirect(self.url("system_news_waiting"))
                return
            if "EDITOR" in self.get_user_roles():
                se = SysEditorsSetting(user=self.current_user).get_one()
                if se:
                    if se['edit_news'] == "all":
                        self.data['news'] = sys_n.get_news_by_search_p4(subsystem=subsystem, collection="all")
                    elif se['edit_news'] == "own":
                        self.data['news'] = sys_n.get_news_by_search_p4(exp=News.user == self.current_user
                                                                        , subsystem=subsystem, collection="all")
                    else:
                        self.data['can_view_news'] = False
                else:
                    self.data['can_view_news'] = False
            else:
                self.data['news'] = sys_n.get_news_by_search_p4(subsystem=subsystem, collection="all")

            self.data['page_number'] = self.page_number
            x = [i['news_id']['id'] for i in SysNews_admin_p4().get_all(self.current_system)]
            ls = self.data['news']
            if x:
                y = self.data['news']
                ls = []
                for i in y:
                    if i['id'] not in x:
                        ls.append(i)
            self.data['total_count'] = len(ls)
            self.data['news'] = ls[(int(self.page_number) - 1) * 10:int(self.page_number) * 10]
            self.data['pagination'] = {
                "next": True if self.data['total_count'] > (self.page_number * 10) else False,
                "prev": True if (self.page_number > 1) else False,
                "next_number": self.page_number + 1,
                "prev_number": self.page_number - 1

            }

            sys = SysSystem().get_all_sub_system(parent_id=self.current_system)
            ls_s = [dict(
                name="همه",
                id="all"
            )]
            for i in sys:
                ls_s.append(i)
            self.data['subsystems'] = ls_s
            self.data['sub_id'] = subsystem
            self.data['help_id'] = "4"
            self.render('base/system/news/waiting_news.html', **self.data)

        if _method == "accept":
            status = False
            try:
                cid = int(self.get_argument("cid", None))
                if cid:
                    n = SysNews(system=self.current_system, _id=cid, status="PUBLISHED")
                    get_one = False
                    if self.current_plan_id == 1:
                        if "EDITOR" in self.get_user_roles():
                            se = SysEditorsSetting(user=self.current_user).get_one()
                            if se:
                                if se['edit_news'] == "own":
                                    get_one = n.get_one_p4(News.user == self.current_user)
                                elif se['edit_news'] == "all":
                                    get_one = n.get_one_p4()
                            else:
                                self.write({"status": False})
                                return
                        else:
                            get_one = n.get_one_p4()
                    else:
                        if "EDITOR" in self.get_user_roles():
                            se = SysEditorsSetting(user=self.current_user).get_one()
                            if se:
                                if se['edit_news'] == "own":
                                    get_one = n.get_one(News.user == self.current_user)
                                elif se['edit_news'] == "all":
                                    get_one = n.get_one()
                            else:
                                self.write({"status": False})
                                return
                        else:
                            get_one = n.get_one()

                    if get_one:
                        if n.update_status_news():
                            status = True

                self.write({"status": status})
            except:
                self.write({"status": status})

        else:
            self.write({"status": ":)"})


class GetCollectionsHandler(WebBaseHandler):
    @gen.coroutine
    # @authentication()
    def post(self):
        try:
            ls_c = []
            _id = self.get_argument("pid", "")
            if _id == "all":
                _id = self.current_system
            colls = SysCollections().get_all(system=_id)
            del (colls[0])
            ls_c = [dict(
                id="all",
                name="همه مجموعه ها "
            )]
            for i in colls:
                ls_c.append(i)
            self.write({'sys_colls': ls_c})
        except Exception, e:
            self.write("0")
