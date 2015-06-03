from gluon.dal import smart_query

api_services_doc = {}

def svc_responsible(svcname):
    q = db.services.svc_name == svcname
    n = db(q).count()
    if n == 0:
        raise Exception("Service %s does not exist" % svcname)
    q &= db.services.svc_app == db.apps.app
    q &= db.apps.id == db.apps_responsibles.app_id
    db.apps_responsibles.group_id.belongs(user_group_ids())
    n = db(q).count()
    if n != 1:
        raise Exception("Not authorized: user is not responsible for service %s" % svcname)


#
api_services_doc["/services/<svcname>"] = """
### GET

Description:

- Display all services properties.
- Display selected services properties.

Optional parameters:

- **props**
. A list of properties to include in data.
. If omitted, all properties are included.
. The separator is ','.
. Available properties are: ``%(props)s``:green.

- **query**
. A web2py smart query

Example:

``# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services/mysvc?props=svcname,app``

""" % dict(
        email=user_email(),
        collector=request.env.http_host,
        props=", ".join(sorted(db.services.fields)),
      )

def get_service(svcname, props=None):
    q = db.services.svc_name == svcname
    q = _where(q, 'services', domain_perms(), 'svc_name')
    cols = props_to_cols(props, tables=["services"])
    data = db(q).select(*cols, cacheable=True).as_list()[0]
    return dict(data=data)


#
api_services_doc["/services"] = """
### GET

Description:

- List all services and their selected properties.
- List service names and their selected properties for services matching a specified
  filterset id.

Optional parameters:

- **props**
. A list of properties to include in each data dictionnary.
. If omitted, all propertoes are included.
. The separator is ','.
. Available properties are: ``%(props)s``:green.

- **fset_id**
. Filter the services list using the filterset identified by fset_id.

- **query**
. A web2py smart query

Example:

``# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services?props=svc_name,app&fset_id=10``

""" % dict(
        email=user_email(),
        collector=request.env.http_host,
        props=", ".join(sorted(db.services.fields)),
      )

def get_services(props=None, fset_id=None, query=None):
    q = db.services.id > 0
    q = _where(q, 'services', domain_perms(), 'svc_name')
    if fset_id:
        q = apply_filters(q, service_field=db.services.svc_name, fset_id=fset_id)
    if query:
        cols = props_to_cols(None, tables=["services"])
        q &= smart_query(cols, query)
    cols = props_to_cols(props, tables=["services"])
    rows = db(q).select(*cols, cacheable=True)
    data = [r.as_dict() for r in rows]
    return dict(data=data)


#
api_services_doc["/services/<service>/alerts"] = """
### GET

Description:

- List a service alerts.

Optional parameters:

- **props**
. A list of properties to include in each dictionnary.
. If omitted, all properties are included.
. The separator is ','.
. Available properties are: ``%(props)s``:green.

- **query**
. A web2py smart query

Example:

``# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services/mysvc/alerts``

""" % dict(
        email=user_email(),
        collector=request.env.http_host,
        props=", ".join(sorted(db.dashboard.fields)),
      )

def get_service_alerts(svcname, props=None, query=None):
    q = db.dashboard.dash_svcname == svcname
    q &= _where(None, 'dashboard', domain_perms(), 'dash_svcname')
    if query:
        cols = props_to_cols(None, ["dashboard"])
        q &= smart_query(cols, query)
    cols = props_to_cols(props, ["dashboard"])
    data = db(q).select(*cols, cacheable=True).as_list()
    data = mangle_alerts(data)
    return dict(data=data)


#
api_services_doc["/services/<svcname>/nodes"] = """
### GET

Description:

- Display service instance status on each of its nodes.

Optional parameters:

- **props**
. A list of properties to include in data.
. If omitted, all properties are included.
. The separator is ','.
. Available properties are: ``%(props)s``:green.

- **query**
. A web2py smart query

Example:

``# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services/mysvc/nodes?props=mon_svcname,mon_availstatus``

""" % dict(
        email=user_email(),
        collector=request.env.http_host,
        props=", ".join(sorted(db.svcmon.fields)),
      )


def get_service_nodes(svcname, props=None, query=None):
    q = db.svcmon.mon_svcname == svcname
    q = _where(q, 'svcmon', domain_perms(), 'mon_svcname')
    if query:
        cols = props_to_cols(None, tables=["svcmon"])
        q &= smart_query(cols, query)
    cols = props_to_cols(props, tables=["svcmon"])
    rows = db(q).select(*cols, cacheable=True)
    data = [r.as_dict() for r in rows]
    return dict(data=data)

#
api_services_doc["/services/<svcname>/nodes/<nodename>"] = """
### GET

Description:

- Display service instance status on the specified node.

Optional parameters:

- **props**
. A list of properties to include in data.
. If omitted, all properties are included.
. The separator is ','.
. Available properties are: ``%(props)s``:green.

- **query**
. A web2py smart query

Example:

``# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services/mysvc/nodes/mynode?props=mon_svcname,mon_availstatus``

""" % dict(
        email=user_email(),
        collector=request.env.http_host,
        props=", ".join(sorted(db.svcmon.fields)),
      )

def get_service_node(svcname, nodename, props=None, query=None):
    q = db.svcmon.mon_svcname == svcname
    q &= db.svcmon.mon_nodname == nodename
    q = _where(q, 'svcmon', domain_perms(), 'mon_svcname')
    if query:
        cols = props_to_cols(None, tables=["svcmon"])
        q &= smart_query(cols, query)
    cols = props_to_cols(props, tables=["svcmon"])
    rows = db(q).select(*cols, cacheable=True)
    data = [r.as_dict() for r in rows]
    return dict(data=data)


