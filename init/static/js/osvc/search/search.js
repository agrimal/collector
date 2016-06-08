function search_get_menu(fk)
{
  var menu = {
    "modulesets": {
        "tab" : 'moduleset_tabs("__rowid__", {"modset_id": "__id__", "modset_name": "__modset_name__"})',
        "title": "__modset_name__",
        "menu_entry_id": "comp-modulesets",
        "class": "modset16 fa-2x search-section-icon",
        "subclass": "meta_moduleset clickable",
        "links": []
    },
    "rulesets": {
        "tab" : 'ruleset_tabs("__rowid__", {"ruleset_id": "__id__", "ruleset_name": "__ruleset_name__"})',
        "title": "__ruleset_name__",
        "menu_entry_id": "comp-rulesets",
        "class": "rset16 fa-2x search-section-icon",
        "subclass": "meta_ruleset clickable",
        "links": []
    },
    "reports": {
        "tab" : 'report_tabs("__rowid__", {"report_id": "__id__", "report_name": "__report_name__"})',
        "title": "__report_name__",
        "menu_entry_id": "adm-reports",
        "class": "spark16 fa-2x search-section-icon",
        "subclass": "meta_report clickable",
        "links": []
    },
    "charts": {
        "tab" : 'chart_tabs("__rowid__", {"chart_id": "__id__", "chart_name": "__chart_name__"})',
        "title": "__chart_name__",
        "menu_entry_id": "adm-charts",
        "class": "spark16 fa-2x search-section-icon",
        "subclass": "meta_chart clickable",
        "links": []
    },
    "metrics": {
        "tab" : 'metric_tabs("__rowid__", {"metric_id": "__id__", "metric_name": "__metric_name__"})',
        "title": "__metric_name__",
        "menu_entry_id": "adm-metrics",
        "class": "spark16 fa-2x search-section-icon",
        "subclass": "meta_metric clickable",
        "links": []
    },
    "forms": {
        "tab" : 'form_tabs("__rowid__", {"form_id": "__id__", "form_name": "__form_name__"})',
        "title": "__form_name__",
        "menu_entry_id": "adm-forms",
        "class": "wf16 fa-2x search-section-icon",
        "subclass": "meta_form clickable",
        "links" : [
          {
            "title": "request",
            "menu_entry_id": "req-new",
            "class": "wf16",
            "link": "/init/forms/forms?form_name=__form_name__",
            "fn": "forms",
            "options": {"form_name": "__form_name__"}
          },
          {
            "title": "forms",
            "menu_entry_id": "adm-forms",
            "class": "wf16",
            "link": "/init/forms/forms_admin?volatile_filters=true&forms_f_form_name=__form_name__",
            "fn": "table_forms",
            "options": {"volatile_filters": true, "request_vars": {"forms_f_form_name": "__form_name__"}}
          }
        ]
    },
    "users": {
        "tab" : 'user_tabs("__rowid__", {"user_id": "__id__", "fullname": "__fullname__"})',
        "title": "__fullname__ <__email__>",
        "menu_entry_id": "adm-usr",
        "class": "guy16 fa-2x search-section-icon",
        "subclass": "meta_username clickable",
        "links" : [
          {
            "title": "users",
            "menu_entry_id": "adm-usr",
            "class": "guys16",
            "link": "/init/users/users?volatile_filters=true&users_f_id=__id__",
            "fn": "table_users",
            "options": {"volatile_filters": true, "request_vars": {"users_f_id": "__id__"}}
          },
          {
            "title": "logs",
            "menu_entry_id": "adm-log",
            "class": "log16",
            "link": "/init/log/log?volatile_filters=true&log_f_log_user=__fullname__",
            "fn": "table_log",
            "options": {"volatile_filters": true, "request_vars": {"log_f_log_user": "__fullname__"}}
          },
        ]
    },
    "safe_files": {
        "tab" : 'safe_file_tabs("__rowid__", {"uuid": "__uuid__", "name": "__name__"})',
        "title": "__name__ (__uuid__)",
        "menu_entry_id": "view-safe",
        "class": "safe16 fa-2x search-section-icon",
        "subclass": "meta_safe_file",
        "links" : []
    },
    "disks": {
        "title": "__disk_id__",
        "menu_entry_id": "view-disks",
        "class": "hd16 fa-2x search-section-icon",
        "subclass": "meta_app",
        "links" : [
          {
            "title": "disk_info",
            "menu_entry_id": "view-disks",
            "class": "hd16",
            "link": "/init/disks/disks?volatile_filters=true&disks_f_disk_id=__disk_id__"
          }
        ]
    },
    "apps": {
        "title": "__app__",
        "tab" : 'app_tabs("__rowid__", {"app_name": "__app__"})',
        "menu_entry_id": "view-dummy",
        "class": "app16 fa-2x search-section-icon",
        "subclass": "meta_app clickable",
        "links" : [
          {
            "title": "nodes",
            "menu_entry_id": "view-nodes",
            "class": "hw16",
            "link": "/init/nodes/nodes?volatile_filters=true&nodes_f_app=__app__",
            "fn": "view_nodes",
            "options": {"volatile_filters": true, "request_vars": {"nodes_f_app": "__app__"}}
          },
          {
            "title": "status",
            "menu_entry_id": "view-service-instances",
            "class": "svc",
            "link": "/init/default/svcmon?volatile_filters=true&svcmon_f_svc_app=__app__",
            "fn": "table_service_instances",
            "options": {"volatile_filters": true, "request_vars": {"svcmon_f_svc_app": "__app__"}}
          },
          {
            "title": "disk_info",
            "menu_entry_id": "view-disks",
            "class": "hd16",
            "link": "/init/disks/disks?volatile_filters=true&disks_f_app=__app__"
          },
          {
            "title": "saves",
            "menu_entry_id": "view-saves",
            "class": "cd16",
            "link": "/init/saves/saves?volatile_filters=true&saves_f_save_app=__app__",
            "fn": "view_saves",
            "options": {"volatile_filters": true, "request_vars": {"saves_f_save_app": "__app__"}}
          },
          {
            "title": "availability",
            "menu_entry_id": "stat-avail",
            "class": "avail16",
            "link": "/init/svcmon_log/svcmon_log?volatile_filters=true&svcmon_log_f_svc_app=__app__"
          },
          {
            "title": "app",
            "menu_entry_id": "adm-app",
            "class": "svc",
            "link": "/init/apps/apps?volatile_filters=true&apps_f_app=__app__",
            "fn": "table_apps",
            "options": {"volatile_filters": true, "request_vars": {"apps_f_app": "__app__"}}
          }
        ]
    },
    "ips": {
        "title": "__node_ip.addr__@__nodes.nodename__  *__nodes.app__",
        "menu_entry_id": "view-node-net",
        "class": "net16 fa-2x search-section-icon",
        "subclass": "meta_username",
        "links" : [
          {
            "title": "nodes",
            "menu_entry_id": "view-nodes",
            "class": "hw16",
            "link": "/init/nodes/nodes?volatile_filters=true&nodes_f_node_id=__nodes.node_id__",
            "fn": "view_nodes",
            "options": {"volatile_filters": true, "request_vars": {"nodes_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "dashboard",
            "menu_entry_id": "view-dashboard",
            "class": "alert16",
            "link": "/init/dashboard/index?volatile_filters=true&dashboard_f_node_id=__nodes.node_id__",
            "fn": "table_dashboard",
            "options": {"volatile_filters": true, "request_vars": {"dashboard_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "services",
            "menu_entry_id": "view-services",
            "class": "svc",
            "link": "/init/default/svcmon?volatile_filters=true&svcmon_f_node_id=__nodes.node_id__",
            "fn": "table_service_instances",
            "options": {"volatile_filters": true, "request_vars": {"svcmon_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "resources",
            "menu_entry_id": "view-resources",
            "class": "svc",
            "link": "/init/resmon/resmon?volatile_filters=true&resmon_f_node_id=__nodes.node_id__",
            "fn": "table_resources",
            "options": {"volatile_filters": true, "request_vars": {"resmon_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "resinfo",
            "menu_entry_id": "view-resinfo",
            "class": "svc",
            "link": "/init/resinfo/resinfo?volatile_filters=true&resinfo_f_node_id=__nodes.node_id__",
            "fn": "table_resinfo",
            "options": {"volatile_filters": true, "request_vars": {"resinfo_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "actions",
            "menu_entry_id": "view-actions",
            "class": "action16",
            "link": "/init/svcactions/svcactions?volatile_filters=true&actions_f_node_id=__nodes.node_id__",
            "fn": "table_actions",
            "options": {"volatile_filters": true, "request_vars": {"actions_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "checks",
            "menu_entry_id": "view-checks",
            "class": "check16",
            "link": "/init/checks/checks?volatile_filters=true&checks_f_node_id=__nodes.node_id__",
            "fn": "table_checks",
            "options": {"volatile_filters": true, "request_vars": {"checks_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "packages",
            "menu_entry_id": "view-pkg",
            "class": "pkg16",
            "link": "/init/packages/packages?volatile_filters=true&packages_f_node_id=__nodes.node_id__",
            "fn": "table_packages",
            "options": {"volatile_filters": true, "request_vars": {"packages_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "network",
            "menu_entry_id": "view-net",
            "class": "net16",
            "link": "/init/nodenetworks/nodenetworks?volatile_filters=true&nodenetworks_f_node_id=__nodes.node_id__",
            "fn": "table_nodenetworks",
            "options": {"volatile_filters": true, "request_vars": {"nodenetworks_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "san",
            "menu_entry_id": "view-san",
            "class": "net16",
            "link": "/init/nodesan/nodesan?volatile_filters=true&nodesan_f_node_id=__nodes.node_id__",
            "fn": "table_nodesan",
            "options": {"volatile_filters": true, "request_vars": {"nodesan_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "disks",
            "menu_entry_id": "view-disks",
            "class": "hd16",
            "link": "/init/disks/disks?volatile_filters=true&disks_f_disk_nodename=__nodename__"
          },
          {
            "title": "saves",
            "menu_entry_id": "view-saves",
            "class": "cd16",
            "link": "/init/saves/saves?volatile_filters=true&saves_f_save_nodename=__nodename__",
            "fn": "view_saves",
            "options": {"volatile_filters": true, "request_vars": {"saves_f_save_nodename": "__nodename__"}}
          },
          {
            "title": "compliance_status",
            "menu_entry_id": "comp-status",
            "class": "comp16",
            "link": "/init/compliance/comp_status?volatile_filters=true&cs0_f_node_id=__nodes.node_id__",
            "fn": "view_comp_status",
            "options": {"volatile_filters": true, "request_vars": {"cs0_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "compliance_log",
            "menu_entry_id": "comp-log",
            "class": "log16",
            "link": "/init/compliance/comp_log?volatile_filters=true&comp_log_f_node_id=__nodes.node_id__",
            "fn": "table_comp_log",
            "options": {"volatile_filters": true, "request_vars": {"comp_log_f_node_id": "__nodes.node_id__"}}
          },
          {
            "title": "logs",
            "menu_entry_id": "adm-log",
            "class": "log16",
            "link": "/init/log/log?volatile_filters=true&log_f_node_id=__nodes.node_id__",
            "fn": "table_log",
            "options": {"volatile_filters": true, "request_vars": {"log_f_node_id": "__nodes.node_id__"}}
          }
        ],
        "special_header_links" : [
          {
            "title": "nodes_net",
            "menu_entry_id": "view-node-net",
            "class": "hw16",
            "link": "/init/nodenetworks/nodenetworks?volatile_filters=true&nodenetworks_f_addr=__addr__",
            "fn": "table_nodenetworks",
            "options": {"volatile_filters": true, "request_vars": {"nodenetworks_f_addr": "__addr__"}}
          }
        ]
    },
    "groups": {
        "tab" : 'group_tabs("__rowid__", {"group_id": "__id__", "group_name": "__role__"})',
        "title": "__role__",
        "menu_entry_id": "adm-usr",
        "class": "guys16 fa-2x search-section-icon",
        "subclass": "meta_username clickable",
        "links" : [
          {
            "title": "nodes",
            "menu_entry_id": "view-nodes",
            "class": "hw16",
            "link": "/init/nodes/nodes?volatile_filters=true&nodes_f_team_responsible=__role__",
            "fn": "view_nodes",
            "options": {"volatile_filters": true, "request_vars": {"nodes_f_team_responsible": "__role__"}}
          },
          {
            "title": "apps",
            "menu_entry_id": "adm-app",
            "class": "svc",
            "link": "/init/apps/apps?volatile_filters=true&apps_f_roles=%__role__%",
            "fn": "table_apps",
            "options": {"volatile_filters": true, "request_vars": {"apps_f_roles": "%__role__%"}}
          },
          {
            "title": "checks",
            "menu_entry_id": "view-checks",
            "class": "check16",
            "link": "/init/checks/checks?volatile_filters=true&checks_f_team_responsible=__role__",
            "fn": "table_checks",
            "options": {"volatile_filters": true, "request_vars": {"checks_f_team_responsible": "__role__"}}
          },
          {
            "title": "compliance_status",
            "menu_entry_id": "comp-status",
            "class": "comp16",
            "link": "/init/compliance/comp_status?volatile_filters=true&cs0_f_team_responsible=__role__",
            "fn": "view_comp_status",
            "options": {"volatile_filters": true, "request_vars": {"cs0_f_team_responsible": "__role__"}}
          }
        ]
    },
    "services": {
        "tab" : 'service_tabs("__rowid__", {"svc_id": "__svc_id__"})',
        "title": "__svcname__  *__svc_app__",
        "menu_entry_id": "view-services",
        "class": "svc fa-2x search-section-icon",
        "subclass": "meta_svcname clickable",
        "links" : [
          {
            "title": "dashboard",
            "menu_entry_id": "view-dashboard",
            "class": "alert16",
            "link": "/init/dashboard/index?volatile_filters=true&dashboard_f_svc_id=__svc_id__",
            "fn": "table_dashboard",
            "options": {"volatile_filters": true, "request_vars": {"dashboard_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "status",
            "menu_entry_id": "view-service-instances",
            "class": "alert16",
            "link": "/init/default/svcmon?volatile_filters=true&svcmon_f_svc_id=__svc_id__",
            "fn": "table_service_instances",
            "options": {"volatile_filters": true, "request_vars": {"svcmon_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "resources",
            "menu_entry_id": "view-resources",
            "class": "svc",
            "link": "/init/resmon/resmon?volatile_filters=true&resmon_f_svc_id=__svc_id__",
            "fn": "table_resources",
            "options": {"volatile_filters": true, "request_vars": {"resmon_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "resinfo",
            "menu_entry_id": "view-resinfo",
            "class": "alert16",
            "link": "/init/resinfo/resinfo?volatile_filters=true&resinfo_f_svc_id=__svc_id__",
            "fn": "table_resinfo",
            "options": {"volatile_filters": true, "request_vars": {"resinfo_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "actions",
            "menu_entry_id": "view-actions",
            "class": "action16",
            "link": "/init/svcactions/svcactions?volatile_filters=true&actions_f_svc_id=__svc_id__",
            "fn": "table_actions",
            "options": {"volatile_filters": true, "request_vars": {"actions_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "checks",
            "menu_entry_id": "view-checks",
            "class": "check16",
            "link": "/init/checks/checks?volatile_filters=true&checks_f_svc_id=__svc_id__",
            "fn": "table_checks",
            "options": {"volatile_filters": true, "request_vars": {"checks_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "disks",
            "menu_entry_id": "view-disks",
            "class": "hd16",
            "link": "/init/disks/disks?volatile_filters=true&disks_f_svc_id=__svc_id__"
          },
          {
            "title": "saves",
            "menu_entry_id": "view-saves",
            "class": "cd16",
            "link": "/init/saves/saves?volatile_filters=true&saves_f_svc_id=__svc_id__",
            "fn": "view_saves",
            "options": {"volatile_filters": true, "request_vars": {"saves_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "compliance_status",
            "menu_entry_id": "comp-status",
            "class": "comp16",
            "link": "/init/compliance/comp_status?volatile_filters=true&cs0_f_svc_id=__svc_id__",
            "fn": "view_comp_status",
            "options": {"volatile_filters": true, "request_vars": {"cs0_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "compliance_log",
            "menu_entry_id": "comp-log",
            "class": "log16",
            "link": "/init/compliance/comp_log?volatile_filters=true&comp_log_f_svc_id=__svc_id__",
            "fn": "table_comp_log",
            "options": {"volatile_filters": true, "request_vars": {"comp_log_f_svc_id": "__svc_id__"}}
          },
          {
            "title": "availability",
            "menu_entry_id": "stat-avail",
            "class": "avail16",
            "link": "/init/svcmon_log/svcmon_log?volatile_filters=true&svcmon_log_f_svc_id=__svc_id__"
          },
          {
            "title": "logs",
            "menu_entry_id": "adm-log",
            "class": "log16",
            "link": "/init/log/log?volatile_filters=true&log_f_svc_id=__svc_id__",
            "fn": "table_log",
            "options": {"volatile_filters": true, "request_vars": {"log_f_svc_id": "__svc_id__"}}
          }
        ]
    },
    "nodes": {
        "tab" : 'node_tabs("__rowid__", {"node_id": "__node_id__"})',
        "title": "__nodename__  *__app__",
        "menu_entry_id": "view-nodes",
        "class": "node16 fa-2x search-section-icon",
        "subclass": "meta_nodename clickable",
        "links" : [
          {
            "title": "nodes",
            "menu_entry_id": "view-nodes",
            "class": "hw16",
            "link": "/init/nodes/nodes?volatile_filters=true&nodes_f_node_id=__node_id__",
            "fn": "view_nodes",
            "options": {"volatile_filters": true, "request_vars": {"nodes_f_node_id": "__node_id__"}}
          },
          {
            "title": "dashboard",
            "menu_entry_id": "view-dashboard",
            "class": "alert16",
            "link": "/init/dashboard/index?volatile_filters=true&dashboard_f_node_id=__node_id__",
            "fn": "table_dashboard",
            "options": {"volatile_filters": true, "request_vars": {"dashboard_f_node_id": "__node_id__"}}
          },
          {
            "title": "services",
            "menu_entry_id": "view-service-instances",
            "class": "svc",
            "link": "/init/default/svcmon?volatile_filters=true&svcmon_f_node_id=__node_id__",
            "fn": "table_service_instances",
            "options": {"volatile_filters": true, "request_vars": {"svcmon_f_node_id": "__node_id__"}}
          },
          {
            "title": "resources",
            "menu_entry_id": "view-resources",
            "class": "svc",
            "link": "/init/resmon/resmon?volatile_filters=true&resmon_f_node_id=__node_id__",
            "fn": "table_resources",
            "options": {"volatile_filters": true, "request_vars": {"resmon_f_node_id": "__node_id__"}}
          },
          {
            "title": "resinfo",
            "menu_entry_id": "view-resinfo",
            "class": "svc",
            "link": "/init/resinfo/resinfo?volatile_filters=true&resinfo_f_node_id=__node_id__",
            "fn": "table_resinfo",
            "options": {"volatile_filters": true, "request_vars": {"resinfo_f_node_id": "__node_id__"}}
          },
          {
            "title": "actions",
            "menu_entry_id": "view-actions",
            "class": "action16",
            "link": "/init/svcactions/svcactions?volatile_filters=true&actions_f_node_id=__node_id__",
            "fn": "table_actions",
            "options": {"volatile_filters": true, "request_vars": {"actions_f_node_id": "__node_id__"}}
          },
          {
            "title": "checks",
            "menu_entry_id": "view-checks",
            "class": "check16",
            "link": "/init/checks/checks?volatile_filters=true&checks_f_node_id=__node_id__",
            "fn": "table_checks",
            "options": {"volatile_filters": true, "request_vars": {"checks_f_node_id": "__node_id__"}}
          },
          {
            "title": "packages",
            "menu_entry_id": "view-pkg",
            "class": "pkg16",
            "link": "/init/packages/packages?volatile_filters=true&packages_f_node_id=__node_id__",
            "fn": "table_packages",
            "options": {"volatile_filters": true, "request_vars": {"packages_f_node_id": "__node_id__"}}
          },
          {
            "title": "network",
            "menu_entry_id": "view-net",
            "class": "net16",
            "link": "/init/nodenetworks/nodenetworks?volatile_filters=true&nodenetworks_f_node_id=__node_id__",
            "fn": "table_nodenetworks",
            "options": {"volatile_filters": true, "request_vars": {"nodenetworks_f_node_id": "__node_id__"}}
          },
          {
            "title": "san",
            "menu_entry_id": "view-san",
            "class": "net16",
            "link": "/init/nodesan/nodesan?volatile_filters=true&nodesan_f_node_id=__node_id__",
            "fn": "table_nodesan",
            "options": {"volatile_filters": true, "request_vars": {"nodesan_f_node_id": "__node_id__"}}
          },
          {
            "title": "disks",
            "menu_entry_id": "view-disks",
            "class": "hd16",
            "link": "/init/disks/disks?volatile_filters=true&disks_f_disk_nodename=__nodename__"
          },
          {
            "title": "saves",
            "menu_entry_id": "view-saves",
            "class": "cd16",
            "link": "/init/saves/saves?volatile_filters=true&saves_f_save_nodename=__nodename__",
            "fn": "view_saves",
            "options": {"volatile_filters": true, "request_vars": {"saves_f_save_nodename": "__nodename__"}}
          },
          {
            "title": "compliance_status",
            "menu_entry_id": "comp-status",
            "class": "comp16",
            "link": "/init/compliance/comp_status?volatile_filters=true&cs0_f_node_id=__node_id__",
            "fn": "view_comp_status",
            "options": {"volatile_filters": true, "request_vars": {"cs0_f_node_id": "__node_id__"}}
          },
          {
            "title": "compliance_log",
            "menu_entry_id": "comp-log",
            "class": "log16",
            "link": "/init/compliance/comp_log?volatile_filters=true&comp_log_f_node_id=__node_id__",
            "fn": "table_comp_log",
            "options": {"volatile_filters": true, "request_vars": {"comp_log_f_node_id": "__node_id__"}}
          },
          {
            "title": "logs",
            "menu_entry_id": "adm-log",
            "class": "log16",
            "link": "/init/log/log?volatile_filters=true&log_f_log_node_id=__node_id__",
            "fn": "table_log",
            "options": {"volatile_filters": true, "request_vars": {"log_f_node_id": "__node_id__"}}
          }
        ]
    },
    "filtersets": {
        "tab" : 'filterset_tabs("__rowid__", {"fset_name": "__fset_name__"})',
        "title": "__fset_name__",
        "menu_entry_id": "adm-filters",
        "class": "filter16 fa-2x search-section-icon",
        "subclass": "meta_username clickable",
        "links" : [
          {
            "title": "designer",
            "menu_entry_id": "comp-designer",
            "class": "wf16",
            "link": "/init/compliance/comp_admin?obj_filter=__fset_name__",
            "fn": "designer",
            "options": {"search": "__fset_name__"},
          }
        ]
    },
    "vms": {
        "tab" : 'node_tabs("__rowid__", {"nodename": "__mon_vmname__"})',
        "title": "__mon_vmname__",
        "menu_entry_id": "view-nodes",
        "class": "hv16 fa-2x search-section-icon",
        "subclass": "meta_nodename",
        "links" : [
          {
            "title": "status",
            "menu_entry_id": "view-service-instances",
            "class": "svc",
            "link": "/init/default/svcmon?volatile_filters=true&svcmon_f_mon_vmname=__mon_vmname__",
            "fn": "table_service_instances",
            "options": {"volatile_filters": true, "request_vars": {"svcmon_f_mon_vmname": "__mon_vmname__"}}
          }
        ]
    }
  }
  return menu[fk]
}

function search_get_val(data, key) {
	var l = key.split(".")
	var val = data
	for (var i=0; i<l.length; i++) {
		val = val[l[i]]
	}
	return val
}

function search_subst_keys(s, data, key) {
	if (is_dict(data[key])) {
		for (subkey in data[key]) {
			var _key = key+"."+subkey
			s = s.replace("__"+_key+"__", search_get_val(data, _key))
		}
	} else {
		s = s.replace("__"+key+"__", search_get_val(data, key))
	}
	return s
}

function search_build_result_row(label, first, res, count) {
  var section_data = search_get_menu(label)

  // init result row, set icon cell
  var row_group = $("<div></div>")
  var row = $("<tr></tr>")
  row_group.append(row)
  var cell_icon = $("<td class='icon'></td>")
  cell_icon.addClass(section_data.class)
  row.append(cell_icon)

  // title cell
  cell_result = $("<td></td>")
  p_title = $("<p></p>")
  cell_result.append(p_title)
  row.append(cell_result)

  if (first==1) {
    // first header with %___%
    var val = $('#search_input').val()
    var title = "%" + search_parse_input(val).substring + "%"
    p_title.text(title)
  } else {
    // substitute key in the title format
    var title = section_data.title
    for (key in res) {
      title = search_subst_keys(title, res, key)
      p_title.text(title)
    }
    p_title.addClass(section_data.subclass)

    var tab = section_data.tab
    if (tab) {
      // create a div to host the result tab
      tab_tr = $("<tr></tr>")
      tab_td = $("<td colspan='2'></td>")
      tab_div = $("<div class='stackable searchtab hidden'></div>")
      tab_tr.append(tab_td)
      tab_td.append(tab_div)
      tab_div.uniqueId()
      row_group.append(tab_tr)

      // mangle extra id to satisfy tabs code constraints
      var rowid = tab_div.attr("id").replace(/[ \/\.-]/g, '_')
      tab_div.attr("id", rowid)

      // substitute the keys in the defined tab action
      tab = tab.replace("__rowid__", rowid)
      for (key in res) {
        tab = search_subst_keys(tab, res, key)
      }

      if (tab[0] == "/") {
        // tab action: load ajax content
        var url = services_get_url() + tab
        var fn = "sync_ajax('"+url+"', [], '"+rowid+"', function() {})"
      } else {
        // tab action: execute a function
        var fn = tab
      }
      fn = '$("#'+ rowid + '").show();' + fn
      p_title.attr("onclick", fn)
    }
  }

  // add links to views
  if (first==1 && section_data.special_header_links != undefined) {
    // special condition for first element if present
    links = section_data.special_header_links
  } else {
    links = section_data.links
  }

  for(j=0; j<links.length; j++) {
    var link_data = links[j]
    if (osvc.hidden_menu_entries.indexOf(link_data.menu_entry_id) >= 0) {
      continue
    }
    var a_link = $("<a class='search-link'></a>")
    $.data(a_link[0], "link_data", link_data)
    a_link.addClass(link_data.class)
    a_link.addClass("nocolor icon")
    a_link.text(i18n.t("search.menu_link."+ link_data.title))
    cell_result.append(a_link)

    a_link.bind("click", function(e) {
      var link_data = $.data($(this)[0], "link_data")
      var url = link_data.link
      for (key in res) {
        url = search_subst_keys(url, res, key)
      }
      // leftover (the first==1 case)
      url = url.replace(/__[\.\w]+__/, title)

      e.preventDefault()
      if (link_data.options) {
        for (opt in link_data.options) {
          if (typeof(link_data.options[opt]) !== "string") {
            continue
          }
          for (key in res) {
            link_data.options[opt] = search_subst_keys(link_data.options[opt], res, key)
          }
          link_data.options[opt] = link_data.options[opt].replace(/__[\.\w]+__/, title)
        }
      }
      if (link_data.options && link_data.options.request_vars) {
        for (opt in link_data.options.request_vars) {
          if (typeof(link_data.options.request_vars[opt]) !== "string") {
            continue
          }
          for (key in res) {
            link_data.options.request_vars[opt] = search_subst_keys(link_data.options.request_vars[opt], res, key)
          }
          link_data.options.request_vars[opt] = link_data.options.request_vars[opt].replace(/__[\.\w]+__/, title)
        }
      }

      if (e.ctrlKey) {
        window.open(url, "_blank")
        return
      }

      $("#search_input").val("").blur()
      $("#search_result").empty().hide()
      app_load_href(url, link_data.fn, {}, link_data.options)
    })
  }
  return row_group.children()
}

function search_build_result_view(label, resultset) {
  var section_data = search_get_menu(label)
  if (osvc.hidden_menu_entries.indexOf(section_data.menu_entry_id) >= 0) {
    return
  }
  var section_div = $("<div class='menu_section'></div>")
  section_div.attr("id", label)
  section_div.text(i18n.t("search.menu_header.title_"+label) + " (" + resultset.total +")")
  var table = $("<table id='search_result_table' style='width:100%'></table>")
  section_div.append(table)

  // Init global row
  table.append(search_build_result_row(label, 1, ""))

  for (i=0; i<resultset.data.length; i++) {
    table.append(search_build_result_row(label, 0, resultset.data[i], i))
  }
  return section_div
}

function search_parse_input(search_query) {
  var data = {}
  if (search_query.match(/^\w+:\s+/)) {
    data["substring"] = search_query.replace(/^\w+:\s+/, "")
    data["in"] = search_query.match(/^\w+:\s+/)[0].replace(/:\s+$/, "")
  } else {
    data["substring"] = search_query
  }
  return data
}

function search_search() {
  var count=0
  var search_query = $('#search_input').val()

  if (search_query == "") {
    return
  }

  var data = search_parse_input(search_query)

  $("#search_div").removeClass("searchidle")
  $("#search_div").addClass("searching")

  $("#search_result").empty()

  services_osvcgetrest("R_SEARCH", "", data, function(jd) {
      var result = jd.data
      for (d in result) {
        if (result[d].data.length>0 && search_get_menu(d) !== undefined) {
          response = search_build_result_view(d, result[d])
          $("#search_result").append(response)
          count += result[d].data.length
        }
      }

      if (count == 0) {
        var div = "<div class='menu_entry meta_not_found'><a><div class='question48'>"+i18n.t("search.nothing_found")+"</div></a></div>"
        $("#search_result").append(div)
      } else if (count == 1) {
        $('#search_result_table tr:first').remove()
        var td = $('#search_title_click0')
        td.trigger("click")
      }

      if (!$("#search_result").is(':visible')) {
        toggle('search_result')
      }
      $("#search_div").removeClass("searching")
      $("#search_div").addClass("searchidle")
      search_highlight($("#search_result"), data.substring)
  })
}

function search(divid) {
	var o = {}
	o.divid = divid
	o.div = $("#"+divid)
	o.placeholders = [
		i18n.t("layout.search"),
		"fset: linux",
		"disk: 6005",
		"user: me",
		"group: Manager",
		"net: intra",
		"ip: 192.168",
		"svc: web",
		"node: 02",
		"vm: 02",
		"safe: etc",
		"form: add_",
		"report: lifecycle",
		"chart: disk",
		"metric: lifecycle",
		"rset: test"
	]

	o.router = function router(delay) {
		if (osvc.menu.menu_div.is(":visible")) {
			filter_menu(null)
		} else if ($(".header [name=fset_selector_entries]").is(":visible")) {
			filter_fset_selector(null)
		} else {
			// close the search result panel if no search keyword
			if ($("#search_input").val() == "") {
				$("#search_result").slideUp()
			} else {
				clearTimeout(o.timer)
				o.timer = setTimeout(search_search, delay)
			}
		}
	}

	o.div.load("/init/static/views/search.html?v="+osvc.code_rev, function() {
		o.init()
	})

	o.init = function() {
		o.timer = null
		o.phi = 0
		o.div.i18n()
		o.e_search_div = $("#search_div")
		o.e_search_input = $("#search_input")

		setInterval(function() {
			o.e_search_input.attr("placeholder", o.placeholders[o.phi++])
			if (o.phi == o.placeholders.length-1) {
				o.phi = 0
			}
		}, 15000)
		o.e_search_input.on("keyup",function (event) {
			if (is_special_key(event)) {
				// do search on special key (esc, arrows, etc...)
				return
			} else if (event.keyCode == 13) {
				// do a search immediately on <enter>
				o.router(0)
			} else {
				// schedule a search
				o.router(1000)
			}
		})
	}

	return o
}


function filter_menu(event) {
  var menu = $("#menu_menu")
  var text = $(".search").find("input").val()

  var reg = new RegExp(text, "i")
  menu.find(".menu_entry").each(function(){
    if ($(this).text().match(reg)) {
      $(this).show()
      $(this).parents(".menu_section").first().show()
    } else {
      $(this).hide()
    }
  })
  menu.find(".menu_section").each(function(){
    if ($(this).children("a").text().match(reg)) {
      $(this).find(".menu_entry").show()
      $(this).show()
    }
    n = $(this).find(".menu_entry:visible").length
    if (n == 0) {
      $(this).hide()
    }
  })
  var entries = menu.find(".menu_entry:visible")
  if (is_enter(event)) {
    if (menu.is(":visible") && (entries.length == 1)) {
      entries.effect("highlight")
      window.location = entries.attr("link")
    }
  }
  if (entries.length==0) {
    menu.append("<div class='menu_entry meta_not_found'><a><div class='question48'>"+i18n.t("search.nothing_found")+"</div></a></div>")
  } else {
    menu.find(".meta_not_found").remove()
  }
  search_highlight(menu, text)
}

function filter_fset_selector(event) {
  var div = $(".header [name=fset_selector_entries]")
  if (!div.is("[ready]")) {
    var timer = setTimeout(function(){filter_fset_selector(event)}, 500)
    return
  }
  var text = $(".search").find("input").val()
  var reg = new RegExp(text, "i")
  div.find(".menu_entry").each(function(){
    if ($(this).find("[name=title]").text().match(reg)) {
      $(this).show()
    } else {
      $(this).hide()
    }
  })
  var entries = div.find(".menu_entry:visible")
  if (entries.length==0) {
    div.append("<div class='menu_entry meta_not_found'><a><div class='question48'>"+i18n.t("search.nothing_found")+"</div></a></div>")
  } else {
    div.find(".meta_not_found").remove()
  }
  search_highlight(div, text)
}

function search_highlight(e, s) {
  // keep track of original texts
  if (e.children("[name=orig]").length == 0) {
    var cache = $("<div name='orig'></div>")
    cache.css({"display": "none"})
    e.find("*").each(function() {
      var clone = $(this).clone()
      clone.children().remove()
      if (clone.text().match(/^$/)) {
        return
      }
      var cache_entry = $("<div></div>")
      cache_entry.uniqueId()
      var id = cache_entry.attr("id")
      $(this).attr("highlight_id", id)
      cache_entry.html(clone.html())
      cache.append(cache_entry)
    })
    e.append(cache)
  }

  var regexp = new RegExp(s, 'ig')

  e.children("[name=orig]").children().each(function(){
    // restore orig
    var id = $(this).attr("id")
    var tgt = e.find("[highlight_id="+id+"]")
    tgt.find("[name=highlighted]").remove()
    var children = tgt.children().detach()

    tgt.empty()
    tgt.text($(this).text())

    if ((s != "") && $(this).text().match(regexp)) {
      var highlighted = $("<span name='highlighted'></span>")
      highlighted.html($(this).text().replace("<", "&lt;").replace(">", "&gt;").replace(regexp, function(x) {
        return '<span class="highlight_light">' + x + '</span>'
      }))
      tgt.text("")
      tgt.prepend(highlighted)
    }
    tgt.append(children)
  })
}
