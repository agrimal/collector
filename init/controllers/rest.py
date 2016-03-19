def call():
    session.forget()
    return service()

class rest_get_api(rest_get_handler):
    def __init__(self):
        desc = [
          "List the api available handlers."
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api"
        ]

        rest_get_handler.__init__(
          self,
          path="/",
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        data = {}
        for a in ("GET", "POST", "DELETE", "PUT"):
            data[a] = []
            for handler in get_handlers(a):
                handler.update_parameters()
                handler.update_data()
                if type(handler.data) == dict:
                    hdata = handler.data
                else:
                    hdata = {}
                data[a].append({
                  "path": handler.path,
                  "pattern": handler.get_pattern(),
                  "data": hdata,
                  "params": handler.params,
                  "examples": handler.examples,
                  "desc": handler.desc,
                })
        return dict(data=data)

def get_handlers(action=None, prefix=None):
    if action == "GET":
        return get_get_handlers(prefix=prefix)
    elif action == "POST":
        return get_post_handlers(prefix=prefix)
    elif action == "DELETE":
        return get_delete_handlers(prefix=prefix)
    elif action == "PUT":
        return get_put_handlers(prefix=prefix)
    else:
        return {
            "GET": get_get_handlers(),
            "POST": get_post_handlers(),
            "DELETE": get_delete_handlers(),
            "PUT": get_put_handlers(),
        }

def get_get_handlers(prefix=None):
    _handlers = {
       "api": [
             "rest_get_api",
       ],
       "actions": [
             "rest_get_action_queue",
             "rest_get_action_queue_stats",
             "rest_get_action_queue_one",
       ],
       "alerts": [
             "rest_get_alerts",
             "rest_get_alert",
       ],
       "alert_event": [
             "rest_get_alert_event",
       ],
       "apps": [
             "rest_get_apps",
             "rest_get_app",
             "rest_get_app_nodes",
             "rest_get_app_quotas",
             "rest_get_app_services",
             "rest_get_app_responsibles",
       ],
       "arrays": [
             "rest_get_arrays",
             "rest_get_array",
             "rest_get_array_diskgroups",
             "rest_get_array_diskgroup",
             "rest_get_array_diskgroup_quota",
             "rest_get_array_diskgroup_quotas",
             "rest_get_array_proxies",
             "rest_get_array_targets",
       ],
       "checks": [
             "rest_get_checks_settings",
             "rest_get_checks_setting",
             "rest_get_checks_contextual_settings",
             "rest_get_checks_contextual_setting",
             "rest_get_checks",
             "rest_get_check",
       ],
       "compliance": [
             "rest_get_compliance_log",
             "rest_get_compliance_logs",
             "rest_get_compliance_modulesets_export",
             "rest_get_compliance_modulesets",
             "rest_get_compliance_moduleset_usage",
             "rest_get_compliance_moduleset_export",
             "rest_get_compliance_moduleset_module",
             "rest_get_compliance_moduleset_modules",
             "rest_get_compliance_moduleset_nodes",
             "rest_get_compliance_moduleset_services",
             "rest_get_compliance_moduleset",
             "rest_get_compliance_rulesets_export",
             "rest_get_compliance_rulesets",
             "rest_get_compliance_ruleset_variables",
             "rest_get_compliance_ruleset_variable",
             "rest_get_compliance_ruleset_export",
             "rest_get_compliance_ruleset_usage",
             "rest_get_compliance_ruleset",
             "rest_get_compliance_status",
             "rest_get_compliance_status_one",
       ],
       "dns": [
             "rest_get_dns_domains",
             "rest_get_dns_domain",
             "rest_get_dns_domain_records",
             "rest_get_dns_records",
             "rest_get_dns_record",
       ],
       "filters": [
             "rest_get_filters",
             "rest_get_filter",
       ],
       "filtersets": [
             "rest_get_filtersets",
             "rest_get_filterset",
             "rest_get_filterset_usage",
             "rest_get_filterset_export",
             "rest_get_filterset_filtersets",
             "rest_get_filterset_filters",
             "rest_get_filterset_nodes",
             "rest_get_filterset_services",
       ],
       "forms": [
             "rest_get_forms_revisions",
             "rest_get_forms_revision",
             "rest_get_forms",
             "rest_get_form",
             "rest_get_form_publications",
             "rest_get_form_responsibles",
       ],
       "frontend": [
             "rest_get_frontend_hidden_menu_entries",
       ],
       "groups": [
             "rest_get_groups",
             "rest_get_group",
             "rest_get_group_apps",
             "rest_get_group_hidden_menu_entries",
             "rest_get_group_modulesets",
             "rest_get_group_nodes",
             "rest_get_group_rulesets",
             "rest_get_group_services",
             "rest_get_group_users",
       ],
       "ips": [
             "rest_get_ips",
             "rest_get_ip",
       ],
       "links": [
             "rest_get_link",
             "rest_get_links",
       ],
       "logs": [
             "rest_get_log",
             "rest_get_logs",
       ],
       "networks": [
             "rest_get_networks",
             "rest_get_network",
             "rest_get_network_ips",
             "rest_get_network_segments",
             "rest_get_network_segment",
             "rest_get_network_segment_responsibles",
             "rest_get_network_nodes",
       ],
       "nodes": [
             "rest_get_nodes",
             "rest_get_node",
             "rest_get_node_alerts",
             "rest_get_node_am_i_responsible",
             "rest_get_node_disks",
             "rest_get_node_checks",
             "rest_get_node_candidate_tags",
             "rest_get_node_compliance_modulesets",
             "rest_get_node_compliance_rulesets",
             "rest_get_node_compliance_status",
             "rest_get_node_compliance_logs",
             "rest_get_node_hbas",
             "rest_get_node_interfaces",
             "rest_get_node_ips",
             "rest_get_node_root_password",
             "rest_get_node_services",
             "rest_get_node_service",
             "rest_get_node_sysreport",
             "rest_get_node_sysreport_timediff", # keep before sysreport_commit
             "rest_get_node_sysreport_commit",
             "rest_get_node_sysreport_commit_tree",
             "rest_get_node_sysreport_commit_tree_file",
             "rest_get_node_tags",
             "rest_get_node_uuid",
       ],
       "obsolescence": [
             "rest_get_obsolescence_settings",
             "rest_get_obsolescence_setting",
       ],
       "packages": [
             "rest_get_packages_diff",
       ],
       "provisioning_templates": [
             "rest_get_provisioning_templates",
             "rest_get_provisioning_template",
             "rest_get_provisioning_template_responsibles",
       ],
       "resources": [
             "rest_get_resources",
       ],
       "search": [
             "rest_get_search",
       ],
       "services": [
             "rest_get_services",
             "rest_get_service",
             "rest_get_service_actions",
             "rest_get_service_actions_unacknowledged_errors",
             "rest_get_service_alerts",
             "rest_get_service_am_i_responsible",
             "rest_get_service_candidate_tags",
             "rest_get_service_checks",
             "rest_get_service_compliance_modulesets",
             "rest_get_service_compliance_rulesets",
             "rest_get_service_compliance_status",
             "rest_get_service_compliance_logs",
             "rest_get_service_disks",
             "rest_get_service_instances",
             "rest_get_service_nodes",
             "rest_get_service_node",
             "rest_get_service_node_resources",
             "rest_get_service_resources",
             "rest_get_service_tags",
       ],
       "services_actions": [
             "rest_get_services_actions",
       ],
       "services_instances_status_log": [
             "rest_get_services_instances_status_log",
       ],
       "services_status_log": [
             "rest_get_services_status_log",
       ],
       "scheduler": [
             "rest_get_scheduler_stats",
             "rest_get_scheduler_tasks",
             "rest_get_scheduler_task",
             "rest_get_scheduler_runs",
             "rest_get_scheduler_run",
             "rest_get_scheduler_workers",
             "rest_get_scheduler_worker",
       ],
       "forms_store": [
             "rest_get_store_forms",
             "rest_get_store_form",
       ],
       "tags": [
             "rest_get_tags_nodes",
             "rest_get_tags_services",
             "rest_get_tags",
             "rest_get_tag",
             "rest_get_tag_nodes",
             "rest_get_tag_services",
       ],
       "users": [
             "rest_get_users",
             "rest_get_user",
             "rest_get_user_apps",
             "rest_get_user_nodes",
             "rest_get_user_services",
             "rest_get_user_groups",
             "rest_get_user_hidden_menu_entries",
             "rest_get_user_primary_group",
             "rest_get_user_filterset",
             "rest_get_user_table_settings",
             "rest_get_user_table_filters",
       ],
       "reports": [
             "rest_get_reports_charts",
             "rest_get_reports_chart",
             "rest_get_reports_metrics",
             "rest_get_reports_metric",
             "rest_get_reports_metric_samples",
             "rest_get_reports_chart_samples",
             "rest_get_report_definition",
             "rest_get_report_export",
             "rest_get_reports",
             "rest_get_report",
       ],
       "safe": [
             "rest_get_safe",
             "rest_get_safe_file",
             "rest_get_safe_file_download",
             "rest_get_safe_file_publications",
             "rest_get_safe_file_responsibles",
       ],
       "sysreport": [
             "rest_get_sysreport_timeline",
             "rest_get_sysreport_nodediff",
             "rest_get_sysreport_secure_patterns",
             "rest_get_sysreport_secure_pattern",
             "rest_get_sysreport_authorizations",
             "rest_get_sysreport_authorization",
       ],
       "wiki": [
             "rest_get_wiki",
             "rest_get_wikis",
       ],
       "workflows": [
             "rest_get_workflow",
             "rest_get_workflows",
       ]
    }
    if prefix:
        return [globals()[h]() for h in _handlers[prefix]]
    data = []
    for l in _handlers.values():
        data += [globals()[h]() for h in l]
    return data


def get_delete_handlers(prefix=None):
    _handlers = {
        "actions": [
             "rest_delete_action_queue_one",
        ],
        "apps": [
             "rest_delete_apps",
             "rest_delete_app",
             "rest_delete_app_responsible",
        ],
        "apps_responsibles": [
             "rest_delete_apps_responsibles",
        ],
        "arrays": [
             "rest_delete_array_diskgroup_quotas",
             "rest_delete_array_diskgroup_quota",
        ],
        "checks": [
             "rest_delete_checks_settings",
             "rest_delete_checks_setting",
             "rest_delete_checks_contextual_settings",
             "rest_delete_checks_contextual_setting",
             "rest_delete_checks",
             "rest_delete_check",
        ],
        "compliance": [
             "rest_delete_compliance_moduleset_moduleset",
             "rest_delete_compliance_moduleset_module",
             "rest_delete_compliance_moduleset_publication",
             "rest_delete_compliance_modulesets_publications",
             "rest_delete_compliance_moduleset_responsible",
             "rest_delete_compliance_modulesets_responsibles",
             "rest_delete_compliance_moduleset_ruleset",
             "rest_delete_compliance_moduleset",
             "rest_delete_compliance_modulesets",
             "rest_delete_compliance_modulesets_nodes",
             "rest_delete_compliance_modulesets_services",
             "rest_delete_compliance_ruleset_filterset",
             "rest_delete_compliance_ruleset_publication",
             "rest_delete_compliance_rulesets_publications",
             "rest_delete_compliance_ruleset_responsible",
             "rest_delete_compliance_rulesets_responsibles",
             "rest_delete_compliance_ruleset_ruleset",
             "rest_delete_compliance_ruleset_variable",
             "rest_delete_compliance_ruleset",
             "rest_delete_compliance_rulesets",
             "rest_delete_compliance_rulesets_nodes",
             "rest_delete_compliance_rulesets_services",
             "rest_delete_compliance_status_run",
             "rest_delete_compliance_status_runs",
        ],
        "dns": [
             "rest_delete_dns_domain",
             "rest_delete_dns_domains",
             "rest_delete_dns_record",
             "rest_delete_dns_records",
        ],
        "filters": [
             "rest_delete_filter",
             "rest_delete_filters",
        ],
        "filtersets": [
             "rest_delete_filterset",
             "rest_delete_filtersets",
             "rest_delete_filterset_filterset",
             "rest_delete_filterset_filter",
        ],
        "filtersets_filtersets": [
             "rest_delete_filtersets_filtersets",
        ],
        "filtersets_filters": [
             "rest_delete_filtersets_filters",
        ],
        "forms": [
             "rest_delete_form",
             "rest_delete_forms",
             "rest_delete_form_publication",
             "rest_delete_form_responsible",
        ],
        "forms_publications": [
             "rest_delete_forms_publications",
        ],
        "forms_responsibles": [
             "rest_delete_forms_responsibles",
        ],
        "groups": [
             "rest_delete_group",
             "rest_delete_groups",
             "rest_delete_group_hidden_menu_entries",
        ],
        "ips": [
             "rest_delete_ips",
             "rest_delete_ip",
        ],
        "networks": [
             "rest_delete_network",
             "rest_delete_networks",
             "rest_delete_network_segment",
             "rest_delete_network_segment_responsible",
        ],
        "nodes": [
             "rest_delete_nodes",
             "rest_delete_node",
             "rest_delete_node_compliance_moduleset",
             "rest_delete_node_compliance_ruleset",
        ],
        "obsolescence": [
             "rest_delete_obsolescence_settings",
             "rest_delete_obsolescence_setting",
        ],
        "provisioning_templates": [
             "rest_delete_provisioning_templates",
             "rest_delete_provisioning_template",
             "rest_delete_provisioning_template_responsible",
        ],
        "provisioning_templates_responsibles": [
             "rest_delete_provisioning_templates_responsibles",
        ],
        "reports": [
             "rest_delete_reports_chart",
             "rest_delete_reports_charts",
             "rest_delete_reports_metric",
             "rest_delete_reports_metrics",
             "rest_delete_reports",
             "rest_delete_report",
        ],
        "resources": [
             "rest_delete_resource",
             "rest_delete_resources",
        ],
        "service_instances": [
             "rest_delete_service_instance",
             "rest_delete_service_instances",
        ],
        "services": [
             "rest_delete_service",
             "rest_delete_services",
             "rest_delete_service_compliance_moduleset",
             "rest_delete_service_compliance_ruleset",
        ],
        "scheduler": [
             "rest_delete_scheduler_task",
             "rest_delete_scheduler_run",
        ],
        "safe": [
             "rest_delete_safe_files_publications",
             "rest_delete_safe_files_responsibles",
             "rest_delete_safe_file_publication",
             "rest_delete_safe_file_responsible",
        ],
        "sysreport": [
             "rest_delete_sysreport_secure_pattern",
             "rest_delete_sysreport_authorization",
        ],
        "tags": [
             "rest_delete_tags_nodes",
             "rest_delete_tags_services",
             "rest_delete_tags",
             "rest_delete_tag",
             "rest_delete_tag_node",
             "rest_delete_tag_service",
        ],
        "users_groups": [
             "rest_delete_users_groups",
        ],
        "users": [
             "rest_delete_users",
             "rest_delete_user",
             "rest_delete_user_group",
             "rest_delete_user_primary_group",
             "rest_delete_user_filterset",
             "rest_delete_user_table_filters",
        ]
    }
    if prefix:
        return [globals()[h]() for h in _handlers[prefix]]
    data = []
    for l in _handlers.values():
        data += [globals()[h]() for h in l]
    return data


def get_post_handlers(prefix=None):
    _handlers = {
        "actions": [
             "rest_post_action_queue",
             "rest_post_action_queue_one",
        ],
        "apps": [
             "rest_post_apps",
             "rest_post_app",
             "rest_post_app_responsible",
        ],
        "apps_responsibles": [
             "rest_post_apps_responsibles",
        ],
        "arrays": [
             "rest_post_array_diskgroup_quotas",
             "rest_post_array_diskgroup_quota",
        ],
        "checks": [
             "rest_post_checks_contextual_settings",
             "rest_post_checks_contextual_setting",
             "rest_post_checks_settings",
             "rest_post_checks_setting",
        ],
        "compliance": [
             "rest_post_compliance_moduleset_moduleset",
             "rest_post_compliance_moduleset_module",
             "rest_post_compliance_moduleset_modules",
             "rest_post_compliance_moduleset_publication",
             "rest_post_compliance_modulesets_publications",
             "rest_post_compliance_moduleset_responsible",
             "rest_post_compliance_modulesets_responsibles",
             "rest_post_compliance_moduleset_ruleset",
             "rest_post_compliance_modulesets_nodes",
             "rest_post_compliance_modulesets_services",
             "rest_post_compliance_modulesets",
             "rest_post_compliance_moduleset",
             "rest_post_compliance_ruleset_filterset",
             "rest_post_compliance_ruleset_publication",
             "rest_post_compliance_rulesets_publications",
             "rest_post_compliance_ruleset_responsible",
             "rest_post_compliance_rulesets_responsibles",
             "rest_post_compliance_ruleset_ruleset",
             "rest_post_compliance_ruleset_variable",
             "rest_post_compliance_ruleset_variables",
             "rest_post_compliance_rulesets_nodes",
             "rest_post_compliance_rulesets_services",
             "rest_post_compliance_rulesets",
             "rest_post_compliance_ruleset",
        ],
        "dns": [
             "rest_post_dns_domains",
             "rest_post_dns_domain",
             "rest_post_dns_records",
             "rest_post_dns_record",
        ],
        "filters": [
             "rest_post_filters",
             "rest_post_filter",
        ],
        "filtersets_filtersets": [
             "rest_post_filtersets_filtersets",
        ],
        "filtersets_filters": [
             "rest_post_filtersets_filters",
        ],
        "filtersets": [
             "rest_post_filtersets",
             "rest_post_filterset",
             "rest_post_filterset_filterset",
             "rest_post_filterset_filter",
        ],
        "forms": [
             "rest_post_forms",
             "rest_post_form",
             "rest_post_form_publication",
             "rest_post_form_responsible",
        ],
        "forms_publications": [
             "rest_post_forms_publications",
        ],
        "forms_responsibles": [
             "rest_post_forms_responsibles",
        ],
        "groups": [
             "rest_post_groups",
             "rest_post_group_hidden_menu_entries",
             "rest_post_group",
        ],
        "links": [
             "rest_post_link",
        ],
        "networks": [
             "rest_post_networks",
             "rest_post_network",
             "rest_post_network_segment",
             "rest_post_network_segments",
             "rest_post_network_segment_responsible",
        ],
        "nodes": [
             "rest_post_nodes",
             "rest_post_node",
             "rest_post_node_compliance_moduleset",
             "rest_post_node_compliance_ruleset",
        ],
        "obsolescence": [
             "rest_post_obsolescence_settings",
             "rest_post_obsolescence_setting",
        ],
        "provisioning_templates": [
             "rest_post_provisioning_templates",
             "rest_post_provisioning_template",
             "rest_post_provisioning_template_responsible",
        ],
        "provisioning_templates_responsibles": [
             "rest_post_provisioning_templates_responsibles",
        ],
        "register": [
             "rest_post_register",
        ],
        "reports": [
             "rest_post_reports_chart",
             "rest_post_reports_charts",
             "rest_post_reports_metric",
             "rest_post_reports_metrics",
             "rest_post_reports_import",
             "rest_post_reports",
             "rest_post_report",
        ],
        "safe": [
             "rest_post_safe_files_publications",
             "rest_post_safe_files_responsibles",
             "rest_post_safe_upload",
             "rest_post_safe_file",
             "rest_post_safe_file_publication",
             "rest_post_safe_file_responsible",
        ],
        "scheduler": [
             "rest_post_scheduler_task",
             "rest_post_scheduler_run",
        ],
        "services": [
             "rest_post_services",
             "rest_post_service",
             "rest_post_service_compliance_moduleset",
             "rest_post_service_compliance_ruleset",
        ],
        "services_actions": [
             "rest_post_services_action",
             "rest_post_services_actions",
        ],
        "sysreport": [
             "rest_post_sysreport_secure_patterns",
             "rest_post_sysreport_authorizations",
        ],
        "tags": [
             "rest_post_tags_nodes",
             "rest_post_tags_services",
             "rest_post_tag",
             "rest_post_tags",
             "rest_post_tag_node",
             "rest_post_tag_service",
        ],
        "users": [
             "rest_post_users",
             "rest_post_user",
             "rest_post_user_group",
             "rest_post_user_primary_group",
             "rest_post_user_filterset",
             "rest_post_user_table_settings",
             "rest_post_user_table_filters",
             "rest_post_user_table_filters_load_bookmark",
             "rest_post_user_table_filters_save_bookmark",
        ],
        "users_groups": [
             "rest_post_users_groups",
        ],
        "wiki": [
             "rest_post_wikis",
        ]
    }
    if prefix:
        return [globals()[h]() for h in _handlers[prefix]]
    data = []
    for l in _handlers.values():
        data += [globals()[h]() for h in l]
    return data


def get_put_handlers(prefix=None):
    _handlers = {
        "actions": [
             "rest_put_action_queue",
        ],
        "dns": [
             "rest_put_dns_domain_sync",
        ],
        "compliance": [
             "rest_put_compliance_moduleset",
             "rest_put_compliance_ruleset",
             "rest_put_compliance_ruleset_variable",
        ],
        "forms": [
             "rest_put_form",
        ],
        "obsolescence": [
             "rest_put_obsolescence_refresh",
        ],
        "provisioning_templates": [
             "rest_put_provisioning_template",
        ],
        "services": [
             "rest_put_service_action_queue",
        ]
    }
    if prefix:
        return [globals()[h]() for h in _handlers[prefix]]
    data = []
    for l in _handlers.values():
        data += [globals()[h]() for h in l]
    return data


def rest_router(action, args, vars):
    # the default restful wrapper suppress the trailing .xxx
    # we need it for fqdn nodenames and svcname though.
    request.raw_args = request.raw_args.replace("(percent)", "%")
    args = request.raw_args.split('/')
    if args[0] == "":
        return rest_get_api().handle(*args, **vars)
    try:
        for handler in get_handlers(action, args[0]):
            if handler.match("/"+request.raw_args):
                return handler.handle(*args, **vars)
    except Exception as e:
        return dict(error=str(e))
    response.status = 404
    return dict(error="Unsupported api url")


@request.restful()
@auth.requires_login()
def api():
    def GET(*args, **vars):
        return rest_router("GET", args, vars)
    def POST(*args, **vars):
        return rest_router("POST", args, vars)
    def PUT(*args, **vars):
        return rest_router("PUT", args, vars)
    def DELETE(*args, **vars):
        return rest_router("DELETE", args, vars)
    return locals()

def doc():
    # the default restful wrapper suppress the trailing .xxx
    # we need it for fqdn nodenames and svcname though.
    args = request.raw_args.split('/')

    d = DIV(
          SCRIPT("""
            api_doc("api_doc", {args: %(args)s})
          """ % dict(args=str(args))),
          _id="api_doc",
        )
    return dict(doc=d)

def doc_load():
    return doc()["doc"]

