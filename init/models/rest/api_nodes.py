import datetime

#
class rest_delete_node_compliance_ruleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a ruleset from a node",
          "Attached rulesets add their variables to the modules execution environment.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/nodes/mynode/compliance/rulesets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/rulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, nodename, rset_id, **vars):
        node_responsible(nodename)
        return lib_comp_ruleset_detach_node(nodename, rset_id)

#
class rest_post_node_compliance_ruleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a ruleset to a node",
          "Attached rulesets add their variables to the modules execution environment.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/nodes/mynode/compliance/rulesets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/rulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, nodename, rset_id, **vars):
        node_responsible(nodename)
        return lib_comp_ruleset_attach_node(nodename, rset_id)

#
class rest_delete_node_compliance_moduleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a moduleset from a node",
          "Modules of attached modulesets are scheduled for check or fix by the node OpenSVC agent.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/nodes/mynode/compliance/modulesets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/modulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, nodename, modset_id, **vars):
        node_responsible(nodename)
        return lib_comp_moduleset_detach_node(nodename, modset_id)

#
class rest_post_node_compliance_moduleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a moduleset to a node",
          "Modules of attached modulesets are scheduled for check or fix by the node OpenSVC agent.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/nodes/mynode/compliance/modulesets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/modulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, nodename, modset_id, **vars):
        node_responsible(nodename)
        return lib_comp_moduleset_attach_node(nodename, modset_id)

#
class rest_get_node_compliance_rulesets(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List compliance rulesets attached to the node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/compliance/rulesets",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/rulesets",
          tables=["comp_rulesets"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.comp_rulesets_nodes.nodename == nodename
        q &= db.comp_rulesets_nodes.ruleset_id == db.comp_rulesets.id
        q = q_filter(q, node_field=db.comp_rulesets_nodes.nodename)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_compliance_modulesets(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List compliance modulesets attached to the node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/compliance/modulesets",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/modulesets",
          tables=["comp_moduleset"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.comp_node_moduleset.modset_node == nodename
        q &= db.comp_node_moduleset.modset_id == db.comp_moduleset.id
        q = q_filter(q, node_field=db.comp_node_moduleset.modset_node)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_interfaces(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List a node network interfaces.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/interfaces?props=intf,mac",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/interfaces",
          tables=["node_ip"],
          props_blacklist=["type", "addr", "mask"],
          groupby=db.node_ip.intf,
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.node_ip.nodename == nodename
        q = q_filter(q, node_field=db.node_ip.nodename)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_ips(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List a node ips.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/ips?props=prio,net_network,net_netmask",
        ]

        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/ips",
          tables=["v_nodenetworks"],
          props_blacklist=db.nodes.fields,
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.v_nodenetworks.nodename == nodename
        q = q_filter(q, app_field=db.v_nodenetworks.app)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_disks(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List a node disks.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/disks?props=b_disk_app.disk_nodename,b_disk_app.disk_id,stor_array.array_name",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/disks",
          tables=["b_disk_app", "stor_array"],
          left=db.stor_array.on(db.b_disk_app.disk_arrayid == db.stor_array.array_name),
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.b_disk_app.disk_nodename == nodename
        l = db.stor_array.on(db.b_disk_app.disk_arrayid == db.stor_array.array_name)
        q = q_filter(q, app_field=db.b_disk_app.app)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_checks(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List a node checks.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/checks",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/checks",
          tables=["checks_live"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.checks_live.chk_nodename == nodename
        q = q_filter(q, node_field=db.checks_live.chk_nodename)
        self.set_q(q)
        return self.prepare_data(**vars)




#
class rest_get_node_hbas(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List a node storage host bus adapters.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/hbas",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/hbas",
          tables=["node_hba"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.node_hba.nodename == nodename
        q = q_filter(q, node_field=db.node_hba.nodename)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_services(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List node OpenSVC services.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/services",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/services",
          tables=["svcmon", "services"],
          left=db.services.on(db.svcmon.mon_svcname == db.services.svc_name),
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.svcmon.mon_nodname == nodename
        q = q_filter(q, svc_field=db.svcmon.mon_svcname)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_service(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display the specified service on the specified node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/services",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/nodes/<nodename>/services/<svcname>",
          tables=["svcmon", "services"],
          left=db.services.on(db.svcmon.mon_svcname == db.services.svc_name),
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, svcname, **vars):
        q = db.svcmon.mon_nodname == nodename
        q = db.svcmon.mon_svcname == svcname
        q = q_filter(q, svc_field=db.svcmon.mon_svcname)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_alerts(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List a node alerts.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/alerts?props=dash_nodename,dash_type",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/alerts",
          tables=["dashboard"],
          vprops={"alert": ["dash_fmt", "dash_dict"]},
          vprops_fn=mangle_alerts,
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.dashboard.dash_nodename == nodename
        f1 = q_filter(svc_field=db.dashboard.svcname)
        f2 = q_filter(node_field=db.dashboard.nodename)
        q &= (f1|f2)
        self.set_q(q)
        data = self.prepare_data(**vars)
        return data


#
class rest_get_node(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display all node properties.",
          "Display selected node properties.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode?props=nodename,loc_city",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/nodes/<nodename>",
          tables=["nodes"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.nodes.nodename == nodename
        q = q_filter(q, app_field=db.nodes.app)
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_node_uuid(rest_get_line_handler):
    def __init__(self):
        desc = [
          "- Display node uuid.",
          "- Only node responsibles and managers are allowed to see this information.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/uuid",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/nodes/<nodename>/uuid",
          tables=["auth_node"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        node_responsible(nodename)
        q = db.auth_node.nodename == nodename
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_node_am_i_responsible(rest_get_handler):
    def __init__(self):
        desc = [
          "- return true if the requester is responsible for this node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/am_i_responsible",
        ]
        rest_get_handler.__init__(
          self,
          path="/nodes/<nodename>/am_i_responsible",
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        node_responsible(nodename)
        return dict(data=True)

 #
class rest_get_node_root_password(rest_get_handler):
    def __init__(self):
        desc = [
          "- Display node root password set by the 'rotate root password' opensvc agent action.",
          "- Only node responsibles and managers are allowed to see this information.",
          "- The password retrieval is logged for audit.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/mynode/root_password",
        ]
        rest_get_handler.__init__(
          self,
          path="/nodes/<nodename>/root_password",
          tables=["auth_node"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        node_responsible(nodename)

        config = local_import('config', reload=True)
        try:
            salt = config.aes_salt
        except Exception as e:
            salt = "tlas"

        node = db(db.auth_node.nodename==nodename).select().first()
        if node is None:
            raise Exception(T("node not found"))
        node_uuid = node.uuid
        sql = """select aes_decrypt(pw, "%(sec)s") from node_pw where
                 nodename="%(nodename)s"
              """ % dict(nodename=nodename, sec=node_uuid+salt)
        pwl = db.executesql(sql)
        if len(pwl) == 0:
            raise Exception(T("This node has not reported its root password (opensvc agent feature not activated or agent too old)"))

        _log('password.retrieve',
             'retrieved root password of node %(nodename)s',
             dict(nodename=nodename),
             nodename=nodename)

        return dict(data=pwl[0][0])

#
#
class rest_get_nodes(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List all node names and their selected properties.",
          "List node names and their selected properties for nodes matching a specified filterset id.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes?props=nodename,loc_city",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes",
          tables=["nodes"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = q_filter(app_field=db.nodes.app)
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_delete_node(rest_delete_handler):
    def __init__(self):
        desc = [
          "- Delete an OpenSVC node.",
          "- The user must be responsible for the node.",
          "- The user must be in the NodeManager privilege group.",
          "- Cascade delete services instances, dashboard, checks, packages and patches entries.",
          "- Log the deletion.",
          "- Send websocket change events on nodes, services instances and dashboard tables.",
        ]
        examples = [
          "# curl -u %(email)s -X DELETE -o- https://%(collector)s/init/rest/api/nodes/mynode",
        ]
        rest_delete_handler.__init__(
          self,
          path="/nodes/<nodename>",
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        check_privilege("NodeManager")
        q = db.nodes.nodename == nodename
        q = q_filter(q, app_field=db.nodes.app)
        row = db(q).select(db.nodes.id, db.nodes.nodename).first()
        if row is None:
            raise Exception("node %s does not exist" % nodename)
        node_responsible(row.nodename)

        db(q).delete()

        _log('node.delete',
             'delete node %(data)s',
             dict(data=row.nodename),
            )
        l = {
          'event': 'nodes_change',
          'data': {'id': row.id},
        }
        _websocket_send(event_msg(l))
        table_modified("nodes")

        q = db.svcmon.mon_nodname == row.nodename
        db(q).delete()
        l = {
          'event': 'svcmon_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("svcmon")

        q = db.dashboard.dash_nodename == row.nodename
        db(q).delete()
        l = {
          'event': 'dashboard_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("dashboard")

        q = db.checks_live.chk_nodename == row.nodename
        db(q).delete()
        l = {
          'event': 'checks_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("checks_live")

        q = db.packages.pkg_nodename == row.nodename
        db(q).delete()
        l = {
          'event': 'packages_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("packages")

        q = db.patches.patch_nodename == row.nodename
        db(q).delete()
        l = {
          'event': 'patches_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("patches")

        q = db.node_tags.nodename == row.nodename
        db(q).delete()
        l = {
          'event': 'node_tags_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("node_tags")

        q = db.node_ip.nodename == row.nodename
        db(q).delete()
        l = {
          'event': 'node_ip_change',
          'data': {'a': 'b'},
        }
        _websocket_send(event_msg(l))
        table_modified("node_ip")

        return dict(info="node %s deleted" % row.nodename)


#
class rest_delete_nodes(rest_delete_handler):
    def __init__(self):
        desc = [
          "- Delete OpenSVC nodes.",
          "- Cascade delete services instances, dashboard, checks, packages and patches entries.",
          "- Log the deletion.",
          "- Send websocket change events on nodes, services instances and dashboard tables.",
        ]
        examples = [
          "# curl -u %(email)s -X DELETE -o- https://%(collector)s/init/rest/api/nodes?filter[]=nodename=test%%",
        ]
        rest_delete_handler.__init__(
          self,
          path="/nodes",
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = None
        if 'nodename' in vars:
            s = vars["nodename"]
            q = db.nodes.nodename == s
        if 'id' in vars:
            s = vars["id"]
            q = db.nodes.nodename == vars["id"]
            s = str(s)
        if q is None:
            raise Exception("nodename or id key must be specified")
        q = q_filter(q, app_field=db.nodes.app)
        row = db(q).select(db.nodes.id, db.nodes.nodename).first()
        if row is None:
            raise Exception("node %s does not exist" % s)
        return rest_delete_node().handler(row.nodename)


#
class rest_post_node(rest_post_handler):
    def __init__(self):
        desc = [
          "Update a set of node properties.",
          "The user must be responsible for the node.",
          "The user must be in the NodeManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the nodes table.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d loc_city="Zanzibar" -d app="ERP" https://%(collector)s/init/rest/api/nodes/mynode""",
        ]
        rest_post_handler.__init__(
          self,
          path="/nodes/<id>",
          tables=["nodes"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        check_privilege("NodeManager")
        node_responsible(id)
        q = db.nodes.nodename == id
        vars["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # a node can not set its team responsible, for it not to gain access to
        # rulesets and safe files it should not see
        if "team_responsible" in vars and auth_is_node():
            del(vars["team_responsible"])

        row = db(q).select().first()
        if row is None:
            raise Exception("node %s does not exist" % str(id))

        vars["updated"] = datetime.datetime.now()
        if "app" in vars and (
             vars["app"] == "" or \
             vars["app"] is None or \
             not common_responsible(app=vars["app"], user_id=auth.user_id)
           ):
            vars["app"] = user_default_app()

        db(q).update(**vars)
        _log('node.change',
             'update properties %(data)s',
             dict(data=beautify_change(row, vars)),
             nodename=id)
        l = {
          'event': 'nodes_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_node().handler(id, props=','.join(["nodename","updated"]+vars.keys()))


#
class rest_post_nodes(rest_post_handler):
    def __init__(self):
        self.get_handler = rest_get_nodes()
        self.update_one_handler = rest_post_node()
        self.update_one_param = "nodename"
        desc = [
          "Create a new node",
          "Update nodes matching the specified query.",
          "If ``team_responsible``:green is not specified, default to user's primary group",
        ]
        examples = [
          """# curl -u %(email)s -o- -d nodename=mynode -d loc_city="Zanzibar" -d team_responsible="SYSADM" https://%(collector)s/init/rest/api/nodes""",
        ]
        rest_post_handler.__init__(
          self,
          path="/nodes",
          tables=["nodes"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        check_privilege("NodeManager")
        if 'nodename' not in vars:
            raise Exception("the nodename property must be set in the POST data")
        nodename = vars['nodename']

        q = db.nodes.nodename == nodename
        node = db(q).select().first()
        if node is not None:
            del(vars["nodename"])
            return rest_post_node().handler(nodename, **vars)

        vars["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "team_responsible" not in vars:
            vars["team_responsible"] = user_primary_group()

        # a node can not set its team responsible, for it not to gain access to
        # rulesets and safe files it should not see
        if "team_responsible" in vars and auth_is_node():
            del(vars["team_responsible"])

        if "app" not in vars or \
           vars["app"] == "" or \
           vars["app"] is None or \
           not common_responsible(app=vars["app"], user_id=auth.user_id):
            vars["app"] = user_default_app()

        k = dict(
          nodename=vars["nodename"],
        )
        db.nodes.update_or_insert(k, **vars)
        _log('node.add',
             'create properties %(data)s',
             dict(data=str(vars)),
             nodename=nodename)
        l = {
          'event': 'nodes_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_node().handler(nodename)


#
class rest_get_node_compliance_status(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List compliance modules' last check run on specified node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/clementine/compliance/status?query=run_status=1",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/status",
          tables=["comp_status"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.comp_status.run_nodename == nodename
        q = q_filter(q, node_field=db.comp_status.run_nodename)
        self.set_q(q)
        return self.prepare_data(**vars)

class rest_get_node_compliance_logs(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List compliance modules' check, fixable and fix logs for the node."
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/clementine/compliance/logs"
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/compliance/logs",
          tables=["comp_log"],
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.comp_log.run_nodename == nodename
        q = q_filter(q, node_field=db.comp_log.run_nodename)
        self.set_q(q)
        return self.prepare_data(**vars)

