def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

class col_dash_icons(HtmlTableColumn):
    def html(self, o):
        d = SPAN(
              _onclick='$("#dashboard_f_dash_type").val("%s");'%o['dash_type']+self.t.ajax_submit(),
              _class="search16 clickable",
            )
        return d

class col_dash_history(HtmlTableColumn):
    def html(self, o):
        id = self.get(o)
        d = DIV(
              T("loading"),
              _class="dynamicsparkline",
              _id=id
            )
        return d

class col_dash_alerts(HtmlTableColumn):
    def html(self, o):
        return html_bar(o['dash_alerts'], self.t.total_alerts)

class col_dash_cumulated_severity(HtmlTableColumn):
    def html(self, o):
        return html_bar(o['dash_severity'], self.t.total_severity)

def spark_data(data):
    if len(data) == 0:
        l = [None]
    elif len(data) == 1:
        l = [str(data[0][1])]
    else:
        d = {}
        l = []
        last_value = data[-1][1]
        begin = data[0][0]
        if begin == 0:
            return str(data[0][1])
        if begin > 20:
            begin = 20
        for a, b in data:
            d[a] = b
        for i in range(0, begin):
            if i in d:
                l.append(d[i])
                last_value = d[i]
            else:
                #l.append(last_value)
                l.append(None)
        l.reverse()
    return l

def html_bar(val, total):
    if total ==  0:
        p = 0
    else:
        p = 100-100*val/total
    p = "%d%%"%int(p)
    n = "%d"%(val)
    d = DIV(
          DIV(
            DIV(
              _style="""font-size: 0px;
                        line-height: 0px;
                        height: 4px;
                        min-width: 0%%;
                        max-width: %(p)s;
                        width: %(p)s;
                        background: #dddddd;
                     """%dict(p=p),
            ),
            _style="""text-align: left;
                      margin: 2px auto;
                      background: #FF7863;
                      overflow: hidden;
                   """,
          ),
          DIV(n),
          _style="""margin: auto;
                    text-align: right;
                    width: 100%;
                 """,
        )
    return d

class table_dash_agg(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['dash_icons', 'dash_type', 'dash_alerts', 'dash_severity', 'dash_history']
        self.colprops = {
            'dash_icons': col_dash_icons(
                     title='Filter',
                     field='dummy',
                     display=True,
                     img='search',
                    ),
            'dash_type': HtmlTableColumn(
                     title='Type',
                     field='dash_type',
                     table='dash_agg',
                     display=True,
                     img='alert16',
                    ),
            'dash_severity': col_dash_cumulated_severity(
                     title='Cumulated severity',
                     field='dash_severity',
                     table='dash_agg',
                     display=True,
                     img='alert16',
                     _class='numeric',
                    ),
            'dash_alerts': col_dash_alerts(
                     title='Number of alerts',
                     field='dash_alerts',
                     table='dash_agg',
                     display=True,
                     img='alert16',
                     _class='numeric',
                    ),
            'dash_history': col_dash_history(
                     title='History',
                     field='dash_history',
                     table='dash_agg',
                     display=True,
                     img='alert16',
                     _class='numeric',
                    ),
        }
        self.colprops['dash_alerts'].t = self
        self.colprops['dash_severity'].t = self

@auth.requires_login()
def ajax_dash_agg():
    t = table_dashboard('dashboard', 'ajax_dashboard')
    mt = table_dash_agg('dash_agg', 'ajax_dash_agg')
    mt.colprops['dash_icons'].t = t

    q = db.dashboard.id > 0
    j = db.dashboard.dash_nodename == db.nodes.nodename
    l1 = db.nodes.on(j)
    j = db.dashboard.dash_svcname == db.services.svc_name
    l2 = db.services.on(j)
    for f in set(t.cols)-set(t.special_filtered_cols):
        q = _where(q, 'dashboard', t.filter_parse(f), f)
    q &= _where(None, 'dashboard', domain_perms(), 'dash_svcname')|_where(None, 'dashboard', domain_perms(), 'dash_nodename')
    q = apply_gen_filters(q, t.tables())

    sql1 = db(q)._select().rstrip(';').replace('services.id, ','').replace('nodes.id, ','').replace('dashboard.id>0 AND', '')
    regex = re.compile("SELECT .* FROM")
    sql1 = regex.sub('', sql1)

    q = db.dash_agg.id > 0
    for f in mt.cols:
        q = _where(q, mt.colprops[f].table, mt.filter_parse(f), f)
    where = str(q).replace("dash_agg.", "t.")

    mt.dbfilterable = False
    mt.pageable = False
    mt.filterable = True
    mt.additional_inputs = t.ajax_inputs()

    sql2 = """select * from (
                select
                  dashboard.id,
                  dashboard.dash_type,
                  count(dashboard.dash_type) as dash_alerts,
                  sum(dashboard.dash_severity) as dash_severity
                from %(sql)s
                group by dash_type
                order by dash_severity desc
              ) t
              where %(where)s
              """%dict(
                sql=sql1,
                where=where,
           )

    rows = db.executesql(sql2)

    mt.object_list = map(lambda x: {'dash_type': x[1],
                                    'dash_alerts':x[2],
                                    'dash_severity':x[3]},
                          rows)

    from hashlib import md5
    o = md5()
    o.update(sql1)
    filters_md5 = str(o.hexdigest())

    q = db.dashboard_log.dash_filters_md5==filters_md5
    row = db(q).select(db.dashboard_log.dash_date,
                       orderby=~db.dashboard_log.id,
                       limitby=(0,1)).first()

    now = datetime.datetime.now()

    if row is None:
        last_date = now - datetime.timedelta(minutes=2)
    else:
        last_date = row.dash_date

    if now > last_date + datetime.timedelta(minutes=1):
        # purge old entries
        q = db.dashboard_log.dash_date < now - datetime.timedelta(hours=24)
        db(q).delete()

    mt.total_alerts = 0
    mt.total_severity = 0
    for i, r in enumerate(mt.object_list):
        mt.total_alerts += mt.object_list[i]['dash_alerts']
        mt.total_severity += mt.object_list[i]['dash_severity']
        if now > last_date + datetime.timedelta(minutes=1):
            db.dashboard_log.insert(dash_filters_md5=filters_md5,
                                    dash_alerts=mt.object_list[i]['dash_alerts'],
                                    dash_type=mt.object_list[i]['dash_type'])
        mt.object_list[i]['dash_history'] = '-'.join((filters_md5, mt.object_list[i]['dash_type'].replace(" ","_")))

    if len(request.args) == 1 and request.args[0] == 'csv':
        return mt.csv()

    return DIV(
             mt.html(),
             SCRIPT(
               """
function refresh_sparklines() {
 $('.dynamicsparkline').each(function(i){
  id=$(this).attr("id")
  $.getJSON("%(url)s/"+id, function(data) {
        $('#'+data[0]).sparkline(data[1])
  })
 })
}
refresh_sparklines()
$('#dash_agg').stopTime();
$('#dash_agg').everyTime(60000,function(){
 refresh_sparklines()
})
"""%dict(url=URL(r=request, f='call/json/update_dashboard_log')),
               _name=mt.id+"_to_eval"
             ),
           )

@service.json
def update_dashboard_log(s):
    try:
        md5, dash_type = s.split('-')
        dash_type = dash_type.replace("_", " ")
    except:
        return [None]

    """ Insert a datapoint in dashboard_log with
        the same value as the last point for dash_filters_md5/dash_type
        If a point already has been inserted in the last minute, skip.
    """
    sql = """insert into dashboard_log
               select
                 NULL,
                 dash_type,
                 dash_filters_md5,
                 dash_alerts,
                 now()
               from dashboard_log
               where
                 dash_filters_md5="%(md5)s" and
                 dash_type="%(dash_type)s" and
                 dash_date < date_sub(now(), interval 1 minute)
               order by dash_date desc
               limit 1
          """%dict(md5=md5, dash_type=dash_type)
    db.executesql(sql)
    with open("/tmp/bar", "w") as f:
        f.write(sql+'\n')

    now = datetime.datetime.now()
    thisminute = now.toordinal()*1440+now.hour*60+now.minute

    q = db.dashboard_log.dash_filters_md5 == md5
    q &= db.dashboard_log.dash_type == dash_type
    q &= db.dashboard_log.dash_date > now - datetime.timedelta(minutes=21)
    rows = db(q).select()
    data = []
    for row in rows:
        rowminute = row.dash_date.toordinal()*1440+row.dash_date.hour*60+row.dash_date.minute
        data.append((thisminute-rowminute,
                     row.dash_alerts))

    return s, spark_data(data)


#############################################################################


class col_dash_entry(HtmlTableColumn):
    def get(self, o):
        dash_dict = self.t.colprops['dash_dict'].get(o)
        dash_fmt = self.t.colprops['dash_fmt'].get(o)
        if dash_dict is None or len(dash_dict) == 0:
            return ""
        try:
            d = json.loads(dash_dict)
            for k in d:
                if isinstance(d[k], str) or isinstance(d[k], unicode):
                    d[k] = d[k].encode('utf8')
            s = T.translate(dash_fmt, d)
        except KeyError:
            s = 'error parsing: %s'%dash_dict
        except json.decoder.JSONDecodeError:
            s = 'error loading JSON: %s'%dash_dict
        except UnicodeEncodeError:
            s = 'error transcoding: %s'%dash_dict
        except TypeError:
            s = 'type error: %s'%dash_dict
        return s

class col_dash_links(HtmlTableColumn):
    def link_action_errors(self, o):
       dash_svcname = self.t.colprops['dash_svcname'].get(o)
       i = A(
             _href=URL(r=request,c='svcactions',f='svcactions',
                    vars={'actions_f_svcname': dash_svcname,
                          'actions_f_status': 'err',
                          'actions_f_ack': '!1|empty',
                          'clear_filters': 'true'}),
             _title=T("Service action errors"),
             _class='alert16 clickable',
           )
       return i

    def link_actions(self, o):
       dash_svcname = self.t.colprops['dash_svcname'].get(o)
       i = A(
             _href=URL(r=request,c='svcactions',f='svcactions',
                    vars={'actions_f_svcname': dash_svcname,
                          'actions_f_begin': '>%s'%str(now-datetime.timedelta(days=7)),
                          'clear_filters': 'true'}),
             _title=T("Service actions"),
             _class='action16 clickable',
           )
       return i

    def link_svcmon(self, o):
       dash_svcname = self.t.colprops['dash_svcname'].get(o)
       i = A(
             _href=URL(r=request,c='default',f='svcmon',
                    vars={'svcmon_f_svc_name': dash_svcname,
                          'clear_filters': 'true'}),
             _title=T("Service status"),
             _class='svc clickable',
           )
       return i

    def link_checks(self, o):
       dash_nodename = self.t.colprops['dash_nodename'].get(o)
       i = A(
             _href=URL(r=request,c='checks',f='checks',
                    vars={'checks_f_chk_nodename': dash_nodename,
                          'clear_filters': 'true'}),
             _title=T("Checks"),
             _class='check16 clickable',
           )
       return i

    def link_nodes(self, o):
       dash_nodename = self.t.colprops['dash_nodename'].get(o)
       i = A(
             _href=URL(r=request,c='nodes',f='nodes',
                    vars={'nodes_f_nodename': dash_nodename,
                          'clear_filters': 'true'}),
             _title=T("Node"),
             _class='node16 clickable',
           )
       return i

    def link_obsolescence(self, o, t):
       i = A(
             _href=URL(r=request,c='obsolescence',f='obsolescence_config',
                    vars={'obs_f_obs_type': t,
                          'clear_filters': 'true'}),
             _title=T("Obsolescence configuration"),
             _class='%s16 clickable'%t,
           )
       return i

    def html(self, o):
       l = []
       dash_type = self.t.colprops['dash_type'].get(o)
       if dash_type == "action errors":
           l.append(self.link_action_errors(o))
           l.append(self.link_actions(o))
       elif dash_type == "check out of bounds" or \
            dash_type == "check value not updated":
           l.append(self.link_checks(o))
       elif dash_type == "service status not updated" or \
            dash_type == "service configuration not updated" or \
            dash_type == "service available but degraded" or \
            dash_type == "service frozen" or \
            dash_type == "service unavailable":
           l.append(self.link_svcmon(o))
       elif dash_type == "node warranty expired" or \
            dash_type == "node information not updated" or \
            dash_type == "node without warranty end date" or \
            dash_type == "node without asset information" or \
            dash_type == "node close to warranty end":
           l.append(self.link_nodes(o))
       elif "os obsolescence" in dash_type:
           l.append(self.link_obsolescence(o, 'os'))
       elif "obsolescence" in dash_type:
           l.append(self.link_obsolescence(o, 'hw'))

       return SPAN(l)

class col_dash_severity(HtmlTableColumn):
    def html(self, o):
       d = self.get(o)
       c = "boxed_small "
       if d == 0:
           c += "bggreen"
       elif d == 1:
           c += "bgorange"
       elif d == 2:
           c += "bgred"
       elif d == 3:
           c += "bgdarkred"
       else:
           c += "bgblack"
       return DIV(d, _class=c)

class table_dashboard(HtmlTable):
    def __init__(self, id=None, func=None, innerhtml=None):
        if id is None and 'tableid' in request.vars:
            id = request.vars.tableid
        HtmlTable.__init__(self, id, func, innerhtml)
        self.cols = ['dash_severity',
                     'dash_links',
                     'dash_type',
                     'dash_svcname',
                     'dash_nodename',
                     'dash_entry',
                     'dash_fmt',
                     'dash_dict',
                     'dash_created']
        self.colprops = {
            'dash_links': col_dash_links(
                     title='Links',
                     field='dummy',
                     img='link16',
                     display=True,
                    ),
            'dash_created': HtmlTableColumn(
                     title='Begin date',
                     table='dashboard',
                     field='dash_created',
                     img='time16',
                     display=True,
                    ),
            'dash_severity': col_dash_severity(
                     title='Severity',
                     table='dashboard',
                     field='dash_severity',
                     img='action16',
                     display=True,
                    ),
            'dash_svcname': col_svc(
                     title='Service',
                     table='dashboard',
                     field='dash_svcname',
                     img='svc',
                     display=True,
                    ),
            'dash_nodename': col_node(
                     title='Node',
                     table='dashboard',
                     field='dash_nodename',
                     img='node16',
                     display=True,
                    ),
            'dash_entry': col_dash_entry(
                     title='Alert',
                     table='dashboard',
                     field='dummy',
                     img='log16',
                     display=True,
                    ),
            'dash_fmt': HtmlTableColumn(
                     title='Format',
                     table='dashboard',
                     field='dash_fmt',
                     img='log16',
                     display=False,
                    ),
            'dash_dict': HtmlTableColumn(
                     title='Dictionary',
                     table='dashboard',
                     field='dash_dict',
                     img='log16',
                     display=False,
                    ),
            'dash_type': HtmlTableColumn(
                     title='Type',
                     table='dashboard',
                     field='dash_type',
                     img='log16',
                     display=True,
                    ),
        }
        self.colprops['dash_svcname'].t = self
        self.colprops['dash_nodename'].t = self
        self.colprops['dash_links'].t = self
        self.colprops['dash_entry'].t = self
        self.dbfilterable = True
        self.extraline = True
        self.checkbox_id_table = 'dashboard'
        self.checkbox_id_col = 'id'
        self.special_filtered_cols = ['dash_entry']
        self.autorefresh = 60000

@auth.requires_login()
def ajax_dashboard_col_values():
    t = table_dashboard('dashboard', 'ajax_dashboard')
    col = request.args[0]
    o = db.dashboard[col]
    q = db.dashboard.id > 0
    for f in set(t.cols)-set(t.special_filtered_cols):
        q = _where(q, 'dashboard', t.filter_parse(f), f)
    q &= _where(None, 'dashboard', domain_perms(), 'dash_svcname')|_where(None, 'dashboard', domain_perms(), 'dash_nodename')
    q = apply_gen_filters(q, t.tables())
    t.object_list = db(q).select(o, orderby=o, groupby=o)
    return t.col_values_cloud(col)

@auth.requires_login()
def ajax_dashboard():
    t = table_dashboard('dashboard', 'ajax_dashboard')
    o = ~db.dashboard.dash_severity|db.dashboard.dash_type
    q = db.dashboard.id > 0
    for f in set(t.cols)-set(t.special_filtered_cols):
        q = _where(q, 'dashboard', t.filter_parse(f), f)
    q &= _where(None, 'dashboard', domain_perms(), 'dash_svcname')|_where(None, 'dashboard', domain_perms(), 'dash_nodename')
    q = apply_gen_filters(q, t.tables())

    n = db(q).count()
    t.setup_pager(n)
    t.object_list = db(q).select(limitby=(t.pager_start,t.pager_end), orderby=o)

    mt = table_dash_agg('dash_agg', 'ajax_dash_agg')

    return DIV(
             SCRIPT(
               mt.ajax_submit(additional_inputs=t.ajax_inputs()),
               _name=t.id+"_to_eval"
             ),
             DIV(
               IMG(_src=URL(r=request,c='static',f='spinner.gif')),
               _id="dash_agg",
             ),
             t.html(),
           )

@auth.requires_login()
def index():
    t = DIV(
          ajax_dashboard(),
          _id='dashboard',
        )
    return dict(table=t)

#
# Dashboard change detection
#
def dash_changed():
    sql = """select (now()-update_time)*6/10
             from information_schema.tables
             where
               table_schema = 'opensvc' and
               table_name = 'dashboard'
          """
    rows = db.executesql(sql)
    return rows[0][0]

