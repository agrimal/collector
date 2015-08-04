from gluon.dal import smart_query

#
class rest_get_filters(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List filters.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/filters?query=f_table=nodes"
        ]
        q = db.gen_filters.id > 0
        rest_get_table_handler.__init__(
          self,
          path="/filters",
          tables=["gen_filters"],
          q=q,
          desc=desc,
          examples=examples,
        )

class rest_get_filter(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display a filter properties.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/filters/10"
        ]
        rest_get_line_handler.__init__(
          self,
          path="/filters/<id>",
          tables=["gen_filters"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = db.gen_filtersets.id == id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_filtersets(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List filtersets.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/filtersets?query=fset_name contains aix"
        ]
        q = db.gen_filtersets.id > 0
        rest_get_table_handler.__init__(
          self,
          path="/filtersets",
          tables=["gen_filtersets"],
          q=q,
          desc=desc,
          examples=examples,
        )

class rest_get_filterset(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display a filterset properties.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/filtersets/10"
        ]
        rest_get_line_handler.__init__(
          self,
          path="/filtersets/<id>",
          tables=["gen_filtersets"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        try:
            id = int(id)
            q = db.gen_filtersets.id == id
        except:
            q = db.gen_filtersets.fset_name == id
        self.set_q(q)
        return self.prepare_data(**vars)

class rest_get_filterset_filtersets(rest_get_table_handler):
    def __init__(self):
        desc = [
          "Display a filterset child filtersets.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/filtersets/10/filtersets"
        ]
        rest_get_table_handler.__init__(
          self,
          path="/filtersets/<id>/filtersets",
          tables=["gen_filtersets"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        id = lib_fset_id(id)
        if id is None:
            return dict(error="filterset not found")
        q = db.gen_filtersets_filters.fset_id == id
        q &= db.gen_filtersets.id == db.gen_filtersets_filters.encap_fset_id
        self.set_q(q)
        return self.prepare_data(**vars)

class rest_get_filterset_filters(rest_get_table_handler):
    def __init__(self):
        desc = [
          "Display a filterset child filters.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/filtersets/10/filters"
        ]
        rest_get_table_handler.__init__(
          self,
          path="/filtersets/<id>/filters",
          tables=["gen_filters", "gen_filtersets_filters"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        id = lib_fset_id(id)
        if id is None:
            return dict(error="filterset not found")
        q = db.gen_filtersets_filters.fset_id == id
        q &= db.gen_filtersets_filters.f_id == db.gen_filters.id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_post_filtersets(rest_post_handler):
    def __init__(self):
        desc = [
          "Create a filterset.",
          "The user must be in the CompManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the filtersets table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -d fset_name=\"my fset\" -d fset_stats=false https://%(collector)s/init/rest/api/filtersets",
        ]
        rest_post_handler.__init__(
          self,
          path="/filtersets",
          tables=["gen_filtersets"],
          props_blacklist=["fset_author", "fset_updated", "id"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        try:
            obj_id = create_filterset(**vars)
        except CompInfo as e:
            return dict(info=str(e))
        return rest_get_filterset().handler(obj_id)


#
class rest_post_filterset(rest_post_handler):
    def __init__(self):
        desc = [
          "Modify a filterset properties.",
          "The user must be in the CompManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the groups table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -d fset_stats=false https://%(collector)s/init/rest/api/filtersets/10",
        ]
        rest_post_handler.__init__(
          self,
          path="/filtersets/<id>",
          tables=["gen_filtersets"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        check_privilege("CompManager")
        try:
            id = int(id)
            q = db.gen_filtersets.id == id
        except:
            q = db.gen_filtersets.fset_name == id
        row = db(q).select().first()
        if row is None:
            return dict(error="filterset %s not found" % str(id))
        if "id" in vars.keys():
            del(vars["id"])
        db(q).update(**vars)
        l = []
        for key in vars:
            l.append("%s: %s => %s" % (str(key), str(row[key]), str(vars[key])))
        _log('filterset.change',
             'change filterset %(data)s',
             dict(data=', '.join(l)),
            )
        l = {
          'event': 'gen_filtersets',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_filterset().handler(row.id)

#
class rest_delete_filterset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete a filterset.",
          "The user must be in the CompManager privilege group.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the filtersets table.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/filtersets/10",
        ]
        rest_delete_handler.__init__(
          self,
          path="/filtersets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, fset_id, **vars):
        try:
            delete_filterset(fset_id, **vars)
        except CompInfo as e:
            return dict(info=str(e))

#
class rest_delete_filterset_filterset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a filterset from a filterset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/filtersets/10/filtersets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/filtersets/<id>/filtersets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, parent_fset_id, child_fset_id, **vars):
        parent_fset_id = lib_fset_id(parent_fset_id)
        child_fset_id = lib_fset_id(child_fset_id)
        if parent_fset_id is None:
            return dict(error="parent filterset not found")
        if child_fset_id is None:
            return dict(error="child filterset not found")
        try:
            detach_filterset_from_filterset(child_fset_id, parent_fset_id)
        except CompError as e:
            return dict(error=str(e))
        except CompInfo as e:
            return dict(info=str(e))

#
class rest_post_filterset_filterset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a filterset to a filterset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/filtersets/10/filtersets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/filtersets/<id>/filtersets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, parent_fset_id, child_fset_id, **vars):
        parent_fset_id = lib_fset_id(parent_fset_id)
        child_fset_id = lib_fset_id(child_fset_id)
        if parent_fset_id is None:
            return dict(error="parent filterset not found")
        if child_fset_id is None:
            return dict(error="child filterset not found")
        try:
            attach_filterset_to_filterset(child_fset_id, parent_fset_id)
        except CompError as e:
            return dict(error=str(e))
        except CompInfo as e:
            return dict(info=str(e))

#
class rest_post_filterset_filter(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a filter to a filterset",
          "Expressions are evaluated as (((1=1 <f_log_op1> expr1) <f_log_op2> expr2) <f_log_op3> expr3)",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/filtersets/10/filters/151",
        ]
        data = """
---
| **f_log_op** | The logical operator (AND, OR, AND NOT, OR NOT) to set between this filter and its predecessor |
| **f_order**  | An integer used to sort the filters before formatting the query                                |
---
"""
        rest_post_handler.__init__(
          self,
          path="/filtersets/<id>/filters/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, fset_id, f_id, **vars):
        fset_id = lib_fset_id(fset_id)
        f_id = int(f_id)
        if fset_id is None:
            return dict(error="filterset not found")
        try:
            attach_filter_to_filterset(f_id, fset_id, **vars)
        except CompError as e:
            return dict(error=str(e))
        except CompInfo as e:
            return dict(info=str(e))

#
class rest_delete_filterset_filter(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a filter from a filterset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/filtersets/10/filters/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/filtersets/<id>/filters/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, fset_id, f_id):
        fset_id = lib_fset_id(fset_id)
        f_id = int(f_id)
        if fset_id is None:
            return dict(error="filterset not found")
        try:
            detach_filter_from_filterset(f_id, fset_id)
        except CompError as e:
            return dict(error=str(e))
        except CompInfo as e:
            return dict(info=str(e))


