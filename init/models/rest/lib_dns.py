def create_zone(zone):
    domain_type = "MASTER"
    data = {
        "name": zone,
        "type": domain_type,
    }
    domain_id = dbdns.domains.insert(**data)

    _log('dns.domains.create',
         'domain %(name)s %(type)s auto created by dns update',
         dict(name=zone, type=domain_type),
        )
    ws_send('pdns_domains_change')

    # SOA
    data = {
        "name": zone,
        "type": "SOA",
        "content": config_get("dns_default_soa_content", config_get("dbopensvc", "")),
        "ttl": 86400,
        "domain_id": domain_id,
        "change_date": int((datetime.datetime.now()-datetime.datetime(1970, 1, 1)).total_seconds())
    }
    dbdns.records.insert(**data)

    fmt = 'record %(name)s %(type)s %(content)s created in domain %(domain)s'
    d = dict(name=data["name"], type=data["type"], content=data["content"], domain=zone)
    _log('dns.records.create', fmt, d)
    ws_send('pdns_records_change')

def sanitize_dns_name(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9\.]', '-', name)
    return name

def get_dns_domain(zone):
    q = dbdns.domains.name == zone
    return dbdns(q).select().first()

def raise_on_error(response):
    if response.errors:
        s = ", ".join(map(lambda x: ": ".join(x), response.errors.items()))
        raise Exception(s)

def addr_from_reverse(name):
    addr = name.split(".in-addr.")[0]
    v = addr.split(".")
    v.reverse()
    addr = ".".join(v)
    return addr

def dns_record_responsible(row, current={}):
    if not hasattr(auth.user, "node_id") and "Manager" in user_groups():
        return
    group_ids = user_group_ids()
    t = row.get("type")
    if t is None:
        t = current.get("type")
    t = str(t)
    name = row.get("name")
    if name is None:
        name = current.get("name")
    name = str(name)
    content = row.get("content")
    if content is None:
        content = current.get("content")
    content = str(content)

    if t in ("A", "AAAA"):
        addr = content
    elif t in ("PTR"):
        addr = addr_from_reverse(name)
    else:
        raise Exception("Manager privilege required to handle the %s record type"%t)
    sql = """
      select networks.id from
      networks, auth_group, auth_membership, auth_user where
        auth_group.id in (%(group_ids)s) and
        auth_group.role=networks.team_responsible and
        inet_aton("%(addr)s") >= inet_aton(networks.begin) and
        inet_aton("%(addr)s") <= inet_aton(networks.end)
    """ % dict(addr=addr, user_id=auth.user_id,
               group_ids = ','.join([repr(str(gid)) for gid in group_ids]))
    networks = db.executesql(sql)
    if len(networks) > 0:
        return

    sql = """
      select network_segments.id from
      network_segments, networks, network_segment_responsibles, auth_group, auth_membership, auth_user where
        network_segment_responsibles.group_id in (%(group_ids)s) and
        network_segments.id=network_segment_responsibles.seg_id and
        inet_aton("%(addr)s") >= inet_aton(network_segments.seg_begin) and
        inet_aton("%(addr)s") <= inet_aton(network_segments.seg_end)
    """ % dict(addr=addr, user_id=auth.user_id,
               group_ids = ','.join([repr(str(gid)) for gid in group_ids]))
    segments = db.executesql(sql)
    if len(segments) > 0:
        return

    raise Exception("Not allowed to manage the record %s %s %s"%(name, t, content))

def create_service_dns_record(instance_name=None, content=None, ttl=None):
    # short record name
    name = auth.user.svcname.split(".")[0]
    if "." in instance_name:
        raise Exception("No dots allowed in instance name '%s'" % instance_name)
    if instance_name and len(instance_name) > 0:
        name = name + "-" + instance_name
    name = sanitize_dns_name(name)

    # domain
    zone = config_get("dns_managed_zone", "opensvc")
    zone = zone.rstrip(".")
    zone = auth.user.svc_app + "." + zone
    zone = sanitize_dns_name(zone)
    domain = get_dns_domain(zone)
    if domain is None:
        create_zone(zone)
        domain = get_dns_domain(zone)
    if domain is None:
        raise Exception("failed to create the %s zone" % zone)

    # full record name
    name = name + "." + zone

    # record type
    if ":" in content:
        record_type = "AAAA"
    elif content.count(".") == 3:
        record_type = "A"
    else:
        raise Exception("invalid content type %s" % str(content))

    # record ttl
    if ttl is None:
        ttl = config_get("dns_default_ttl", 120)

    data = {
        "name": name,
        "type": record_type,
        "content": content,
        "ttl": ttl,
        "domain_id": domain.id,
        "change_date": int((datetime.datetime.now()-datetime.datetime(1970, 1, 1)).total_seconds())
    }
    dns_record_responsible(data)

    q = dbdns.records.id > 0
    q &= dbdns.records.name == data["name"]
    q &= dbdns.records.domain_id == data["domain_id"]
    row = dbdns(q).select().first()

    if row is not None:
        response = dbdns(q).validate_and_update(**data)
        op = "change"
    else:
        response = dbdns.records.validate_and_insert(**data)
        op = "create"
    raise_on_error(response)
    row = dbdns(q).select().first()

    fmt = 'record %(name)s %(type)s %(content)s %(op)sd in domain %(domain)s'
    d = dict(name=row.name, type=row.type, op=op, content=row.content, domain=str(row.domain_id))
    _log('dns.records.'+op, fmt, d)
    ws_send('pdns_records_change')

    return {
        "data": row,
        "info": fmt % d,
    }
