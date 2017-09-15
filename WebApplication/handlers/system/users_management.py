#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from WebApplication.classes.auth_role import ScopeTree
from WebApplication.classes.functions import read_xlsx
import random

from WebApplication.db_models.models.login import LoginMethod

__author__ = 'ReS4'

from WebApplication.handlers.base import *


class SystemUserManagementHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "مدیریت نقش های کاربر"
        self.data['help_id'] = "11"
        self.render('base/system/user_roles_management/user_roles_management.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):

        _username = self.get_argument("username", None)
        if _username:
            u = SysUsers.is_exist(user_name=_username, system=self.current_system)
            if u:
                r = map(int, SysUserRoles.get_all(u['id']))
                self.write({"status": True, "tree": SysRoles(system=self.current_system).get_js_tree(r)})
            else:
                self.write({"status": False})
        else:
            self.write({"status": False})

    @gen.coroutine
    @authentication()
    def post(self):
        username = self.get_argument("username", None)
        roles = self.get_argument("roles", None)
        if roles:
            try:
                roles = json.loads(roles)
            except:
                roles = []

        u = SysUsers.is_exist(user_name=username, system=self.current_system)
        editor_role = SysRoles(system=self.current_system, name="EDITOR").get_one_by_name()
        if u and roles:
            if "0" in roles:
                roles.remove("0")

            if SysUserRoles.add_user_roles(u['id'], roles):
                if str(editor_role['id']) in roles:
                    SysEditorsSetting(
                        user=u['id'],
                        edit_news=SysEditorsSetting.Disable,
                        direct_publish=SysEditorsSetting.No
                    ).add_setting()
                else:
                    SysEditorsSetting(user=u['id']).delete_setting()

                self.write({"status": True})
            else:
                self.write({"status": False})


class SystemUmAddUsersHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):
        self.data['title'] = "افزودن کاربران جدید"
        self.data['roles'] = SysRoles(system=self.current_system).get_all()
        self.data['js_tree'] = SysRoles(system=self.current_system).get_js_tree()
        self.data['help_id'] = "9"
        self.render('base/system/users_management/add_users.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self):

        _username = self.get_argument("u", None)

        if _username:

            u = SysUsers.is_exist(user_name=_username, system=self.current_system)
            if u:
                self.write("true")
            else:
                self.write("false")
            return
        self.finish("true")

    @gen.coroutine
    @authentication()
    def post(self):

        _method = self.get_argument("method", None)
        m = SysUsers(system=self.current_system).count()
        n = SysSystemPlanFeatures(system=self.current_system).get_one()
        if _method == "save":
            if (n['max_users'] - m) > 0:
                _u = {}
                cp = {}
                self.check_sent_value("fname", _u, "first_name", "نام را وارد کنید.")
                self.check_sent_value("lname", _u, "last_name", "نام خانوادگی را وارد کنید.")
                self.check_sent_value("username", _u, "username", "نام کاربری را وارد کنید.", default=None)
                self.check_sent_value("password", _u, "password", "گذرواژه را وارد کنید.")
                self.check_sent_value("conf_password", cp, "password2", "تکرار گذرواژه را وارد کنید.")
                role = self.get_argument("role", None)
                if role:
                    try:
                        role = json.loads(role)
                        if "0" in role:
                            role.remove("0")
                        role = map(int, role)
                    except:
                        role = []

                if self.errors:
                    for i in self.errors:
                        self.add_error(i)
                    self.redirect(self.reverse_url("system_um_add_users"))
                    return

                if _u['username']:
                    if SysUsers.is_exist(user_name=_u['username'], system=self.current_system):
                        self.add_error("این نام کاربری قبلاً ثبت شده است.")
                        self.redirect(self.reverse_url("system_um_add_users"))
                        return

                try:
                    _u['password'] = LoginMethod.mk_pass(_u['password'])
                    u = SysUsers(system=self.current_system, **_u).add_user()
                    if u:
                        ur = [i['id'] for i in SysRoles(system=self.current_system).get_all()]
                        c = []
                        for i in role:
                            if i not in ur:
                                self.set_flash("msg", "مجموعه ها را به درستی وارد کنید.")
                                self.redirect(self.reverse_url("system_um_add_users"))
                                return
                            k = SysCollectionRoles().get_all_ids(i)
                            for i in k:
                                if i['status'] == "yes":
                                    if i['collection_id'] not in c:
                                        c.append(i['collection_id'])
                        SysUserRoles.add_user_roles(u, role)
                        SysUserCollections(user=u).set_user_collections(c)
                        self.set_flash("msg", "اطلاعات کاربر با موفقیت ذخیره شد.")
                        # else:
                        #     self.set_flash("msg", "خطا در ثبت کاربر. مجدداً تلاش نمایید.")
                    else:
                        self.set_flash("msg", "خطا در ثبت کاربر. مجدداً تلاش نمایید.")
                except Exception, e:
                    self.set_flash("msg", "خطا در ثبت کاربر. مجدداً تلاش نمایید.")
            else:
                self.add_error("خطا در ثبت کاربر.تعداد کاربران بیش از حد مجاز است.")
            self.redirect(self.reverse_url("system_um_add_users"))
        elif _method == "group_save":

            try:
                role = int(self.get_argument("users_role", None))
            except:
                role = None

            counter = [0, 0, 0]
            if role:
                if role in [i['id'] for i in SysRoles(system=self.current_system).get_all()]:
                    k = SysCollectionRoles().get_all_ids(role)
                    c = []
                    for i in k:
                        c.append(i['collection_id'])
                    try:
                        _file = self.request.files['inp'][0]
                        if os.path.splitext(_file['filename'])[-1].lower() == ".xlsx":

                            filename = os.path.join(sh.web['static_address'], 'tmp', 'RsTmp.%s.xlsx' % os.getpid())
                            temp = open(filename, 'w+b')
                            try:
                                temp.write(_file['body'])
                                temp.close()
                                rows = read_xlsx(filename)
                                if rows:
                                    if rows[0]['A'].strip() == u"نام":
                                        del rows[0]

                                    row_dicts = [
                                        {
                                            'system': self.current_system,
                                            'username': r['C'],
                                            "password": LoginMethod.mk_pass(r['D']),
                                            "first_name": r['A'],
                                            "last_name": r['B']
                                        } for r in rows
                                        ]
                                    # print len(rows)

                                    for i in row_dicts:
                                        if counter[0] < n['max_users'] - m:
                                            try:
                                                # i['username'] = int(i['username'])
                                                # print i['username']
                                                # print type(i['username'])
                                                s = re.match(ur'^09\d{9}$', i['username'])
                                                if s:
                                                    u = SysUsers(**i).add_user()
                                                    if u:
                                                        SysUserRoles.add_user_roles(u, [role])
                                                        SysUserCollections(user=u).set_user_collections(c)
                                                        counter[0] += 1
                                                    else:
                                                        counter[1] += 1
                                                else:
                                                    counter[1] += 1
                                            except:
                                                counter[1] += 1
                                        else:
                                            counter[2] += 1
                            finally:
                                if not temp.closed:
                                    temp.close()
                                # Clean up the temporary file yourself
                                os.remove(filename)

                        else:
                            self.errors = "فرمت فایل آپلود شده صحیح نمی باشد."

                    except Exception, e:
                        self.errors = "خطا در دریافت فایل ورودی. مجدداً تلاش نمایید."
                else:
                    self.errors = "گروه کاربری انتخاب شده مربوط به این سیستم نمی باشد."
            else:
                self.errors = "گروه کاربری را انتخاب کنید."

            if self.errors:
                self.add_error(self.errors)
            else:
                if not counter[0]:
                    self.add_error("متاسفانه به علت تکراری بودن و یا عدم صحت اطلاعات ورودی ، هیچ رکوردی ثبت نگردید.")
                else:
                    if counter[2]:
                        self.set_flash("msg",
                                       "بارگذاری با موفقیت انجام شد. تعداد {} رکورد قابل قبول و {} رکورد غیرقابل قبول ثبت گردید. تعداد {} رکورد بیش از حد مجاز بود.".format(
                                           counter[0], counter[1], counter[2]))
                    else:
                        self.set_flash("msg",
                                       "بارگذاری با موفقیت انجام شد. تعداد {} رکورد قابل قبول و {} رکورد غیرقابل قبول ثبت گردید.".format(
                                           counter[0], counter[1]))
            self.redirect(self.reverse_url("system_um_add_users"))

        else:
            self.redirect(self.reverse_url("system_um_add_users"))


class SystemUmAUsersListHandler(WebBaseHandler):
    @staticmethod
    def check_regex(arg, regex):
        p = re.compile(regex, re.IGNORECASE)
        z = re.findall(p, arg)
        if z:
            return z[0]
        else:
            return None

    def check_parameters(self, arg):
        ret_dict = dict()
        if arg:

            ret_dict['name'] = self.check_regex(arg, ur'(?is)fn:([\w+]+)')
            ret_dict['family'] = self.check_regex(arg, ur'(?is)ln:([\w+]+)')
            ret_dict['role'] = self.check_regex(arg, ur'(?is)role:([\w+]+)')
            ret_dict['username'] = self.check_regex(arg, ur'(?is)username:([\w+]+)')
            ret_dict['page'] = self.check_regex(arg, ur'(?is)page:([\d+]+)')
            # ret_dict['sort'] = self.check_regex(arg, ur'(?is)sort:([\d+]+)')

            return ret_dict
        else:
            return None

    @gen.coroutine
    @authentication()
    def get(self, *args, **kwargs):
        self.data['search'] = True
        self.data['title'] = "لیست کاربران"
        # if args:
        #     print self.check_parameters(args[0])
        self.data['subsystems'] = []
        if self.current_plan_id == 1:
            sys = SysSystem().get_all_sub_system(self.current_system)
            if len(sys) > 0:
                sys.insert(0, dict(
                    name="کاربران همین سیستم",
                    id="all"
                ))
                self.data['subsystems'] = sys
        self.data['roles'] = SysRoles(system=self.current_system).get_all()
        self.data['users'] = SysUsers(system=self.current_system).get_all()
        self.data['help_id'] = "8"
        self.render('base/system/users_management/users_list.html', **self.data)

    @gen.coroutine
    @authentication()
    def put(self, *args, **kwargs):

        method = self.get_argument("method", "get")
        if method == "get":
            sys_id = self.get_argument("sys_id", "all")
            if sys_id == "all":
                sys_id = self.current_system
            data = SysUsers.is_exist(user_id=self.get_argument("user", None), system=sys_id)
            self.finish(
                {
                    "data": data,
                    "status": True if data else False
                }
            )
        elif method == "delete":
            _id = self.get_argument("user", None)
            sys_id = self.get_argument("sys_id", "all")
            if sys_id == "all":
                sys_id = self.current_system
            try:
                _id = int(_id)
            except:
                _id = None
            # self.data['full_system']['admin_username'] ==
            if _id:
                if _id != self.current_user:
                    if self.current_plan_id == 1:
                        a_u = SysUsers().get_admin_id_system(sys_id)
                    else:
                        a_u = SysUsers.is_exist(
                            system=sys_id,
                            user_name=self.data['full_system']['admin_username']
                        )
                    if a_u and a_u['id'] != _id:
                        if SysUsers(_id=_id, system=sys_id).delete_user():
                            self.finish({"status": True})
                        else:
                            self.finish({"status": False})
                    else:
                        self.finish({"status": False})
                else:
                    self.finish({"status": False})
            else:
                self.finish({"status": False})

        elif method == "save":
            u = dict()
            self.check_sent_value("user", u, "_id", "کاربر مورد نظر یافت نشد.")
            if not self.errors:
                self.check_sent_value("fn", u, "first_name", "نام را وارد کنید.")
                self.check_sent_value("ln", u, "last_name", "نام خانوادگی را وارد کنید.")
                self.check_sent_value("username", u, "username", "نام کاربری را وارد کنید.")

                if not self.errors:
                    p = self.get_argument("pass", '')
                    cp = self.get_argument("cpass", '')
                    if p != '':
                        if cp != '':
                            if p == cp:
                                u['password'] = LoginMethod.mk_pass(p)
                            else:
                                self.errors.append("رمز عبور و تکرار آن مطابقت ندارند.")
                        else:
                            self.errors.append("تکرار رمز عبور را وارد کنید.")

                if not self.errors:
                    sys_id = self.get_argument("sys_id", "all")
                    if sys_id == "all":
                        sys_id = self.current_system
                    _user = SysUsers.is_exist(user_id=u['_id'], system=sys_id)
                    if _user:
                        if _user['name'] != u['username']:
                            if SysUsers.is_exist(user_name=u['username'], system=sys_id):
                                self.errors.append("این نام کاربری قبلاً ثبت شده است.")

                    if not self.errors:
                        u['system'] = sys_id
                        if SysUsers(**u).update_user():
                            self.finish({"status": True, "errors": []})
                        else:
                            self.finish({"status": False, "errors": ['خطا در ثبت اطلاعات. مجدداً تلاش نمایید.']})
                    else:
                        self.finish({"status": False, "errors": self.errors})
                else:
                    self.finish({"status": False, "errors": self.errors})
        else:
            self.finish({"status": False})

    @gen.coroutine
    @authentication()
    def post(self, *args, **kwargs):
        self.data['search'] = True
        dt = dict()

        def chk(val, default):
            z = self.get_argument(val, default)
            if z:
                if z != '':
                    dt[val] = z
                else:
                    dt[val] = None
            else:
                dt[val] = None

        chk("page", 1)
        chk("fn", None)
        chk("ln", None)
        chk("username", None)
        chk("role", "all")
        chk("sort", "asc")
        chk("subsystem", "all")
        if dt['sort'] == "asc":
            dt['sort'] = False
        else:
            dt['sort'] = True

        if dt['page']:
            try:
                dt['page'] = int(dt['page'])
            except:
                dt['page'] = 1

        if dt['subsystem'] == "all":
            dt['subsystem'] = self.current_system
        data = SysUsers(first_name=dt['fn'], last_name=dt['ln'], username=dt['username'], system=dt['subsystem'])
        if dt['role'] == "all":
            data = data.get_all(dt['page'], desc=dt['sort'])
        else:
            data = data.get_all_by_role(dt['role'], dt['page'], desc=dt['sort'])

        self.finish(
            {
                "data": data,
                "status": True if data else False,
                "more": True if len(data) == 15 else False
            }
        )


class GetRolsHandler(WebBaseHandler):
    @gen.coroutine
    # @authentication()
    def post(self):
        status = False
        try:
            ls_r = []
            _id = self.get_argument("pid", "")
            if _id == "all":
                _id = self.current_system
            roles = SysRoles(system=_id).get_all()
            users = SysUsers(system=_id).get_all()
            ls_r = [dict(
                id="all",
                name="تمام گروه های کاربری"
            )]
            for i in roles:
                ls_r.append(i)
            status = True
            self.write({
                'status': status,
                'sys_roles': ls_r,
                'sys_users': users,
                # "more": True if len(users) == 15 else False
            })
        except Exception, e:
            self.write({'status': status})


class SystemManageUserGuestHandler(WebBaseHandler):
    @gen.coroutine
    @authentication()
    def get(self):

        self.data['guest_users'] = SysUsers(system=self.current_system, username="guest").get_guest_users()
        ls_s = [dict(id=0, parent="#", text="همه  ", icon='fa fa-comment-o colorBlue')]

        ls_s.append(dict(id=self.current_system, parent=0, text="سامانه اصلی", icon='fa fa-comment-o colorBlue'))

        x = SysSystem().get_all_sub_system(self.current_system)
        for i in x:
            ls_s.append(
                dict(
                    id=i['id'],
                    parent=0,
                    text=i['name'],
                    icon='fa fa-comment-o colorBlue'
                )
            )
        ls_s = json.dumps(ls_s)
        self.data['js_tree'] = ls_s
        self.render('base/system/manage_guest_user/manage_guest_user.html', **self.data)

    @gen.coroutine
    @authentication()
    def post(self):
        guest_name = self.get_argument("guest_name", None)
        subsystems = json.loads(self.get_argument("subsystems", '[]'))
        if guest_name and subsystems:
            rand = random.randint(1, 10000)
            g_user = "guest" + str(rand)
            g_pass = LoginMethod.mk_pass(g_user)
            user = SysUsers(system=self.current_system, username=g_user, password=g_pass, first_name=guest_name,
                            last_name="").add_user()
            for i in subsystems:
                if int(i) != 0:
                    guest_role_id = SysRoles(system=i).get_guest_role_id()
                    SysUserRoles.add_user_roles2(user_id=user, roles=[guest_role_id])
            self.set_flash("msg", "اطلاعات با موفقیت ثبت شد.")
        else:
            self.add_error("خطا در ثبت اطلاعات.")
        self.redirect(self.reverse_url("system_manage_user_guest"))

    @gen.coroutine
    @authentication()
    def put(self):
        id = self.get_argument("cid", None)
        if id:
            SysUsers(_id=id, system=self.current_system).delete_user()
            self.write({"status": True})
        else:
            self.write({"status": False})
