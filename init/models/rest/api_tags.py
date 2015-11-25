

#
class rest_get_tags(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List existing tags.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/tags",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/tags",
          tables=["tags"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.tags.id > 0
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_node_tags(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List tags attached to a node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/node1/tags",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/tags",
          tables=["tags"],
          orderby=db.tags.tag_name,
          desc=desc,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.node_tags.nodename == nodename
        q &= db.node_tags.tag_id == db.tags.id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_node_candidate_tags(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List attachable tags for node.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/nodes/node1/candidate_tags",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/nodes/<nodename>/candidate_tags",
          tables=["tags"],
          desc=desc,
          orderby=db.tags.tag_name,
          examples=examples,
        )

    def handler(self, nodename, **vars):
        q = db.node_tags.nodename == nodename
        q &= db.node_tags.tag_id == db.tags.id
        rows = db(q).select(db.tags.ALL)

        ids = set([r.id for r in rows])
        pattern = '|'.join([r.tag_exclude for r in rows if r.tag_exclude is not None and r.tag_exclude != ""])
        q = db.tags.id > 0
        q &= ~db.tags.id.belongs(ids)
        if len(pattern) > 0:
            qx = _where(None, "tags", pattern, "tag_name")
            q &= ~qx
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_service_tags(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List tags attached to a service.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services/svc1/tags",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/services/<svcname>/tags",
          tables=["tags"],
          orderby=db.tags.tag_name,
          desc=desc,
          examples=examples,
        )

    def handler(self, svcname, **vars):
        q = db.svc_tags.svcname == svcname
        q &= db.svc_tags.tag_id == db.tags.id
        self.set_q(q)
        return self.prepare_data(**vars)

#
class rest_get_service_candidate_tags(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List attachable tags for service.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/services/svc1/candidate_tags",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/services/<svcname>/candidate_tags",
          tables=["tags"],
          orderby=db.tags.tag_name,
          desc=desc,
          examples=examples,
        )

    def handler(self, svcname, **vars):
        q = db.svc_tags.svcname == svcname
        q &= db.svc_tags.tag_id == db.tags.id
        rows = db(q).select(db.tags.ALL)

        ids = set([r.id for r in rows])
        pattern = '|'.join([r.tag_exclude for r in rows if r.tag_exclude is not None and r.tag_exclude != ""])
        q = db.tags.id > 0
        q &= ~db.tags.id.belongs(ids)
        if len(pattern) > 0:
            qx = _where(None, "tags", pattern, "tag_name")
            q &= ~qx
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_post_tag(rest_post_handler):
    def __init__(self):
        desc = [
          "Update a tag properties.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST -d tag_name=foo https://%(collector)s/init/rest/api/tags/10",
        ]
        rest_post_handler.__init__(
          self,
          path="/tags/<id>",
          tables=["tags"],
          desc=desc,
          examples=examples
        )

    def handler(self, tag_id, **vars):
        check_privilege("TagManager")
        try:
            tag_id = int(tag_id)
            q = db.tags.id == tag_id
        except:
            q = db.tags.tag_name == tag_id
        row = db(q).select().first()
        if row is None:
            raise Exception("tag %s not found" % tag_id)
        db(q).update(**vars)
        _log('tag.change',
             'change tag %(tag_name)s: %(data)s',
             dict(tag_name=row.tag_name, data=str(vars)),
            )
        l = {
          'event': 'tags',
          'data': {'foo': 'bar'},
        }
        _websocket_send(event_msg(l))
        return rest_get_tag().handler(row.id)


#
class rest_post_tags(rest_post_handler):
    def __init__(self):
        self.get_handler = rest_get_tags()
        self.update_one_handler = rest_post_tag()
        self.update_one_param = "id"
        desc = [
          "Create a tag.",
          "Update tags matching the specified query.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST -d tag_name=foo https://%(collector)s/init/rest/api/tags",
        ]
        rest_post_handler.__init__(
          self,
          path="/tags",
          tables=["tags"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        check_privilege("TagManager")
        if 'tag_name' not in vars:
            raise Exception("the tag_name property is mandatory")
        tag_name = vars['tag_name']
        q = db.tags.tag_name == tag_name
        if db(q).count() == 1:
            raise Exception("tag already exist")
        db.tags.insert(**vars)
        data = db(q).select().first()
        _log('tag.create',
             "tag '%(tag_name)s' created",
             dict(tag_name=data.tag_name),
            )
        return dict(info="tag created", data=data)


#
class rest_get_tag(rest_get_line_handler):
    def __init__(self):
        desc = [
          "Display tag property.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/tags/10",
        ]
        rest_get_line_handler.__init__(
          self,
          path="/tags/<id>",
          tables=["tags"],
          desc=desc,
          examples=examples,
        )

    def handler(self, tagid, **vars):
        q = db.tags.id == int(tagid)
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_delete_tag(rest_delete_handler):
    def __init__(self):
        desc = [
          "Delete the tag with id <id>.",
          "Also delete the attachments to nodes and services",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/tags/1001",
        ]
        rest_delete_handler.__init__(
          self,
          path="/tags/<id>",
          desc=desc,
          examples=examples,
        )

    def handler(self, tagid, **vars):
        check_privilege("TagManager")

        info = []

        q = db.tags.id == tagid
        tag = db(q).select().first()
        if tag is None:
            return dict(info="tag not found")

        q = db.node_tags.tag_id == tagid
        q &= _where(None, 'node_tags', domain_perms(), 'nodename')
        n = db(q).delete()
        info += ["%d node attachments deleted"%n]

        q = db.svc_tags.tag_id == tagid
        q &= _where(None, 'svc_tags', domain_perms(), 'svcname')
        n = db(q).delete()
        info += ["%d service attachments deleted"%n]

        q = db.node_tags.tag_id == tagid
        n = db(q).count()
        q = db.svc_tags.tag_id == tagid
        n += db(q).count()
        if n > 0:
            info += ["tag not deleted: still attached to %d objects you are not responsible for"%n]
            return dict(info=', '.join(info))

        q = db.tags.id == tagid
        n = db(q).delete()
        info += ["%d tag deleted"%n]

        _log('tag.delete',
             "tag '%(tag_name)s' deleted",
             dict(tag_name=tag.tag_name),
            )
        return dict(info=', '.join(info))


#
class rest_get_tag_nodes(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List nodes where tag <id> is attached.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/tags/1001/nodes?props=nodename",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/tags/<id>/nodes",
          tables=["nodes"],
          desc=desc,
          examples=examples,
        )

    def handler(self, tagid, **vars):
        q = db.node_tags.tag_id == tagid
        q &= db.node_tags.nodename == db.nodes.nodename
        q &= _where(None, 'node_tags', domain_perms(), 'nodename')
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_get_tag_services(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List services where tag <id> is attached.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/tags/1001/services?props=svc_name",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/tags/<id>/services",
          tables=["services"],
          desc=desc,
          examples=examples,
        )

    def handler(self, tagid, **vars):
        q = db.svc_tags.tag_id == tagid
        q &= db.svc_tags.svcname == db.services.svc_name
        q &= _where(None, 'svc_tags', domain_perms(), 'svcname')
        self.set_q(q)
        return self.prepare_data(**vars)


#
class rest_post_tag_node(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a tag to a node",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/tags/1001/nodes/mynode",
        ]
        rest_post_handler.__init__(
          self,
          path="/tags/<id>/nodes/<nodename>",
          desc=desc,
          examples=examples
        )

    def handler(self, tagid, nodename, **vars):
        return lib_tag_attach_node(tagid, nodename)


#
class rest_delete_tag_node(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a tag from a node.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/tags/1001/nodes/mynode",
        ]
        rest_delete_handler.__init__(
          self,
          path="/tags/<id>/nodes/<nodename>",
          desc=desc,
          examples=examples,
        )

    def handler(self, tagid, nodename, **vars):
        return lib_tag_detach_node(tagid, nodename)



#
class rest_post_tag_service(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach a tag to a service",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST https://%(collector)s/init/rest/api/tags/1001/services/mysvc",
        ]
        rest_post_handler.__init__(
          self,
          path="/tags/<id>/services/<svcname>",
          desc=desc,
          examples=examples
        )

    def handler(self, tagid, svcname, **vars):
        return lib_tag_attach_service(tagid, svcname)

#
class rest_delete_tag_service(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach a tag from a service.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE https://%(collector)s/init/rest/api/tags/1001/services/mysvc",
        ]
        rest_delete_handler.__init__(
          self,
          path="/tags/<id>/services/<svcname>",
          desc=desc,
          examples=examples,
        )

    def handler(self, tagid, svcname, **vars):
        return lib_tag_detach_service(tagid, svcname)


#
# /tags/nodes :: GET
#
class rest_get_tags_nodes(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List tags-nodes attachments.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/tags/nodes",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/tags/nodes",
          tables=["node_tags"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.node_tags.id > 0
        q &= _where(None, 'node_tags', domain_perms(), 'nodename')
        self.set_q(q)
        return self.prepare_data(**vars)

#
# /tags/nodes :: POST
#
class rest_post_tags_nodes(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach tags to nodes",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST -d nodename=mynode -d tag_id=10 https://%(collector)s/init/rest/api/tags/nodes",
        ]
        rest_post_handler.__init__(
          self,
          path="/tags/nodes",
          tables=["node_tags"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        if "nodename" not in vars:
            raise Exception("the 'nodename' key is mandatory")
        if "tag_id" not in vars:
            raise Exception("the 'tag_id' key is mandatory")
        return lib_tag_attach_node(vars["tag_id"], vars["nodename"])

#
# /tags/nodes :: DELETE
#
class rest_delete_tags_nodes(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach tags from a nodes.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE -d nodename=mynode -d tag_id=10 https://%(collector)s/init/rest/api/tags/nodes",
        ]
        rest_delete_handler.__init__(
          self,
          path="/tags/nodes",
          tables=["node_tags"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        if "nodename" not in vars:
            raise Exception("the 'nodename' key is mandatory")
        if "tag_id" not in vars:
            raise Exception("the 'tag_id' key is mandatory")
        return lib_tag_detach_node(vars["tag_id"], vars["nodename"])

#
# /tags/services :: GET
#
class rest_get_tags_services(rest_get_table_handler):
    def __init__(self):
        desc = [
          "List tags-services attachments.",
        ]
        examples = [
          "# curl -u %(email)s -o- https://%(collector)s/init/rest/api/tags/services",
        ]
        rest_get_table_handler.__init__(
          self,
          path="/tags/services",
          tables=["svc_tags"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        q = db.svc_tags.id > 0
        q &= _where(None, 'svc_tags', domain_perms(), 'svcname')
        self.set_q(q)
        return self.prepare_data(**vars)

#
# /tags/services :: POST
#
class rest_post_tags_services(rest_post_handler):
    def __init__(self):
        desc = [
          "Attach tags to services",
        ]
        examples = [
          "# curl -u %(email)s -o- -X POST -d svcname=mysvc -d tag_id=10 https://%(collector)s/init/rest/api/tags/services",
        ]
        rest_post_handler.__init__(
          self,
          path="/tags/services",
          tables=["svc_tags"],
          desc=desc,
          examples=examples
        )

    def handler(self, **vars):
        if "svcname" not in vars:
            raise Exception("the 'svcname' key is mandatory")
        if "tag_id" not in vars:
            raise Exception("the 'tag_id' key is mandatory")
        return lib_tag_attach_service(vars["tag_id"], vars["svcname"])

#
# /tags/services :: DELETE
#
class rest_delete_tags_services(rest_delete_handler):
    def __init__(self):
        desc = [
          "Detach tags from services.",
        ]
        examples = [
          "# curl -u %(email)s -o- -X DELETE -d svcname=mysvc -d tag_id=10 https://%(collector)s/init/rest/api/tags/services",
        ]
        rest_delete_handler.__init__(
          self,
          path="/tags/services",
          tables=["svc_tags"],
          desc=desc,
          examples=examples,
        )

    def handler(self, **vars):
        if "svcname" not in vars:
            raise Exception("the 'svcname' key is mandatory")
        if "tag_id" not in vars:
            raise Exception("the 'tag_id' key is mandatory")
        return lib_tag_detach_service(vars["tag_id"], vars["svcname"])

