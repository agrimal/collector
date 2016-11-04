def get_tag_name(tag_id):
    try:
        q = db.tags.tag_id == tag_id
        tag_name = db(q).select().first().tag_name
    except Exception as e:
        raise Exception({"error": "tag does not exist"})
    return tag_name

def tag_allowed(node_id=None, svc_id=None, tag_name=None):
    if node_id is None and svc_id is None:
        return False
    if tag_name is None:
        return False
    if node_id:
        q = db.node_tags.node_id == node_id
        q &= db.node_tags.tag_id == db.tags.id
        q &= db.tags.tag_exclude != None
        q &= db.tags.tag_exclude != ""
        rows = db(q).select(db.tags.tag_exclude,
                            groupby=db.tags.tag_exclude)
    elif svc_id:
        q = db.svc_tags.svc_id == svc_id
        q &= db.svc_tags.tag_id == db.tags.id
        q &= db.tags.tag_exclude != None
        q &= db.tags.tag_exclude != ""
        rows = db(q).select(db.tags.tag_exclude,
                            groupby=db.tags.tag_exclude)
    if len(rows) == 0:
        return True

    pattern = '|'.join([r.tag_exclude for r in rows])
    q = db.tags.tag_name == tag_name
    qx = _where(None, "tags", pattern, "tag_name")
    q &= ~qx
    if db(q).count() == 0:
        return False
    return True

def lib_tag_detach_node(tag_id, node_id):
    node_responsible(node_id=node_id)
    tag_name = get_tag_name(tag_id)
    q = db.node_tags.tag_id == tag_id
    q &= db.node_tags.node_id == node_id
    q = q_filter(q, node_field=db.node_tags.node_id)
    if db(q).count() == 0:
        return dict(info="tag already detached")
    db(q).delete()
    table_modified("node_tags")
    _log("node.tag",
         "tag '%(tag_name)s' detached",
         dict(tag_name=tag_name),
         node_id=node_id)
    ws_send('tags', {'action': 'detach', 'tag_id': tag_id, 'node_id': node_id})
    return dict(info="tag detached")

def lib_tag_detach_service(tag_id, svc_id):
    svc_responsible(svc_id)
    tag_name = get_tag_name(tag_id)
    q = db.svc_tags.tag_id == tag_id
    q &= db.svc_tags.svc_id == svc_id
    q = q_filter(q, svc_field=db.svc_tags.svc_id)
    if db(q).count() == 0:
        return dict(info="tag already detached")
    db(q).delete()
    table_modified("svc_tags")
    _log("service.tag",
         "tag '%(tag_name)s' detached",
         dict(tag_name=tag_name),
         svc_id=svc_id)
    ws_send('tags', {'action': 'detach', 'tag_id': tag_id, 'svc_id': svc_id})
    return dict(info="tag detached")


def lib_tag_attach_node(tag_id, node_id):
    if not node_id:
        raise Exception("invalid node_id: '%s'" % str(node_id))
    node_responsible(node_id=node_id)
    tag_name = get_tag_name(tag_id)
    q = db.node_tags.tag_id == tag_id
    q &= db.node_tags.node_id == node_id
    q = q_filter(q, node_field=db.node_tags.node_id)
    if db(q).count() == 1:
        return dict(info="tag '%s' already attached to node '%s'" % (tag_name, get_nodename(node_id)))
    if not tag_allowed(tag_name=tag_name, node_id=node_id):
        return dict(error="tag '%s' is not compatible with other tags attached to node '%s'" % (tag_name, get_nodename(node_id)))

    db.node_tags.insert(tag_id=tag_id, node_id=node_id)
    table_modified("node_tags")
    _log("node.tag",
         "tag '%(tag_name)s' attached",
         dict(tag_name=tag_name),
         node_id=node_id)
    ws_send('tags', {
         'action': 'attach',
         'tag_id': tag_id,
         'tag_name': tag_name,
         'node_id': node_id
    })
    return dict(info="tag '%s' attached to node '%s'" % (tag_name, get_nodename(node_id)))


def lib_tag_attach_service(tag_id, svc_id):
    if not svc_id or len(svc_id) == 0:
        raise Exception("invalid svc_id: '%s'" % str(svc_id))
    svc_responsible(svc_id)
    tag_name = get_tag_name(tag_id)
    q = db.svc_tags.tag_id == tag_id
    q &= db.svc_tags.svc_id == svc_id
    q = q_filter(q, svc_field=db.svc_tags.svc_id)
    if db(q).count() == 1:
        return dict(info="tag '%s' already attached to service '%s'" % (tag_name, svc_id))
    if not tag_allowed(tag_name=tag_name, svc_id=svc_id):
        return dict(error="tag '%s' is not compatible with other tags attached to node '%s'" % (tag_name, get_nodename(node_id)))
    db.svc_tags.insert(tag_id=tag_id, svc_id=svc_id)
    table_modified("svc_tags")
    _log("service.tag",
         "tag '%(tag_name)s' attached",
         dict(tag_name=tag_name),
         svc_id=svc_id)
    ws_send('tags', {
        'action': 'attach',
        'tag_id': tag_id,
        'tag_name': tag_name,
        'svc_id': svc_id
    })
    return dict(info="tag '%s' attached to service '%s'" % (tag_name, svc_id))



