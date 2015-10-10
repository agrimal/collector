from gluon.dal import smart_query
import json

def moduleset_id_q(id):
    try:
        id = int(id)
        q = db.comp_moduleset.id == id
    except:
        q = db.comp_moduleset.modset_name == id
    return q

def ruleset_id_q(id):
    try:
        id = int(id)
        q = db.comp_rulesets.id == id
    except:
        q = db.comp_rulesets.ruleset_name == id
    return q

#
class rest_get_compliance_logs(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List compliance modules' check, fixable and fix logs."
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/logs?query=run_module=mymod"
        ]
        q = db.comp_log.id > 0
        q &= _where(q, 'comp_log', domain_perms(), 'run_nodename')
        rest_get_table_handler.__init__(
          self,
          path="/compliance/logs",
          tables=["comp_log"],
          q=q,
          desc=desc,
          examples=examples,
        )

#
class rest_get_compliance_log(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display properties of a module run."
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/log/10"
        ]
        rest_get_line_handler.__init__(
          self,
          path="/compliance/logs/<id>",
          tables=["comp_log"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = db.comp_log.id == int(id)
        q &= _where(q, 'comp_log', domain_perms(), 'run_nodename')
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_compliance_status(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List compliance modules' last check run."
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/status?query=run_status=1 and run_module=mymod"
        ]
        q = db.comp_status.id > 0
        q &= _where(q, 'comp_status', domain_perms(), 'run_nodename')
        rest_get_table_handler.__init__(
          self,
          path="/compliance/status",
          tables=["comp_status"],
          q=q,
          desc=desc,
          examples=examples,
        )

#
class rest_get_compliance_status_one(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display properties of the last check run of a specific module-node-service tuple"
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/status/10"
        ]
        rest_get_line_handler.__init__(
          self,
          path="/compliance/status/<id>",
          tables=["comp_status"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = db.comp_status.id == int(id)
        q &= _where(q, 'comp_status', domain_perms(), 'run_nodename')
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_delete_compliance_status_run(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete the last check run information of a specific module-node-service tuple.",
          "Requires the CompManager privilege and node ownership.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/status/10"
        ]

        rest_delete_handler.__init__(
          self,
          path="/compliance/status/<id>",
          tables=["comp_status"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        check_privilege("CompManager")
        q = db.comp_status.id == int(id)
        q &= _where(q, 'comp_status', domain_perms(), 'run_nodename')
        row = db(q).select().first()
        if row is None:
            return dict(info="Task %s does not exist in the scheduler" % id)
        node_responsible(row.run_nodename)
        db(q).delete()
        _log('rest.compliance.status.delete',
             'deleted run %(u)s',
             dict(u="-".join((row.run_module, row.run_nodename, row.run_svcname if row.run_svcname else ""))),
             nodename=row.run_nodename,
             svcname=row.run_svcname,
        )
        return dict(info="Run %s deleted" % id)

#
class rest_delete_compliance_ruleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete a ruleset.",
          "All ruleset parent and child relations are also removed.",
          "All ruleset nodes and services attachements are also removed.",
          "All ruleset publication and responsible groups are also detached.",
          "The user have the CompManager privilege.",
          "One of the user's groups must be responsible for the ruleset.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/rulesets/10"
        ]

        rest_delete_handler.__init__(
          self,
          path="/compliance/rulesets/<id>",
          tables=["comp_rulesets"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        try:
            id = int(id)
        except:
            id = comp_ruleset_id(id)
        delete_ruleset(id)
        return dict(info="Ruleset %s deleted" % id)

#
class rest_post_compliance_rulesets(rest_post_handler):
    def __init__(self):
        desc = [
          "Create a ruleset.",
          "The user have the CompManager privilege.",
          "The created ruleset inherits the user's primary group as publication and responsible groups.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the rulesets table.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d ruleset_name="testapi" https://%(collector)s/init/rest/api/compliance/rulesets""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets",
          tables=["comp_rulesets"],
          props_blacklist=["created", "author"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        ruleset_name = vars.get("ruleset_name")
        obj_id = create_ruleset(ruleset_name)
        return rest_get_compliance_ruleset().handler(obj_id)

#
class rest_delete_compliance_moduleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete a moduleset.",
          "All moduleset parent and child relations are also removed.",
          "All moduleset nodes and services attachements are also removed.",
          "All moduleset publication and responsible groups are also detached.",
          "The user have the CompManager privilege.",
          "One of the user's groups must be responsible for the moduleset.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/modulesets/10"
        ]

        rest_delete_handler.__init__(
          self,
          path="/compliance/modulesets/<id>",
          tables=["comp_moduleset"],
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        try:
            id = int(id)
        except:
            id = comp_moduleset_id(id)
        delete_moduleset(id)
        return dict(info="Moduleset %s deleted" % id)

#
class rest_post_compliance_modulesets(rest_post_handler):
    def __init__(self):
        desc = [
          "Create a moduleset.",
          "The user have the CompManager privilege.",
          "The created moduleset inherits the user's primary group as publication and responsible groups.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the modulesets table.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d modset_name="testapi" https://%(collector)s/init/rest/api/compliance/modulesets""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets",
          tables=["comp_moduleset"],
          props_blacklist=["created", "author"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        modset_name = vars.get("modset_name")
        obj_id = create_moduleset(modset_name)
        return rest_get_compliance_moduleset().handler(obj_id)

#
class rest_post_compliance_moduleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Update a set of moduleset properties.",
          "The user must be responsible for the moduleset.",
          "The user must be in the CompManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the modulesets table.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d modset_name=new_name https://%(collector)s/init/rest/api/compliance/modulesets/10""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>",
          tables=["comp_moduleset"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        check_privilege("CompManager")
        try:
            id = int(id)
        except:
            id = comp_moduleset_id(id)
        if id is None:
            return dict(error="moduleset not found")
        if not moduleset_responsible(id):
            return dict(error="you are not responsible for this moduleset")
        q = db.comp_moduleset.id == id
        vars["modset_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db(q).update(**vars)
        _log('compliance.moduleset.change',
             'update properties %(data)s',
             dict(data=str(vars)),
        )
        l = {
          'event': 'comp_moduleset_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_compliance_moduleset().handler(id, props=','.join(["modset_name"]+vars.keys()))

#
class rest_get_compliance_modulesets(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List modulesets published to the requesting user's groups.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/modulesets"
        ]

        rest_get_table_handler.__init__(
          self,
          path="/compliance/modulesets",
          tables=["comp_moduleset"],
          groupby=db.comp_moduleset.id,
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.auth_group.id.belongs(user_group_ids())
        q &= db.comp_moduleset_team_publication.group_id == db.auth_group.id
        q &= db.comp_moduleset_team_publication.modset_id == db.comp_moduleset.id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_compliance_moduleset(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display the moduleset properties, if published to the requesting users's group.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/modulesets/2"
        ]

        rest_get_line_handler.__init__(
          self,
          path="/compliance/modulesets/<id>",
          tables=["comp_moduleset"],
          groupby=db.comp_moduleset.id,
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = db.auth_group.id.belongs(user_group_ids())
        q &= moduleset_id_q(id)
        q &= db.comp_moduleset_team_publication.group_id == db.auth_group.id
        q &= db.comp_moduleset_team_publication.modset_id == db.comp_moduleset.id
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_compliance_moduleset_export(rest_get_handler):
    def __init__(self):
        desc = [
          "Export the moduleset in a JSON format compatible with the import handler.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/modulesets/2/export"
        ]

        rest_get_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/export",
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        try:
            id = int(id)
        except:
            id = comp_moduleset_id(id)
        return _export_modulesets([id])


#
class rest_get_compliance_modulesets_export(rest_get_handler):
    def __init__(self):
        desc = [
          "Export all modulesets in a JSON format compatible with the import handler.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/modulesets/2/export"
        ]

        rest_get_handler.__init__(
          self,
          path="/compliance/modulesets/export",
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.auth_group.id.belongs(user_group_ids())
        q &= db.comp_moduleset.id > 0
        q &= db.comp_moduleset_team_publication.group_id == db.auth_group.id
        q &= db.comp_moduleset_team_publication.modset_id == db.comp_moduleset.id
        ids = [r.id for r in db(q).select(db.comp_moduleset.id)]
        return _export_modulesets(ids)


#
class rest_get_compliance_rulesets(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List rulesets published to the requesting users's group.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/rulesets"
        ]

        rest_get_table_handler.__init__(
          self,
          path="/compliance/rulesets",
          tables=["comp_rulesets"],
          groupby=db.comp_rulesets.id,
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.auth_group.id.belongs(user_group_ids())
        q &= db.comp_ruleset_team_publication.group_id == db.auth_group.id
        q &= db.comp_ruleset_team_publication.ruleset_id == db.comp_rulesets.id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_compliance_ruleset(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display the ruleset properties, if published to the requesting users's group.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/rulesets/2"
        ]

        rest_get_line_handler.__init__(
          self,
          path="/compliance/rulesets/<id>",
          tables=["comp_rulesets"],
          groupby=db.comp_rulesets.id,
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        q = db.auth_group.id.belongs(user_group_ids())
        q &= ruleset_id_q(id)
        q &= db.comp_ruleset_team_publication.group_id == db.auth_group.id
        q &= db.comp_ruleset_team_publication.ruleset_id == db.comp_rulesets.id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_compliance_ruleset_export(rest_get_handler):
    def __init__(self):
        desc = [
          "Export the ruleset in a JSON format compatible with the import handler.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/rulesets/2/export"
        ]

        rest_get_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/export",
          desc=desc,
          examples=examples,
        )

    def handler(self, id, **vars):
        try:
            id = int(id)
        except:
            id = comp_ruleset_id(id)
        return _export_rulesets([id])


#
class rest_get_compliance_rulesets_export(rest_get_handler):
    def __init__(self):
        desc = [
          "Export all rulesets in a JSON format compatible with the import handler.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/rulesets/export"
        ]

        rest_get_handler.__init__(
          self,
          path="/compliance/rulesets/export",
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.auth_group.id.belongs(user_group_ids())
        q &= db.comp_rulesets.id > 0
        q &= db.comp_ruleset_team_publication.group_id == db.auth_group.id
        q &= db.comp_ruleset_team_publication.ruleset_id == db.comp_rulesets.id
        ids = [r.id for r in db(q).select(db.comp_rulesets.id)]
        return _export_rulesets(ids)


#
class rest_delete_compliance_moduleset_moduleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a moduleset from a moduleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/modulesets/10/modulesets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, parent_modset_id, child_modset_id, **vars):
        try:
            parent_modset_id = int(parent_modset_id)
        except:
            parent_modset_id = comp_moduleset_id(parent_modset_id)
        try:
            child_modset_id = int(child_modset_id)
        except:
            child_modset_id = comp_moduleset_id(child_modset_id)
        try:
            detach_moduleset_from_moduleset(child_modset_id, parent_modset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="moduleset detached")

#
class rest_post_compliance_moduleset_moduleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a moduleset to a moduleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/modulesets/10/modulesets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, parent_modset_id, child_modset_id, **vars):
        try:
            parent_modset_id = int(parent_modset_id)
        except:
            parent_modset_id = comp_moduleset_id(parent_modset_id)
        try:
            child_modset_id = int(child_modset_id)
        except:
            child_modset_id = comp_moduleset_id(child_modset_id)
        try:
            attach_moduleset_to_moduleset(child_modset_id, parent_modset_id)
        except CompError as e:
            return dict(error=str(e))
        except CompInfo as e:
            return dict(info=str(e))
        return dict(info="moduleset attached")

#
class rest_delete_compliance_moduleset_ruleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a ruleset from a moduleset",
          "Attached rulesets add their variables to the moduleset's modules execution environment.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/modulesets/10/rulesets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/rulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, rset_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        try:
            rset_id = int(rset_id)
        except:
            rset_id = comp_ruleset_id(rset_id)
        try:
            detach_ruleset_from_moduleset(rset_id, modset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="ruleset detached")

#
class rest_post_compliance_moduleset_ruleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a ruleset to a moduleset",
          "Attached rulesets add their variables to the moduleset's modules execution environment.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/modulesets/10/rulesets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/rulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, rset_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        try:
            rset_id = int(rset_id)
        except:
            rset_id = comp_ruleset_id(rset_id)
        try:
            attach_ruleset_to_moduleset(rset_id, modset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="ruleset attached")

#
class rest_delete_compliance_ruleset_ruleset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a ruleset from a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/rulesets/10/rulesets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/rulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, parent_rset_id, child_rset_id, **vars):
        try:
            parent_rset_id = int(parent_rset_id)
        except:
            parent_rset_id = comp_ruleset_id(parent_rset_id)
        try:
            child_rset_id = int(child_rset_id)
        except:
            child_rset_id = comp_ruleset_id(child_rset_id)
        try:
            detach_ruleset_from_ruleset(child_rset_id, parent_rset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="ruleset detached")

#
class rest_post_compliance_ruleset_ruleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a ruleset to a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/rulesets/10/rulesets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/rulesets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, parent_rset_id, child_rset_id, **vars):
        try:
            parent_rset_id = int(parent_rset_id)
        except:
            parent_rset_id = comp_ruleset_id(parent_rset_id)
        try:
            child_rset_id = int(child_rset_id)
        except:
            child_rset_id = comp_ruleset_id(child_rset_id)
        try:
            attach_ruleset_to_ruleset(child_rset_id, parent_rset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="ruleset attached")

#
class rest_post_compliance_ruleset(rest_post_handler):
    def __init__(self):
        desc = [
          "Update a set of ruleset properties.",
          "The user must be responsible for the ruleset.",
          "The user must be in the CompManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
          "A websocket event is sent to announce the change in the rulesets table.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d public=true https://%(collector)s/init/rest/api/compliance/rulesets/10""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>",
          tables=["comp_rulesets"],
          desc=desc,
          examples=examples
        )

    def handler(self, id, **vars):
        check_privilege("CompManager")
        try:
            id = int(id)
        except:
            id = comp_ruleset_id(id)
        if id is None:
            return dict(error="ruleset not found")
        if not ruleset_responsible(id):
            return dict(error="you are not responsible for this ruleset")
        q = db.comp_rulesets.id == id
        #vars["ruleset_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db(q).update(**vars)
        _log('compliance.ruleset.change',
             'update properties %(data)s',
             dict(data=str(vars)),
        )
        l = {
          'event': 'comp_rulesets_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_compliance_ruleset().handler(id, props=','.join(["ruleset_name"]+vars.keys()))


#
# rulesets/<id>/variables
#
class rest_get_compliance_ruleset_variables(rest_get_table_handler):
    def __init__(self):
        desc = [
          "Display a ruleset variables.",
          "The user must be member of one of the ruleset publication groups.",
        ]
        examples = [
          """# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/rulesets/10/variables""",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/variables",
          tables=["comp_rulesets_variables"],
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        if not ruleset_publication(ruleset_id):
            return dict(error="you are not member of one of the ruleset publication groups")
        q = db.comp_rulesets_variables.ruleset_id == ruleset_id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_compliance_ruleset_variable(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display a ruleset variable properties.",
          "The user must be member of one of the ruleset publication groups.",
        ]
        examples = [
          """# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/rulesets/10/variables/40""",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/variables/<id>",
          tables=["comp_rulesets_variables"],
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, var_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        if not ruleset_publication(ruleset_id):
            return dict(error="you are not member of one of the ruleset publication groups")
        try:
            var_id = int(var_id)
        except:
            var_id = comp_ruleset_variable_id(ruleset_id, var_id)
        if var_id is None:
            return dict(error="variable not found")
        q = db.comp_rulesets_variables.ruleset_id == ruleset_id
        q &= db.comp_rulesets_variables.id == var_id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_delete_compliance_ruleset_variable(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete a ruleset variable.",
          "The user must be responsible for the ruleset.",
          "The user must be in the CompManager privilege group.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          """# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/rulesets/10/variables/40""",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/variables/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, var_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        if not ruleset_publication(ruleset_id):
            return dict(error="you are not member of one of the ruleset publication groups")
        try:
            var_id = int(var_id)
        except:
            var_id = comp_ruleset_variable_id(ruleset_id, var_id)
        if var_id is None:
            return dict(error="variable not found")
        q = db.comp_rulesets_variables.ruleset_id == ruleset_id
        q &= db.comp_rulesets_variables.id == var_id
        db(q).delete()
        return dict(info="variable deleted")

#
class rest_post_compliance_ruleset_variable(rest_post_handler):
    def __init__(self):
        desc = [
          "Modify a ruleset variable properties.",
          "The user must be responsible for the ruleset.",
          "The user must be in the CompManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d var_class=raw-d var_value=bar https://%(collector)s/init/rest/api/compliance/rulesets/10/variables/40""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/variables/<id>",
          tables=["comp_rulesets_variables"],
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, var_id, **vars):
        check_privilege("CompManager")
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        if not ruleset_responsible(ruleset_id):
            return dict(error="you are not responsible for this ruleset")
        try:
            var_id = int(var_id)
        except:
            var_id = comp_ruleset_variable_id(ruleset_id, var_id)
        if var_id is None:
            return dict(error="variable not found")
        q = db.comp_rulesets_variables.ruleset_id == ruleset_id
        q &= db.comp_rulesets_variables.id == var_id
        if db(q).count() == 0:
            return dict(error="this variable name already exists")
        vars["var_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vars["var_author"] = user_name()
        vars["ruleset_id"] = ruleset_id
        db(q).update(**vars)
        _log('compliance.ruleset.variable.change',
             'changed properties %(data)s',
             dict(data=str(vars)),
        )
        l = {
          'event': 'comp_rulesets_variables_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_compliance_ruleset_variable().handler(ruleset_id, var_id)

#
class rest_post_compliance_ruleset_variables(rest_post_handler):
    def __init__(self):
        desc = [
          "Create a variable in a ruleset",
          "The user must be responsible for the ruleset.",
          "The user must be in the CompManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d public=true https://%(collector)s/init/rest/api/compliance/rulesets/10/variables""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/variables",
          tables=["comp_rulesets_variables"],
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, **vars):
        check_privilege("CompManager")
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        if not ruleset_responsible(ruleset_id):
            return dict(error="you are not responsible for this ruleset")
        if "var_name" not in vars:
            return dict(error="var_name is mandatory in the posted data")
        q = db.comp_rulesets_variables.ruleset_id == ruleset_id
        q &= db.comp_rulesets_variables.var_name == vars["var_name"]
        if db(q).count() > 0:
            return dict(error="this variable name already exists")
        vars["var_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vars["var_author"] = user_name()
        vars["ruleset_id"] = ruleset_id
        obj_id = db.comp_rulesets_variables.insert(**vars)
        _log('compliance.ruleset.variable.create',
             'properties %(data)s',
             dict(data=str(vars)),
        )
        l = {
          'event': 'comp_rulesets_variables_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_compliance_ruleset_variable().handler(ruleset_id, obj_id)

#
# modulesets/<id>/modules
#
class rest_get_compliance_moduleset_modules(rest_get_table_handler):
    def __init__(self):
        desc = [
          "Display a moduleset modules.",
          "The user must be member of one of the moduleset publication groups.",
        ]
        examples = [
          """# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/modulesets/10/modules""",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modules",
          tables=["comp_moduleset_modules"],
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        if modset_id is None:
            return dict(error="moduleset not found")
        if not moduleset_publication(modset_id):
            return dict(error="you are not member of one of the moduleset publication groups")
        q = db.comp_moduleset_modules.modset_id == modset_id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_compliance_moduleset_module(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display a moduleset module properties.",
          "The user must be member of one of the moduleset publication groups.",
        ]
        examples = [
          """# curl -u %(email)s -o- https://%(collector)s/init/rest/api/compliance/modulesets/10/modules/40""",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modules/<id>",
          tables=["comp_moduleset_modules"],
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, mod_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        if modset_id is None:
            return dict(error="moduleset not found")
        if not moduleset_publication(modset_id):
            return dict(error="you are not member of one of the moduleset publication groups")
        try:
            mod_id = int(mod_id)
        except:
            mod_id = comp_moduleset_module_id(modset_id, mod_id)
        if mod_id is None:
            return dict(error="module not found")
        q = db.comp_moduleset_modules.modset_id == modset_id
        q &= db.comp_moduleset_modules.id == mod_id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_delete_compliance_moduleset_module(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete a moduleset module.",
          "The user must be responsible for the moduleset.",
          "The user must be in the CompManager privilege group.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          """# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/modulesets/10/modules/40""",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modules/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, mod_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        if modset_id is None:
            return dict(error="moduleset not found")
        if not moduleset_publication(modset_id):
            return dict(error="you are not member of one of the moduleset publication groups")
        try:
            mod_id = int(mod_id)
        except:
            mod_id = comp_moduleset_module_id(modset_id, mod_id)
        if mod_id is None:
            return dict(error="module not found")
        q = db.comp_moduleset_modules.modset_id == modset_id
        q &= db.comp_moduleset_modules.id == mod_id
        db(q).delete()
        return dict(info="module deleted")

#
class rest_post_compliance_moduleset_module(rest_post_handler):
    def __init__(self):
        desc = [
          "Modify a moduleset module properties.",
          "The user must be responsible for the moduleset.",
          "The user must be in the CompManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d var_class=raw-d var_value=bar https://%(collector)s/init/rest/api/compliance/modulesets/10/modules/40""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modules/<id>",
          tables=["comp_moduleset_modules"],
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, mod_id, **vars):
        check_privilege("CompManager")
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        if modset_id is None:
            return dict(error="moduleset not found")
        if not moduleset_responsible(modset_id):
            return dict(error="you are not responsible for this moduleset")
        try:
            mod_id = int(mod_id)
        except:
            mod_id = comp_moduleset_module_id(modset_id, mod_id)
        if mod_id is None:
            return dict(error="module not found")
        q = db.comp_moduleset_modules.modset_id == modset_id
        q &= db.comp_moduleset_modules.id == mod_id
        if db(q).count() == 0:
            return dict(error="this module name already exists")
        vars["modset_mod_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vars["modset_mod_author"] = user_name()
        vars["modset_id"] = modset_id
        db(q).update(**vars)
        _log('compliance.moduleset.module.change',
             'changed properties %(data)s',
             dict(data=str(vars)),
        )
        l = {
          'event': 'comp_moduleset_modules_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_compliance_moduleset_module().handler(modset_id, mod_id)

#
class rest_post_compliance_moduleset_modules(rest_post_handler):
    def __init__(self):
        desc = [
          "Create a module in a moduleset",
          "The user must be responsible for the moduleset.",
          "The user must be in the CompManager privilege group.",
          "The updated timestamp is automatically updated.",
          "The action is logged in the collector's log.",
        ]
        examples = [
          """# curl -u %(email)s -o- -d public=true https://%(collector)s/init/rest/api/compliance/modulesets/10/modules""",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/modules",
          tables=["comp_moduleset_modules"],
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, **vars):
        check_privilege("CompManager")
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        if modset_id is None:
            return dict(error="moduleset not found")
        if not moduleset_responsible(modset_id):
            return dict(error="you are not responsible for this moduleset")
        if "modset_mod_name" not in vars:
            return dict(error="modset_mod_name is mandatory in the posted data")
        q = db.comp_moduleset_modules.modset_id == modset_id
        q &= db.comp_moduleset_modules.modset_mod_name == vars["modset_mod_name"]
        if db(q).count() > 0:
            return dict(error="this module name already exists")
        vars["modset_mod_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vars["modset_mod_author"] = user_name()
        vars["modset_id"] = modset_id
        obj_id = db.comp_moduleset_modules.insert(**vars)
        _log('compliance.moduleset.module.create',
             'properties %(data)s',
             dict(data=str(vars)),
        )
        l = {
          'event': 'comp_moduleset_modules_change',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_compliance_moduleset_module().handler(modset_id, obj_id)

#
# groups
#
class rest_post_compliance_moduleset_publication(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a publication group to a moduleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/modulesets/10/publications/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/publications/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, group_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            attach_group_to_moduleset(group_id, modset_id, gtype="publication")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group attached")

class rest_delete_compliance_moduleset_publication(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a publication group from a moduleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/modulesets/10/publications/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/publications/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, group_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            detach_group_from_moduleset(group_id, modset_id, gtype="publication")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group detached")

class rest_post_compliance_moduleset_responsible(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a responsible group to a moduleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/modulesets/10/responsibles/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/responsibles/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, group_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            attach_group_to_moduleset(group_id, modset_id, gtype="responsible")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group attached")

class rest_delete_compliance_moduleset_responsible(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a responsible group from a moduleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/modulesets/10/responsibles/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/modulesets/<id>/responsibles/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, modset_id, group_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            detach_group_from_moduleset(group_id, modset_id, gtype="responsible")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group detached")

class rest_post_compliance_ruleset_publication(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a publication group to a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/rulesets/10/publications/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/publications/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, group_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            attach_group_to_ruleset(group_id, ruleset_id, gtype="publication")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group attached")

class rest_delete_compliance_ruleset_publication(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a publication group from a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/rulesets/10/publications/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/publications/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, group_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            detach_group_from_ruleset(group_id, ruleset_id, gtype="publication")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group detached")

class rest_post_compliance_ruleset_responsible(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a responsible group to a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/rulesets/10/responsibles/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/responsibles/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, group_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            attach_group_to_ruleset(group_id, ruleset_id, gtype="responsible")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group attached")

class rest_delete_compliance_ruleset_responsible(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a responsible group from a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/rulesets/10/responsibles/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/responsibles/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, group_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        try:
            group_id = int(group_id)
        except:
            group_id = lib_group_id(group_id)
        try:
            detach_group_from_ruleset(group_id, ruleset_id, gtype="responsible")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="group detached")

#
# ruleset/filterset
#
class rest_post_compliance_ruleset_filterset(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a filterset to a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/compliance/rulesets/10/filtersets/151",
        ]
        rest_post_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/filtersets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, fset_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        try:
            fset_id = int(fset_id)
        except:
            fset_id = lib_filterset_id(fset_id)
        if fset_id is None:
            return dict(error="filterset not found")
        try:
            attach_filterset_to_ruleset(fset_id, ruleset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="filterset attached")

class rest_delete_compliance_ruleset_filterset(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a filterset from a ruleset",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/compliance/rulesets/10/filtersets/151",
        ]
        rest_delete_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/filtersets/<id>",
          desc=desc,
          examples=examples
        )

    def handler(self, ruleset_id, fset_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        try:
            detach_filterset_from_ruleset(ruleset_id)
        except CompError as e:
            return dict(error=str(e))
        return dict(info="filterset detached")

class rest_put_compliance_ruleset_variable(rest_put_handler):
    def __init__(self):
        desc = [
          "Special actions on a ruleset variable: copy, move.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X PUT -d action=copy -d dst_ruleset_id=152 https://%(collector)s/init/rest/api/compliance/rulesets/10/variables/151",
        ]
        data = """
----
| **action**      | move or copy                                                  |
| **dst_ruleset** | The name or id of the ruleset to move or copy the variable to |
----
"""
        rest_put_handler.__init__(
          self,
          path="/compliance/rulesets/<id>/variables/<id>",
          desc=desc,
          data=data,
          examples=examples
        )

    def handler(self, ruleset_id, var_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        try:
            var_id = int(var_id)
        except:
            var_id = comp_ruleset_variable_id(ruleset_id, var_id)
        if var_id is None:
            return dict(error="variable not found")
        dst_ruleset =  vars.get("dst_ruleset")
        if dst_ruleset is None:
            return dict(error="dst_ruleset not found in data")
        try:
            dst_ruleset = int(dst_ruleset)
        except:
            dst_ruleset = comp_ruleset_id(dst_ruleset)
        if dst_ruleset is None:
            return dict(error="dst_ruleset not found")
        action = vars.get("action")
        try:
            if action == "copy":
                copy_variable_to_ruleset(var_id, dst_ruleset)
            elif action == "move":
                move_variable_to_ruleset(var_id, dst_ruleset)
            else:
                raise CompError("unsupported action")
        except CompError as e:
            return dict(error=str(e))
        return dict(info="variable %s done"%action)

class rest_put_compliance_ruleset(rest_put_handler):
    def __init__(self):
        desc = [
          "Special actions on a ruleset: clone.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X PUT -d action=clone https://%(collector)s/init/rest/api/compliance/rulesets/10",
        ]
        data = """
----
| **action**      | clone |
----
"""
        rest_put_handler.__init__(
          self,
          path="/compliance/rulesets/<id>",
          desc=desc,
          data=data,
          examples=examples
        )

    def handler(self, ruleset_id, **vars):
        try:
            ruleset_id = int(ruleset_id)
        except:
            ruleset_id = comp_ruleset_id(ruleset_id)
        if ruleset_id is None:
            return dict(error="ruleset not found")
        action = vars.get("action")
        try:
            if action == "clone":
                d = clone_ruleset(ruleset_id)
                info = "clone done. new ruleset name %s" % d.get("name", "?")
            else:
                raise CompError("unsupported action")
        except CompError as e:
            return dict(error=str(e))
        return dict(info=info)

class rest_put_compliance_moduleset(rest_put_handler):
    def __init__(self):
        desc = [
          "Special actions on a moduleset: clone.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X PUT -d action=clone https://%(collector)s/init/rest/api/compliance/modulesets/10",
        ]
        data = """
----
| **action**      | clone |
----
"""
        rest_put_handler.__init__(
          self,
          path="/compliance/modulesets/<id>",
          desc=desc,
          data=data,
          examples=examples
        )

    def handler(self, modset_id, **vars):
        try:
            modset_id = int(modset_id)
        except:
            modset_id = comp_moduleset_id(modset_id)
        if modset_id is None:
            return dict(error="moduleset not found")
        action = vars.get("action")
        try:
            if action == "clone":
                d = clone_moduleset(modset_id)
                info = "clone done. new moduleset name %s" % d.get("name", "?")
            else:
                raise CompError("unsupported action")
        except CompError as e:
            return dict(error=str(e))
        return dict(info=info)


