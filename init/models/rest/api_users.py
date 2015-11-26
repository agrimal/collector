user_max_perpage = 500

def allowed_user_ids():
    """ Return ids of the users member of the same groups than the requester.
    """
    q = db.auth_membership.group_id.belongs(user_group_ids())
    rows = db(q).select(db.auth_membership.user_id)
    return [r.user_id for r in rows]

def allowed_user_ids_q():
    try:
        check_privilege("UserManager")
        q = db.auth_user.id > 0
    except:
        user_ids = allowed_user_ids()
        q = db.auth_user.id.belongs(user_ids)
    return q

def user_id_q(id):
    """ Return a DAL expression limiting the query to the users member of the same groups than the requester.
    """
    if type(id) in (unicode, str) and "@" in id:
        q = db.auth_user.email == id
    elif id == "self":
        q = db.auth_user.id == auth.user_id
    else:
        q = db.auth_user.id == id
    return q


#
class rest_get_users(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List existing users.",
          "Managers and UserManager are allowed to see all users.",
          "Others can only see users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users?query=email contains opensvc",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/users",
          tables=["auth_user"],
          props_blacklist=["password", "registration_key"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = allowed_user_ids_q()
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_user(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display user properties.",
          "Managers and UserManager are allowed to see all users.",
          "Others can only see users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s?props=lock_filter",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/users/<id>",
          tables=["auth_user"],
          props_blacklist=["password", "registration_key"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_user_apps(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List apps the user is responsible for.",
          "Managers and UserManager are allowed to see all users' information.",
          "Others can only see information for users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/apps",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/users/<id>/apps",
          tables=["apps"],
          desc=desc,
          groupby=db.apps.id,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        q &= db.apps_responsibles.group_id == db.auth_membership.group_id
        q &= db.auth_membership.user_id == db.auth_user.id
        q &= db.apps.id == db.apps_responsibles.app_id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_user_nodes(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List nodes the user is responsible of.",
          "Managers and UserManager are allowed to see all users' information.",
          "Others can only see information for users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/nodes",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/users/<id>/nodes",
          tables=["nodes"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        q &= db.nodes.team_responsible == db.auth_group.role
        q &= db.auth_group.id == db.auth_membership.group_id
        q &= db.auth_membership.user_id == db.auth_user.id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_user_services(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List services the user is responsible of.",
          "Managers and UserManager are allowed to see all users' information.",
          "Others can only see information for users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/services",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/users/<id>/services",
          tables=["services"],
          groupby=db.services.id,
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        q &= db.services.svc_app == db.apps.app
        q &= db.apps.id == db.apps_responsibles.app_id
        q &= db.apps_responsibles.group_id == db.auth_membership.group_id
        q &= db.auth_membership.user_id == db.auth_user.id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_user_groups(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List groups the user is member of.",
          "Managers and UserManager are allowed to see all users' information.",
          "Others can only see information for users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/groups",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/users/<id>/groups",
          tables=["auth_group"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        q &= db.auth_membership.user_id == db.auth_user.id
        q &= db.auth_group.id == db.auth_membership.group_id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_post_users(rest_post_handler):
    def __init__(self):
        self.get_handler = rest_get_users()
        self.update_one_handler = rest_post_user()
        self.update_one_param = "email"

        desc = [
          "Create a user.",
          "Update users matching the specified query."
          "The user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -X POST -o- -d first_name=John -d last_name=Smith https://%(collector)s/init/rest/api/users",
        ]
        rest_post_handler.__init__(
          self,
          path="/users",
          tables=["auth_user"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        check_privilege("UserManager")

        if "perpage" in vars and int(vars["perpage"]) > user_max_perpage:
            raise Exception(T("perpage can not be more than %(n)d", dict(n=user_max_perpage)))

        obj_id = db.auth_user.insert(**vars)
        _log('user.create',
             'add user %(data)s',
             dict(data=str(vars)),
            )
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_user().handler(obj_id)


#
class rest_post_user(rest_post_handler):
    def __init__(self):
        desc = [
          "Modify a user properties.",
          "The user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST -d perpage=20 https://%(collector)s/init/rest/api/users/10",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>",
          tables=["auth_user"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        check_privilege("UserManager")
        q = user_id_q(id)
        row = db(q).select().first()
        if row is None:
            return dict(error="User %s does not exist" % str(id))
        if "id" in vars.keys():
            del(vars["id"])

        if "perpage" in vars and int(vars["perpage"]) > user_max_perpage:
            raise Exception(T("perpage can not be more than %(n)d", dict(n=user_max_perpage)))

        db(q).update(**vars)
        l = []
        for key in vars:
            l.append("%s: %s => %s" % (str(key), str(row[key]), str(vars[key])))
        _log('user.change',
             'change user %(data)s',
             dict(data=', '.join(l)),
            )
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_user().handler(row.id)


#
class rest_delete_user(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete a user.",
          "Delete all group membership.",
          "The user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the changed tables.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/users/10",
        ]

        rest_delete_handler.__init__(
          self,
          path="/users/<id>",
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        check_privilege("UserManager")
        try:
            id = int(id)
            q = db.auth_user.id == id
        except:
            q = db.auth_user.email == id

        row = db(q).select().first()
        if row is None:
            return dict(info="User %s does not exists" % str(id))

        # group
        db(q).delete()
        _log('user.delete',
             'deleted user %(email)s',
             dict(email=row.email))
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))

        # group membership
        q = db.auth_membership.user_id == row.id
        db(q).delete()

        return dict(info="User %s deleted" % row.email)

#
# /users/<id>/group...
#
class rest_post_user_group(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a user to a group.",
          "The api user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/users/10/groups/10",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/groups/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, group_id, **vars):
        check_privilege("UserManager")
        try:
            id = int(user_id)
            q = db.auth_user.id == user_id
        except:
            q = db.auth_user.email == user_id
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user_id))

        try:
            id = int(id)
            q = db.auth_group.id == group_id
        except:
            q = db.auth_group.role == group_id
        group = db(q).select().first()
        if group is None:
            return dict(error="Group %s does not exist" % str(group_id))

        q = db.auth_membership.user_id == user.id
        q &= db.auth_membership.group_id == group.id
        q &= db.auth_membership.primary_group == 'F'
        row = db(q).select().first()
        if row is not None:
            return dict(info="User %s is already attached to group %s" % (str(user.email), str(group.role)))

        db.auth_membership.insert(user_id=user_id, group_id=group_id, primary_group='F')
        _log('user.group.attach',
             'user %(u)s attached to group %(g)s',
             dict(u=user.email, g=group.role),
            )
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return dict(info="User %s attached to group %s" % (str(user.email), str(group.role)))


#
class rest_delete_user_group(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a user from a group.",
          "The api user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/users/10/groups/10",
        ]
        rest_delete_handler.__init__(
          self,
          path="/users/<id>/groups/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, group_id, **vars):
        check_privilege("UserManager")
        try:
            id = int(user_id)
            q = db.auth_user.id == user_id
        except:
            q = db.auth_user.email == user_id
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user_id))

        try:
            id = int(id)
            q = db.auth_group.id == group_id
        except:
            q = db.auth_group.role == group_id
        group = db(q).select().first()
        if group is None:
            return dict(error="Group %s does not exist" % str(group_id))

        q = db.auth_membership.user_id == user.id
        q &= db.auth_membership.group_id == group.id
        q &= db.auth_membership.primary_group == 'F'
        row = db(q).select().first()
        if row is None:
            return dict(info="User %s is already detached from group %s" % (str(user.email), str(group.role)))

        db(q).delete()
        _log('user.group.detach',
             'user %(u)s detached from group %(g)s',
             dict(u=user.email, g=group.role),
            )
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return dict(info="User %s detached from group %s" % (str(user.email), str(group.role)))


#
# /users/<id>/primary_group
#
class rest_get_user_primary_group(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display the user's primary group properties.",
          "Managers and UserManager are allowed to see all users' information.",
          "Others can only see information for users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/primary_group",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/users/<id>/primary_group",
          tables=["auth_group"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        q &= db.auth_membership.user_id == db.auth_user.id
        q &= db.auth_membership.primary_group == True
        q &= db.auth_group.id == db.auth_membership.group_id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_post_user_primary_group(rest_post_handler):
    def __init__(self):
        desc = [
          "Set a user's primary group.",
          "The api user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/users/10/primary_group/10",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/primary_group/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, group_id, **vars):
        check_privilege("UserManager")
        try:
            id = int(user_id)
            q = db.auth_user.id == user_id
        except:
            q = db.auth_user.email == user_id
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user_id))

        try:
            id = int(id)
            q = db.auth_group.id == group_id
        except:
            q = db.auth_group.role == group_id
        group = db(q).select().first()
        if group is None:
            return dict(error="Group %s does not exist" % str(group_id))

        q = db.auth_membership.user_id == user.id
        q &= db.auth_membership.group_id == group.id
        q &= db.auth_membership.primary_group == 'T'
        row = db(q).select().first()
        if row is not None:
            return dict(info="User %s primary group is already %s" % (str(user.id), str(group.id)))

        q = db.auth_membership.user_id == user_id
        q &= db.auth_membership.primary_group == 'T'
        db(q).delete()
        db.auth_membership.insert(user_id=user.id, group_id=group.id, primary_group='T')
        _log('user.primary_group.attach',
             'user %(u)s primary group set to %(g)s',
             dict(u=user.email, g=group.role),
            )
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return dict(info="User %s primary group set to %s" % (str(user.email), str(group.role)))


#
class rest_delete_user_primary_group(rest_delete_handler):
    def __init__(self):
        desc = [
          "Unset a user's primary group.",
          "The api user must be in the UserManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/users/10/primary_group/10",
        ]
        rest_delete_handler.__init__(
          self,
          path="/users/<id>/primary_group",
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, **vars):
        check_privilege("UserManager")
        try:
            id = int(user_id)
            q = db.auth_user.id == user_id
        except:
            q = db.auth_user.email == user_id
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user.email))

        q = db.auth_membership.user_id == user.id
        q &= db.auth_membership.primary_group == 'T'
        row = db(q).select().first()
        if row is None:
            return dict(info="User %s has already no primary group" % str(user.email))

        db(q).delete()
        _log('user.primary_group.detach',
             'user %(u)s primary group unset',
             dict(u=user.email),
            )
        l = {
          'event': 'auth_user',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return dict(info="User %s primary group unset" % str(user.email))


#
# /users/<id>/filterset...
#
class rest_get_user_filterset(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display the user's current filterset.",
          "Managers and UserManager are allowed to see all users' current filterset.",
          "Others can only see the current filterset of users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/filterset",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/users/<id>/filterset",
          tables=["gen_filtersets"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        q &= db.gen_filterset_user.user_id == db.auth_user.id
        q &= db.gen_filtersets.id == db.gen_filterset_user.fset_id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_post_user_filterset(rest_post_handler):
    def __init__(self):
        desc = [
          "Set a user's current filterset.",
          "The api user must be in the UserManager privilege group or the specified user himself.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/users/10/filterset/10",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/filterset/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, fset_id, **vars):
        q = user_id_q(user_id)
        q &= db.auth_user.id == auth.user_id
        row = db(q).select().first()
        if row is None:
            check_privilege("UserManager")

        q = user_id_q(user_id)
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user_id))

        if user.lock_filter:
            if "UserManager" not in user_groups():
                return dict(error="User %s filterset is locked" % str(user_id))

        try:
            id = int(fset_id)
            q = db.gen_filtersets.id == fset_id
        except:
            q = db.gen_filtersets.fset_name == fset_id
        fset = db(q).select().first()
        if fset is None:
            return dict(error="Filterset %s does not exist" % str(fset_id))

        q = db.gen_filterset_user.user_id == user.id
        q &= db.gen_filterset_user.fset_id == fset.id
        row = db(q).select().first()
        if row is not None:
            return dict(info="User %s filterset is already %s" % (str(user.email), str(fset.fset_name)))

        q = db.gen_filterset_user.user_id == user.id
        db(q).delete()
        db.gen_filterset_user.insert(user_id=user.id, fset_id=fset.id)
        _log('user.filterset.attach',
             'user %(u)s filterset set to %(g)s',
             dict(u=user.email, g=fset.fset_name),
            )
        l = {
          'event': 'gen_filterset_user_change',
          'data': {
            'user_id': user.id,
            'fset_id': fset.id,
            'fset_name': fset.fset_name,
          },
        }
        _websocket_send(event_msg(l))
        return dict(info="User %s filterset set to %s" % (str(user.email), str(fset.fset_name)))

#
class rest_delete_user_filterset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Unset a user's current filterset.",
          "The api user must be in the UserManager privilege group or the specified user himself.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/users/10/filterset",
        ]
        rest_delete_handler.__init__(
          self,
          path="/users/<id>/filterset",
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, **vars):
        q = user_id_q(user_id)
        q &= db.auth_user.id == auth.user_id
        row = db(q).select().first()
        if row is None:
            check_privilege("UserManager")

        q = user_id_q(user_id)
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user_id))

        if user.lock_filter:
            if "UserManager" not in user_groups():
                return dict(error="User %s filterset is locked" % str(user_id))

        q = db.gen_filterset_user.user_id == user.id
        row = db(q).select().first()
        if row is None:
            return dict(info="User %s has already no filterset" % str(user.email))
        db(q).delete()
        _log('user.filterset.detach',
             'user %(u)s filterset unset',
             dict(u=user.email),
            )
        l = {
          'event': 'gen_filterset_user_delete',
          'data': {
            'user_id': user.id,
          },
        }
        _websocket_send(event_msg(l))
        return dict(info="User %s filterset unset" % str(user.email))

#
# /users/<id>/table_settings
#
class rest_get_user_table_settings(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List user's table settings: columns display and live-update enable.",
          "Managers and UserManager are allowed to see all settings.",
          "Others can only see their own settings.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/self/table_settings",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/users/<id>/table_settings",
          tables=["user_prefs_columns"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to see another user table settings")

        q = db.user_prefs_columns.upc_user_id == user.id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_post_user_table_settings(rest_post_handler):
    def __init__(self):
        desc = [
          "Change user's table settings: columns display and live-update enable.",
          "Managers and UserManager are allowed to change all settings.",
          "Others can only change their own settings.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          "# curl -u %(email)s -X POST -o- -d upc_field=wsenabled -d upc_visible=1 https://%(collector)s/init/rest/api/users/self/table_settings",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/table_settings",
          tables=["user_prefs_columns"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        if "upc_table" not in vars:
            raise Exception("upc_table is mandatory in POST data")
        if "upc_field" not in vars:
            raise Exception("upc_field is mandatory in POST data")
        if "upc_visible" not in vars:
            raise Exception("upc_visible is mandatory in POST data")

        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to change another user table settings")

        vars["upc_user_id"] = user.id

        k = dict(
          upc_user_id=user.id,
          upc_table=vars["upc_table"],
          upc_field=vars["upc_field"],
        )
        obj_id = db.user_prefs_columns.update_or_insert(k, **vars)
        _log('user.table_settings.change',
             'change user table settings %(data)s',
             dict(data=str(vars)),
            )
        qvars = dict(
          meta="0",
          query="upc_table=%s and upc_field=%s" % (vars["upc_table"], vars["upc_field"])
        )
        return rest_get_user_table_settings().handler(id, **qvars)

#
# /users/<id>/table_filters
#
class rest_get_user_table_filters(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List user's table column filters.",
          "Managers and UserManager are allowed to see all settings.",
          "Others can only see their own settings.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/self/table_filters",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/users/<id>/table_filters",
          tables=["column_filters"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to see another user table settings")

        q = db.column_filters.user_id == user.id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_post_user_table_filters(rest_post_handler):
    def __init__(self):
        desc = [
          "Change user's table filters.",
          "Managers and UserManager are allowed to change all settings.",
          "Others can only change their own settings.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          "# curl -u %(email)s -X POST -o- -d -d col_tableid=nodes -d col_name=v_nodes.sec_zone -d col_filter=a https://%(collector)s/init/rest/api/users/self/table_filters",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/table_filters",
          tables=["column_filters"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        if "col_tableid" not in vars:
            raise Exception("col_tableid is mandatory in POST data")
        if "col_name" not in vars:
            raise Exception("col_name is mandatory in POST data")
        if "col_filter" not in vars:
            raise Exception("col_filter is mandatory in POST data")

        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to change another user table settings")

        vars["user_id"] = user.id

        if "bookmark" not in vars:
            vars["bookmark"] = "current"

        k = dict(
          user_id=user.id,
          col_tableid=vars["col_tableid"],
          col_name=vars["col_name"],
          bookmark=vars["bookmark"],
        )
        obj_id = db.column_filters.update_or_insert(k, **vars)
        _log('user.table_filters.change',
             'change user table filters %(data)s',
             dict(data=str(vars)),
            )
        qvars = dict(
          meta="0",
          query="col_tableid=%s and col_name=%s and bookmark=%s" % (vars["col_tableid"], vars["col_name"], vars["bookmark"])
        )
        return rest_get_user_table_filters().handler(id, **qvars)

#
class rest_delete_user_table_filters(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete user's table filters matching criteria.",
          "Managers and UserManager are allowed to change all settings.",
          "Others can only change their own settings.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          "# curl -u %(email)s -X DELETE -o- -d https://%(collector)s/init/rest/api/users/self/table_filters",
        ]
        rest_delete_handler.__init__(
          self,
          path="/users/<id>/table_filters",
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to change another user table settings")

        vars["user_id"] = user.id

        q = db.column_filters.user_id == user.id
        if "col_tableid" in vars:
            q &= db.column_filters.col_tableid == vars["col_tableid"]
        if "col_name" in vars:
            q &= ((db.column_filters.col_name == vars["col_name"]) | \
                  (db.column_filters.col_name.like("%."+vars["col_name"])))
        if "col_filter" in vars:
            q &= db.column_filters.col_filter == vars["col_filter"]
        if "bookmark" in vars:
            q &= db.column_filters.bookmark == vars["bookmark"]

        db(q).delete()
        _log('user.table_filters.delete',
             'delete user table filters %(data)s',
             dict(data=str(vars)),
            )
        return dict(info=T("column filters deleted"))

#
class rest_post_user_table_filters_load_bookmark(rest_post_handler):
    def __init__(self):
        desc = [
          "Set bookmarked filters as current and return their data.",
          "Managers and UserManager are allowed to change all settings.",
          "Others can only change their own settings.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          "# curl -u %(email)s -X POST -o- -d -d col_tableid=nodes -d bookmark=foo https://%(collector)s/init/rest/api/users/self/table_filters/load_bookmark",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/table_filters/load_bookmark",
          tables=["column_filters"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        if "col_tableid" not in vars:
            raise Exception("col_tableid is mandatory in POST data")
        if "bookmark" not in vars:
            raise Exception("bookmark is mandatory in POST data")

        if "col_name" in vars:
            delete(vars["col_name"])
        if "col_filter" in vars:
            delete(vars["col_filter"])

        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to change another user table settings")

        q = db.column_filters.col_tableid == vars["col_tableid"]
        q &= db.column_filters.bookmark == "current"
        q &= db.column_filters.user_id == user.id
        db(q).delete()

        sql = """insert into column_filters
                 (
                   col_tableid,
                   col_name,
                   col_filter,
                   user_id,
                   bookmark
                 )
                 select
                   col_tableid,
                   col_name,
                   col_filter,
                   user_id,
                   "current"
                 from column_filters
                 where
                   col_tableid="%(table_id)s" and
                   user_id=%(user_id)d and
                   bookmark="%(bookmark)s"
              """ % dict(
                      user_id=user.id,
                      table_id=vars["col_tableid"],
                      bookmark=vars["bookmark"]
                    )
        db.executesql(sql)
        db.commit()

        _log('user.table_filters.change',
             'load bookmark %(data)s',
             dict(data=vars["bookmark"]),
            )
        qvars = dict(
          meta="0",
          query="col_tableid=%s and bookmark=current" % (vars["col_tableid"])
        )
        return rest_get_user_table_filters().handler(id, **qvars)

#
class rest_post_user_table_filters_save_bookmark(rest_post_handler):
    def __init__(self):
        desc = [
          "Save current filters as a bookmark.",
          "Managers and UserManager are allowed to change all settings.",
          "Others can only change their own settings.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          "# curl -u %(email)s -X POST -o- -d -d col_tableid=nodes -d bookmark=foo https://%(collector)s/init/rest/api/users/self/table_filters/save_bookmark",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/table_filters/save_bookmark",
          tables=["column_filters"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        if "col_tableid" not in vars:
            raise Exception("col_tableid is mandatory in POST data")
        if "bookmark" not in vars:
            raise Exception("bookmark is mandatory in POST data")

        if "col_name" in vars:
            delete(vars["col_name"])
        if "col_filter" in vars:
            delete(vars["col_filter"])

        q = user_id_q(id)
        user = db(q).select().first()
        if user is None:
            raise Exception("User %s does not exist" % str(id))

        if user.id != auth.user_id:
            ug = user_groups()
            if "UserManager" not in ug and "Manager" not in ug:
                raise Exception("You are not allowed to change another user table settings")

        q = db.column_filters.col_tableid == vars["col_tableid"]
        q &= db.column_filters.bookmark == vars["bookmark"]
        q &= db.column_filters.user_id == user.id
        db(q).delete()

        sql = """insert into column_filters
                 (
                   col_tableid,
                   col_name,
                   col_filter,
                   user_id,
                   bookmark
                 )
                 select
                   col_tableid,
                   col_name,
                   col_filter,
                   user_id,
                   "%(bookmark)s"
                 from column_filters
                 where
                   col_tableid="%(table_id)s" and
                   user_id=%(user_id)d and
                   bookmark="current"
              """ % dict(
                      user_id=user.id,
                      table_id=vars["col_tableid"],
                      bookmark=vars["bookmark"]
                    )
        db.executesql(sql)
        db.commit()

        _log('user.table_filters.change',
             'save bookmark %(data)s',
             dict(data=vars["bookmark"]),
            )
        qvars = dict(
          meta="0",
          query="col_tableid=%s and bookmark=current" % (vars["col_tableid"])
        )
        return rest_get_user_table_filters().handler(id, **qvars)


#
# /users/<id>/domains
#
class rest_get_user_domains(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display the domains pattern the user is allowed to see.",
          "Managers and UserManager are allowed to see all users' domains values.",
          "Others can only see the domains values of users in their organisational groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/users/%(email)s/domains",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/users/<id>/domains",
          tables=["domain_permissions"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        gid = auth.user_group(id)
        q = allowed_user_ids_q()
        q &= user_id_q(id)
        user = db(q).select().first()
        if user is None:
            check_privilege("UserManager")

        q &= db.domain_permissions.group_id == gid
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_post_user_domains(rest_post_handler):
    def __init__(self):
        desc = [
          "Set the domain pattern the user is allowed to see.",
          "The api user must be in the UserManager or Manager privilege group",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the users table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/users/10/domains",
        ]
        rest_post_handler.__init__(
          self,
          path="/users/<id>/domains",
          tables=["domain_permissions"],
          desc=desc,
          examples=examples
        )

    def handler(self, user_id, **vars):
        check_privilege("UserManager")

        q = user_id_q(user_id)
        user = db(q).select().first()
        if user is None:
            return dict(error="User %s does not exist" % str(user_id))
        gid = auth.user_group(user_id)
        vars["group_id"] = gid

        if 'domains' not in vars:
            raise Exception("The 'domains' parameter must be specified")

        q = db.domain_permissions.group_id == gid
        row = db(q).select().first()
        if row is None or row.domains == "":
            current_domains = "None"
        else:
            current_domains = row.domains

        k = dict(
          group_id=gid
        )
        db.domain_permissions.update_or_insert(k, **vars)
        _log('user.change',
             'user %(u)s domain permissions changed from %(c)s to %(g)s',
             dict(u=user.email, c=current_domains, g=vars["domains"]),
            )
        l = {
          'event': 'auth_user',
          'data': {
            'foo': 'bar',
          },
        }
        _websocket_send(event_msg(l))
        return rest_get_user_domains().handler(user_id)


