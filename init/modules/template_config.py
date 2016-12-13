#!/usr/bin/env python
# coding: utf8

# server timezone
server_timezone = "Europe/Madrid"

# connection to the database
dbopensvc = "dbopensvc"
dbopensvc_user = "opensvc"
dbopensvc_password = "opensvc"

# pdns database
dbdns = "pdns"
dbdns_host = "dbopensvc"
dbdns_user = "opensvc"
dbdns_password = "opensvc"

# the dns zone whose records the collector manages
dns_managed_zone = "opensvc.dom.net"
dns_default_ttl = 120

# connection to the redis
redis_host = "dbopensvc"

# ldap / ad
ldap_mode = "ad"
ldap_server = "ad.my.corp"
ldap_base_dn = ""
ldap_allowed_groups = []
ldap_group_dn = ""
ldap_group_name_attrib= "cn"
ldap_group_member_attrib = "memberUid"
ldap_group_filterstr = "objectClass=*"
ldap_manage_groups = False
ldap_group_mapping = {
  "adgrp": ["CheckExec", "CompExec"]
}
ldap_bind_dn = ""
ldap_bind_pw = ""
ldap_filter = ""

http_host = "opensvc.mydomain.com"

# websocket
websocket_url = "http://dbopensvc:8889"
websocket_key = "magix123"

# mail sending configuration
mail_server = "localhost:25"
mail_sender = "admin@opensvc.com"
mail_tls = False
mail_login = 'username:password'

# time between relogin, in seconds
session_expire = 36000000

# refuse node register without a collector user credentials
# default: False
refuse_anon_register = True

# groups to attach to a newly registered user
membership_on_register = [
 "AppManager",
 "GroupManager",
 "SelfManager",
 "NodeManager",
 "NodeExec",
 "CompExec",
 "CheckExec",
 "CheckRefresh",
 "CheckManager",
]

# set to True if newly registered users should have a private app code
# created, for them to register nodes and add services
create_app_on_register = True

# allow users to create their own account
# default: True
allow_register = False

# max billing tokens
# default: unset, meaning unlimited
token_quota = 150000

# default user quota
default_quota_app = 1
default_quota_org_group = 3

# billing tunables
billing_method = "agents"

# callouts
nodejs = "/usr/bin/nodejs"
vm2 = "/usr/local/bin/vm2"

#
# DataCore SAN symphony config
#
sansymphony_v_pool = {
  'local': {
    'sds1_pool1': 'sds1:sds1_pool1',
    'sds2_pool2': 'sds2:sds2_pool2',
  },
  'dcspra2': {
  },
  'dcslmw1': {
  },
}
sansymphony_v_mirrored_pool = {
  'local': {
    'sds1_pool1': 'sds1:sds1_pool1,sds2:sds2_pool2',
    'sds2_pool2': 'sds1:sds1_pool1,sds2:sds2_pool2',
  },
  'dcspra2': {
    'sdsert01_sas_optima3': 'sdsert01:sdsert01_sas_optima3,sdsert02:sdsert02_sas_optima3',
    'sdsert02_sas_optima3': 'sdsert01:sdsert01_sas_optima3,sdsert02:sdsert02_sas_optima3',
  },
  'dcslmw1': {
    'sdslmw01_miroir_n2_argent': 'sdslmw01:sdslmw01_miroir_n2_argent,sdslmw03:sdslmw03_miroir_n3_argent',
    'sdslmw03_miroir_n3_argent': 'sdslmw01:sdslmw01_miroir_n2_argent,sdslmw03:sdslmw03_miroir_n3_argent',
    'sdslmw01_miroir_n2_or': 'sdslmw01:sdslmw01_miroir_n2_or,sdslmw03:sdslmw03_miroir_n3_or',
    'sdslmw03_miroir_n3_or': 'sdslmw01:sdslmw01_miroir_n2_or,sdslmw03:sdslmw03_miroir_n3_or',
    'sdslmw01_miroir_n2_platine': 'sdslmw01:sdslmw01_miroir_n2_platine,sdslmw03:sdslmw03_miroir_n3_platine',
    'sdslmw03_miroir_n3_platine': 'sdslmw01:sdslmw01_miroir_n2_platine,sdslmw03:sdslmw03_miroir_n3_platine',
  },
}

# default number of days before stats data purge
stats_retention_days = 367

# per table retention. takes precedence over stats_retention_days
retentions = {
 'metrics_log': 1600,
 'stats_cpu': 31,
 'stats_swap': 31,
 'stats_netdev': 31,
 'stats_blockdev': 31,
 'stats_block': 31,
 'stats_mem_u': 31,
 'stats_netdev_err': 31,
 'stats_proc': 31,
 'stats_svc': 31,
 'stats_fs_u': 31,
 'comp_log': 365,
 'appinfo_log': 365,
 'SVCactions': 365,
 'services_log': 700,
 'dashboard_events': 165,
}


#
# Alerts config
#
email = True
email_from = "admin@localhost"
email_host = "localhost"
email_port = 35

gtalk = True
gtalk_username = "opensvc"
gtalk_password = "opensvc"

