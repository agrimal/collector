#
class rest_get_search(rest_get_handler):
    def __init__(self):
        desc = [
          "Search the collector data for objects with name containing the substring.",
        ]
        examples = [
          """# curl -u %(email)s -o- https://%(collector)s/init/rest/api/search?substring=manager""",
        ]
        params = {
          "substring": {
             "desc": "The substring to search.",
          },
          "in": {
             "desc": "Limit the search to the selected object type: fset, disk, app, svc, vm, ip, node, user, group, safe",
          },
        }
        rest_get_handler.__init__(
          self,
          path="/search",
          desc=desc,
          params=params,
          examples=examples,
        )

    def handler(self, **vars):
        data = {}
        substring = vars.get("substring")
        otype = vars.get("in")
        if substring is None:
            return dict(data=data)
        substring = "%" + substring + "%"
        if otype is None or otype == "fset":
            data["filtersets"] = lib_search_fset(substring)
        if otype is None or otype == "disk":
            data["disks"] = lib_search_disk(substring)
        if otype is None or otype == "app":
            data["apps"] = lib_search_app(substring)
        if otype is None or otype == "svc":
            data["services"] = lib_search_service(substring)
        if otype is None or otype == "vm":
            data["vms"] = lib_search_vm(substring)
        if otype is None or otype == "ip":
            data["ips"] = lib_search_ip(substring)
        if otype is None or otype == "node":
            data["nodes"] = lib_search_node(substring)
        if otype is None or otype == "user":
            data["users"] = lib_search_user(substring)
        if otype is None or otype == "group":
            data["groups"] = lib_search_group(substring)
        if otype is None or otype == "safe":
            data["safe_files"] = lib_search_safe_file(substring)
        return dict(data=data)

