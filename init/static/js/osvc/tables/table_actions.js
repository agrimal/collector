table_actions_defaults = {
     'pager': {'page': 1},
     'extrarow': false,
     'extrarow_class': "",
     'flash': "",
     'checkboxes': true,
     'ajax_url': '/init/svcactions/ajax_actions',
     'span': ['pid'],
     'columns': ['svcname', 'hostname', 'pid', 'action', 'status', 'begin', 'end', 'time', 'id', 'status_log', 'cron', 'ack', 'acked_by', 'acked_date', 'acked_comment', 'assetname', 'fqdn', 'serial', 'model', 'environnement', 'role', 'type', 'sec_zone', 'loc_country', 'loc_zip', 'loc_city', 'loc_addr', 'loc_building', 'loc_floor', 'loc_room', 'loc_rack', 'enclosure', 'enclosureslot', 'hvvdc', 'hvpool', 'hv', 'os_name', 'os_release', 'os_vendor', 'os_arch', 'os_kernel', 'cpu_dies', 'cpu_cores', 'cpu_threads', 'cpu_model', 'cpu_freq', 'mem_banks', 'mem_slots', 'mem_bytes', 'listener_port', 'version', 'action_type', 'host_mode', 'team_responsible', 'team_integ', 'team_support', 'project', 'last_boot', 'warranty_end', 'maintenance_end', 'os_obs_warn_date', 'os_obs_alert_date', 'hw_obs_warn_date', 'hw_obs_alert_date'],
     'colprops': {'loc_city': {'field': 'loc_city', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'City', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_envdate': {'field': 'svc_envdate', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Env file date', '_class': '', 'table': 'v_svcmon', 'display': 0, 'default_filter': ''}, 'cpu_threads': {'field': 'cpu_threads', 'filter_redirect': '', 'force_filter': '', 'img': 'cpu16', '_dataclass': '', 'title': 'CPU threads', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'cpu_dies': {'field': 'cpu_dies', 'filter_redirect': '', 'force_filter': '', 'img': 'cpu16', '_dataclass': '', 'title': 'CPU dies', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'assetname': {'field': 'assetname', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Asset name', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'loc_country': {'field': 'loc_country', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Country', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'cpu_vendor': {'field': 'cpu_vendor', 'filter_redirect': '', 'force_filter': '', 'img': 'cpu16', '_dataclass': '', 'title': 'CPU vendor', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'loc_building': {'field': 'loc_building', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Building', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'team_responsible': {'field': 'team_responsible', 'filter_redirect': '', 'force_filter': '', 'img': 'guys16', '_dataclass': '', 'title': 'Team responsible', '_class': 'groups', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'cpu_cores': {'field': 'cpu_cores', 'filter_redirect': '', 'force_filter': '', 'img': 'cpu16', '_dataclass': '', 'title': 'CPU cores', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'loc_rack': {'field': 'loc_rack', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Rack', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_drpnode': {'field': 'svc_drpnode', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'DRP node', '_class': 'nodename_no_os', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'cpu_model': {'field': 'cpu_model', 'filter_redirect': '', 'force_filter': '', 'img': 'cpu16', '_dataclass': '', 'title': 'CPU model', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_flex_min_nodes': {'field': 'svc_flex_min_nodes', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Flex min nodes', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'loc_zip': {'field': 'loc_zip', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'ZIP', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_containertype': {'field': 'svc_containertype', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Service mode', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'svc_ha': {'field': 'svc_ha', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'HA', '_class': 'svc_ha', 'table': 'v_services', 'display': 1, 'default_filter': ''}, 'svc_created': {'field': 'svc_created', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Service creation date', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'hw_obs_warn_date': {'field': 'hw_obs_warn_date', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Hardware obsolescence warning date', '_class': 'date_future', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'action_type': {'field': 'action_type', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Action type', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_breaker1': {'field': 'power_breaker1', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power breaker #1', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_breaker2': {'field': 'power_breaker2', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power breaker #2', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'status': {'field': 'status', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Status', '_class': 'action_status', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}, 'mem_bytes': {'field': 'mem_bytes', 'filter_redirect': '', 'force_filter': '', 'img': 'mem16', '_dataclass': '', 'title': 'Memory', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_protect_breaker': {'field': 'power_protect_breaker', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power protector breaker', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'hvpool': {'field': 'hvpool', 'filter_redirect': '', 'force_filter': '', 'img': 'hv16', '_dataclass': '', 'title': 'Hypervisor pool', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'cron': {'field': 'cron', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Scheduled', '_class': 'action_cron', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}, 'acked_by': {'field': 'acked_by', 'filter_redirect': '', 'force_filter': '', 'img': 'guy16', '_dataclass': '', 'title': 'Acked by', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_flex_cpu_high_threshold': {'field': 'svc_flex_cpu_high_threshold', 'filter_redirect': '', 'force_filter': '', 'img': 'spark16', '_dataclass': '', 'title': 'Flex cpu high threshold', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'team_support': {'field': 'team_support', 'filter_redirect': '', 'force_filter': '', 'img': 'guys16', '_dataclass': '', 'title': 'Support', '_class': 'groups', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'host_mode': {'field': 'host_mode', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Host Mode', '_class': 'env', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'enclosure': {'field': 'enclosure', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Enclosure', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'responsibles': {'field': 'responsibles', 'filter_redirect': '', 'force_filter': '', 'img': 'guy16', '_dataclass': '', 'title': 'Responsibles', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'svc_cluster_type': {'field': 'svc_cluster_type', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Cluster type', '_class': '', 'table': 'v_services', 'display': 1, 'default_filter': ''}, 'svc_autostart': {'field': 'svc_autostart', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Primary node', '_class': 'svc_autostart', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'version': {'field': 'version', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Agent version', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_wave': {'field': 'svc_wave', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Drp wave', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'mem_slots': {'field': 'mem_slots', 'filter_redirect': '', 'force_filter': '', 'img': 'mem16', '_dataclass': '', 'title': 'Memory slots', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'os_obs_alert_date': {'field': 'os_obs_alert_date', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'OS obsolescence alert date', '_class': 'date_future', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'warranty_end': {'field': 'warranty_end', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Warranty end', '_class': 'date_future', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'last_boot': {'field': 'last_boot', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Last boot', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'loc_addr': {'field': 'loc_addr', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Address', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'ack': {'field': 'ack', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Ack', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'fqdn': {'field': 'fqdn', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Fqdn', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'hvvdc': {'field': 'hvvdc', 'filter_redirect': '', 'force_filter': '', 'img': 'hv16', '_dataclass': '', 'title': 'Virtual datacenter', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'action': {'field': 'action', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Action', '_class': 'action', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}, 'svc_updated': {'field': 'updated', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Last service update', '_class': 'datetime_daily', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'sec_zone': {'field': 'sec_zone', 'filter_redirect': '', 'force_filter': '', 'img': 'fw16', '_dataclass': '', 'title': 'Security zone', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_app': {'field': 'svc_app', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'App', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'app': {'field': 'app', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'App', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_cabinet1': {'field': 'power_cabinet1', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power cabinet #1', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_cabinet2': {'field': 'power_cabinet2', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power cabinet #2', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_status': {'field': 'svc_status', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Service overall status', '_class': 'status', 'table': 'v_services', 'display': 1, 'default_filter': ''}, 'os_vendor': {'field': 'os_vendor', 'filter_redirect': '', 'force_filter': '', 'img': 'os16', '_dataclass': '', 'title': 'OS vendor', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'mailto': {'field': 'mailto', 'filter_redirect': '', 'force_filter': '', 'img': 'guy16', '_dataclass': '', 'title': 'Responsibles emails', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'svc_flex_cpu_low_threshold': {'field': 'svc_flex_cpu_low_threshold', 'filter_redirect': '', 'force_filter': '', 'img': 'spark16', '_dataclass': '', 'title': 'Flex cpu low threshold', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'cpu_freq': {'field': 'cpu_freq', 'filter_redirect': '', 'force_filter': '', 'img': 'cpu16', '_dataclass': '', 'title': 'CPU freq', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'type': {'field': 'type', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Type', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'enclosureslot': {'field': 'enclosureslot', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Enclosure Slot', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_type': {'field': 'svc_type', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Service type', '_class': 'env', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'svc_envfile': {'field': 'svc_envfile', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Env file', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'hv': {'field': 'hv', 'filter_redirect': '', 'force_filter': '', 'img': 'hv16', '_dataclass': '', 'title': 'Hypervisor', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_availstatus': {'field': 'svc_availstatus', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Service availability status', '_class': 'status', 'table': 'v_services', 'display': 1, 'default_filter': ''}, 'svc_drptype': {'field': 'svc_drptype', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'DRP type', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'os_concat': {'field': 'os_concat', 'filter_redirect': '', 'force_filter': '', 'img': 'os16', '_dataclass': '', 'title': 'OS full name', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_status_updated': {'field': 'svc_status_updated', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Status updated', '_class': 'datetime_status', 'table': 'services', 'display': 1, 'default_filter': ''}, 'listener_port': {'field': 'listener_port', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Listener port', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'environnement': {'field': 'environnement', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Env', '_class': 'env', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_drpnodes': {'field': 'svc_drpnodes', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'DRP nodes', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'svc_nodes': {'field': 'svc_nodes', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Nodes', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'os_obs_warn_date': {'field': 'os_obs_warn_date', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'OS obsolescence warning date', '_class': 'date_future', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_name': {'field': 'svc_name', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Service', '_class': 'svcname', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'loc_room': {'field': 'loc_room', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Room', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'project': {'field': 'project', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Project', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'loc_floor': {'field': 'loc_floor', 'filter_redirect': '', 'force_filter': '', 'img': 'loc', '_dataclass': '', 'title': 'Floor', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'mem_banks': {'field': 'mem_banks', 'filter_redirect': '', 'force_filter': '', 'img': 'mem16', '_dataclass': '', 'title': 'Memory banks', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'os_kernel': {'field': 'os_kernel', 'filter_redirect': '', 'force_filter': '', 'img': 'os16', '_dataclass': '', 'title': 'OS kernel', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'pid': {'field': 'pid', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Pid', '_class': 'action_pid', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}, 'updated': {'field': 'updated', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Last node update', '_class': 'datetime_daily', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'serial': {'field': 'serial', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Serial', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'id': {'field': 'id', 'filter_redirect': '', 'force_filter': '', 'img': 'columns', '_dataclass': '', 'title': 'Id', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_hostid': {'field': 'svc_hostid', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Host id', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'end': {'field': 'end', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'End', '_class': 'action_end', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'hostname': {'field': 'hostname', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Node name', '_class': 'nodename', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}, 'os_arch': {'field': 'os_arch', 'filter_redirect': '', 'force_filter': '', 'img': 'os16', '_dataclass': '', 'title': 'OS arch', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'node_updated': {'field': 'node_updated', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Last node update', '_class': 'datetime_daily', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_comment': {'field': 'svc_comment', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Comment', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'role': {'field': 'role', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Role', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'team_integ': {'field': 'team_integ', 'filter_redirect': '', 'force_filter': '', 'img': 'guys16', '_dataclass': '', 'title': 'Integrator', '_class': 'groups', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_supply_nb': {'field': 'power_supply_nb', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power supply number', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svc_flex_max_nodes': {'field': 'svc_flex_max_nodes', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Flex max nodes', '_class': '', 'table': 'v_services', 'display': 0, 'default_filter': ''}, 'maintenance_end': {'field': 'maintenance_end', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Maintenance end', '_class': 'date_future', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'begin': {'field': 'begin', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Begin', '_class': 'datetime_no_age', 'table': 'v_svcactions', 'display': 1, 'default_filter': '>-1d'}, 'os_name': {'field': 'os_name', 'filter_redirect': '', 'force_filter': '', 'img': 'os16', '_dataclass': '', 'title': 'OS name', '_class': 'os_name', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'nodename': {'field': 'nodename', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Node name', '_class': 'nodename', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'power_protect': {'field': 'power_protect', 'filter_redirect': '', 'force_filter': '', 'img': 'pwr', '_dataclass': '', 'title': 'Power protector', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'status_log': {'field': 'status_log', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Log', '_class': 'action_log', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}, 'acked_date': {'field': 'acked_date', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Ack date', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'acked_comment': {'field': 'acked_comment', 'filter_redirect': '', 'force_filter': '', 'img': 'action16', '_dataclass': '', 'title': 'Ack comment', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'hw_obs_alert_date': {'field': 'hw_obs_alert_date', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Hardware obsolescence alert date', '_class': 'date_future', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'os_release': {'field': 'os_release', 'filter_redirect': '', 'force_filter': '', 'img': 'os16', '_dataclass': '', 'title': 'OS release', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'time': {'field': 'time', 'filter_redirect': '', 'force_filter': '', 'img': 'time16', '_dataclass': '', 'title': 'Duration', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'model': {'field': 'model', 'filter_redirect': '', 'force_filter': '', 'img': 'node16', '_dataclass': '', 'title': 'Model', '_class': '', 'table': 'v_svcactions', 'display': 0, 'default_filter': ''}, 'svcname': {'field': 'svcname', 'filter_redirect': '', 'force_filter': '', 'img': 'svc', '_dataclass': '', 'title': 'Service', '_class': 'svcname', 'table': 'v_svcactions', 'display': 1, 'default_filter': ''}},
     'volatile_filters': false,
     'child_tables': [],
     'parent_tables': [],
     'dataable': true,
     'linkable': true,
     'dbfilterable': true,
     'filterable': true,
     'refreshable': true,
     'bookmarkable': true,
     'exportable': true,
     'columnable': true,
     'commonalityable': true,
     'headers': true,
     'wsable': true,
     'pageable': true,
     'on_change': false,
     'events': ['begin_action', 'end_action', 'svcactions_change'],
     'request_vars': {}
}

function table_actions(divid, options) {
  var _options = {"id": "actions"}
  $.extend(true, _options, table_actions_defaults, options)
  _options.divid = divid
  _options.caller = "table_actions"
  table_init(_options)
}

function table_actions_node(divid, nodename) {
  var id = "actions_" + nodename.replace(".","_").replace("-", "_")
  var f_hostname = id+"_f_hostname"
  var f_begin = id+"_f_begin"
  var request_vars = {}
  request_vars[f_hostname] = nodename
  request_vars[f_begin] = ">-60d"
  table_actions(divid, {
    "id": id,
    "caller": "table_actions_node",
    "request_vars": request_vars,
    "volatile_filters": true,
    "bookmarkable": false,
    "refreshable": false,
    "linkable": false,
    "exportable": false,
    "pageable": false,
    "columnable": false,
    "commonalityable": false,
    "filterable": false,
    "wsable": false,
    "visible_columns": [
	'svcname',
	'pid',
	'action',
	'status',
	'begin',
	'end',
	'time',
	'id',
	'status_log',
	'cron',
	'ack',
	'acked_by',
	'acked_date',
	'acked_comment'
    ]
  })
}

function table_actions_svc(divid, svcname) {
  var id = "actions_" + svcname.replace(".","_").replace("-", "_")
  var f_svcname = id+"_f_svcname"
  var f_begin = id+"_f_begin"
  var perpage = id+"_perpage"
  var request_vars = {}
  request_vars[f_svcname] = svcname
  request_vars[f_begin] = ">-60d"
  table_actions(divid, {
    "id": id,
    "caller": "table_actions_svc",
    "request_vars": request_vars,
    "volatile_filters": true,
    "bookmarkable": false,
    "refreshable": false,
    "linkable": false,
    "exportable": false,
    "pageable": false,
    "columnable": false,
    "commonalityable": false,
    "filterable": false,
    "wsable": false,
    "visible_columns": [
	'hostname',
	'pid',
	'action',
	'status',
	'begin',
	'end',
	'time',
	'id',
	'status_log',
	'cron',
	'ack',
	'acked_by',
	'acked_date',
	'acked_comment'
    ]
  })
}
