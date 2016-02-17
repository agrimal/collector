class table_packages(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['nodename']
        self.cols += ['id',
                      'pkg_name',
                      'pkg_version',
                      'pkg_arch',
                      'pkg_type',
                      'sig_provider',
                      'pkg_sig',
                      'pkg_install_date',
                      'pkg_updated']
        self.cols += nodes_cols
        self.colprops = nodes_colprops
        self.colprops.update(packages_colprops)
        self.ajax_col_values = 'ajax_packages_col_values'
        self.span = ["id"]
        self.keys = ["id"]

@auth.requires_login()
def ajax_packages_col_values():
    table_id = request.vars.table_id
    t = table_packages(table_id, 'ajax_packages')
    col = request.args[0]
    o = db[t.colprops[col].table][col]
    q = db.packages.pkg_nodename==db.nodes.nodename
    q = _where(q, 'packages', domain_perms(), 'pkg_nodename')
    q = apply_filters(q, db.packages.pkg_nodename, None)
    j = db.packages.pkg_sig == db.pkg_sig_provider.sig_id
    l = db.pkg_sig_provider.on(j)
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)
    t.object_list = db(q).select(o, orderby=o, left=l)
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_packages():
    table_id = request.vars.table_id
    t = table_packages(table_id, 'ajax_packages')
    o = db.packages.pkg_nodename
    o |= db.packages.pkg_name
    o |= db.packages.pkg_arch

    q = db.packages.id>0
    q &= db.packages.pkg_nodename==db.nodes.nodename
    q = _where(q, 'packages', domain_perms(), 'pkg_nodename')
    q = apply_filters(q, db.packages.pkg_nodename, None)
    j = db.packages.pkg_sig == db.pkg_sig_provider.sig_id
    l = db.pkg_sig_provider.on(j)
    for f in t.cols:
        q = _where(q, t.colprops[f].table, t.filter_parse(f), f)

    if len(request.args) == 1 and request.args[0] == 'csv':
        t.csv_q = q
        t.csv_left = l
        t.csv_orderby = o
        return t.csv()
    if len(request.args) == 1 and request.args[0] == 'commonality':
        t.csv_q = q
        t.csv_left = l
        return t.do_commonality()
    if len(request.args) == 1 and request.args[0] == 'data':
        n = db(q).select(db.packages.id.count(), left=l).first()(db.packages.id.count())
        t.setup_pager(n)
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns()
        t.object_list = db(q).select(*cols, orderby=o, limitby=limitby, cacheable=False, left=l)
        return t.table_lines_data(n, html=False)



@auth.requires_login()
def packages():
    t = SCRIPT(
          """table_packages("layout", %s)""" % request_vars_to_table_options(),
        )
    return dict(table=t)

def packages_load():
    return packages()["table"]

