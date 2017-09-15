#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from peewee import *

from shared_connection import SharedConnection

__author__ = 'ReS4'

sh = SharedConnection()

web_db = MySQLDatabase(
    database=sh.web['mysql']['db'],
    host=sh.web['mysql']['host'],
    user=sh.web['mysql']['user'],
    passwd=sh.web['mysql']['password'],
    charset="utf8"
)


class PeeweeBaseModel(Model):
    class Meta:
        database = web_db


class Province(PeeweeBaseModel):
    id = PrimaryKeyField()
    name = CharField()


class City(PeeweeBaseModel):
    id = PrimaryKeyField()
    province = ForeignKeyField(Province, to_field=Province.id)
    name = CharField()


class System(PeeweeBaseModel):
    id = PrimaryKeyField()
    name = CharField(255)
    pname = CharField(255)
    pic = CharField(45)
    color = CharField(10)
    address = CharField(100)
    admin_username = CharField(50)
    tel = CharField(20)
    province = ForeignKeyField(Province, to_field=Province.id)
    city = ForeignKeyField(City, to_field=City.id)
    status = CharField()
    confirmed = CharField()
    email = CharField()
    reg_date = DateTimeField()
    parent_system = ForeignKeyField(db_column='parent_system_id', rel_model='self', to_field='id')


class Roles(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    name = CharField(100)
    title = CharField(100)


class Collections(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    name = CharField(100)
    parent = IntegerField()
    left_node = IntegerField()
    right_node = IntegerField()
    parent_col_p4 = IntegerField()
    coll_img = CharField()


class Collections_roles(PeeweeBaseModel):
    id = PrimaryKeyField()
    status = CharField()
    role = ForeignKeyField(Roles, to_field=Roles.id)
    collection = ForeignKeyField(Collections, to_field=Collections.id)


class Users(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    username = CharField(100)
    password = CharField(50)
    first_name = CharField(100)
    last_name = CharField(255)
    status = CharField()


class User_roles(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    role = ForeignKeyField(Roles, to_field=Roles.id)


class User_collections(PeeweeBaseModel):
    id = PrimaryKeyField()
    device_id = CharField(45)
    user = ForeignKeyField(Users, to_field=Users.id)
    collection = ForeignKeyField(Collections, to_field=Collections.id)


class System_permissions(PeeweeBaseModel):
    name = CharField(100, primary_key=True)
    title = CharField(100)
    handlers = CharField(500)
    url = CharField(100)
    default = IntegerField()
    icon = CharField(45)
    parent = CharField(100)
    perm_order = IntegerField()


class Permissions(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    perm_name = ForeignKeyField(System_permissions, to_field=System_permissions.name, db_column="perm_name")


class Editors_collections(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    collection = ForeignKeyField(Collections, to_field=Collections.id)


class Editors_setting(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    edit_news = CharField(10)
    direct_publish = CharField(10)


class News(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    title = CharField(255)
    text = TextField()
    web_text = TextField()
    _type = CharField()
    public = IntegerField()
    status = CharField()
    date = DateTimeField()
    visit = IntegerField()
    like = IntegerField()
    comment = IntegerField()
    news_site_id = CharField()
    source_news_site = TextField()


class News_admin_p4(PeeweeBaseModel):
    id = PrimaryKeyField()
    news = ForeignKeyField(News, to_field=News.id)
    system = ForeignKeyField(System, to_field=System.id)
    news_admin_id = IntegerField()


class News_collections(PeeweeBaseModel):
    id = PrimaryKeyField()
    news = ForeignKeyField(News, to_field=News.id)
    collection = ForeignKeyField(Collections, to_field=Collections.id)


class News_file(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    news = ForeignKeyField(News, to_field=News.id)
    file_name = CharField(45)
    file_type = CharField(45)
    file_random_name = CharField(45)


class News_link(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    news = ForeignKeyField(News, to_field=News.id)
    link_name = CharField(45)
    link_address = CharField(150)
    random_id = IntegerField()


class News_pic(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    news = ForeignKeyField(News, to_field=News.id)
    pic_name = CharField(45)


class News_comments(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    news = ForeignKeyField(News, to_field=News.id)
    text = CharField(150)
    confirmed = CharField()
    date = DateTimeField()


class News_likes(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    news = ForeignKeyField(News, to_field=News.id)
    # confirmed = CharField()
    date = DateTimeField()


class News_visit(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    news = ForeignKeyField(News, to_field=News.id)
    date = DateTimeField()


class News_favorite(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    news = ForeignKeyField(News, to_field=News.id)
    date = DateTimeField()


class Manager(PeeweeBaseModel):
    id = PrimaryKeyField()
    username = CharField()
    passwd = CharField()
    first_name = CharField()
    last_name = CharField()


class Tags(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    name = CharField(45)
    date = DateTimeField()


class News_tag(PeeweeBaseModel):
    id = PrimaryKeyField()
    news = ForeignKeyField(News, to_field=News.id)
    tag = ForeignKeyField(Tags, to_field=Tags.id)


class Gcm_users(PeeweeBaseModel):
    id = PrimaryKeyField()
    gcm_regid = TextField()
    user = ForeignKeyField(Users, to_field=Users.id)
    system = ForeignKeyField(System, to_field=System.id)
    device_id = CharField(50)
    created_at = DateTimeField()
    notification_enabled = IntegerField()


class System_log(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = IntegerField()
    request_type = CharField()
    device_id = CharField(45)
    handler = CharField(100)
    link = CharField(255)
    ip = CharField(255)
    user_agent = CharField(255)
    date = DateTimeField()


class Plans(PeeweeBaseModel):
    id = PrimaryKeyField()
    plan_name = CharField(100)
    plan_type = CharField()
    price = CharField()


class System_plans(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    plan = ForeignKeyField(Plans, to_field=Plans.id)


class Plan_permissions(PeeweeBaseModel):
    id = PrimaryKeyField()
    plan = ForeignKeyField(Plans, to_field=Plans.id)
    permission = ForeignKeyField(System_permissions, to_field=System_permissions.name)


class Plan_features(PeeweeBaseModel):
    id = PrimaryKeyField()
    plan = ForeignKeyField(Plans, to_field=Plans.id)
    max_users = IntegerField()
    active_days = IntegerField()
    sub_system = IntegerField()


class System_plan_features(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    max_users = IntegerField()
    active_days = IntegerField()
    sub_system = IntegerField()


class Suggestions(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    system = ForeignKeyField(System, to_field=System.id)
    text = CharField(500)
    date = DateTimeField()
    status = CharField()
    read_by = CharField()


class Messages(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    user = ForeignKeyField(Users, to_field=Users.id)
    text = TextField()
    date = DateTimeField()
    status = CharField()
    msg_type = CharField()
    type = CharField()


class Poll_question(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    question = TextField()
    date = DateTimeField()
    status = CharField()
    parent_question = IntegerField()


class Poll_item(PeeweeBaseModel):
    id = PrimaryKeyField()
    question = ForeignKeyField(Poll_question, to_field=Poll_question.id)
    item = CharField()


class Poll_answer(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    question = ForeignKeyField(Poll_question, to_field=Poll_question.id)
    item = ForeignKeyField(Poll_item, to_field=Poll_item.id)
    date = DateTimeField()


class Tickets(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    topic = TextField()
    status = TextField()
    priority = TextField()
    last_update = DateTimeField()


class Subticket(PeeweeBaseModel):
    id = PrimaryKeyField()
    users = ForeignKeyField(Users, to_field=Users.id)
    tickets = ForeignKeyField(Tickets, to_field=Tickets.id)
    text = TextField()
    file = CharField()
    date = DateTimeField()
    type = CharField()


class Sub_domain(PeeweeBaseModel):
    id = PrimaryKeyField()
    site_id = CharField()
    sub_domain = CharField()


class Notification_by_type(PeeweeBaseModel):
    id = PrimaryKeyField()
    _type = CharField()
    name = CharField()
    status = CharField()


class Forum(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    system = ForeignKeyField(System, to_field=System.id)
    name = CharField()
    icon = CharField()
    date = DateTimeField()
    status = CharField()
    condition = CharField()


class Forum_topic(PeeweeBaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, to_field=Users.id)
    forum = ForeignKeyField(Forum, to_field=Forum.id)
    system = ForeignKeyField(System, to_field=System.id)
    name = CharField()
    date = DateTimeField()
    status = TextField()
    condition = CharField()


class Forum_post(PeeweeBaseModel):
    id = PrimaryKeyField()
    text = CharField()
    date = DateTimeField()
    confirm = TextField()
    user = ForeignKeyField(Users, to_field=Users.id)
    forum_topic = ForeignKeyField(Forum_topic, to_field=Forum_topic.id)
    system = ForeignKeyField(System, to_field=System.id)


class Forum_tag(PeeweeBaseModel):
    id = PrimaryKeyField()
    system = ForeignKeyField(System, to_field=System.id)
    name = CharField()


class Forum_topic_tag(PeeweeBaseModel):
    id = PrimaryKeyField()
    forum_tag = ForeignKeyField(Forum_tag, to_field=Forum_tag.id)
    forum_topic_tag = ForeignKeyField(Forum_topic, to_field=Forum_tag.id)
