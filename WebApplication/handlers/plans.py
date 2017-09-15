#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from tornado.web import HTTPError
from WebApplication.classes.MailClass import R_Mail
from WebApplication.classes.functions import upload_photo
from WebApplication.db_models.models.login import LoginMethod

from WebApplication.handlers.base import *


def chk():
    def f(func):
        @functools.wraps(func)
        def func_wrapper(self, _id, step):
            if self.get_current_user() is not None:
                self.redirect(self.reverse_url('index'))
                return

            if _id:
                try:
                    _id = int(_id)
                except:
                    self.redirect(self.reverse_url("index"))
                    return

                p = SysPlans(_id=_id).get_one()
                if not p:
                    self.redirect(self.reverse_url("index"))
                    return

                self.data['plan'] = p

            else:
                self.redirect(self.reverse_url("index"))
                return

            return func(self, _id, step)

        return func_wrapper

    return f


class PlansHandler(WebBaseHandler):
    @gen.coroutine
    @chk()
    def get(self, _id, step):

        if step is None or step == "Step1":
            self.data['title'] = "ثبت سفارش جدید - مرحله اول"
            self.data['province'] = SysProvince.get_all()

            self.render('base/auth/signup.html', **self.data)

        if step == "Step2":
            self.data['title'] = "ثبت سفارش جدید - مرحله دوم"
            self.data['grade'] = []
            self.render('base/auth/signup_complete.html', **self.data)

        if step == "Step3":
            self.data['title'] = "ثبت سفارش جدید - مرحله سوم"
            self.data['visitor'] = False
            self.render('base/auth/signup_finish.html', **self.data)

    @gen.coroutine
    @chk()
    def post(self, _id, step):
        if step == "Step2":
            _data = {
                "plan": self.data['plan'],
                "username": self.get_argument("user_name", None),
                "password": self.get_argument("pass", None),
                "ip": self.request.remote_ip,
                "province": self.get_argument("user_province", None),
                "city": self.get_argument("user_city", None),
                "visitor_id": self.get_argument("visitor", None)
            }
            # print self.data['plan']
            # return
            if not _data['username'] or not _data['password'] or not _data['province'] or not _data['city']:
                self.set_flash("msg", "تمامی اطلاعات لازم را به درستی وارد کنید.")
                self.redirect(self.reverse_url('plans_order_by_step', self.data['plan']['id'], "Step1"))
                return


            self.session.set('pre_register', _data)
            self.set_flash("msg", "لطفاً اطلاعات تکمیلی خود را وارد کنید.")

            self.redirect(self.reverse_url('plans_order_by_step', self.data['plan']['id'], "Step2"))

        if step == "Step3":
            u1 = self.session.get("pre_register")
            # status = Users.get_status(id=self.get_current_user())
            # if status == 0 and u:
            self.session.delete("pre_register")
            if u1:

                u2 = {
                    "first_name": self.get_argument("fname", None),
                    "last_name": self.get_argument("lname", None),
                    "phone": self.get_argument("phone", None),
                    "school_name": self.get_argument("school_name", None),
                    "address": self.get_argument("address", None),
                    "grade": self.get_argument("level", None),
                    "email": self.get_argument("email", None)
                }

                for i in u2:
                    if not u2[i]:
                        self.add_error("تمامی موارد را کامل کنید.")
                        self.redirect(self.reverse_url('plans_order_by_step', self.data['plan']['id'], "Step2"))
                        return

                pic = upload_photo(self, name="pic", folder="logos")
                u2['pic'] = pic if pic else "new.jpg"

                if u1 and u2:

                    have_visitor = True if u1['visitor_id'] else False
                    _sys = SysSystem(
                        _pname=u2['school_name'],
                        pic=u2['pic'],
                        color="#63A0DD",
                        address=u2['address'],
                        admin_username=u1['username'],
                        province=u1['province'],
                        city=u1['city'],
                        tel=u2['phone'],
                        grade=u2['grade'],
                        status="indebted",
                        confirmed="yes" if have_visitor else "no",
                        _email=u2['email'],
                        visitor_id=u1['visitor_id'] if have_visitor else None
                    ).add_system()

                    if _sys:
                        _u = SysUsers(
                            system=_sys,
                            username=u1['username'],
                            password=LoginMethod.mk_pass(u1["password"]),
                            first_name=u2['first_name'],
                            last_name=u2['last_name']
                        ).add_user()
                        if _u:

                            if SysSystemPlans(system=_sys, plan=u1['plan']['id']).insert():

                                admin_role_id = SysRoles(system=_sys).add_new_system_role()
                                if admin_role_id:
                                    SysUserRoles.add_user_roles(_u, [admin_role_id])

                                    pr = SysPlanPermissions(plan=u1['plan']['id']).get_all_perms_by_plan()
                                    if SysPermissions(
                                            system=_sys,
                                            user=_u
                                    ).add_user_permission([i['name'] for i in pr]):
                                        if SysSystemPlanFeatures(system=_sys).copy_plan_features(u1['plan']['id']):



                                            self.add_default_news(_sys, _u)
                                            active_code = str(random.randint(100000000000, 999999999999) * random.randrange(100000, 999999))[4:13]
                                            is_exist = SysEmailActive(_active_code=active_code).is_exist()
                                            while is_exist:
                                                active_code = str(random.randint(100000000000, 999999999999) * random.randrange(100000, 999999))[4:13]
                                                is_exist = SysEmailActive(_active_code=active_code).is_exist()

                                            # print active_code

                                            email = SysEmailActive(_system_id=_sys,_active_code=active_code).insert()
                                            if email:
                                                try:
                                                    x = R_Mail(from_address='admin@bamadrese.ir',
                                                           from_name='BaMadrese :)',
                                                           subject='Active Profile',
                                                           tag_list=['?'],
                                                           to=[{'email': u2['email'], 'name': u2['first_name'],
                                                                'type': 'to'}])
                                                    x.render_html(template_name='active_mail.html',active_code=active_code)
                                                    x.send()
                                                except:
                                                    try:
                                                        x = R_Mail(from_address='admin@bamadrese.ir',
                                                               from_name='BaMadrese :)',
                                                               subject='Active Profile',
                                                               tag_list=['?'],
                                                               to=[{'email': u2['email'], 'name': u2['first_name'],
                                                                    'type': 'to'}])
                                                        x.render_html(template_name='active_mail.html',active_code=active_code)
                                                        x.send()
                                                    except:
                                                        pass

                                            if have_visitor:

                                                l = LoginMethod(u1['username'], u1['password'], _sys, self)
                                                if l.check():

                                                    if ("ADMIN" in l.user_roles) or ("EDITOR" in l.user_roles):
                                                        self.session.set("current_system",
                                                                         l.user_object['system']['id'])
                                                        self.session.set("current_plan", SysSystemPlans(
                                                            system=l.user_object['system']['id']).get_one())
                                                        self.session.set("full_current_system", l.user_object['system'])
                                                        self.session.set("current_system_name",
                                                                         l.user_object['system']['name'])
                                                        self.session.set("current_user", l.user_object['id'])
                                                        self.session.set("full_current_user", l.user_object)
                                                        self.session.set('user_roles', l.user_roles)
                                                        self.session.set('user_permissions', l.user_permissions)
                                                        self.session.set('sidebar_menu', l.sidebar_menu)

                                            self.data['visitor'] = have_visitor
                                            self.data['title'] = "ثبت سفارش جدید - مرحله سوم"
                                            self.render('base/auth/signup_finish.html', **self.data)

                                            return

                                        else:
                                            self.set_flash(
                                                "msg",
                                                "متاسفانه خطایی در مراحل ثبت نام رخ داده است. مجدداً تلاش نمایید."
                                            )
                                    else:
                                        self.set_flash(
                                            "msg",
                                            "متاسفانه خطایی در مراحل ثبت نام رخ داده است. مجدداً تلاش نمایید."
                                        )

                                else:
                                    self.set_flash(
                                        "msg",
                                        "متاسفانه خطایی در مراحل ثبت نام رخ داده است. مجدداً تلاش نمایید."
                                    )
                            else:
                                self.set_flash(
                                    "msg",
                                    "متاسفانه خطایی در مراحل ثبت نام رخ داده است. مجدداً تلاش نمایید."
                                )
                        else:
                            self.set_flash("msg", "متاسفانه خطایی در مراحل ثبت نام رخ داده است. مجدداً تلاش نمایید.")
                    else:
                        self.set_flash("msg", "متاسفانه خطایی در مراحل ثبت نام رخ داده است. مجدداً تلاش نمایید.")
                else:
                    self.set_flash("msg", "اطلاعات ارسالی نادرست است.")
            else:
                self.set_flash("msg", "اطلاعات ارسالی نادرست است.")

            self.session.delete("pre_register")

            self.redirect(self.reverse_url('plans_order_by_step', self.data['plan']['id'], "Step1"))

    def add_default_news(self, sys, user_id):
        d = SysCollections(system=sys).add_default_collections()
        if d:
            nid = SysNews(
                _user=user_id,
                system=sys,
                title=u"جشنواره بین المللی رباتیک و هوش مصنوعی دانشگاه امیرکبیر",
                text=u"پیش ثبت‌نام جشنواره بین‌المللی رباتیک و هوش مصنوعی امیرکبیر با شعار «ربات‌ها در خدمت صنایع» از 24 مرداد ماه آغاز شده است و تا 16 شهریور ماه ادامه دارد.",
                _type=SysNews.TypeNews,
                public=1,
                status=SysNews.Published
            ).add_news()
            SysNewsCollections(news=nid, collection=d['c1']).add_one()

            nid = SysNews(
                _user=user_id,
                system=sys,
                title=u"چگونه فرزندانمان را با شخصیت تربیت کنیم؟",
                text=u'''اگر بَرآنید تا فرزندی پاک، مؤمن، متشخّص، و متخلّق به اخلاق حسنه داشته باشید، سعی کنید به فرزندانتان “مسئولیت” بدهید، و بعد، از آنان مسئولیت بخواهید، و بدانید که این کار، کودکان را متشخّص بار می آورد. و احساس می کنند، که بقدری مهم و ارزشمند هستند، که به آنان مسئولیت واگذار می گردد. کودکان باید احساس “شخصیت” کنند، کسی که احساس شخصیت می کند با شدتِ تمام، خود را کنترل می کند، و سعی می کند کاری نکند که شخصیت او آسیب بییند، و یا لکه دار شود. وقتی که کودکان، احساس شخصیت نکنند، کم کم بی عار می شوند؛ یعنی “بی تفاوت” می گردند، چه از آنان تعریف کنید یا سرزنش نمایید، در هر دو حالت، بی تفاوت خواهند بود، و بدون هیچ عکس العمل.''',
                _type=SysNews.TypeNews,
                public=1,
                status=SysNews.Published
            ).add_news()
            SysNewsCollections(news=nid, collection=d['c2']).add_one()

            nid = SysNews(
                _user=user_id,
                system=sys,
                title=u"فرزند بهتر، زندگی بهتر",
                text=u"بر اثر یک فرایند اجتماعی عمومی و با شعار «فرزند کمتر، زندگی بهتر»، کودکان امروز با پدیده ای درد آور رو به رو می شوند و آن این واقعیت تلخ است که بخش زیادی از طول روز را به تنهایی در خانه ای بزرگ و با انواع امکانات رفاهی بدون حضور پدر و مادر می گذرانند و در برخی موارد، از این تنهایی به افراد خیالی و ساخته شده در عوالم کودکی خود پناه می برند که البته گاهی این دوست خیالی، دستورات خطرناکی را نیز صادر کرده و مشکلات بسیار جدی و دردناکی به بار می آورد. در هفت سال اول زندگی، که کودکان به دنبال کسب تجربه هستند و اشتیاق بیشتری به فهمیدن و یادگیری دارند، حضور دائمی مادر در کنار آنها از اهمیت ویژه ای برخوردار است. ",
                _type=SysNews.TypeNews,
                public=1,
                status=SysNews.Published
            ).add_news()
            SysNewsCollections(news=nid, collection=d['c2']).add_one()

            nid = SysNews(
                _user=user_id,
                system=sys,
                title=u"وابستگی کودکان به تبلت و گوشی هوشمند؛ چاره چیست؟",
                text=u'''- قدیم‌ترها، بچه‌ها از در و دیوار خانه بالا می‌رفتند و کودکانی که گوشه ای از خانه کز می‌کردند و کاری به کار کسی نداشتند به نظر می‌آمد مریض هستند. بازی و سرگرمی طبیعی‌ترین خصلت کودکان است؛ شاید در سال‌ های اولیه زندگیشان تمایل داشته باشند به تنهایی و با اسباب بازی‌ هایشان بازی کنند اما هر چه که بزرگ‌تر می‌شوند علاقمند به بازی با دوستان و همسالان خود می‌شوند. بگذریم از مزیت‌های بازی‌های گروهی و آموزش‌های ناخودآگاهی که این بازی‌ها در رشد و تقویت خلاقیت و مهارت کودکمان دارد؛ شادابی و نشاط حاصل از باهم بودن بزرگ‌ترین خاصیتی است که جمع‌های کودکان همسال دارد.''',
                _type=SysNews.TypeNews,
                public=1,
                status=SysNews.Published
            ).add_news()
            SysNewsCollections(news=nid, collection=d['c2']).add_one()

            return True
        else:
            return False
