max_search_result = 10

def lib_search_form(pattern):
    t = datetime.datetime.now()
    o = db.forms.form_name
    q = db.forms.form_name.like(pattern)
    q &= db.forms.id == db.forms_team_publication.form_id
    q &= db.forms_team_publication.group_id.belongs(user_group_ids())
    n = db(q).count()
    data = db(q).select(db.forms.form_name,
                        db.forms.id,
                        groupby=o,
                        orderby=o,
                        limitby=(0,max_search_result)
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_fset(pattern):
    t = datetime.datetime.now()
    o = db.gen_filtersets.fset_name
    q = _where(None, 'gen_filtersets', pattern, 'fset_name')
    n = db(q).count()
    data = db(q).select(db.gen_filtersets.id,
                        o,
                        orderby=o,
                        limitby=(0,max_search_result)
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_disk(pattern):
    t = datetime.datetime.now()
    o = db.b_disk_app.disk_id
    q = _where(None, 'b_disk_app', pattern, 'disk_id')
    q = q_filter(q, app_field=db.b_disk_app.app)
    q = apply_filters(q, db.b_disk_app.disk_nodename, None)
    n = len(db(q).select(o, groupby=o))
    data = db(q).select(o,
                        orderby=o,
                        groupby=o,
                        limitby=(0,max_search_result)
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_app(pattern):
    t = datetime.datetime.now()
    o = db.apps.app
    q = db.apps.app.like(pattern)
    if not "Manager" in user_groups():
        q &= db.apps.id.belongs(user_app_ids())
    n = db(q).count()
    data = db(q).select(o, orderby=o, limitby=(0,max_search_result)).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_service(pattern):
    t = datetime.datetime.now()
    o = db.services.svc_name
    q = _where(None, 'services', pattern, 'svc_name')
    q = q_filter(q, app_field=db.services.svc_app)
    q = apply_filters(q, db.services.svc_name, None)
    n = db(q).count()
    data = db(q).select(o, orderby=o, limitby=(0,max_search_result),).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_vm(pattern):
    t = datetime.datetime.now()
    o = db.svcmon.mon_vmname
    q = _where(None, 'svcmon', pattern, 'mon_vmname')
    q = _where(None, 'svcmon', "!empty", 'mon_vmname')
    q = q_filter(q, svc_field=db.svcmon.mon_svcname)
    q = apply_filters(q, db.svcmon.mon_svcname, None)
    n = db(q).count()
    data = db(q).select(o,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_ip(pattern):
    t = datetime.datetime.now()
    o = db.node_ip.addr
    q = _where(None, 'node_ip', pattern, 'addr')
    q = q_filter(q, node_field=db.node_ip.nodename)
    q = apply_filters(q, db.node_ip.nodename, None)

    n = db(q).count()
    data = db(q).select(o,
                        db.node_ip.nodename,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }


def lib_search_node(pattern):
    t = datetime.datetime.now()
    o = db.nodes.nodename
    q = _where(None, 'nodes', pattern, 'nodename')
    q = q_filter(q, app_field=db.nodes.app)
    q = apply_filters(q, db.nodes.nodename, None)
    n = db(q).count()
    data = db(q).select(o,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_user(pattern):
    t = datetime.datetime.now()
    o = db.v_users.fullname
    q = _where(None, 'v_users', pattern, 'fullname')
    if "Manager" not in user_groups():
        q &= db.v_users.id == db.auth_membership.user_id
        q &= db.auth_membership.group_id.belongs(user_group_ids())
        q &= db.auth_membership.group_id == db.auth_group.id
        q &= db.auth_group.role != "Everybody"
    row = db(q).select(db.v_users.id.count(), groupby=db.v_users.id).first()
    if row is None:
        n = 0
    else:
        n = row._extra[db.v_users.id.count()]
    data = db(q).select(db.v_users.fullname,
                        db.v_users.id,
                        db.v_users.email,
                        orderby=o,
                        limitby=(0,max_search_result),
                        groupby=db.v_users.id,
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_group(pattern):
    t = datetime.datetime.now()
    o = db.auth_group.role
    q = db.auth_group.privilege == 'F'
    q = _where(q, 'auth_group', pattern, 'role')
    q = q_filter(q, group_field=db.auth_group.role)
    n = db(q).count()
    data = db(q).select(o,
                        db.auth_group.id,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_safe_file(pattern):
    t = datetime.datetime.now()
    o = db.safe.uuid
    q = db.safe.uuid.like(pattern) | db.safe.name.like(pattern)
    l = db.safe_team_publication.on(db.safe.id == db.safe_team_publication.file_id)
    q &= db.safe_team_publication.group_id.belongs(user_group_ids()) | \
         (db.safe.uploader == auth.user_id)
    n = db(q).count()
    data = db(q).select(o,
                        db.safe.name,
                        left=l,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_metric(pattern):
    t = datetime.datetime.now()
    o = db.metrics.metric_name
    q = db.metrics.metric_name.like(pattern)
    n = db(q).count()
    data = db(q).select(o,
                        db.metrics.id,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_chart(pattern):
    t = datetime.datetime.now()
    o = db.charts.chart_name
    q = db.charts.chart_name.like(pattern)
    n = db(q).count()
    data = db(q).select(o,
                        db.charts.id,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

def lib_search_report(pattern):
    t = datetime.datetime.now()
    o = db.reports.report_name
    q = db.reports.report_name.like(pattern)
    n = db(q).count()
    data = db(q).select(o,
                        db.reports.id,
                        orderby=o,
                        limitby=(0,max_search_result),
    ).as_list()
    t = datetime.datetime.now() - t
    return {
      "total": n,
      "data": data,
      "elapsed": "%f" % (t.seconds + 1. * t.microseconds / 1000000),
    }

