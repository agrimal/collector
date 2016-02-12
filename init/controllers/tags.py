#
# adm-tags view code
#

class table_tags(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)

        # from models/colprops/
        self.cols = tags_cols
        self.colprops = tags_colprops

        self.dataable = True
        self.wsable = True
        #self.extraline = True
        self.checkboxes = True
        self.checkbox_id_col = 'id'
        self.checkbox_id_table = 'tags'
        self.ajax_col_values = 'ajax_tags_col_values'
        self.force_cols = ["id", "tag_name"]
        self.span = ["id"]
        self.keys = ["id"]
        self.events = ["tags_change"]

@auth.requires_login()
def ajax_tags_col_values():
    table_id = request.vars.table_id
    t = table_tags(table_id, 'ajax_tags')
    col = request.args[0]
    o = db[t.colprops[col].table][col]
    q = db.tags.id > 0
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)
    t.object_list = db(q).select(o, orderby=o)
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_tags():
    table_id = request.vars.table_id
    t = table_tags(table_id, 'ajax_tags')
    o = db.tags.tag_name
    q = db.tags.id>0
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
        n = db(q).select(db.tags.id.count()).first()(db.tags.id.count())
        t.setup_pager(n)
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns()
        t.object_list = db(q).select(*cols, orderby=o, limitby=limitby, cacheable=False)
        return t.table_lines_data(n, html=False)

@auth.requires_login()
def tags():
    t = SCRIPT(
          """table_tags("layout", %s)""" % request_vars_to_table_options(),
        )
    return dict(table=t)

def tags_load():
    return tags()["table"]

#
# view-tagattach view code
#

class table_tagattach(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['tag_id',
                     'tag_name',
                     'nodename',
                     'svcname',
                     'created']
        self.colprops = {
            'tag_id': HtmlTableColumn(
                     table='v_tags_full',
                     field='tag_id',
                    ),
            'tag_name': HtmlTableColumn(
                     table='v_tags_full',
                     field='tag_name',
                    ),
            'created': HtmlTableColumn(
                     table='v_tags_full',
                     field='created',
                    ),
            'nodename': HtmlTableColumn(
                     table='v_tags_full',
                     field='nodename',
                    ),
            'svcname': HtmlTableColumn(
                     table='v_tags_full',
                     field='svcname',
                    ),
        }
        self.dataable = True
        #self.extraline = True
        self.checkboxes = True
        self.checkbox_id_col = 'ckid'
        self.checkbox_id_table = 'v_tags_full'
        self.ajax_col_values = 'ajax_tagattach_col_values'
        self.force_cols = ["ckid"]
        self.span = ["tag_id"]
        self.keys = ["tag_id", "nodename", "svcname"]
        self.events = ["tags", "node_tags_change", "svc_tags_change"]


@auth.requires_login()
def ajax_tagattach_col_values():
    table_id = request.vars.table_id
    t = table_tagattach(table_id, 'ajax_tagattach')
    col = request.args[0]
    o = db[t.colprops[col].table][col]
    q = db.v_tags_full.id >= 0
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)
    t.object_list = db(q).select(o, orderby=o)
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_tagattach():
    table_id = request.vars.table_id
    t = table_tagattach(table_id, 'ajax_tagattach')
    o = db.v_tags_full.tag_name | db.v_tags_full.nodename | db.v_tags_full.svcname

    q = db.v_tags_full.id >= 0
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
        n = db(q).select(db.v_tags_full.id.count()).first()(db.v_tags_full.id.count())
        t.setup_pager(n)
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns()
        t.object_list = db(q).select(*cols, orderby=o, limitby=limitby, cacheable=False)
        return t.table_lines_data(n, html=False)

@auth.requires_login()
def tagattach():
    t = SCRIPT(
          """table_tagattach("layout", %s)""" % request_vars_to_table_options(),
        )
    return dict(table=t)

def tagattach_load():
    return tagattach()["table"]

