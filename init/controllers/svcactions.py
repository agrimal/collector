class table_actions(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['svc_id',
                     'svcname',
                     'node_id',
                     'nodename',
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
                     'acked_comment',
                    ]
        self.colprops = {
            'svc_id': HtmlTableColumn(
                table = 'svcactions',
                field='svcname',
            ),
            'svcname': HtmlTableColumn(
                table = 'services',
                field='svcname',
            ),
            'node_id': HtmlTableColumn(
                table = 'svcactions',
                field='node_id',
            ),
            'nodename': HtmlTableColumn(
                table = 'nodes',
                field='nodename',
            ),
            'pid': HtmlTableColumn(
                table = 'svcactions',
                field='pid',
            ),
            'action': HtmlTableColumn(
                table = 'svcactions',
                field='action',
            ),
            'status': HtmlTableColumn(
                table = 'svcactions',
                field='status',
            ),
            'begin': HtmlTableColumn(
                table = 'svcactions',
                field='begin',
            ),
            'end': HtmlTableColumn(
                table = 'svcactions',
                field='end',
            ),
            'status_log': HtmlTableColumn(
                table = 'svcactions',
                field='status_log',
            ),
            'cron': HtmlTableColumn(
                table = 'svcactions',
                field='cron',
            ),
            'time': HtmlTableColumn(
                table = 'svcactions',
                field='time',
            ),
            'id': HtmlTableColumn(
                table = 'svcactions',
                field='id',
            ),
            'ack': HtmlTableColumn(
                table = 'svcactions',
                field='ack',
            ),
            'acked_comment': HtmlTableColumn(
                table = 'svcactions',
                field='acked_comment',
            ),
            'acked_by': HtmlTableColumn(
                table = 'svcactions',
                field='acked_by',
            ),
            'acked_date': HtmlTableColumn(
                table = 'svcactions',
                field='acked_date',
            ),
        }
        cp = nodes_colprops
        del(cp['status'])
        self.colprops.update(cp)
        self.colprops.update(services_colprops)
        ncols = nodes_cols
        ncols.remove('updated')
        ncols.remove('status')
        self.cols += services_cols
        self.cols += ncols
        self.ajax_col_values = 'ajax_actions_col_values'
        self.span = ['pid']
        self.keys = ["id"]
        self.force_cols = ['node_id', 'nodename', 'svc_id', 'svcname', 'os_name', 'action']

@auth.requires_login()
def ajax_actions_col_values():
    table_id = request.vars.table_id
    t = table_actions(table_id, 'ajax_actions')
    col = request.args[0]
    o = db[t.colprops[col].table][col]
    q = db.svcactions.node_id == db.nodes.node_id
    q &= db.svcactions.svc_id == db.services.svc_id
    q = q_filter(q, app_field=db.services.svc_app)
    q = apply_filters_id(q, db.svcactions.node_id, db.svcactions.svc_id)
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)
    t.object_list = db(q).select(db[t.colprops[col].table][col],
                                 orderby=o,
                                 limitby=(0,10000))
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_actions():
    table_id = request.vars.table_id
    t = table_actions(table_id, 'ajax_actions')

    o = ~db.svcactions.id
    q = db.svcactions.node_id == db.nodes.node_id
    q &= db.svcactions.svc_id == db.services.svc_id
    q = q_filter(q, app_field=db.services.svc_app)
    q = apply_filters_id(q, db.svcactions.node_id, db.svcactions.svc_id)
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)

    if len(request.args) == 1 and request.args[0] == 'csv':
        t.csv_q = q
        t.csv_orderby = o
        return t.csv()
    if len(request.args) == 1 and request.args[0] == 'commonality':
        t.csv_q = q
        return t.do_commonality()
    if len(request.args) == 1 and request.args[0] == 'data':
        n = db(q).count()
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns()
        t.object_list = db(q).select(*cols, limitby=limitby, orderby=o, cacheable=True)
        return t.table_lines_data(n, html=False)

@auth.requires_login()
def svcactions():
    t = SCRIPT(
          """table_actions("layout", %s)""" % request_vars_to_table_options(),
        )
    return dict(table=t)

def svcactions_load():
    return svcactions()["table"]

