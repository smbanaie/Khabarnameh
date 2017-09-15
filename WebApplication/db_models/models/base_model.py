#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
import time
from WebApplication.classes.functions import strip_tags, to_jalali, to_time
from WebApplication.db_models.table_models import *


class SysProvince:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_all():
        try:
            p = Province().select().execute()
            ls = []
            for i in p:
                ls.append(
                    dict(
                        id=i.id,
                        name=i.name
                    )
                )

            return ls
        except:
            return []


class SysCity:
    def __init__(self, province_id=None):
        self.province_id = province_id

    def get_all(self):
        try:
            p = City().select().where(City.province == self.province_id)

            ls = []
            for i in p:
                ls.append(
                    dict(
                        id=i.id,
                        name=i.name
                    )
                )

            return ls
        except Exception, e:
            print("city get_all", e)
            return []


class SysSystem(System):
    def __init__(self, _id=None, _email=None, _name=None,
                 _pname=None, pic=None,
                 color=None, address=None,
                 admin_username=None,
                 parent_system=None,
                 province=None, city=None, tel=None, status=None, confirmed=None,
                 reg_date=None, *args, **kwargs):
        super(SysSystem, self).__init__(*args, **kwargs)

        self.id = _id
        self.name = _name
        self.pname = _pname
        self.pic = pic
        self.color = color
        self.address = address
        self.admin_username = admin_username
        self.province = province
        self.city = city
        self.tel = tel
        self.status = status
        self.confirmed = confirmed
        self.reg_date = reg_date
        self.email = _email
        self.parent_system = parent_system

    def get_children(self):
        try:
            x = System.select().where(System.parent_system == self.id)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        child_id=i.id
                    )
                )
            return ls
        except Exception, e:
            return []

    def add_system(self):
        try:
            d = dict(
                name=self.name,
                pname=self.pname,
                pic=self.pic,
                color=self.color,
                address=self.address,
                admin_username=self.admin_username,
                province=self.province,
                city=self.city,
                tel=self.tel,
                status=self.status,
                confirmed=self.confirmed,
                email=self.email
            )
            try:
                if self.parent_system:
                    d['parent_system'] = self.parent_system
            except Exception, e:
                pass
            r = System().insert(**d).execute()
            if r:
                return r
            else:
                return False

        except Exception, e:
            return False

    def update_system(self):
        try:
            r = System().update(
                name=self.name,
                pname=self.pname,
                pic=self.pic,
                color=self.color,
                address=self.address,
                province=self.province,
                city=self.city,
                tel=self.tel,
                status=self.status,
                confirmed=self.confirmed,
                email=self.email,
                admin_username=self.admin_username,
            ).where(System.id == self.id, System.parent_system == self.parent_system).execute()
            return r
        except Exception, e:
            print e
            return False

    def update_system1(self, confirmed):
        try:
            System().update(confirmed=confirmed). \
                where(System.id == self.id).execute()
            return True
        except Exception, e:
            return {}

    @staticmethod
    def get_all(only_active=False):
        try:
            if only_active:
                r = System().select().where((System.confirmed == "yes") & (System.parent_system == None))
                # r = System().select().where((System.confirmed == "yes"))
            else:
                r = System().select()
            ls = []
            for i in r:
                ls.append(
                    dict(
                        id=i.id,
                        name=i.name,
                        pname=i.pname,
                        pic=i.pic,
                        color=i.color,
                        address=i.address,
                        admin_username=i.admin_username,
                        province=dict(id=i.province.id, name=i.province.name),
                        city=dict(id=i.city.id, name=i.city.name),
                        tel=i.tel,
                        status=i.status,
                        confirmed=i.confirmed,
                        reg_date=to_jalali(i.reg_date, "%C"),
                        email=i.email,
                        bazar_name=i.bazar_name,
                        bazar_link=i.bazar_link,
                        status_mail=i.status_mail
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_all_sub_system(self, parent_id):
        try:
            r = System.select().order_by(System.reg_date.desc()).where(System.parent_system == int(parent_id))
            list_ret = []
            for i in r:
                list_ret.append(dict(id=i.id, name=i.pname, confirmed=i.confirmed, date=to_jalali(i.reg_date, "%C")))
            return list_ret
        except:
            return []

    @staticmethod
    def get_all_deactive():
        try:
            r = System().select().where(System.confirmed == "no")
            ls = []
            for i in r:
                uu = SysUsers.is_exist(system=i.id, user_name=i.admin_username)
                if uu:
                    ls.append(
                        dict(
                            id=i.id,
                            name=i.name,
                            pname=i.pname,
                            pic=i.pic,
                            color=i.color,
                            address=i.address,
                            admin=dict(id=uu['id'], name=u"{} {}".format(uu['first_name'], uu['last_name'])),
                            province=dict(id=i.province.id, name=i.province.name),
                            city=dict(id=i.city.id, name=i.city.name),
                            tel=i.tel,
                            status=i.status,
                            confirmed=i.confirmed,
                            reg_date=to_jalali(i.reg_date, "%C"),
                            email=i.email,
                            bazar_name=i.bazar_name,
                            bazar_link=i.bazar_link,
                            status_mail=i.status_mail
                        )
                    )
            return ls
        except Exception, e:
            return []

    def get_parent(self):
        try:
            ss = System().get(System.id == self.id)
            if ss.parent_system:
                return ss.parent_system
            return False
        except Exception, e:
            return False

    def get_one(self, active_only=False):
        try:
            if active_only:
                r = System().get(System.id == self.id, System.confirmed == "yes")
            else:
                r = System().get(System.id == self.id)

            if r:
                return dict(
                    id=r.id,
                    name=r.name,
                    pname=r.pname,
                    pic=r.pic,
                    color=r.color,
                    address=r.address,
                    admin_username=r.admin_username,
                    province=dict(id=r.province.id, name=r.province.name),
                    city=dict(id=r.city.id, name=r.city.name),
                    tel=r.tel,
                    status=r.status,
                    confirmed=r.confirmed,
                    reg_date=to_jalali(r.reg_date, "%C"),
                    date_obj=r.reg_date,
                    email=r.email
                )
            else:
                return False
        except Exception, e:
            return {}

    def get_all_data_of_one_sub_system(self, sub_id):
        try:
            i = System().get(System.parent_system == self.id, System.id == sub_id)
            return dict(
                id=i.id,
                name=i.name,
                pname=i.pname,
                pic=i.pic,
                address=i.address,
                admin_username=i.admin_username,
                province=dict(id=i.province.id, name=i.province.name),
                city=dict(id=i.city.id, name=i.city.name),
                tel=i.tel,
                reg_date=i.reg_date,
                email=i.email,
            )
        except Exception, e:
            return {}

    def delete_system(self):
        try:
            r = System().delete().where(System.id == self.id).execute()
            return True
        except Exception, e:
            return False

    def check_for_sub_system(self):
        data_ret = []
        try:
            parent_system = System.select(System.id, System.pname, System.pic).where(
                (System.parent_system == int(self.id)) & (System.confirmed == "yes")).naive()
            for i in parent_system:
                data_ret.append({'name': i.pname, 'img': i.pic, 'id': i.id})
            if (len(data_ret) != 0):
                return {'status': True, 'data': data_ret}
            return {'status': False, 'data': data_ret}
        except:
            return {'status': False, 'data': data_ret}


class SysRoles(Roles):
    def __init__(self, _id=None, system=None, name=None, title=None, *args, **kwargs):
        super(SysRoles, self).__init__(*args, **kwargs)
        self.id = _id
        self.system = system
        self.name = name
        self.title = title

    def add_role(self):
        return Roles(system=self.system, title=self.title).save()

    def is_exist(self):
        try:
            t = Roles().select().where(Roles.id == self.id, Roles.system == self.system).count()
            if t:
                return True
            else:
                return False
        except:
            return False

    def add_new_system_role(self):
        try:
            u = [
                dict(system=self.system, name="ADMIN", title="مدیریت کل"),
                dict(system=self.system, name="USER", title="کاربر"),
                dict(system=self.system, name="EDITOR", title="ویرایشگر"),
                dict(system=self.system, name="GUEST", title="مهمان")
            ]
            x = Roles().insert_many(u).execute()
            if x:
                return Roles().get(Roles.system == self.system, Roles.name == "ADMIN").id
            else:
                return False
        except:
            return False

    def get_all(self):
        ls = []
        try:
            z = Roles().select().where(Roles.system == self.system)
            for i in z:
                ls.append({
                    "id": i.id,
                    "name": i.title,
                    "role_name": i.name
                })
        except Exception, e:
            pass
        return ls

    def get_js_tree(self, selected_roles=None):
        if not selected_roles:
            selected_roles = []

        tree = [
            {
                'id': "0", 'parent': "#",
                'text': "نقش های سیستم", 'state': {'selected': False}, 'icon': 'fa fa-comments-o'
            }
        ]

        for child in SysRoles(system=self.system).get_all():
            selected = True if child['id'] in selected_roles else False
            tree.append({
                'id': child['id'], 'parent': "0",
                'text': child['name'], 'state': {'selected': selected}, 'icon': 'fa fa-comments-o'
            })
        return json.dumps(tree)

    def get_one(self):
        d = {}
        try:
            z = Roles().get(Roles.id == self.id, Roles.system == self.system)
            d = {
                "id": z.id,
                "name": z.title,
                "role_name": z.name
            }
        except Exception, e:
            pass

        return d

    def get_one_by_name(self):
        d = {}
        try:
            z = Roles().get(Roles.name == self.name, Roles.system == self.system)
            d = {
                "id": z.id,
                "name": z.title,
                "role_name": z.name
            }
        except Exception, e:
            pass

        return d

    def delete_role(self):
        try:
            Roles().delete().where(Roles.id == self.id, Roles.system == self.system).execute()
        except Exception, e:
            pass

    def update_role(self):
        try:
            Roles(id=self.id, title=self.title, system=self.system).save()
        except Exception, e:
            pass

    def get_guest_role_id(self):
        try:
            rr = Roles.get(Roles.system == self.system, Roles.name == "GUEST")
            return rr.id
        except Exception, e:
            print e
            return False


class SysCollections(Collections):
    def __init__(self, _id=None, system=None, name=None, parent=None, left_node=None, parent_col_p4=None,
                 right_node=None, coll_img=None,
                 *args,
                 **kwargs):
        super(SysCollections, self).__init__(*args, **kwargs)
        self.id = _id
        self.system = system
        self.name = name
        self.parent = parent
        self.left_node = left_node
        self.right_node = right_node
        self.parent_col_p4 = parent_col_p4
        self.coll_img = coll_img

    def is_exists(self):
        try:
            i = Collections.get(Collections.id == self.id, Collections.system == self.system)
            return dict(
                id=i.id,
                name=i.name,
                system=i.system,
                parent=i.parent,
                left_node=i.left_node,
                right_node=i.right_node,
            )

        except Exception, e:
            return {}

    def insert_one(self):
        try:
            Collections(system=self.system, name=self.name, parent=self.parent, right_node=0, left_node=0).save()
            return True
        except:
            return False

    def add_collection(self):
        try:
            pr = SysCollections(system=self.system, _id=self.parent).get_one()
            if pr:
                z = Collections.insert(system=self.system, name=self.name, parent=self.parent, right_node=0,
                                       left_node=0, coll_img=self.coll_img,
                                       parent_col_p4=self.parent_col_p4).execute()

                root = Collections().select().where(Collections.parent == None, Collections.system == self.system).get()
                SysCollections.build_tree(root.id, root.left_node, self.system)
                return z
            else:
                return False
        except Exception, e:
            return False

    def add_default_collections(self):
        try:
            z = Collections().insert(
                system=self.system,
                name=u"مجموعه های سیستم",
                parent=None,
                right_node=5,
                left_node=0
            ).execute()
            z1 = Collections().insert(
                system=self.system,
                name=u"اخبار عمومی",
                parent=z,
                right_node=2,
                left_node=1
            ).execute()
            z2 = Collections().insert(
                system=self.system,
                name=u"اطلاعیه",
                parent=z,
                right_node=4,
                left_node=3
            ).execute()

            return dict(cp=z, c1=z1, c2=z2)
        except:
            return {}

    def add_parent_collection(self, sys_parent_id):
        try:
            z = Collections().insert(
                system=self.system,
                name=u"مجموعه های سیستم",
                parent=None,
                right_node=5,
                left_node=0
            ).execute()
            z1 = Collections().insert(
                system=self.system,
                name=u"اخبار عمومی",
                parent=z,
                right_node=2,
                left_node=1
            ).execute()
            z2 = Collections().insert(
                system=self.system,
                name=u"اطلاعیه",
                parent=z,
                right_node=4,
                left_node=3
            ).execute()
            try:
                all_parent_col = Collections.select().where(Collections.system == sys_parent_id)
                for i in all_parent_col:
                    if i.parent:
                        pp = SysCollections(system=self.system, parent_col_p4=i.parent).get_sub_col()
                        if not pp:
                            pp = z
                        Collections().insert(system=self.system, name=i.name, parent=pp, right_node=1, left_node=1,
                                             parent_col_p4=i.id).execute()
            except Exception, e:
                pass
            return dict(cp=z, c1=z1, c2=z2)
        except Exception, e:
            return {}
        pass

    def edit_collection(self):
        try:
            pr = SysCollections(system=self.system, _id=self.parent).get_one()
            if pr:
                z = Collections(
                    id=self.id,
                    name=self.name,
                    parent=self.parent,
                    system=self.system,
                    right_node=0,
                    left_node=0,
                ).save()

                root = Collections().select().where(Collections.parent == None, Collections.system == self.system).get()
                SysCollections.build_tree(root.id, root.left_node, self.system)

                return True
            else:
                return False
        except:
            return False

    def edit_collection_p4(self):
        try:

            Collections.update(name=self.name, coll_img=self.coll_img) \
                .where(Collections.system == self.system, Collections.id == self.id).execute()
            root = Collections().select().where(Collections.parent == None, Collections.system == self.system).get()
            SysCollections.build_tree(root.id, root.left_node, self.system)

            return True
        except Exception, e:
            return False

    def get_id_by_groupid(self):
        try:
            ls = []
            x = Collections.select().where(Collections.system == self.system)
            for i in x:
                ls.append(
                    i.id
                )
            return ls
        except Exception, e:
            return []

    @staticmethod
    def build_tree(parent, left, system):
        right = left + 1
        children = Collections().select().where(Collections.parent == parent, Collections.system == system)
        for child in children:
            right = SysCollections.build_tree(child.id, right, system)

        Collections().update(left_node=left, right_node=right).where(
            Collections.id == parent,
            Collections.system == system,
        ).execute()
        return right + 1

    @staticmethod
    def get_parent(_id=None, system=None):
        try:
            return Collections().select().where(Collections.parent == _id, Collections.system == system).get()
        except Exception, e:

            return None

    def get_rood_id(self):
        try:
            return Collections.get(Collections.system == self.system, Collections.parent == None)
        except Exception, e:
            return None

    def get_sub_col(self):
        try:
            x = Collections.get(Collections.system == self.system, Collections.parent_col_p4 == self.parent_col_p4)
            return x.id

        except Exception, e:
            return None

    def get_parent_col_p4_id(self):
        try:
            i = Collections.get(Collections.id == self.id)
            # print i.parent_col_p4
            return i.parent_col_p4
        except Exception, e:
            return None

    def get_one(self):
        try:
            pr = Collections().select().where(Collections.id == self.id, Collections.system == self.system).get()
            return {
                'id': pr.id,
                'name': pr.name,
                'parent': pr.parent,
                'left_node': pr.left_node,
                'right_node': pr.right_node,
            }
        except Exception, e:
            return {}

    def get_system(self):
        try:
            pr = Collections().get(Collections.id == self.id, Collections.system == self.system)
            if pr:
                return True
            return False
        except Exception, e:
            print e
            return False

    def get_image_id(self):
        try:
            pr = Collections().select().where(Collections.id == self.id).get()
            return pr.coll_img
        except Exception, e:
            return {}

    @staticmethod
    def get_all(system):
        try:
            pr = Collections().select().where(Collections.system == system)
            ls = []
            for i in pr:
                ls.append(
                    {
                        'id': i.id,
                        'name': i.name,
                        'parent': i.parent,
                    }
                )

            return ls
        except Exception, e:
            return []

    # @staticmethod
    def get_children(self):
        try:
            return Collections().select().where(
                Collections.system == self.system,
                Collections.left_node > self.left_node,
                Collections.right_node < self.right_node
            ).execute()
        except:
            return []

    def get_children_id(self):
        try:
            ch = SysCollections.get_children(self)
            ls = []
            for i in ch:
                ls.append(i.id)
            return ls
        except:
            return []

    def delete_collection(self):
        try:
            childs = Collections().select().where(Collections.parent == self.id,
                                                  Collections.system == self.system).count()
            if not childs:
                z = Collections().delete().where(Collections.id == self.id, Collections.system == self.system).execute()
                root = Collections().select().where(Collections.parent == None, Collections.system == self.system).get()
                SysCollections.build_tree(root.id, root.left_node, self.system)

                return True
            else:
                return False
        except:
            return False


class SysCollectionRoles(Collections_roles):
    @staticmethod
    def add_role_collections(role, collections=None):
        if not collections:
            collections = []

        if len(collections):
            row_dicts = ({'collection': col, 'role': role} for col in collections)
            try:
                if SysCollectionRoles.__delete_all_role(role):
                    if Collections_roles().insert_many(row_dicts).execute():
                        return True
                    else:
                        return False
                else:
                    return False
            except:
                return False
        else:
            return False

    @staticmethod
    def change_defualt_collections(role, collections=None):
        try:
            if not collections:
                collections = []
            Collections_roles().update(status="no").where(Collections_roles.role == role).execute()
            Collections_roles().update(status="yes").where(Collections_roles.role == role,
                                                           Collections_roles.collection << collections).execute()
            return True
        except Exception, e:
            print e
            return False

    @staticmethod
    def get_all_ids(role, only_id=False):
        try:
            ls = []
            for i in Collections_roles().select().where(Collections_roles.role == role):
                if not only_id:
                    ls.append(
                        {
                            'id': i.id,
                            'role': i.role.id,
                            'collection_id': i.collection.id,
                            'status': i.status
                        }
                    )
                else:
                    ls.append(int(i.collection.id))
            return ls
        except Exception, e:
            return []

    @staticmethod
    def get_all_ids2(role):
        try:
            ls = []
            for i in Collections_roles().select().where(Collections_roles.role == role):
                if i.status == "yes":
                    ls.append(int(i.collection.id))
            return ls
        except Exception, e:
            return []

    @staticmethod
    def __delete_all_role(role):
        try:
            Collections_roles().delete().where(Collections_roles.role == role).execute()
            return True
        except:
            return False


class SysUsers(Users):
    def __init__(self, _id=None, system=None, username=None, password=None, first_name=None, last_name=None, *args,
                 **kwargs):
        super(SysUsers, self).__init__(*args, **kwargs)

        self.id = _id
        self.system = system
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def get_all_users_subsystem(self):
        try:
            x = Users().select() \
                .join(System, JOIN_INNER, (Users.system == System.id)).where(System.parent_system == self.system)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        first_name=i.first_name,
                        last_name=i.last_name,
                        username=i.username,
                        system=i.system.id,
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_all_for_login(self):
        try:
            ls = []
            x = Users.select().where(Users.username == self.username)
            for i in x:
                ls.append(
                    dict(
                        username=i.username,
                        password=i.password,
                        system=i.system
                    )

                )
            return ls
        except Exception, e:
            return []

    def get_admin_system(self):
        try:
            x = Users().get(Users.system == self.system, Users.username == self.username)
            return dict(id=x.id, f_name=x.first_name, l_name=x.last_name)
        except Exception, e:
            return {}

    def get_admin_id_system(self, system):
        try:
            z = SysSystem(_id=system).get_one()
            return SysUsers(system=system, username=z['admin_username']).get_admin_system()
        except Exception, e:
            return False

    def get_system(self):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system.id)]
            sub_sys.append(self.system.id)
            x = Users().get(Users.id == self.id)
            if x.system.id in sub_sys:
                return x.system.id
            else:
                return False
        except Exception, e:
            print e
            return False

    def _update_user_(self):
        try:
            z = Users().update(
                username=self.username,
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name
            ).where(Users.id == self.id).execute()
            return z
        except Exception, e:
            return {}

    def add_user(self):
        try:
            if not SysUsers.is_exist(user_name=self.username, system=self.system):
                z = Users().insert(
                    system=self.system,
                    username=self.username,
                    password=self.password,
                    first_name=self.first_name,
                    last_name=self.last_name
                ).execute()
                if z:
                    return z
                else:
                    return False
            else:
                return False
        except Exception, e:
            return False

    def is_exist_for_login(self):
        try:
            x = Users().select().where(Users.username == self.username)
            for i in x:
                if i.password == self.password:
                    return True
            return False
        except Exception, e:
            return False

    @staticmethod
    def is_exist(user_id=None, user_name=None, system=None):
        try:
            u = Users.get(((Users.id == user_id) | (Users.username == user_name)) & (Users.system == system))
            if u:
                return {
                    "id": u.id,
                    "system": dict(
                        id=u.system.id,
                        name=u.system.name,
                        pname=u.system.pname,
                        pic=u.system.pic,
                        color=u.system.color,
                        address=u.system.address,
                        admin_username=u.system.admin_username,
                        tel=u.system.tel,
                        status=u.system.status,
                        reg_date=to_jalali(u.system.reg_date, "%C"),
                    ),
                    "name": u.username,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "password": u.password,
                    "status": u.status
                }
        except Exception, e:
            print("system is_exist", e)
            return False

    def get_one(self):
        try:
            return SysUsers.is_exist(self.id, self.username, self.system)
        except Exception, e:
            print("system get_one", e)
            return False

    @staticmethod
    def check_password(user_id=None, system=None, old_pass_hash=None):
        try:
            u = Users().get((Users.id == user_id) & (Users.system == system))
            if u:
                if u.password == old_pass_hash:
                    return True
                else:
                    return False
            else:
                return False
        except Exception, e:
            print("system check_pass", e)
            return False

    def get_all(self, page=1, count=15, desc=False, not_paginate=False):

        # x = dict(
        #     f=string.Template(u"`t1`.`first_name` LIKE '%$q%'").substitute({"q": self.first_name}) if self.first_name is not None else None,
        #     l=u"`t1`.`last_name` LIKE '%{}%'".format(self.last_name) if self.last_name is not None else None,
        #     u=u"`t1`.`username` = '{}'".format(self.username) if self.username is not None else None
        # )
        # z = ur"{} {} {} {} {}".format(
        #     x['f'] if x['f'] else ur"1=1",
        #     ur"OR" if ((x['f'] and x['l']) or (x['f'] and x['u'])) else ur"",
        #     x['l'] if x['l'] else u"",
        #     ur"OR" if (x['l'] and x['u']) else ur"",
        #     x['u'] if x['u'] else ur""
        # )
        # value = {'q': z}
        # sql_template = string.Template(ur'''SELECT
        #         `t1`.`id`,
        #         `t1`.`system_id`,
        #         `t1`.`username`,
        #         `t1`.`password`,
        #         `t1`.`first_name`,
        #         `t1`.`last_name`
        #         FROM `users` AS t1 WHERE $q LIMIT 15 ''')
        #
        # z = sql_template.substitute(value)
        #
        # print(z)
        # us = web_db.execute_sql(z)
        # # us = Users().select().paginate(2, count).where(True,
        # #     SQL(z)
        # # )
        #
        # # us = web_db.execute_sql(
        # #     '''
        # #     SELECT
        # #         `t1`.`id`,
        # #         `t1`.`system_id`,
        # #         `t1`.`username`,
        # #         `t1`.`password`,
        # #         `t1`.`first_name`,
        # #         `t1`.`last_name`
        # #     FROM `users` AS t1 WHERE $q LIMIT 15
        # #     '''
        # # )
        try:
            if not not_paginate:
                if self.username:
                    us = Users().select().order_by(
                        SQL("`t1`.`id` DESC") if desc else SQL("`t1`.`id` ASC")
                    ).paginate(page, count).where(
                        (Users.username.contains(self.username)) & (Users.system == self.system)
                    )
                else:
                    us = Users().select().order_by(
                        SQL("`t1`.`id` DESC") if desc else SQL("`t1`.`id` ASC")
                    ).paginate(page, count).where(Users.system == self.system)
            else:
                if self.username:
                    us = Users().select().order_by(
                        SQL("`t1`.`id` DESC") if desc else SQL("`t1`.`id` ASC")
                    ).where(
                        (Users.username.contains(self.username)) & (Users.system == self.system)
                    )
                else:
                    us = Users().select().order_by(
                        SQL("`t1`.`id` DESC") if desc else SQL("`t1`.`id` ASC")
                    ).where(Users.system == self.system)

            ls = []
            for u in us:
                if "guest" not in u.username:
                    ls.append(
                        {
                            "id": u.id,
                            "username": u.username,
                            "first_name": u.first_name,
                            "last_name": u.last_name,
                            "system": u.system.id,
                            "status": u.status
                        }
                    )

            return ls
        except Exception, e:
            print("system get_all", e)
            return []

    def get_all_by_role(self, role, page=1, count=15, desc=False):
        try:
            if self.username:
                us = Users().select().join(
                    User_roles, JOIN_INNER, on=(Users.id == User_roles.user)
                ).order_by(
                    SQL("`t1`.`id` DESC") if desc else SQL("`t1`.`id` ASC")
                ).paginate(page, count).where(
                    Users.username.contains(self.username) & (User_roles.role == role) & (Users.system == self.system)
                )
            else:
                us = Users().select().join(
                    User_roles, JOIN_INNER, on=(Users.id == User_roles.user)
                ).order_by(
                    SQL("`t1`.`id` DESC") if desc else SQL("`t1`.`id` ASC")
                ).paginate(page, count).where((User_roles.role == role) & (Users.system == self.system))

            ls = []
            for u in us:
                if "guest" not in u.username:
                    ls.append(
                        {"id": u.id, "username": u.username, "first_name": u.first_name, "last_name": u.last_name})

            return ls
        except:
            return []

    def get_guest_users(self):
        try:
            us = Users().select().where((Users.system == self.system) & (Users.username.contains(self.username)))
            g_r = User_roles().select().join(
                Roles, JOIN_INNER, on=(Roles.id == User_roles.role)
            ).where((Roles.name == "GUEST"))
            ls = []

            for u in us:
                sys = []
                for i in g_r:
                    if u.id == i.user.id:
                        sys.append(i.role.system.pname)
                name = u.first_name + u.last_name
                ls.append(
                    {"id": u.id, "first_name": name, "username": u.username, "sys": sys})

            return ls
        except Exception, e:
            print e
            return []

    def get_all_by_collection(self, col_id):
        try:
            # us = Users().select().join(
            #     User_collections, JOIN_INNER, on=(User_collections.user == Users.id)
            # ).where()
            ls = []
            us = User_collections.select().where(User_collections.collection == col_id)
            for u in us:
                ls.append(
                    {
                        #     u.user.id
                        # "id": u.id,
                        "id": u.user.id,
                        "first_name": u.user.first_name,
                        "last_name": u.user.last_name,
                        # "system": u.user.system.id,
                        # "status": u.user.status
                    }
                )
            return ls

        except Exception, e:
            return []

    def delete_user(self):
        try:
            u = Users().delete().where(Users.id == self.id, Users.system == self.system).execute()
            if u:
                return True
            else:
                return False
        except:
            return False

    def update_user(self):
        try:
            if self.password:
                u = Users().update(
                    first_name=self.first_name,
                    last_name=self.last_name,
                    username=self.username,
                    password=self.password
                ).where(Users.id == self.id, Users.system == self.system).execute()
            else:
                u = Users().update(
                    first_name=self.first_name,
                    last_name=self.last_name,
                    username=self.username
                ).where(Users.id == self.id, Users.system == self.system).execute()
            return True
        except Exception, e:
            return False

    def update_password(self):
        try:
            if self.password:
                u = Users().update(
                    password=self.password
                ).where(Users.id == self.id, Users.system == self.system).execute()
            else:
                return False
            return True
        except Exception, e:
            return False

    def count(self):
        m = 0
        try:
            m = Users().select().where(Users.system == self.system).count()
            return m
        except:
            return m


class SysUserCollections:
    def __init__(self, _id=None, user=None, collection=None, device_id=None, *args, **kwargs):
        self.id = _id
        self.user = user
        self.collection = collection
        self.device_id = device_id

    def get_all(self, only_id=False, device_id=None):
        try:
            if device_id:
                r = User_collections().select().where(User_collections.user == self.user,
                                                      User_collections.device_id == device_id)
            else:
                r = User_collections().select().where(User_collections.user == self.user)
            if r:
                if only_id:
                    return [i.collection.id for i in r]
                else:
                    return [
                        {"id": i.id, "collection_id": i.collection.id, "collection_name": i.collection.name} for i in r
                        ]

        except Exception, e:
            return []

    def get_all_(self, device_id=None):
        try:
            cr = User_collections().select().where(User_collections.user == self.user,
                                                   User_collections.device_id == device_id)

            ls = []
            ls2 = []
            ls3 = []
            for cc in cr:
                ls2.append(int(cc.collection.id))
                if cc.collection.parent:
                    ls3.append((int(cc.collection.parent)))
            for i in cr:
                # if i.collection.parent:
                if i.collection.parent in ls2:
                    if i.collection.id in ls3:
                        ls.append(dict(id=i.collection.id, name=i.collection.name, parent=i.collection.parent,
                                       has_child=True))
                    else:
                        ls.append(dict(id=i.collection.id, name=i.collection.name, parent=i.collection.parent,
                                       has_child=False))
                else:
                    if i.collection.id in ls3:
                        ls.append(dict(id=i.collection.id, name=i.collection.name, parent=-1, has_child=True))
                    else:
                        ls.append(dict(id=i.collection.id, name=i.collection.name, parent=-1, has_child=False))
            return ls
        except Exception, e:
            return []

            # def get_all_class(self, only_id=False):
            #     try:
            #         r = User_collections().select().where(User_collections.user == self.user)
            #         ls = []
            #         for i in r:
            #             if i.collection.class_type == 'yes':
            #                 ls.append({
            #                     "collection_id": i.collection.id,
            #                     "collection_name": i.collection.name
            #                 })
            #     except Exception, e:
            #         return []
            #

    def set_user_collections(self, collection, device_id=None):
        try:
            if len(collection):
                if device_id:
                    row_dicts = ({'collection': nm, 'user': self.user, 'device_id': device_id} for nm in collection)
                    try:
                        if SysUserCollections.__delete_all_collection2(self, device_id):
                            if User_collections().insert_many(row_dicts).execute():
                                return True
                            else:
                                return False
                        else:
                            return False
                    except Exception, e:
                        return False
                else:
                    row_dicts = ({'collection': nm, 'user': self.user} for nm in collection)
                    try:
                        if SysUserCollections.__delete_all_collection(self):
                            if User_collections().insert_many(row_dicts).execute():
                                return True
                            else:
                                return False
                        else:
                            return False
                    except Exception, e:
                        return False
            else:
                return False

        except Exception, e:
            return False

    def __delete_all_collection(self):
        try:
            User_collections().delete().where(User_collections.user == self.user).execute()
            return True
        except:
            return False

    def __delete_all_collection2(self, device_id):
        try:
            # User_collections().delete().where(User_collections.user == self.user).execute()
            User_collections().delete().where(User_collections.user == self.user,
                                              User_collections.device_id == device_id).execute()
            return True
        except:
            return False

    def get_all_user_col(self, system):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=system)]
            sub_sys.append(system)
            us = Users().select().join(User_collections, JOIN_INNER, on=(Users.id == User_collections.user)) \
                .order_by(SQL("`t1`.`id` ASC")).where(User_collections.collection == self.id, Users.system << sub_sys)
            ls = []
            for u in us:
                if "guest" not in u.username:
                    ls.append(
                        {
                            "id": u.id,
                            "username": u.username,
                            "first_name": u.first_name,
                            "last_name": u.last_name,
                            "system": u.system.id,
                            "status": u.status
                        }
                    )

            return ls
        except Exception, e:
            print("system get_all", e)
            return []


class SysSubDomain:
    def __init__(self, _id=None, site_id=None, sub_domain=None, *args, **kwargs):
        self.id = _id
        self.site_id = site_id
        self.sub_domain = sub_domain

    def get_all(self):
        try:
            sub_d = []
            ss = Sub_domain().select()
            for i in ss:
                sub_d.append(
                    dict(
                        id=i.id,
                        site_id=i.site_id,
                        sub_domain=i.sub_domain
                    )
                )
            return sub_d
        except Exception, e:
            print e
            return []

    def get_one_sub(self):
        try:
            sub = Sub_domain().get(Sub_domain.site_id == self.site_id)
            if sub:
                return sub.sub_domain
            return False
        except Exception, e:
            print e
            return False

    def add_sub_domain(self):

        return Sub_domain(site_id=self.site_id, sub_domain=self.sub_domain).save()

    def delete_sub(self):
        try:
            if Sub_domain.delete().where(Sub_domain.id == self.id).execute():
                return True
            return False
        except Exception, e:
            print e
            return False

    def update_sub(self):
        try:
            if Sub_domain.update(site_id=self.site_id, sub_domain=self.sub_domain).where(
                            Sub_domain.id == self.id).execute():
                return True
            return False
        except Exception, e:
            print e
            return False


class SysNotificationByType:
    def __init__(self, _id=None, _type=None, name=None, status=None, *args, **kwargs):
        self.id = _id
        self._type = _type
        self.name = name
        self.status = status

    def get_all(self):
        try:
            all_type = []
            ss = Notification_by_type().select()
            for i in ss:
                all_type.append(
                    dict(
                        id=i.id,
                        name=i.name,
                        type=i._type,
                        status=i.status
                    )
                )
            return all_type
        except Exception, e:
            print e
            return []

    def _update(self):
        try:
            Notification_by_type().update(status=self.status).where(Notification_by_type.id == self.id).execute()
            return True
        except Exception, e:
            print e
            return False

    def get_one_status(self):
        try:
            type = Notification_by_type().get(Notification_by_type._type == self._type)
            if type.status == "yes":
                return True
            return False
        except Exception, e:
            print e
            return False


class SysUserRoles(User_roles):
    @staticmethod
    def get_all(user_id, only_id=True):
        try:
            r = User_roles().select().where(User_roles.user == user_id)
            if r:
                if only_id:
                    return [i.role.id for i in r]
                else:
                    return [{"id": i.id, "role_id": i.role.id, "role_name": i.role.name} for i in r]
        except Exception, e:
            return []

    @staticmethod
    def is_editor(user_id):
        try:
            r = User_roles().select().where(User_roles.user == user_id)
            if "EDITOR" in [i['role_name'] for i in SysUserRoles.get_all(user_id, False)]:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def add_user_roles(user_id, roles=None):
        if not roles:
            roles = []

        if len(roles):
            row_dicts = ({'role': r, 'user': user_id} for r in roles)
            try:
                if SysUserRoles.__delete_all_roles(user_id):
                    if User_roles().insert_many(row_dicts).execute():
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception, e:
                return False
        else:
            return False

    @staticmethod
    def add_user_roles2(user_id, roles=None):
        if not roles:
            roles = []
        if len(roles):
            row_dicts = ({'role': r, 'user': user_id} for r in roles)
            try:
                User_roles().insert_many(row_dicts).execute()
            except Exception, e:
                return False
        else:
            return False

    @staticmethod
    def __delete_all_roles(user_id):
        try:
            User_roles().delete().where(User_roles.user == user_id).execute()
            return True
        except:
            return False

    @staticmethod
    def add_user_roles_2(user_id, roles=None, sys_id=None):
        if not roles:
            roles = []

        if len(roles):
            row_dicts = ({'role': r, 'user': user_id} for r in roles)
            try:
                if SysUserRoles.__delete_all_roles_2(user_id, sys_id):
                    if User_roles().insert_many(row_dicts).execute():
                        c = []
                        for i in roles:
                            k = SysCollectionRoles().get_all_ids(i)
                            for j in k:
                                if j['collection_id'] not in c:
                                    c.append(j['collection_id'])
                            SysUserCollections(user=user_id).set_user_collections(c)
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception, e:
                return False
        else:
            return False

    @staticmethod
    def __delete_all_roles_2(user_id, sys_id):
        try:
            x = User_roles().select().join(Roles, JOIN_INNER, on=(User_roles.role == Roles.id)).where(
                User_roles.user == user_id, Roles.system == sys_id).execute()
            for i in x:
                User_roles().delete().where(User_roles.id == i.id).execute()
            return True
        except Exception, e:
            return False


class SysEditorsCollections(Editors_collections):
    @staticmethod
    def get_all(user_id, only_id=True):
        try:
            r = Editors_collections().select().where(Editors_collections.user == user_id)
            if r:
                if only_id:
                    return [i.collection.id for i in r]
                else:
                    return [
                        {"id": i.id, "role_id": i.collection.id, "collection_name": i.collection.name}
                        for i in r
                        ]
        except Exception, e:
            return []

    @staticmethod
    def add_editors_collection(user_id, collection=None):
        if not collection:
            collection = []

        row_dicts = [{'collection': c, 'user': user_id} for c in collection]
        try:
            if SysEditorsCollections.__delete_all_editors_collection(user_id):
                if row_dicts:
                    if Editors_collections().insert_many(row_dicts).execute():
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        except Exception, e:
            return False

    @staticmethod
    def __delete_all_editors_collection(user_id):
        try:
            Editors_collections().delete().where(Editors_collections.user == user_id).execute()
            return True
        except:
            return False


class SysEditorsSetting(Editors_setting):
    All = "ALL"
    Own = "OWN"
    Disable = "DISABLE"

    Yes = "YES"
    No = "NO"

    def __init__(self, _id=None, user=None, edit_news=None, direct_publish=None, *args, **kwargs):
        super(SysEditorsSetting, self).__init__(*args, **kwargs)

        self.id = _id
        self.user = user
        self.edit_news = edit_news
        self.direct_publish = direct_publish

    def add_setting(self):
        try:
            z = Editors_setting(user=self.user, edit_news=self.edit_news, direct_publish=self.direct_publish).save()
            if z:
                return True
        except:
            return False

    def get_one(self):
        try:
            e = Editors_setting().get(Editors_setting.user == self.user)
            if e:
                return dict(edit_news=e.edit_news.lower(), direct_publish=e.direct_publish.lower())
        except:
            return {}

    def update_setting(self):
        try:
            z = Editors_setting().update(edit_news=self.edit_news, direct_publish=self.direct_publish).where(
                Editors_setting.user == self.user
            ).execute()
            if z:
                return True
        except:
            return False

    def delete_setting(self):
        try:
            z = Editors_setting().delete().where(
                Editors_setting.user == self.user
            ).execute()
            if z:
                return True
        except:
            return False


class SysNews(News):
    Published = "PUBLISHED"
    Draft = "DRAFT"
    Disabled = "DISABLED"

    TypeNews = "news"
    TypeNotification = "notification"
    TypeGallery = "gallery"
    TypeInstant = "instant"
    TypeImportant = "important"
    TypeFavorite = "favorite"

    def __init__(self, _id=None, _user=None, system=None, title=None, text=None, _type=None, public=None,
                 status=None, visit=None, like=None, comment=None, news_site_id=None, source_news_site=None,
                 *args, **kwargs):
        super(SysNews, self).__init__(*args, **kwargs)
        self.system = system
        self.id = _id
        self.user = _user
        self.title = title
        self.text = text
        self._type = _type
        self.status = status
        self.public = public
        self.visit = visit
        self.like = like
        self.comment = comment
        self.news_site_id = news_site_id
        self.source_news_site = source_news_site

        self.__exp = True

    def add_news(self):
        try:
            x = News().insert(
                system=self.system,
                user=self.user,
                title=self.title,
                text=strip_tags(self.text),
                web_text=self.text,
                _type=self._type,
                public=self.public,
                status=self.status,
            ).execute()

            if x:
                return x
            return False
        except Exception, e:
            return False

    def add_news_site(self):
        try:
            x = News().insert(
                system=self.system,
                user=self.user,
                title=self.title,
                text=strip_tags(self.text),
                web_text=strip_tags(self.text),
                _type=self._type,
                public=self.public,
                status=self.status,
                news_site_id=self.news_site_id,
                source_news_site=self.source_news_site
            ).execute()

            if x:
                return x
            return False
        except Exception, e:
            print e, "      add_news_site"
            return False

    def update_news(self):
        try:
            d = dict(
                title=self.title,
                text=strip_tags(self.text),
                web_text=self.text,
                _type=self._type,
                public=self.public,
                status=self.status
            )
            x = News().update(**d).where(News.id == self.id).execute()

            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def update_status_news(self):
        try:
            x = News().update(
                status=self.status
            ).where(News.id == self.id).execute()

            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def get_news(self, page=1, count=10, exp=True, collection=None):
        try:
            self.__exp = exp
            ls = []
            if collection:
                x = News().select().join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)) \
                    .order_by(News.date.desc()).where(
                    News.system == self.system,
                    News_collections.collection == collection,
                    News.status == self.status, exp)
            else:
                x = News().select().order_by(News.date.desc()).where(News.system == self.system,
                                                                     News.status == self.status, exp)

            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        title=i.title,
                        text=strip_tags(i.text),
                        web_text=i.text,
                        _type=i._type,
                        public=i.public,
                        status=i.status,
                        date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                        visit=i.visit,
                        like=i.like,
                        comment=i.comment,
                    )
                )
            return ls
        except Exception, e:
            print("get_news", e)
            pass

    def get_news_p4(self, page=1, count=10, exp=True, collection=None):
        try:
            self.__exp = exp
            ls = []
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system.id)]
            sub_sys.append(self.system.id)
            if collection:
                x = News().select().join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)) \
                    .order_by(News.date.desc()).where(
                    News.system << sub_sys,
                    News_collections.collection == collection,
                    News.status == self.status, exp)
            else:
                x = News().select().order_by(News.date.desc()).where(News.system << sub_sys, News.status == self.status,
                                                                     exp)

            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        title=i.title,
                        text=strip_tags(i.text),
                        web_text=i.text,
                        _type=i._type,
                        public=i.public,
                        status=i.status,
                        date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                        visit=i.visit,
                        like=i.like,
                        comment=i.comment,
                    )
                )
            return ls
        except Exception, e:
            print(e)
            pass

    def total_count_p4(self, collection=None):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system.id)]
            sub_sys.append(self.system.id)
            if collection:
                z = News().select().join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)) \
                    .order_by(News.date.desc()).where(
                    News.system << sub_sys,
                    News_collections.collection == collection,
                    News.status == self.status
                ).count()
            else:
                z = News().select() \
                    .order_by(News.date.desc()).where(News.system << sub_sys, News.status == self.status).count()

            if z:
                return z
            return 0
        except Exception, e:
            return 0

    def total_count_search_p4(self, sys_id=None, coll_id=None):
        try:
            # sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system.id)]
            sub_sys = []
            sub_sys.append(sys_id)
            if coll_id:
                z = News().select().join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)) \
                    .order_by(News.date.desc()).where(
                    News.system << sub_sys,
                    News_collections.collection == coll_id,
                    News.status == self.status
                ).count()
            else:
                z = News().select().order_by(News.date.desc()).where(News.system << sub_sys,
                                                                     News.status == self.status).count()
            if z:
                return z
            return 0
        except Exception, e:
            return 0

    def get_news_by_search(self, page=1, count=10, exp=True, collection=None):
        try:
            self.__exp = exp
            ls = []

            m = News().select(
                News.id.alias("news_id"),
                News.user,
                News.title,
                News.text,
                News._type,
                News.public,
                News.status,
                News.date,
                News.visit,
                News.like,
                News.comment,
                Users.id.alias("user_id"),
                Users.first_name,
                Users.last_name
            ).join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)).join(
                Users, JOIN_INNER, on=(Users.id == News.user)
            ).where(
                News.system == self.system,
                News.status == self.status,
                News_collections.collection == collection
            ).naive()
            for i in m:
                ls.append(
                    dict(
                        user=dict(id=i.user_id, name=u"{} {}".format(i.first_name, i.last_name)),
                        id=i.news_id,
                        # user=i.user,
                        title=i.title,
                        text=strip_tags(i.text),
                        web_text=i.text,
                        _type=i._type,
                        public=i.public,
                        status=i.status,
                        date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                        visit=i.visit,
                        like=i.like,
                        comment=i.comment,
                    )
                )
            return ls
        except Exception, e:
            pass

    def get_news_by_search_p4(self, page=1, count=10, exp=True, subsystem=None, collection=None):
        try:
            ls = []
            if subsystem == "all":
                sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system.id)]
                sub_sys.append(self.system.id)
                for i in News().select(
                        News.id.alias("news_id"),
                        News.user,
                        News.title,
                        News.text,
                        News._type,
                        News.public,
                        News.status,
                        News.date,
                        News.visit,
                        News.like,
                        News.comment,
                ).join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)) \
                        .order_by(News.date.desc()).where(
                            News.system << sub_sys,
                            News.status == self.status,
                            News_collections.collection == collection,
                    exp):
                    ls.append(
                        dict(
                            user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                            id=i.news_id,
                            title=i.title,
                            text=strip_tags(i.text),
                            web_text=i.text,
                            _type=i._type,
                            public=i.public,
                            status=i.status,
                            date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                            visit=i.visit,
                            like=i.like,
                            comment=i.comment,
                        )
                    )

            elif collection == "all":
                x = News().select().order_by(News.date.desc()).where(
                    News.system == subsystem,
                    News.status == self.status,
                )
                for i in x:
                    ls.append(
                        dict(
                            id=i.id,
                            user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                            title=i.title,
                            text=strip_tags(i.text),
                            web_text=i.text,
                            _type=i._type,
                            public=i.public,
                            status=i.status,
                            date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                            visit=i.visit,
                            like=i.like,
                            comment=i.comment,
                        )
                    )

            else:
                x = News().select(
                    News.id.alias("news_id"),
                    News.user,
                    News.title,
                    News.text,
                    News._type,
                    News.public,
                    News.status,
                    News.date,
                    News.visit,
                    News.like,
                    News.comment,
                ).join(News_collections, JOIN_INNER, on=(News.id == News_collections.news)) \
                    .order_by(News.date.desc()).where(
                    News.system == subsystem,
                    News.status == self.status,
                    News_collections.collection == collection
                )
                for i in x:
                    ls.append(
                        dict(
                            id=i.news_id,
                            user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                            title=i.title,
                            text=strip_tags(i.text),
                            web_text=i.text,
                            _type=i._type,
                            public=i.public,
                            status=i.status,
                            date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                            visit=i.visit,
                            like=i.like,
                            comment=i.comment,
                        )
                    )
            return ls
        except Exception, e:
            pass

    def get_one_p4(self, exp=True):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system.id)]
            sub_sys.append(self.system.id)
            i = News().get(News.system << sub_sys, News.id == self.id, exp)
            return dict(
                id=i.id,
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                title=i.title,
                system=i.system.id,
                text=strip_tags(i.text),
                web_text=i.web_text,
                _type=i._type,
                public=i.public,
                status=i.status,
                date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S")
            )

        except Exception, e:
            return {}

    def get_by_news_site_id(self):
        try:
            x = News.get(News.system == 1, News.news_site_id == self.news_site_id)
            if x:
                return x
            return False
        except Exception, e:
            return False

    def delete_by_news_site_id(self):
        try:
            News().delete().where(News.news_site_id == self.news_site_id).execute()
            return True
        except Exception, e:
            return False

    def update_by_news_site_id(self):
        try:
            ls_news = News.select().where(News.news_site_id == self.news_site_id)
            ls_news2 = []
            News.update(title=self.title, web_text=strip_tags(self.text), text=strip_tags(self.text),
                        source_news_site=self.source_news_site).where(
                News.news_site_id == self.news_site_id).execute()
            for i in ls_news:
                try:
                    ls_news2.append(dict(news=i.id, _sys=i.system))
                    News_collections.delete().where(News_collections.news == i.id).execute()
                    collections = SysCollections(system=i.system).get_id_by_groupid()
                    # if not collections:
                    #     collections = SysCollections(system=i.system, group_id=183).get_id_by_groupid()
                    SysNewsCollections(news=i.id).add_many(collections)
                except Exception, e:
                    print e, "    update collection news site"
                    pass

            return ls_news2
        except Exception, e:
            print e, "     update_by_news_site_id"
            return []

    def get_one(self, exp=True):
        try:
            i = News().get(News.system == self.system, News.id == self.id, exp)
            return dict(
                id=i.id,
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                title=i.title,
                text=strip_tags(i.text),
                web_text=i.web_text,
                _type=i._type,
                public=i.public,
                status=i.status,
                date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S")
            )
        except Exception, e:
            return {}

    def delete_news(self):
        try:
            i = News().delete().where(News.system == self.system, News.id == self.id).execute()
            if i:
                return True
            else:
                return False
        except Exception, e:
            print("del_news", e)
            return False

    def delete_subnews(self):
        try:
            News().delete().where(News.id == self.id).execute()
            return True
        except Exception, e:
            return False

    def get_count(self, collection=None):
        try:
            # z = News().select().where(News.system == self.system, News.status == self.status, self.__exp).count()
            if collection:
                z = News().select().join(News_collections, JOIN_INNER, on=(News_collections.news == News.id)) \
                    .order_by(News.date.desc()).where(
                    News.system == self.system,
                    News_collections.collection == collection,
                    News.status == self.status
                ).count()
            else:
                z = News().select().order_by(News.date.desc()).where(News.system == self.system,
                                                                     News.status == self.status).count()

            if z:
                return z
            else:
                return 0
        except:
            return 0


class SysNewsCollections(News_collections):
    def __init__(self, _id=None, news=None, collection=None, *args, **kwargs):
        super(SysNewsCollections, self).__init__(*args, **kwargs)

        self.id = _id
        self.news = news
        self.collection = collection

    def add_one(self):
        try:
            x = News_collections(
                news=self.news,
                collection=self.collection
            ).save()
            if x.get_id():
                return x.get_id()
            else:
                return False
        except:
            return False

    def add_many(self, collections=None):
        if not collections:
            collections = []

        if len(collections):
            row_dicts = ({'collection': c, 'news': self.news} for c in collections)
            try:
                if News_collections().insert_many(row_dicts).execute():
                    return True
                else:
                    return False
            except Exception, e:
                return False
        else:
            return False

    def update_many(self, collections=None):
        if not collections:
            collections = []

        if len(collections):
            row_dicts = ({'collection': c, 'news': self.news} for c in collections)
            try:
                try:
                    if self.get_collection_id_by_news():
                        self._delete_collections()
                except Exception, e:
                    pass
                if News_collections().insert_many(row_dicts).execute():
                    return True
                else:
                    return False
                    # else:
                    #     return False
            except Exception, e:
                return False
        else:
            return False

    def get_collection_id_by_news(self):
        try:
            n = News_collections().select().where(News_collections.news == self.news)
            ls = []
            for i in n:
                ls.append(int(i.collection.id))
            return ls
        except:
            return []

    def get_count_by_collection_id(self):
        try:
            n = News_collections().select().where(News_collections.collection == self.collection).count()
            print n
            return n
        except:
            return 0

    def _delete_collections(self):
        try:
            n = News_collections().delete().where(News_collections.news == self.news).execute()
            if n:
                return True
        except:
            return False


class SysNewsVisit(News_visit):
    def __init__(self, _id=None, system=None, news=None, user=None, date=None, *args, **kwargs):
        super(SysNewsVisit, self).__init__(*args, **kwargs)
        self.id = _id
        self.system = system
        self.news = news
        self.user = user
        self.date = date

    def last_visit(self):
        try:
            ls = []
            x = News_visit().select().order_by(SQL("`date` DESC")).where(News_visit.system == self.system)
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        news_name=i.news.title,
                        user_name=u"{} {}".format(i.user.first_name, i.user.last_name),
                        date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S")
                    )
                )
            return ls
        except Exception, e:
            return []


class SysNewsFile(News_file):
    def __init__(self, _id=None, system=None, news=None, file_name=None, file_type=None, file_random_name=None, *args,
                 **kwargs):
        super(SysNewsFile, self).__init__(*args, **kwargs)
        self.id = _id
        self.system = system
        self.news = news
        self.file_name = file_name
        self.file_type = file_type
        self.file_random_name = file_random_name

    def add_one(self):
        try:
            x = News_file().insert(
                system=self.system,
                news=self.news,
                file_name=self.file_name,
                file_type=self.file_type,
                file_random_name=self.file_random_name
            ).execute()
            if x:
                return x
            else:
                return False
        except:
            return False

    def update_file_name(self):
        try:
            News_file().update(file_name=self.file_name).where(News_file.id == self.id, News_file.system == self.system,
                                                               News_file.news == self.news).execute()
            return True
        except Exception, e:
            pass

    def update_file_name_p4(self):
        try:
            ff = News_file.get(News_file.id == self.id, News_file.system == self.system, News_file.news == self.news)
            News_file().update(file_name=self.file_name).where(
                News_file.file_random_name == ff.file_random_name).execute()
            return True
        except Exception, e:
            pass

    def get_all_dict(self):
        try:
            n = News_file().select().where(News_file.news == self.news, News_file.system == self.system)
            ls = []
            for i in n:
                ls.append(dict(id=i.id, name_file=i.file_name, file_random_name=i.file_random_name))
            return ls
        except:
            return []

    def get_all_dict_api(self, lnk=""):
        try:
            n = News_file().select().where(News_file.news == self.news)
            ls = []
            for i in n:
                link = "%s%s" % (lnk, i.file_random_name)
                ls.append(dict(link=link, name_file=i.file_name, file_type=i.file_type))
            return ls
        except Exception, e:
            return []

    def get_one(self):
        try:
            i = News_file().get(News_file.news == self.news, News_file.id == self.id, News_file.system == self.system)
            return dict(id=i.id, name=i.file_random_name)
        except Exception, e:
            return []

    def delete_bash_files(self, ls, hard_delete=True):
        try:
            if ls and type(ls) == list:
                for i in ls:
                    self.id = i
                    p = self.get_one()
                    if p:
                        try:
                            if hard_delete:
                                os.remove(
                                    os.path.join(sh.web['static_address'], "upload", "news_attach_file", p['name']))
                        except:
                            pass

                        n = News_file().delete().where(
                            News_file.news == self.news,
                            News_file.id == i,
                            News_file.system == self.system
                        ).execute()
                return True
            else:
                return False

        except Exception, e:
            return False

    def delete_bash_files_p4(self, ls):
        try:
            if ls and type(ls) == list:
                for i in ls:
                    self.id = i
                    p = self.get_one()
                    if p:
                        try:
                            os.remove(os.path.join(sh.web['static_address'], "upload", "news_attach_file", p['name']))
                        except:
                            pass

                        n = News_file().delete().where(
                            # News_file.news == self.news,
                            News_file.file_random_name == p['name'],
                            # News_file.system == self.system
                        ).execute()
                return True
            else:
                return False

        except Exception, e:
            return False


class SysNewsLink(News_file):
    def __init__(self, _id=None, system=None, news=None, link_name=None, link_address=None, random_id=None, *args,
                 **kwargs):
        super(SysNewsLink, self).__init__(*args, **kwargs)
        self.id = _id
        self.system = system
        self.news = news
        self.link_name = link_name
        self.link_address = link_address
        self.random_id = random_id

    def add_one(self):
        try:
            x = News_link().insert(
                system=self.system,
                news=self.news,
                link_name=self.link_name,
                link_address=self.link_address,
                random_id=self.random_id,
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            print e
            return False

    def get_all_dict(self):
        try:
            n = News_link().select().where(News_link.news == self.news, News_link.system == self.system)
            ls = []
            for i in n:
                ls.append(dict(id=i.id, link_name=i.link_name, link_address=i.link_address))
            return ls
        except:
            return []

    def get_all_dict_api(self):
        try:
            n = News_link().select().where(News_link.news == self.news)
            ls = []
            for i in n:
                ls.append(dict(link_name=i.link_name, link_address=i.link_address))
            return ls
        except Exception, e:
            return []

    def update_link(self):
        try:
            News_link().update(link_name=self.link_name, link_address=self.link_address).where(News_link.id == self.id,
                                                                                               News_link.news == self.news,
                                                                                               News_link.system == self.system).execute()
            return True
        except Exception, e:
            pass

    def update_link_p4(self):
        try:
            ll = News_link.get(News_link.id == self.id, News_link.news == self.news, News_link.system == self.system)
            News_link().update(link_name=self.link_name, link_address=self.link_address).where(
                News_link.random_id == ll.random_id).execute()
            return True
        except Exception, e:
            pass

    def delete_links(self, ls):
        try:
            if ls and type(ls) == list:
                for i in ls:
                    self.id = i
                    News_link().delete().where(
                        News_link.news == self.news,
                        News_link.id == i,
                        News_link.system == self.system
                    ).execute()
                return True
            else:
                return False

        except Exception, e:
            return False

    def delete_links_p4(self, ls):
        try:
            if ls and type(ls) == list:
                for i in ls:
                    ll = News_link.get(News_link.id == i, News_link.system == self.system, News_link.news == self.news
                                       )
                    News_link().delete().where(
                        News_link.link_address == ll.link_address,
                        News_link.link_name == ll.link_name,
                        News_link.random_id == ll.random_id
                    ).execute()
                return True
            else:
                return False

        except Exception, e:
            return False

    def delete_links_news_site(self):
        try:
            News_link().delete().where(
                News_link.news == self.news,
                News_link.system == self.system
            ).execute()
            return True
        except Exception, e:
            print e
            return False


class SysNewsPic:
    def __init__(self, _id=None, system=None, news=None, pic_name=None, *args, **kwargs):
        self.id = _id
        self.system = system
        self.news = news
        self.pic_name = pic_name

    def add_one(self):
        try:
            x = News_pic().insert(
                system=self.system,
                news=self.news,
                pic_name=self.pic_name
            ).execute()
            if x:
                return x
            return False
        except Exception, e:
            print e, "    add_one"
            return False

    def add_one_pic_site(self):
        try:
            sys_id = self.system.id
            news_id = self.news.id
            x = News_pic.insert(
                system=sys_id,
                news=news_id,
                pic_name=self.pic_name
            ).execute()
            if x:
                return x
            return False
        except Exception, e:
            print e.message, "    add_one"
            return False

    def add_many(self, collections=None):
        if not collections:
            collections = []

        if len(collections):
            row_dicts = ({'pic_name': c, 'system': self.system, 'news': self.news} for c in collections)
            try:
                if News_pic().insert_many(row_dicts).execute():
                    return True
                else:
                    return False
            except Exception, e:
                return False
        else:
            return False

    def get_all(self, lnk=""):
        try:
            n = News_pic().select().where(News_pic.news == self.news)
            ls = []
            for i in n:
                ls.append("%s%s" % (lnk, i.pic_name))
            return ls
        except:
            return []

    def get_one2(self, lnk=""):
        try:
            i = News_pic().get(News_pic.news == self.news)
            return "%s%s" % (lnk, i.pic_name)
        except:
            return None

    def get_all_dict(self):
        try:
            n = News_pic().select().where(News_pic.news == self.news, News_pic.system == self.system)
            ls = []
            for i in n:
                ls.append(dict(id=i.id, name=i.pic_name))
            return ls
        except:
            return []

    def get_one(self):
        try:
            i = News_pic().get(News_pic.news == self.news, News_pic.id == self.id, News_pic.system == self.system)
            return dict(id=i.id, name=i.pic_name)
        except:
            return []

    def delete_pics(self, hard_delete=True):
        try:
            try:
                if hard_delete:
                    for i in self.get_all():
                        os.remove(os.path.join(sh.web['static_address'], "upload", "news_pic", i))
            except:
                pass
            n = News_pic().delete().where(News_pic.news == self.news, News_pic.system == self.system).execute()
            if n:
                return True
        except:
            return False

    def delete_bash_pics(self, ls, hard_delete=True):
        try:
            if ls and type(ls) == list:
                for i in ls:
                    self.id = i
                    p = self.get_one()
                    if p:
                        try:
                            if hard_delete:
                                os.remove(os.path.join(sh.web['static_address'], "upload", "news_pic", p['name']))
                        except:
                            pass

                        n = News_pic().delete().where(
                            News_pic.news == self.news,
                            News_pic.id == i,
                            News_pic.system == self.system
                        ).execute()
                return True
            else:
                return False

        except:
            return False

    def delete_bash_pics_p4(self, ls):
        try:
            if ls and type(ls) == list:
                for i in ls:
                    self.id = i
                    p = self.get_one()
                    if p:
                        try:
                            os.remove(os.path.join(sh.web['static_address'], "upload", "news_pic", p['name']))
                        except:
                            pass

                        n = News_pic().delete().where(
                            # News_pic.news == self.news,
                            News_pic.pic_name == p['name'],
                            # News_pic.system == self.system
                        ).execute()
                return True
            else:
                return False

        except:
            return False


class SysGcmUsers:
    def __init__(self, _id=None, gcm_regid=None, user=None, system=None, device_id=None, created_at=None,
                 notification_enabled=None, *args, **kwargs):

        self.id = _id
        self.gcm_regid = gcm_regid
        self.user = user
        self.system = system
        self.device_id = device_id
        self.created_at = created_at
        self.notification_enabled = notification_enabled

    def get_all_users_for_news(self, collections):
        try:
            if collections:
                # u = User_collections().select(
                #     User_collections.user,
                #     Gcm_users.gcm_regid.alias("regid")
                # ).join(
                #     Gcm_users, JOIN_INNER, on=(User_collections.user == Gcm_users.user)
                # ).where(
                #     User_collections.collection << collections
                # )
                u = Gcm_users().select(
                    Gcm_users.gcm_regid
                ).join(
                    User_collections, JOIN_INNER, on=(User_collections.user == Gcm_users.user)
                ).where(
                    User_collections.collection << collections
                )

                ls = []
                for i in u:
                    ls.append(i.gcm_regid)
                return ls
            else:
                return []
        except Exception, e:
            return []

    def get_all_users_for_poll(self, sys_id):
        try:
            if sys_id:
                u = Gcm_users().select(
                    Gcm_users.gcm_regid
                ).join(
                    Users, JOIN_INNER, on=(Users.id == Gcm_users.user)
                ).where(
                    Users.system == sys_id
                )

                ls = []
                for i in u:
                    ls.append(i.gcm_regid)
                return ls
            else:
                return []
        except Exception, e:
            return []

    def get_all_users_reg_id(self):
        try:
            if type(self.user) == list:
                u = Gcm_users().select(Gcm_users.gcm_regid).where(Gcm_users.user << self.user)
                ls = []
                for i in u:
                    ls.append(i.gcm_regid)
                return ls
            else:
                return []
        except Exception, e:
            return []


class SysSystemLog(System_log):
    def __init__(self, _id=None, system=None, user=None, request_type=None, device_id=None, handler=None, link=None,
                 ip=None, user_agent=None, _date=None, *args, **kwargs):
        super(SysSystemLog, self).__init__(*args, **kwargs)

        self.id = _id
        self.system = system
        self.user = user
        self.request_type = request_type
        self.device_id = device_id
        self.handler = handler
        self.link = link
        self.ip = ip
        self.user_agent = user_agent
        self.date = _date

    def add_log(self):
        try:
            x = System_log().insert(
                system=self.system,
                user=self.user,
                request_type=self.request_type,
                device_id=self.device_id,
                handler=self.handler,
                link=self.link,
                ip=self.ip,
                user_agent=self.user_agent
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            return False


class SysSuggestions:
    Read = "READ"
    UnRead = "UNREAD"
    Delete = "DELETE"

    def __init__(self, _id=None, system=None, user=None, text=None, date=None, status=None, read_by=None, *args,
                 **kwargs):
        self.id = _id
        self.system = system
        self.user = user
        self.text = text
        self.date = date
        self.status = status
        self.read_by = read_by

    def add(self):
        try:
            x = Suggestions().insert(
                system=self.system,
                user=self.user,
                text=self.text,
                date=self.date,
                status=self.status,
                read_by=self.read_by
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def get_new_count(self):
        try:
            x = Suggestions().select(fn.Count(Suggestions.id)).where(
                Suggestions.system == self.system, Suggestions.status == "UNREAD"
            ).count()
            return x
        except Exception, e:
            return 0

    def get_all(self, page=1, count=12):
        try:
            x = Suggestions().select().paginate(page=page, paginate_by=count).order_by(SQL("`date` DESC")).where(
                Suggestions.system == self.system, Suggestions.status != "DELETE"
            )
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        text=i.text,
                        date=to_jalali(i.date, "%C"),
                        status=i.status,
                        read_by=i.read_by
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_all_p4(self, page=1, count=12):
        try:
            ls = []
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            sub_sys.append(self.system)
            for i in Suggestions().select().paginate(page=page, paginate_by=count).order_by(SQL("`date` DESC")).where(
                            Suggestions.system << sub_sys):
                ls.append(
                    dict(
                        id=i.id,
                        system_name=i.system.pname,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        text=i.text,
                        date=to_jalali(i.date, "%C"),
                        status=i.status,
                        read_by=i.read_by
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_one(self):
        try:
            i = Suggestions().get(Suggestions.system == self.system, Suggestions.id == self.id)
            ls = dict(
                id=i.id,
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                text=i.text,
                date=to_jalali(i.date, "%C"),
                status=i.status,
                read_by=i.read_by
            )

            return ls
        except Exception, e:
            return {}

    def delete_p4(self):
        try:
            Suggestions().delete().where(Suggestions.id == self.id).execute()
            return True
        except Exception, e:
            pass

    def update_p4(self):
        try:
            Suggestions().update(status=SysSuggestions.Read).where(Suggestions.id == self.id).execute()
            return True
        except Exception, e:
            pass

    def get_one_p4(self):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            sub_sys.append(self.system)
            i = Suggestions().get(Suggestions.system << sub_sys, Suggestions.id == self.id)
            ls = dict(
                id=i.id,
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                text=i.text,
                date=to_jalali(i.date, "%C"),
                status=i.status,
                read_by=i.read_by
            )
            return ls
        except Exception, e:
            return {}

    def update(self, **k):
        try:
            i = Suggestions().update(**k).where(Suggestions.system == self.system, Suggestions.id == self.id).execute()
            return True
        except Exception, e:
            return False

    def change_status(self):
        try:
            x = Suggestions().update(
                status=self.status
            ).where(
                Suggestions.system == self.system,
                Suggestions.id == self.id
            ).execute()
            return True
        except Exception, e:
            return False


class SysTags:
    def __init__(self, _id=None, system=None, name=None, date=None, *args, **kwargs):
        self.id = _id
        self.system = system
        self.name = name
        self.date = date

    def add(self):
        try:
            x = Tags().insert(
                system=self.system,
                name=self.name
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def add_many(self, news_id, ls=None):
        if not ls:
            ls = []

        if ls:
            for i in ls:
                self.name = i
                p = self.get_one_by_name()
                if p:
                    SysNewsTag(news=news_id, tag=p['id']).add()
                else:
                    try:
                        x = Tags().insert(
                            system=self.system,
                            name=self.name
                        ).execute()
                        if x:
                            SysNewsTag(news=news_id, tag=x).add()
                    except Exception, e:
                        pass

            return True
        else:
            return False

    def get_all(self):
        try:
            x = Tags().select().where(Tags.system == self.system)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        name=i.name,
                        date=to_jalali(i.date, "%C")
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_one(self):
        try:
            i = Tags().get(Tags.system == self.system, Tags.id == self.id)
            ls = dict(
                id=i.id,
                name=i.name,
                date=to_jalali(i.date, "%C")
            )
            return ls
        except Exception, e:
            return {}

    def get_one_by_name(self):
        try:
            i = Tags().get(Tags.system == self.system, Tags.name == self.name)
            ls = dict(
                id=i.id,
                name=i.name,
                date=to_jalali(i.date, "%C")
            )
            return ls
        except Exception, e:
            return {}

    def update(self, **k):
        try:
            i = Tags().update(**k).where(Tags.system == self.system, Tags.id == self.id).execute()
            return True
        except Exception, e:
            return False


class SysNewsTag:
    def __init__(self, _id=None, news=None, tag=None):
        self.id = _id
        self.news = news
        self.tag = tag

    def add(self):
        try:
            x = News_tag().insert(
                news=self.news,
                tag=self.tag
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def get_all(self):
        try:
            x = News_tag().select().where((News_tag.news == self.news) | (News_tag.tag == self.tag))
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        news=dict(id=i.news.id, name=i.news.title),
                        tag=dict(id=i.tag.id, name=i.tag.name, date=to_jalali(i.tag.date, "%C"))
                    )
                )
            return ls
        except Exception, e:
            return []

    def delete_by_news_id(self):
        try:
            i = News_tag().delete().where(News_tag.news == self.news).execute()
            return True
        except Exception, e:
            return False

    def delete_by_tag_id(self):
        try:
            i = News_tag().delete().where(News_tag.tag == self.tag).execute()
            return True
        except Exception, e:
            return False


class SysNewsComments:
    def __init__(self, _id=None, system=None, news=None, user=None, text=None, confirmed=None, date=None):
        self.id = _id
        self.system = system
        self.news = news
        self.user = user
        self.text = text
        self.confirmed = confirmed
        self.date = date

    def add(self):
        try:
            x = News_comments().insert(
                system=self.system,
                news=self.news,
                user=self.user,
                text=self.text
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def get_all(self, only_new=False, page=1, count=10):
        try:
            if not only_new:
                x = News_comments().select().paginate(page, count).order_by(SQL("`date` DESC")).where(
                    News_comments.system == self.system, News_comments.confirmed == "yes"
                )
            else:
                x = News_comments().select().paginate(page, count).order_by(SQL("`date` DESC")).where(
                    News_comments.system == self.system, News_comments.confirmed == "no"
                )
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        news=dict(id=i.news.id, name=i.news.title),
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        text=i.text,
                        confirmed=i.confirmed,
                        date=to_jalali(i.date, "%C")
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_one(self):
        try:
            i = News_comments().get(News_comments.system == self.system, News_comments.id == self.id)
            return dict(
                id=i.id,
                news=dict(id=i.news.id, name=i.news.title),
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                text=i.text,
                confirmed=i.confirmed,
                date=to_jalali(i.date, "%C")
            )

        except Exception, e:
            return {}

    def get_one_p4(self):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            sub_sys.append(self.system)
            i = News_comments().get(News_comments.system << sub_sys, News_comments.id == self.id)
            return dict(
                id=i.id,
                news=dict(id=i.news.id, name=i.news.title),
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                text=i.text,
                confirmed=i.confirmed,
                date=to_jalali(i.date, "%C")
            )

        except Exception, e:
            return {}

    def delete_by_id(self):
        try:
            x2 = News_comments().get(News_comments.id == self.id)
            if x2.confirmed == "yes":
                News.update(comment=News.comment - 1).where(News.id == x2.news).execute()
            News_comments().delete().where(
                News_comments.id == self.id,
                News_comments.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def delete_by_id_p4(self):
        try:
            x2 = News_comments().get(News_comments.id == self.id)
            if x2.confirmed == "yes":
                News.update(comment=News.comment - 1).where(News.id == x2.news).execute()
            News_comments().delete().where(
                News_comments.id == self.id,
                News_comments.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def update(self, **kwargs):
        try:
            News_comments().update(**kwargs).where(
                News_comments.id == self.id,
                News_comments.system == self.system
            ).execute()
            x2 = News_comments().get(News_comments.id == self.id)
            News.update(comment=News.comment + 1).where(News.id == x2.news).execute()
            return True
        except Exception, e:
            return False

    def update_p4(self, **kwargs):
        try:
            News_comments().update(**kwargs).where(
                News_comments.id == self.id,
            ).execute()
            x2 = News_comments().get(News_comments.id == self.id)
            News.update(comment=News.comment + 1).where(News.id == x2.news).execute()
            return True
        except Exception, e:
            return False

    def new_news_comment_count(self):
        try:
            x = News_comments().select(fn.Count(News_comments.id)).where(
                News_comments.system == self.system, News_comments.confirmed == "no"
            ).count()
            return x
        except Exception, e:
            return 0


class SysNewsLikes:
    def __init__(self, _id=None, system=None, news=None, user=None, date=None):
        self.id = _id
        self.system = system
        self.news = news
        self.user = user
        self.date = date

    def add_like(self):
        try:
            x = News_likes().insert(
                system=self.system,
                news=self.news,
                user=self.user,
            ).execute()
            if x:
                return x
            else:
                return False
        except Exception, e:
            return False

    def delete_like(self):
        try:
            News_likes().delete().where(
                News_likes.news == self.news,
                News_likes.user == self.user,
                News_likes.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def get_all(self):
        try:
            x = News_likes().select().order_by(SQL("`date` DESC")).where(News_likes.system == self.system)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        news=dict(id=i.news.id, name=i.news.title),
                        user=dict(id=i.user.id, name="{} {}".format(i.user.first_name, i.user.last_name)),
                        date=to_jalali(i.date, "%C")
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_one_news_like_count(self):
        try:
            x = News_likes().select(fn.COUNT(News_likes.id)).where(News_likes.news == self.news).count()
            return x
        except Exception, e:
            return 0

    def is_user_liked(self):
        try:
            x = News_likes().get(News_likes.user == self.user, News_likes.news == self.news)
            if x:
                return True
            return False
        except Exception, e:
            return False

    def delete_by_id(self):
        try:
            i = News_likes().delete().where(
                News_likes.id == self.id,
                News_likes.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False


class SysMessages:
    Sent = "sent"
    Viewed = "viewed"
    Deleted = "deleted"

    SystemToUser = "s2u"
    UserToSystem = "u2s"

    TypeSMS = "sms"
    TypeAdvice = "advice"

    def __init__(self, _id=None, system=None, user=None, text=None, date=None, status=None, msg_type=None, type=None):
        self.id = _id
        self.system = system
        self.user = user
        self.text = text
        self.date = date
        self.status = status
        self.msg_type = msg_type
        self.type = type

    def send(self):
        try:
            z = Messages().insert(
                system=self.system,
                user=self.user,
                text=self.text,
                status=self.status,
                msg_type=self.msg_type,
                type=self.type
            ).execute()
            return z if z else False
        except:
            return False

    def get_system(self):
        try:
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            sub_sys.append(self.system)
            x = Messages().get(Messages.id == self.id, Messages.type == self.type)
            if x.system.id in sub_sys:
                return dict(system=x.system.id, system_user=x.user.system)
            else:
                return False
        except Exception, e:
            return False

    def delete_msg_p4(self):
        try:
            Messages().delete().where(Messages.id == self.id, Messages.system == self.system,
                                      Messages.type == self.type).execute()
            return True
        except Exception, e:
            return False

    def send_many(self, ls=None):
        if not ls:
            ls = []

        if ls:
            try:
                x = [
                    dict(
                        system=self.system,
                        user=i,
                        text=self.text,
                        status=self.status,
                        msg_type=self.msg_type,
                        type=self.type
                    ) for i in ls
                    ]
                if x:
                    x1 = Messages().insert_many(x).execute()
                    if x1:
                        return True
                    else:
                        return False
                else:
                    return False

            except:
                return False

    def __get_all(self, ex, page=1, count=12, distinct_user=True):
        try:
            if distinct_user:
                x = Messages().select().group_by(Messages.user).paginate(page=page, paginate_by=count).order_by(
                    SQL("`date` DESC")).where(ex, Messages.type == self.type)
            else:
                x = Messages().select().order_by(SQL("`date` DESC")).where(ex, Messages.type == self.type)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        date=to_jalali(i.date, "%C"),
                        status=i.status
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_all_for_system_p4(self, page=1, count=12, only_new=False, distinct_user=True):
        sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
        sub_sys.insert(0, int(self.system))
        if only_new:
            return self.__get_all(
                (
                    (Messages.system << sub_sys) &
                    (Messages.status == self.Sent) &
                    (Messages.msg_type == self.UserToSystem) &
                    (Messages.type == self.type)
                ), page, count, distinct_user=False
            )
        else:
            return self.__get_all(
                (
                    (Messages.system << sub_sys) &
                    (Messages.status != self.Deleted) & (Messages.status != self.Sent) &
                    (Messages.msg_type == self.UserToSystem) &
                    (Messages.type == self.type)
                ), page, count, distinct_user
            )

    def get_all_for_system(self, page=1, count=12, only_new=False, distinct_user=True):
        if only_new:
            return self.__get_all(
                (
                    (Messages.system == self.system) &
                    (Messages.status == self.Sent) &
                    (Messages.msg_type == self.UserToSystem) &
                    (Messages.type == self.type)
                ), page, count, distinct_user=False
            )
        else:
            return self.__get_all(
                (
                    (Messages.system == self.system) &
                    (Messages.status != self.Deleted) & (Messages.status != self.Sent) &
                    (Messages.msg_type == self.UserToSystem) &
                    (Messages.type == self.type)
                ), page, count, distinct_user
            )

    def get_all_for_user(self, page=1, count=12):
        try:
            x = Messages().select().paginate(
                page=page,
                paginate_by=count
            ).order_by(
                SQL("`date` DESC")
            ).where(
                Messages.system == self.system,
                Messages.user == self.user,
                Messages.status != "deleted",
                Messages.type == self.type
            )

            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        date=to_jalali(i.date, "%y/%m/%d - %H:%M"),
                        text=i.text,
                        status=i.status,
                        type=i.msg_type
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_all_for_user_p4(self, page=1, count=12, parent=None):
        try:
            sys = []
            sys.append(parent)
            sys.append(self.system)
            x = Messages().select().paginate(
                page=page,
                paginate_by=count
            ).order_by(
                SQL("`date` DESC")
            ).where(
                Messages.system << sys,
                Messages.user == self.user,
                Messages.status != "deleted",
                Messages.type == self.type
            )

            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        date=to_jalali(i.date, "%y/%m/%d - %H:%M"),
                        text=i.text,
                        status=i.status,
                        type=i.msg_type
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_new_messages_count(self):
        try:

            x = Messages().select(fn.Count(Messages.id)).where(
                (Messages.system == self.system) &
                (Messages.status == self.Sent) &
                (Messages.msg_type == self.UserToSystem) &
                (Messages.type == self.type)
            ).count()
            return x
        except Exception, e:
            return 0

    def get_one(self):
        try:
            i = Messages().get(Messages.system == self.system, Messages.id == self.id, Messages.type == self.type)
            ls = dict(
                id=i.id,
                user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                text=i.text,
                date=to_jalali(i.date, "%C"),
                status=i.status
            )

            return ls
        except Exception, e:
            return {}

    def get_one_with_parent(self):
        try:
            # x = .get()
            c = Messages().select().where(
                Messages.system == self.system,
                Messages.type == self.type,
                Messages.user == Messages().select(Messages.user).where(Messages.system == self.system,
                                                                        Messages.id == self.id),
                Messages.status != self.Deleted
            ).order_by(SQL("`date` DESC"))
            # print c
            # x = Messages().select(Messages.user).where(Messages.system == self.system, Messages.id == self.id).get()
            # c = Messages().select().where(
            #     Messages.system == self.system, Messages.user == x.user.id, Messages.status != self.Deleted
            # ).order_by(SQL("`date` DESC"))

            ls = []
            for i in c:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        text=i.text,
                        date=to_jalali(i.date, "%C"),
                        status=i.status,
                        msg_type=i.msg_type
                    )
                )
            return ls
        except Exception, e:
            return {}

    def get_one_with_parent_p4(self, parent_sys):
        try:
            sub_sys = []
            sub_sys.append(parent_sys)
            sub_sys.append(self.system)
            c = Messages().select().where(
                Messages.system << sub_sys,
                Messages.type == self.type,
                Messages.user == Messages().select(Messages.user).where(Messages.system << sub_sys,
                                                                        Messages.id == self.id)
            ).order_by(SQL("`date` DESC"))
            ls = []
            for i in c:
                ls.append(
                    dict(
                        id=i.id,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                        text=i.text,
                        date=to_jalali(i.date, "%C"),
                        status=i.status,
                        msg_type=i.msg_type
                    )
                )
            return ls
        except Exception, e:
            return {}

    def update(self, **k):
        try:
            i = Messages().update(**k).where(Messages.system == self.system, Messages.id == self.id).execute()
            return True
        except Exception, e:
            return False

    def update_all_messages_from_user(self):
        try:
            i = Messages().update(status=self.Viewed).where(
                Messages.system == self.system,
                Messages.user == self.user,
                Messages.status != self.Deleted,
                Messages.type == self.type,
                Messages.msg_type == self.UserToSystem,
            ).execute()
            return True
        except Exception, e:
            return False

    def update_all_messages_from_user_p4(self, parent_sys):
        try:
            sub_sys = []
            sub_sys.append(parent_sys)
            sub_sys.append(self.system)
            i = Messages().update(status=self.Viewed).where(
                Messages.system << sub_sys,
                Messages.user == self.user,
                Messages.status != self.Deleted,
                Messages.msg_type == self.UserToSystem,
                Messages.type == self.type
            ).execute()
            return True
        except Exception, e:
            return False

    def change_status(self):
        try:
            x = Messages().update(
                status=self.status
            ).where(
                Messages.system == self.system,
                Messages.id == self.id
            ).execute()
            return True
        except Exception, e:
            return False

    def get_all_sent_for_system_p4(self, page=1, count=12):
        try:
            ls = []
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            sub_sys.insert(0, int(self.system))

            x = Messages().select().group_by(Messages.text).paginate(page=page, paginate_by=count).order_by(
                SQL("`date` DESC")).where((Messages.system << sub_sys) & (Messages.status != self.Deleted) & (
                Messages.msg_type == self.SystemToUser) & (Messages.type == self.type))
            for i in x:
                ls.append(dict(
                    id=i.id,
                    text=i.text,
                    date=to_jalali(i.date, "%C"),
                ))
            return ls
        except Exception, e:
            print e
            return []

    def get_all_sent_for_system(self, page=1, count=12):
        try:
            ls = []
            x = Messages().select().group_by(Messages.text).paginate(page=page, paginate_by=count).order_by(
                SQL("`date` DESC")).where((Messages.system == self.system) & (Messages.status != self.Deleted) & (
                Messages.msg_type == self.SystemToUser) & (Messages.type == self.type))
            for i in x:
                ls.append(dict(
                    id=i.id,
                    text=i.text,
                    date=to_jalali(i.date, "%C"),
                ))
            return ls
        except Exception, e:
            print e
            return []


class SysNews_admin_p4:
    def __init__(self, news_id=None, system_id=None, news_admin_id=None):
        self.news = news_id
        self.system = system_id
        self.news_admin = news_admin_id

    def get_one(self):
        try:
            i = News_admin_p4.get(News_admin_p4.system == self.system, News_admin_p4.news_admin_id == self.news_admin)
            return dict(
                news_id=dict(id=i.news.id),
            )
        except Exception, e:
            return {}

    def insert(self, n_admin_id):
        try:
            News_admin_p4().insert(news=self.news, system=self.system, news_admin_id=n_admin_id).execute()
            return True
        except Exception, e:
            return False

    def get_sub_news(self):
        try:
            x = News_admin_p4.select().where(News_admin_p4.news_admin_id == self.news_admin)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        sub_news_id=dict(id=i.news.id)
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_all(self, p_sys_id):
        try:
            x = News_admin_p4().select().join(
                System, JOIN_INNER, on=(News_admin_p4.system == System.id)
            ).where(System.parent_system == p_sys_id)
            ls = []
            for i in x:
                ls.append(
                    dict(news_id=dict(id=i.news_id)
                         )
                )
            return ls
        except Exception, e:
            return []

    def get_admin_news(self):
        try:
            x = News_admin_p4().select().where(News_admin_p4.system == self.system)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        news_id=dict(id=i.news.id),
                        system_id=dict(id=i.system.id)
                    )
                )
            return ls
        except Exception, e:
            return False


class SysPollQuestion:
    def __init__(self, _id=None, _system_id=None, _question=None, date=None, _status=None, parent_question=None):
        self.id = _id
        self.system = _system_id
        self.question = _question
        self.date = date
        self.status = _status
        self.parent_question = parent_question

    def insert(self):
        try:
            m = Poll_question().insert(
                system=self.system,
                question=self.question,
                parent_question=self.parent_question
            ).execute()
            return m
        except Exception, e:
            return False

    def children_question(self):
        try:
            ls = []
            x = Poll_question().select().where(Poll_question.parent_question == self.parent_question)
            for i in x:
                ls.append(i.id)
            return ls
        except Exception, e:
            return []

    def update_status(self):
        try:
            m = Poll_question().update(status=self.status).where(Poll_question.id == self.id).execute()
            if m:
                return True
            else:
                return False
        except Exception, e:
            return False

    # @property
    def delete(self):
        try:
            m = Poll_question().delete().where(Poll_question.id == self.id).execute()
            return True
        except Exception, e:
            return False

    def get_all_p4(self):
        try:
            ls = []
            sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            sub_sys.append(self.system)
            for i in Poll_question().select().order_by(SQL("`date` DESC")).where(Poll_question.system << sub_sys):
                if i.parent_question == 0 or not i.parent_question:
                    ls.append(
                        dict(
                            system_name=i.system.pname,
                            id=i.id,
                            text=i.question,
                            date=to_jalali(i.date),
                            status=i.status
                        )
                    )
            return ls
        except Exception, e:
            return {}

    def get_all(self):
        try:
            m = Poll_question().select().order_by(SQL("`date` DESC")).where(Poll_question.system == self.system)
            ls = []
            for i in m:
                if i.parent_question == 0 or not i.parent_question:
                    ls.append(
                        dict(
                            id=i.id,
                            # sysyem = dict()
                            text=i.question,
                            date=to_jalali(i.date),
                            status=i.status
                        )
                    )
            return ls
        except Exception, e:
            return {}


class SysPoolItem:
    def __init__(self, _id=None, _question_id=None, _item=None):
        self.id = _id
        self.question = _question_id
        self.item = _item

    @staticmethod
    def insert_list_item(question_id, item=None):
        if not item:
            item = []

        if len(item):
            row_dicts = ({'item': r, 'question': question_id} for r in item)
            try:
                # if User_roles().insert_many(row_dicts).execute():
                if Poll_item().insert_many(row_dicts).execute():
                    return True
                else:
                    return False
            except Exception, e:
                return False
        else:
            return False
            # try:
            #
            #     pass
            #     # m = Item().insert(
            #     #     question=self.question,
            #     #     item=self.item
            #     # ).execute()
            #     # return m
            # except Exception, e:
            #     return False

    def get_all(self):
        try:
            m = Poll_item().select().where(Poll_item.question == self.question)
            ls = []
            for i in m:
                ls.append(
                    dict(
                        id=i.id,
                        count=0,
                        darsad=0,
                        # sysyem = dict()
                        # question=dict(id=i.question.id, text=i.question.question),
                        # user=dict(id=i.user.id),
                        item=i.item,  # dict(id=i.item.id, text=i.item.item),
                        # date=to_jalali(i.date)
                    )
                )
            return ls
        except Exception, e:
            return {}


class SysPollAnswer:
    def __init__(self, _id=None, _user_id=None, _question_id=None, _item_id=None, date=None):
        self.id = _id
        self.question = _question_id
        self.item = _item_id
        self.user = _user_id
        self.date = date

    def get_all_p4(self):

        try:
            ls = []
            sub_sys_q = SysPollQuestion(parent_question=self.question).children_question()
            sub_sys_q.append(self.question)
            for i in Poll_answer().select().where(
                            Poll_answer.question << sub_sys_q):
                ls.append(
                    dict(
                        id=i.id,
                        question=dict(id=i.question.id, text=i.question.question),
                        user=dict(id=i.user.id),
                        item=dict(id=i.item.id, text=i.item.item),
                        date=to_jalali(i.date)
                    )
                )
            return ls
        except Exception, e:
            print(e)
            pass

    def get_all(self):
        try:
            m = Poll_answer().select().where(Poll_answer.question == self.question)
            ls = []
            for i in m:
                ls.append(
                    dict(
                        id=i.id,
                        # sysyem = dict()
                        question=dict(id=i.question.id, text=i.question.question),
                        user=dict(id=i.user.id),
                        item=dict(id=i.item.id, text=i.item.item),
                        date=to_jalali(i.date)
                    )
                )
            return ls
        except Exception, e:
            return {}


class SysTickets:
    def __init__(self, _id=None, system_id=None, topic=None, priority=None, status=None, last_update=None):
        self.id = _id
        self.system = system_id
        self.topic = topic
        self.status = status
        self.priority = priority
        self.last_update = last_update

    def send(self):
        try:
            z = Tickets().insert(
                system=self.system,
                topic=self.topic,
                priority=self.priority,
                status=self.status
            ).execute()

            return z if z else False
        except:
            return False

    def date_update(self, date):
        try:
            Tickets().update(last_update=date).where(Tickets.id == self.id).execute()
        except:
            return False

    def change_status(self, status):
        try:
            Tickets().update(status=status).where(Tickets.id == self.id).execute()
        except:
            return False

    def get_all(self, page=1, count=3, desc=False, paginate=False):
        try:
            if paginate:
                x = Tickets().select().order_by(SQL("`last_update` DESC")).where(
                    Tickets.system == self.system).paginate(page, count)
            else:
                x = Tickets().select().order_by(SQL("`last_update` DESC")).where(Tickets.system == self.system)
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        topic=i.topic,
                        last_update=to_jalali(i.last_update, "%C"),
                        status=i.status,
                        priority=i.priority
                    )
                )
            return ls
        except Exception, e:
            return []

    def is_exist(self):
        try:
            i = Tickets.get(Tickets.system == self.system, Tickets.id == self.id)
            return dict(
                id=i.id,
                topic=i.topic,
                last_update=to_jalali(i.last_update, "%C"),
                status=i.status,
                priority=i.priority
            )

        except Exception, e:
            return {}


class SysSubticket:
    SystemToAdmin = "s2a"
    AdminToSystem = "a2s"

    def __init__(self, _id=None, tickets_id=None, user_id=None, type=None, text=None, file=None):
        self.id = _id
        self.tickets_id = tickets_id
        self.user_id = user_id
        self.type = type
        self.text = text
        self.file = file

    def send_subticket(self):
        try:
            z = Subticket().insert(
                users=self.user_id,
                tickets=self.tickets_id,
                text=self.text,
                file=self.file,
                type=self.type
            ).execute()

            return z if z else False
        except Exception, e:
            print("subticket", e)
            return False

    def get_all(self):
        try:
            x = Subticket().select().join(
                Users, JOIN_INNER, on=(Subticket.users == Users.id)) \
                .where(Subticket.tickets == self.tickets_id).order_by(SQL("`date` DESC"))
            ls = []
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        text=i.text,
                        date=to_jalali(i.date, "%C"),
                        file=i.file,
                        type=i.type,
                        user=dict(
                            id=i.users.id,
                            full_name=u"{} {}".format(i.users.first_name, i.users.last_name)
                        )
                    )
                )
            return ls
        except Exception, e:
            return []


class SysForum(Forum):
    def __init__(self, _id=None, user=None, system=None, name=None, icon=None, date=None, status=None,
                 condition=None, *args, **kwargs):
        super(SysForum, self).__init__(*args, **kwargs)
        self.id = _id
        self.user = user
        self.system = system
        self.name = name
        self.icon = icon
        self.date = date
        self.status = status
        self.condition = condition

    def add_forum(self):
        try:
            x = Forum.insert(user=self.user, system=self.system, name=self.name, status=self.status,
                             condition="open").execute()
            if x:
                return True
            else:
                return False
        except Exception, e:
            return False

    def update_forum(self):
        try:
            x = Forum.update(name=self.name).where(Forum.id == self.id, Forum.system == self.system).execute()
            if x:
                return True
            return False
        except Exception, e:
            return False

    def get_all(self):
        try:
            ls = []
            x = Forum.select().order_by(SQL("`date` DESC")).where(Forum.system == self.system)
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        name=i.name,
                        date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                        status=i.status,
                        condition=i.condition,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                    )
                )
            return ls
        except Exception, e:
            return []

    def forum_delete(self):

        try:
            r = Forum().delete().where(Forum.id == self.id).execute()
            if r:
                return True
            else:
                return False
        except Exception, e:
            return False

    def update_status(self):
        try:
            m = Forum().update(status=self.status).where(Forum.id == self.id).execute()
            if m:
                return True
            else:
                return False
        except Exception, e:
            return False

    def get_one(self):
        try:
            x = False
            try:
                x = Forum().get(Forum.system == self.system)
            except:
                pass
            if x:
                return x.id
            else:
                y = Forum.insert(system=self.system, user=self.user, name="test",
                                 status="active", condition="open").execute()
                return y
        except Exception, e:
            print e
            return False


class SysForumTopic(Forum_topic):
    def __init__(self, _id=None, user=None, system=None, forum=None, name=None, date=None, status=None,
                 condition=None, *args, **kwargs):
        super(SysForumTopic, self).__init__(*args, **kwargs)
        self.id = _id
        self.user = user
        self.forum = forum
        self.name = name
        self.date = date
        self.status = status
        self.system = system
        self.condition = condition

    def get_all(self):
        try:
            ls = []
            x = Forum_topic().select().order_by(SQL("`date` DESC")).where(Forum_topic.system == self.system)
            for i in x:
                ls.append(
                    dict(
                        id=i.id,
                        name=i.name,
                        date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                        status=i.status,
                        condition=i.condition,
                        user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                    )
                )
            return ls
        except Exception, e:
            return []

    def get_one(self):
        try:
            return Forum_topic().get(Forum_topic.system == self.system, Forum_topic.id == self.id)
        except Exception, e:
            print e
            return False

    def topic_delete(self):

        try:
            r = Forum_topic().delete().where(Forum_topic.id == self.id, Forum_topic.system == self.system).execute()
            if r:
                return True
            return False
        except Exception, e:
            return False

    def update_status(self):
        try:
            m = Forum_topic().update(status=self.status).where(Forum_topic.id == self.id,
                                                               Forum_topic.system == self.system).execute()
            if m:
                return True
            else:
                return False
        except Exception, e:
            return False

    def update_topic(self):
        try:
            x = Forum_topic.update(name=self.name).where(Forum_topic.id == self.id).execute()
            if x:
                return True
            return False
        except Exception, e:
            return False

    def add_topic(self):
        try:
            x = Forum_topic.insert(system=self.system, user=self.user, forum=self.forum, name=self.name,
                                   status=self.status, condition="open").execute()
            if x:
                return True
            return False
        except Exception, e:
            print e
            return False


class SysForumPost(Forum_post):
    def __init__(self, _id=None, user=None, text=None, system=None, confirm=None, date=None, forum_topic=None, *args,
                 **kwargs):
        super(SysForumPost, self).__init__(*args, **kwargs)
        self.id = _id
        self.user = user
        self.text = text
        self.confirm = confirm
        self.date = date
        self.system = system
        self.forum_topic = forum_topic

    def get_all(self, only_new=False, page=1, count=15):
        try:
            if not only_new:
                x = Forum_post().select().paginate(page, count).order_by(SQL("`date` DESC")).where(
                    Forum_post.forum_topic == self.forum_topic.id, Forum_post.confirm == "yes",
                    Forum_post.system == self.system.id)
            else:
                x = Forum_post().select().paginate(page, count).order_by(SQL("`date` DESC")).where(
                    Forum_post.forum_topic == self.forum_topic.id, Forum_post.confirm == "no",
                    Forum_post.system == self.system.id)
            ls = []
            for i in x:
                ls.append(dict(
                    id=i.id,
                    user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                    text=i.text,
                    date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                    # date=to_jalali(i.date, "%C"),
                    confirm=i.confirm

                )
                )
            return ls
        except Exception, e:
            print e
            return []

    def get_all_pending(self, page=1, count=15):
        try:
            x = Forum_post().select().paginate(page, count).order_by(SQL("`date` DESC")).where(
                Forum_post.system == self.system, Forum_post.confirm == "no")
            ls1 = []
            for i in x:
                ls1.append(dict(
                    id=i.id,
                    user=dict(id=i.user.id, name=u"{} {}".format(i.user.first_name, i.user.last_name)),
                    text=i.text,
                    date=to_jalali(i.date, u"%Y/%m/%d ساعت %H:%M:%S"),
                    # date=to_jalali(i.date, "%C"),
                    confirm=i.confirm

                )
                )
            return ls1
        except Exception, e:
            print e
            return []

    def get_one(self):
        try:
            i = Forum_post().get(Forum_post.id == self.id)
            return dict(
                id=i.id,
                text=i.text,
                date=i.date,
                confirm=i.confirm,
                user=i.user,
                forum_topic=i.forum_topic
            )

        except Exception, e:
            return {}

    def get_one_p4(self):
        try:
            # sub_sys = [ss['id'] for ss in SysSystem().get_all_sub_system(parent_id=self.system)]
            # sub_sys.append(self.system)
            # i = News_comments().get(News_comments.system << sub_sys, News_comments.id == self.id)
            i = Forum_post().get(Forum_post.id == self.id, Forum_post.system == self.system)
            return dict(
                id=i.id,
                text=i.text,
                date=i.date,
                confirm=i.confirm,
                user=i.user,
                forum_topic=i.forum_topic
            )

        except Exception, e:
            return {}

    def delete_by_id(self):
        try:
            Forum_post().delete().where(
                Forum_post.id == self.id,
                Forum_post.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def delete_by_id_p4(self):
        try:
            Forum_post().delete().where(
                Forum_post.id == self.id,
                Forum_post.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def update(self, **kwargs):
        try:
            Forum_post().update(**kwargs).where(
                Forum_post.id == self.id,
                Forum_post.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def update_p4(self, **kwargs):
        try:
            Forum_post().update(**kwargs).where(
                Forum_post.id == self.id,
                Forum_post.system == self.system
            ).execute()
            return True
        except Exception, e:
            return False

    def send_post(self):
        try:
            Forum_post.insert(system=self.system, user=self.user, confirm=self.confirm, forum_topic=self.forum_topic,
                              text=self.text).execute()
            return True
        except Exception, e:
            print e
            return False

