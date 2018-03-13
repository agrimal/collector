import json

def mangle_alerts(data):
    for i, row in enumerate(data):
        try:
            data[i]['dash_dict'] = json.loads(data[i]['dash_dict'])
            data[i]['alert'] = data[i]['dash_fmt'] % data[i]['dash_dict']
        except:
            pass
    return data

#
class rest_get_alerts(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List existing alerts.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/alerts?query=not dash_type contains save"
        ]

        rest_get_table_handler.__init__(
          self,
          path="/alerts",
          tables=["dashboard"],
          vprops={"alert": ["dash_fmt", "dash_dict"]},
          vprops_fn=mangle_alerts,
          orderby=~db.dashboard.id,
          desc=desc,
          examples=examples,
          allow_fset_id=True,
        )

    def handler(self, **vars):
        q = db.dashboard.id > 0
        fset_id = vars.get("fset-id")
        if fset_id:
            q = apply_filters_id(q, node_field=db.dashboard.node_id, fset_id=fset_id)
        self.set_q(q)
        data = self.prepare_data(**vars)
        data["data"] = mangle_alerts(data["data"])
        return data

#
class rest_get_alert(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display an alert properties.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/alerts/10"
        ]

        rest_get_line_handler.__init__(
          self,
          path="/alerts/<id>",
          tables=["dashboard"],
          vprops={"alert": ["dash_fmt", "dash_dict"]},
          vprops_fn=mangle_alerts,
          desc=desc,
          examples=examples,
        )

    def handler(self, _id, **vars):
        q = db.dashboard.id == int(_id)
        self.set_q(q)
        data = self.prepare_data(**vars)
        data["data"] = mangle_alerts(data["data"])
        return data

#
class rest_delete_alert(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete an alert",
        ]
        examples = [
          "# curl -u %(email)s -X DELETE -o- https://%(collector)s/init/rest/api/alerts/1"
        ]

        rest_delete_handler.__init__(
          self,
          path="/alerts/<id>",
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        check_privilege("Manager")

        q = db.dashboard.id == id
        row = db(q).select().first()
        if row is None:
            raise Exception("Alert %s not found"%str(id))

        db(q).delete()
        table_modified("dashboard")
        ws_send('dashboard_change', {'id': id})

        fmt = "Alert %(id)s deleted"
        d = dict(id=str(id))

        _log('alert.del', fmt, d)

        return dict(info=fmt%d)

class rest_delete_alerts(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete multiple alerts",
        ]
        examples = [
          "# curl -u %(email)s -X DELETE -d id=1 -o- https://%(collector)s/init/rest/api/alerts"
        ]

        rest_delete_handler.__init__(
          self,
          path="/alerts",
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        return rest_delete_alert().handler(**vars)

#
class rest_post_alert(rest_post_handler):
    def __init__(self):
        desc = [
          "Update a set of alert properties.",
          "The user must be in the Manager or AlertsManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The alert signature is automatically computed.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the dashboard table.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d loc_city="Zanzibar" -d app="ERP" https://%(collector)s/init/rest/api/alerts/1""",
        ]
        rest_post_handler.__init__(
          self,
          path="/alerts/<id>",
          tables=["dashboard"],
          desc=desc,
          examples=examples,
        )

    def handler(self, alert_id, **vars):
        check_privilege("AlertsManager")
        q = db.dashboard.id == alert_id
        row = db(q).select().first()
        if row is None:
            raise HTTP(404, "alert %d does not exist" % alert_id)
        vars["dash_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        env = None
        if vars.get("svc_id"):
            svc = get_svc(vars.get("svc_id"))
            if svc:
                env = svc.svc_env
        if env is None and vars.get("node_id"):
            node = get_node(vars.get("node_id"))
            if node:
                env = node.node_env
        vars["dash_env"] = env
        vars["dash_md5"] = ""
        if vars.get("dash_fmt") is not None:
            fmt = vars["dash_fmt"]
        else:
            fmt = row.dash_fmt
        if vars.get("dash_dict") is not None:
            _d = vars["dash_dict"]
        else:
            _d = json.loads(row.dash_dict)
        try:
            fmt % _d
        except:
            raise HTTP(400, "incompatible 'dash_fmt' and 'dash_dict'")
        if vars.get("dash_severity"):
            try:
                sev = int(vars.get("dash_severity"))
            except:
                raise HTTP(400, "'dash_severity' must be an integer")
            if sev < 0 or sev > 5:
                raise HTTP(400, "'dash_severity' must be between 0 and 5")

        db(q).update(**vars)
        _log('dashboard.change',
             'update alert %(data)s',
             dict(data=beautify_change(row, vars)),
             node_id=vars.get("node_id"), svc_id=vars.get("svc_id"))
        ws_send('dashboard_change')
        return rest_get_alert().handler(alert_id)

#
class rest_post_alerts(rest_post_handler):
    def __init__(self):
        desc = [
          "Create or update multiple alerts",
        ]
        examples = [
          """# curl -u %(email)s -o- -d node_id=node_id -d svc_id=svc_id dash_type=custom https://%(collector)s/init/rest/api/alerts""",
        ]
        rest_post_handler.__init__(
          self,
          path="/alerts",
          tables=["dashboard"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        check_privilege("AlertsManager")
        vars["dash_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        env = None
        if vars.get("svc_id"):
            svc = get_svc(vars.get("svc_id"))
            if svc:
                env = svc.svc_env
        if env is None and vars.get("node_id"):
            node = get_node(vars.get("node_id"))
            if node:
                env = node.node_env
        if "dash_type" not in vars:
            raise HTTP(400, str(vars))
            raise HTTP(400, "'dash_type' is mandatory")
        if vars.get("dash_fmt") is None:
            vars["dash_fmt"] = ""
        if vars.get("dash_dict") is None:
            vars["dash_dict"] = {}
        try:
            vars.get("dash_fmt") % vars.get("dash_dict")
        except:
            raise HTTP(400, "incompatible 'dash_fmt' and 'dash_dict'")
        try:
            vars["dash_dict"] = json.dumps(vars["dash_dict"])
        except ValueError:
            raise HTTP(400, "'dash_dict' must be a dictionary")
        try:
            sev = int(vars.get("dash_severity"))
        except:
            raise HTTP(400, "'dash_severity' must be an integer")
        if sev < 0 or sev > 5:
            raise HTTP(400, "'dash_severity' must be between 0 and 5")

        q = db.dashboard.dash_type == vars["dash_type"]
        q &= db.dashboard.dash_fmt == vars["dash_fmt"]
        q &= db.dashboard.dash_dict == vars["dash_dict"]
        q &= db.dashboard.node_id == vars["node_id"]
        q &= db.dashboard.svc_id == vars["svc_id"]
        row = db(q).select().first()

        if row:
            db(db.dashboard.id==row.id).update(
                dash_updated=vars["dash_updated"],
                dash_env=env,
                dash_severity=vars["dash_severity"],
            )
            alert_id = row.id
            _log('dashboard.change',
                 'update alert %(data)s',
                 dict(data=beautify_change(row, vars)),
                 node_id=vars.get("node_id"), svc_id=vars.get("svc_id"))
        else:
            alert_id = db.dashboard.insert(**vars)
            _log('dashboard.create',
                 'create alert %(data)s',
                 dict(data=beautify_data(vars)),
                 node_id=vars.get("node_id"), svc_id=vars.get("svc_id"))
        ws_send('dashboard_change')
        return rest_get_alert().handler(alert_id)


