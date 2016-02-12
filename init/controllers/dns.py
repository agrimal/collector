import os

#
# Domains
#
class table_dns_domains(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['id',
                     'name',
                     'master',
                     'last_check',
                     'type',
                     'notified_serial',
                     'account']
        self.colprops = {
            'id': HtmlTableColumn(
                     table="domains",
                     field='id',
                    ),
            'name': HtmlTableColumn(
                     table="domains",
                     field='name',
                    ),
            'master': HtmlTableColumn(
                     table="domains",
                     field='master',
                    ),
            'last_check': HtmlTableColumn(
                     table="domains",
                     field='last_check',
                    ),
            'type': HtmlTableColumn(
                     table="domains",
                     field='type',
                    ),
            'notified_serial': HtmlTableColumn(
                     table="domains",
                     field='notified_serial',
                    ),
            'account': HtmlTableColumn(
                     table="domains",
                     field='account',
                    ),
        }
        self.keys = ["id"]
        self.span = ["id"]
        self.force_cols = ["id"]
        self.dbfilterable = False
        self.ajax_col_values = 'ajax_dns_domains_col_values'
        self.checkboxes = True
        self.dataable = True
        self.wsable = True
        self.events = ["pdns_domains_change"]

@auth.requires_login()
def ajax_dns_domains_col_values():
    table_id = request.vars.table_id
    t = table_dns_domains(table_id, 'ajax_dns_domains')
    col = request.args[0]
    o = dbdns.domains[col]
    q = dbdns.domains.id > 0
    for f in set(t.cols):
        q = _where(q, 'domains', t.filter_parse(f), f, db=dbdns)
    t.object_list = dbdns(q).select(o, orderby=o)
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_dns_domains():
    table_id = request.vars.table_id
    t = table_dns_domains(table_id, 'ajax_dns_domains')
    o = ~dbdns.domains.name
    q = dbdns.domains.id > 0
    for f in set(t.cols):
        q = _where(q, 'domains', t.filter_parse(f), f, db=dbdns)

    if len(request.args) == 1 and request.args[0] == 'data':
        n = dbdns(q).count()
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns(db=dbdns)
        t.object_list = dbdns(q).select(*cols, orderby=o, limitby=limitby, cacheable=False)
        return t.table_lines_data(n, html=False)

#
# Records
#
class table_dns_records(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['id',
                     'domain_id',
                     'name',
                     'type',
                     'content',
                     'ttl',
                     'prio',
                     'change_date']
        self.force_cols = ["id"]
        self.keys = ["id"]
        self.span = ["id"]
        self.colprops = {
            'id': HtmlTableColumn(
                     table='records',
                     field='id',
                    ),
            'domain_id': HtmlTableColumn(
                     table='records',
                     field='domain_id',
                    ),
            'name': HtmlTableColumn(
                     table='records',
                     field='name',
                    ),
            'type': HtmlTableColumn(
                     table='records',
                     field='type',
                    ),
            'content': HtmlTableColumn(
                     table='records',
                     field='content',
                    ),
            'ttl': HtmlTableColumn(
                     table='records',
                     field='ttl',
                    ),
            'prio': HtmlTableColumn(
                     table='records',
                     field='prio',
                    ),
            'change_date': HtmlTableColumn(
                     table='records',
                     field='change_date',
                    ),
        }
        self.dataable = True
        self.wsable = True
        self.events = ["pdns_records_change"]
        self.dbfilterable = False
        self.ajax_col_values = 'ajax_dns_records_col_values'
        self.checkboxes = True

def ptr_add():
    if request.vars.type != 'A':
        return
    request.vars.type = 'PTR'
    tmp = request.vars.content
    l = tmp.split('.')
    l.reverse()
    tmp = '.'.join(l)
    tmp += ".in-addr.arpa"
    request.vars.content = request.vars.name
    request.vars.name = tmp
    form = _record_form()
    if form.accepts(request.vars):
        response.flash = T("a and ptr recorded")
        _log('dns.records.add',
             'added record %(u)s',
             dict(u=request.vars.name))
    elif form.errors:
        response.flash = T("errors in ptr form")

@auth.requires_login()
def ajax_dns_records_col_values():
    table_id = request.vars.table_id
    t = table_dns_records(table_id, 'ajax_dns_records')
    col = request.args[0]
    o = dbdns.records[col]
    q = dbdns.records.id > 0
    for f in set(t.cols):
        q = _where(q, 'records', t.filter_parse(f), f, db=dbdns)
    t.object_list = dbdns(q).select(o, orderby=o)
    return t.col_values_cloud_ungrouped(col)

@auth.requires_login()
def ajax_dns_records():
    table_id = request.vars.table_id
    t = table_dns_records(table_id, 'ajax_dns_records')

    o = ~dbdns.records.name
    q = dbdns.records.id > 0
    for f in set(t.cols):
        q = _where(q, 'records', t.filter_parse(f), f, db=dbdns)

    if len(request.args) == 1 and request.args[0] == 'data':
        n = dbdns(q).count()
        limitby = (t.pager_start,t.pager_end)
        cols = t.get_visible_columns(db=dbdns)
        t.object_list = dbdns(q).select(*cols, orderby=o, limitby=limitby, cacheable=False)
        return t.table_lines_data(n, html=False)

def is_exe(fpath):
    """Returns True if file path is executable, False otherwize
    does not follow symlink
    """
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

def which(program):
    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext

    fpath, fname = os.path.split(program)
    if fpath:
        if os.path.isfile(program) and is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return candidate

    return None

@auth.requires_login()
def ping():
    if not which("fping"):
        return SPAN(T("fping not found. disable ip testing"))
    ip = request.args[0]
    import subprocess
    cmd = ['fping', ip]
    p = subprocess.Popen(cmd)
    out, err = p.communicate()
    if p.returncode == 0:
        return DIV(
                 T("ip is alive"),
                 _style="font-weight:bold;color:darkred",
               )
    return SPAN(T("ip is not alive"))

#
# Common
#
@auth.requires_login()
def dns():
    t = SCRIPT(
          """view_dns("layout", %s)""" % request_vars_to_table_options(),
        )
    return dict(table=t)

def dns_load():
    return dns()["table"]

