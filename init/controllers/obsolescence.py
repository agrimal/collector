class table_obs(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['id',
                     'obs_count',
                     'obs_type',
                     'obs_name',
                     'obs_warn_date',
                     'obs_alert_date']
        self.keys = ['id']
        self.colprops = {
            'obs_type': HtmlTableColumn(
                     title='Type',
                     table='v_obsolescence',
                     field='obs_type',
                     img='obs16',
                     display=True,
                     _class="obs_type",
                    ),
            'obs_name': HtmlTableColumn(
                     title='Name',
                     table='v_obsolescence',
                     field='obs_name',
                     img='obs16',
                     display=True,
                    ),
            'obs_warn_date': HtmlTableColumn(
                     title='Warn date',
                     table='v_obsolescence',
                     field='obs_warn_date',
                     img='time16',
                     display=True,
                     _class="datetime_no_age",
                    ),
            'obs_alert_date': HtmlTableColumn(
                     title='Alert date',
                     table='v_obsolescence',
                     field='obs_alert_date',
                     img='time16',
                     display=True,
                     _class="datetime_no_age",
                    ),
            'obs_count': HtmlTableColumn(
                     title='Count',
                     table='v_obsolescence',
                     field='obs_count',
                     img='obs16',
                     display=True,
                     _class="obs_count",
                    ),
            'id': HtmlTableColumn(
                     title='Id',
                     table='v_obsolescence',
                     field='id',
                     img='key',
                    ),
        }
        self.ajax_col_values = 'ajax_obs_col_values'
        self.checkboxes = True
        self.extraline = True
        self.dataable = True
        self.wsable = True
        self.events = ["obsolescence_change"]
        self.force_cols = ["id", "obs_type", "obs_name"]

@auth.requires_login()
def ajax_obs_col_values():
    table_id = request.vars.table_id
    t = table_obs(table_id, 'ajax_obs')
    col = request.args[0]
    o = db[t.colprops[col].table][col]
    q = db.v_obsolescence.id >0
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)

    t.object_list = db(q).select(o, orderby=o)
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_obs():
    table_id = request.vars.table_id
    t = table_obs(table_id, 'ajax_obs')

    o = ~db.v_obsolescence.obs_count

    q = db.v_obsolescence.id >0
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)

    if len(request.args) == 1 and request.args[0] == 'csv':
        t.csv_q = q
        t.csv_orderby = o
        t.csv_limit = 10000
        return t.csv()
    if len(request.args) == 1 and request.args[0] == 'commonality':
        t.csv_q = q
        return t.do_commonality()
    if len(request.args) == 1 and request.args[0] == 'data':
        n = db(q).count()
        t.setup_pager(n)
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns()
        t.object_list = db(q).select(*cols, orderby=o, limitby=limitby)
        return t.table_lines_data(n, html=False)


@auth.requires_login()
def obsolescence_config():
    t = SCRIPT(
          """$.when(osvc.app_started).then(function(){ table_obsolescence("layout", %s) })""" % request_vars_to_table_options(),
        )
    return dict(table=t)

def obsolescence_config_load():
    return obsolescence_config()["table"]

