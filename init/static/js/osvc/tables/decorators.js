//
// cell decorators
//
var action_img_h = {
  'checks': 'check16',
  'enable': 'check16',
  'disable': 'nok',
  'pushservices': 'svc',
  'pushpkg': 'pkg16',
  'pushpatch': 'pkg16',
  'reboot': 'action_restart_16',
  'shutdown': 'action_stop_16',
  'syncservices': 'action_sync_16',
  'sync_services': 'action_sync_16',
  'updateservices': 'action16',
  'updatepkg': 'pkg16',
  'updatecomp': 'pkg16',
  'stop': 'action_stop_16',
  'stopapp': 'action_stop_16',
  'stopdisk': 'action_stop_16',
  'stopvg': 'action_stop_16',
  'stoploop': 'action_stop_16',
  'stopip': 'action_stop_16',
  'stopfs': 'action_stop_16',
  'umount': 'action_stop_16',
  'shutdown': 'action_stop_16',
  'boot': 'action_start_16',
  'start': 'action_start_16',
  'startstandby': 'action_start_16',
  'startapp': 'action_start_16',
  'startdisk': 'action_start_16',
  'startvg': 'action_start_16',
  'startloop': 'action_start_16',
  'startip': 'action_start_16',
  'startfs': 'action_start_16',
  'mount': 'action_start_16',
  'restart': 'action_restart_16',
  'provision': 'prov',
  'switch': 'action_switch_16',
  'freeze': 'frozen16',
  'thaw': 'frozen16',
  'sync_all': 'action_sync_16',
  'sync_nodes': 'action_sync_16',
  'sync_drp': 'action_sync_16',
  'syncall': 'action_sync_16',
  'syncnodes': 'action_sync_16',
  'syncdrp': 'action_sync_16',
  'syncfullsync': 'action_sync_16',
  'postsync': 'action_sync_16',
  'push': 'log16',
  'check': 'check16',
  'fixable': 'fixable16',
  'fix': 'comp16',
  'pushstats': 'spark16',
  'pushasset': 'node16',
  'stopcontainer': 'action_stop_16',
  'startcontainer': 'action_start_16',
  'stopapp': 'action_stop_16',
  'startapp': 'action_start_16',
  'prstop': 'action_stop_16',
  'prstart': 'action_start_16',
  'push': 'svc',
  'syncquiesce': 'action_sync_16',
  'syncresync': 'action_sync_16',
  'syncupdate': 'action_sync_16',
  'syncverify': 'action_sync_16',
  'toc': 'action_toc_16',
  'stonith': 'action_stonith_16',
  'switch': 'action_switch_16'
}


var os_class_h = {
  'darwin': 'os_darwin',
  'linux': 'os_linux',
  'hp-ux': 'os_hpux',
  'osf1': 'os_tru64',
  'opensolaris': 'os_opensolaris',
  'solaris': 'os_solaris',
  'sunos': 'os_solaris',
  'freebsd': 'os_freebsd',
  'aix': 'os_aix',
  'windows': 'os_win',
  'vmware': 'os_vmware'
}

function cell_decorator_boolean(e) {
  var v = $(e).attr("v")
  true_vals = [1, "1", "T", "True", true]
  if (typeof v === "undefined") {
    var cl = ""
  } else if (true_vals.indexOf(v) >= 0) {
    var cl = "toggle-on"
  } else {
    var cl = "toggle-off"
  }
  s = "<span class='"+cl+"' title='"+v+"'></span>"
  $(e).html(s)
}

function cell_decorator_network(e) {
  var v = $(e).attr("v")
  $(e).html("<span class='clickable'>"+v+"</span>")
  $(e).click(function(){
    var line = $(this).parent(".tl")
    var net_id = line.children("[name$=_c_id]").attr("v")
    url = $(location).attr("origin") + "/init/networks/segments/"+net_id
    toggle_extra(url, net_id, $(this), 0)
  })
}

function cell_decorator_chk_instance(e) {
  var v = $(e).attr("v")
  var line = $(e).parent(".tl")
  var chk_type = line.children("[name$=_chk_type]").attr("v")
  if (chk_type == "mpath") {
    url = $(location).attr("origin") + "/init/disks/disks?disks_f_disk_id="+v+"&volatile_filters=true"
    s = "<a class='hd16' href='"+url+"' target='_blank'>"+v+"</a>"
    $(e).html(s)
  }
}

function cell_decorator_chk_high(e) {
  var high = $(e).attr("v")
  var line = $(e).parent(".tl")
  var v = line.children("[name$=_chk_value]").attr("v")
  var cl = []
  v = parseInt(v)
  high = parseInt(high)
  if (v > high) {
    cl.push("highlight")
  }
  $(e).html("<span class='"+cl.join(" ")+"'>"+high+"</span>")
}

function cell_decorator_chk_low(e) {
  var low = $(e).attr("v")
  var line = $(e).parent(".tl")
  var v = line.children("[name$=_chk_value]").attr("v")
  var cl = []
  v = parseInt(v)
  low = parseInt(low)
  if (v < low) {
    cl.push("highlight")
  }
  $(e).html("<span class='"+cl.join(" ")+"'>"+low+"</span>")
}

function cell_decorator_chk_value(e) {
  var v = $(e).attr("v")
  var line = $(e).parent(".tl")
  var low = line.children("[name$=_chk_low]").attr("v")
  var high = line.children("[name$=_chk_high]").attr("v")
  var cl = []
  v = parseInt(v)
  low = parseInt(low)
  high = parseInt(high)
  if ((v > high) || (v < low)) {
    cl.push("highlight")
  }
  $(e).html("<span class='"+cl.join(" ")+"'>"+v+"</span>")
}

function cell_decorator_action_pid(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    $(e).empty()
    return
  }
  var s = "<a>"+v+"</a>"
  $(e).html(s)
  $(e).bind('click', function(){
    var line = $(e).parent(".tl")
    var hostname = line.children("[name$=_hostname]").attr("v")
    var svcname = line.children("[name$=_svcname]").attr("v")
    var begin = line.children("[name$=_begin]").attr("v")
    var end = line.children("[name$=_end]").attr("v")

    var _begin = begin.replace(/ /, "T")
    var d = new Date(+new Date(_begin) - 1000*60*60*24)
    begin = print_date(d)

    var _end = end.replace(/ /, "T")
    var d = new Date(+new Date(_end) + 1000*60*60*24)
    end = print_date(d)

    url = $(location).attr("origin") + "/init/svcactions/svcactions?actions_f_svcname="+svcname+"&actions_f_hostname="+hostname+"&actions_f_pid="+v+"&actions_f_begin=>"+begin+"&actions_f_end=<"+end+"&volatile_filters=true"

    $(this).children("a").attr("href", url)
    $(this).children("a").attr("target", "_blank")
    //$(this).children("a").click()
  })
}

function cell_decorator_action_status(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    $(e).html("<div class='spinner'></div>")
    return
  }
  cl = ["status_"+v.replace(' ', '_')]
  var line = $(e).parent(".tl")
  var ack = line.children("[name$=_ack]").attr("v")
  if (ack == 1) {
    cl.push("ack_1")
  }
  s = "<div class='"+cl.join(" ")+"'>"+v+"</diV>"
  $(e).html(s)
  if (ack != 1) {
    return
  }
  $(e).bind("mouseout", function(){
    ackpanel(event, false, "")
  })
  $(e).bind("mouseover", function(){
    var acked_date = line.children("[name$=_acked_date]").attr("v")
    var acked_by = line.children("[name$=_acked_by]").attr("v")
    var acked_comment = line.children("[name$=_acked_comment]").attr("v")
    s = "<div>"
    s += "<b>acked by </b>"+acked_by+"<br>"
    s += "<b> on </b>"+acked_date+"<br>"
    s += "<b>with comment:</b><br>"+acked_comment
    s += "</div>"
    ackpanel(event, true, s)
  })
}

function cell_decorator_action_end(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    $(e).empty()
    return
  } else if (v == "1000-01-01 00:00:00") {
    $(e).html("<span class='highlight'>timed out</span>")
    return
  }
  var line = $(e).parent(".tl")
  var id = line.children("[name$=_id]").attr("v")
  s = "<span class='highlight nowrap' id='spin_span_end_"+id+"'>"+v+"</span>"
}

function cell_decorator_action_log(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    $(e).empty()
    return
  }
  s = "<pre>"+v+"</pre>"
  $(e).html(s)
}

function cell_decorator_action(e) {
  var v = $(e).attr("v")
  var line = $(e).parent(".tl")
  var status_log = line.children("[name$=status_log]").attr("v")
  cl = []
  if (status_log == "empty") {
    cl.push("metaaction")
  }
  action = v.split(/\s+/).pop()
  if (action in action_img_h) {
    cl.push(action_img_h[action])
  }
  s = "<div class='"+cl.join(" ")+"'>"+v+"</div>"
  $(e).html(s)
}

function cell_decorator_svc_action_err(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    $(e).empty()
    return
  }
  var line = $(e).parent(".tl")
  var svcname = line.children("[name$=mon_svcname]").attr("v")
  url = $(location).attr("origin") + "/init/svcactions/svcactions?actions_f_svcname="+svcname+"&actions_f_status=err&actions_f_ack=!1|empty&actions_f_begin=>-30d&volatile_filters=true"
  s = "<a class='action16 icon-red clickable' href='"+url+"' target='_blank'>"+v+"</a>"
  $(e).html(s)
}

function cell_decorator_nodename(e) {
  _cell_decorator_nodename(e, true)
}

function cell_decorator_nodename_no_os(e) {
  _cell_decorator_nodename(e, false)
}

function _cell_decorator_nodename(e, os_icon) {
  var v = $(e).attr("v")
  if ((v=="") || (v=="empty")) {
    return
  }
  $(e).empty()
  $(e).append("<div class='a nowrap'>"+v+"</div>")
  $(e).addClass("corner")
  div = $(":first-child", e)
  if (os_icon) {
    try {
      os_cell = $(e).parent().children(".os_name")
      os_c = os_class_h[os_cell.attr("v").toLowerCase()]
      div.addClass(os_c)
    } catch(e) {}
  }
  try {
    svc_autostart_cell = $(e).parent().children(".svc_autostart")
    if (svc_autostart_cell.attr("v") == v) {
      div.addClass("b")
    }
  } catch(e) {}
  $(e).click(function(){
    if (get_selected() != "") {return}
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = $(e).parent(".tl").attr("spansum")
    id = table_id + "_x_" + span_id
    toggle_extra(null, id, e, 0)
    node_tabs(id, {"nodename": v})
  })
}

function cell_decorator_groups(e) {
  var v = $(e).attr("v")
  if ((v=="") || (v=="empty")) {
    return
  }
  $(e).addClass("corner")
  l = v.split(', ')
  s = ""
  for (i=0; i<l.length; i++) {
    g = l[i]
    s += "<span>"+g+"</span>"
  }
  $(e).html(s)
  table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
  span_id = $(e).parent(".tl").attr("spansum")
  id = table_id + "_x_" + span_id
  $(e).children().each(function(){
    $(this).click(function(){
      if (get_selected() != "") {return}
      g = $(this).text()
      url = $(location).attr("origin") + "/init/ajax_group/ajax_group?groupname="+encodeURIComponent(g)+"&rowid="+id
      toggle_extra(url, id, e, 0)
    })
  })
}

function cell_decorator_username(e) {
  var v = $(e).attr("v")
  if ((v=="") || (v=="empty")) {
    return
  }
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = $(e).parent(".tl").attr("spansum")
    id = table_id + "_x_" + span_id
    url = $(location).attr("origin") + "/init/ajax_user/ajax_user?username="+encodeURIComponent(v)+"&rowid="+id
    toggle_extra(url, id, e, 0)
  })
}

function cell_decorator_svcname(e) {
  var v = $(e).attr("v")
  if ((v=="") || (v=="empty")) {
    return
  }
  $(e).empty()
  $(e).append("<div class='a nowrap'>"+v+"</div>")
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = $(e).parent(".tl").attr("spansum")
    id = table_id + "_x_" + span_id
    url = $(location).attr("origin") + "/init/default/ajax_service?node="+v+"&rowid="+id
    toggle_extra(url, id, e, 0)
  })
}

function cell_decorator_status(e) {
  var v = $(e).attr("v")
  if ((v=="") || (v=="empty")) {
    v = "undef"
  }
  var c = v
  var line = $(e).parent(".tl")
  if (status_outdated(line)) {
    c = "undef"
  }
  t = {
    "warn": "orange",
    "up": "green",
    "stdby up": "green",
    "down": "red",
    "stdby down": "red",
    "undef": "gray",
    "n/a": "gray",
  }
  $(e).html("<div class='svc nowrap icon-"+t[c]+"'></div>")
}

function cell_decorator_forms_links(e) {
  var line = $(e).parent(".tl")
  var form_id = line.children("[name$=id]").attr("v")
  var query = "form_id="+form_id
  url = $(location).attr("origin") + "/init/forms/forms_editor?"+query
  var d = "<a class='clickable edit16' target='_blank' href="+url+"></a>"
  $(e).html(d)
}

function cell_decorator_svcmon_links(e) {
  var line = $(e).parent(".tl")
  var mon_svcname = line.children("[name$=mon_svcname]").attr("v")
  var query = "volatile_filters=true&actions_f_svcname="+mon_svcname
  query += "&actions_f_status_log=empty"
  query += "&actions_f_begin="+encodeURIComponent(">-1d")
  url = $(location).attr("origin") + "/init/svcactions/svcactions?"+query
  var d = "<a class='clickable action16' target='_blank' href="+url+"></a>"

  var mon_frozen = line.children("[name$=mon_frozen]").attr("v")
  if (mon_frozen == "1") {
    d += "<span class='frozen16'>&nbsp</span>"
  }
  $(e).html(d)
}

function cell_decorator_chk_type(e) {
  var v = $(e).attr("v")
  if (v=="") {
    return
  }
  $(e).empty()
  $(e).append("<div>"+v+"</div>")
  div = $(":first-child", e)
  div.addClass("a")
  div.addClass("nowrap")
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = $(e).parent(".tl").attr("spansum")
    id = table_id + "_x_" + span_id
    url = $(location).attr("origin") + "/init/checks/ajax_chk_type_defaults/"+v
    toggle_extra(url, id, e, 0)
  })
}

function cell_decorator_dash_link_comp_tab(e) {
  var line = $(e).parent(".tl")
  var svcname = line.find("[name$=dash_svcname]").attr("v")
  var nodename = line.find("[name$=dash_nodename]").attr("v")
  s = "<div class='comp16 clickable'></div>"
  $(e).html(s)
  $(e).addClass("corner")
  if (svcname != "") {
    $(e).click(function(){
      table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
      span_id = $(e).parent(".tl").attr("spansum")
      id = table_id + "_x_" + span_id
      url = $(location).attr("origin") + "/init/default/ajax_service?node="+svcname+"&tab=tab11&rowid="+id
      toggle_extra(url, id, e, 0)
    })
  } else if (nodename != "") {
    $(e).click(function(){
      table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
      span_id = $(e).parent(".tl").attr("spansum")
      id = table_id + "_x_" + span_id
      toggle_extra(null, id, e, 0)
      node_tabs(id, {"nodename": nodename, "tab": "node_tabs.compliance"})
    })
  }
}

function cell_decorator_dash_link_pkg_tab(e) {
  var line = $(e).parent(".tl")
  var svcname = line.find("[name$=dash_svcname]").attr("v")
  s = "<div class='pkg16 clickable'></div>"
  $(e).html(s)
  $(e).addClass("corner")
  if (svcname != "") {
    $(e).click(function(){
      table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
      span_id = $(e).parent(".tl").attr("spansum")
      id = table_id + "_x_" + span_id
      url = $(location).attr("origin") + "/init/default/ajax_service?node="+svcname+"&tab=tab10&rowid="+id
      toggle_extra(url, id, e, 0)
    })
  }
}

function cell_decorator_dash_link_feed_queue(e) {
  s = "<a class='action16' href=''></a>"
  $(e).html(s)
}

function _cell_decorator_dash_link_actions(svcname) {
  url = $(location).attr("origin") + "/init/svcactions/svcactions?actions_f_svcname="+svcname+"&actions_f_begin=>-7d&volatile_filters=true"
  s = "<a class='action16 clickable' target='_blank' href='"+url+"'></a>"
  return s
}

function _cell_decorator_dash_link_action_error(svcname) {
  url = $(location).attr("origin") + "/init/svcactions/svcactions?actions_f_svcname="+svcname+"&actions_f_status=err&actions_f_ack=!1|empty&actions_f_begin=>-30d&volatile_filters=true"
  s = "<a class='alert16 clickable' target='_blank' href='"+url+"'></a>"
  return s
}

function cell_decorator_dash_link_action_error(e) {
  var line = $(e).parent(".tl")
  var svcname = line.find("[name$=dash_svcname]").attr("v")
  var s = ""
  s += _cell_decorator_dash_link_action_error(svcname)
  s += _cell_decorator_dash_link_actions(svcname)
  $(e).html(s)
}

function _cell_decorator_dash_link_svcmon(svcname) {
  url = $(location).attr("origin") + "/init/default/svcmon?svcmon_f_mon_svcname="+svcname+"&volatile_filters=true"
  s = "<a class='svc clickable' target='_blank' href='"+url+"'></a>"
  return s
}

function cell_decorator_dash_link_svcmon(e) {
  var line = $(e).parent(".tl")
  var svcname = line.find("[name$=dash_svcname]").attr("v")
  var s = ""
  s += _cell_decorator_dash_link_svcmon(svcname)
  $(e).html(s)
}

function _cell_decorator_dash_link_node(nodename) {
  url = $(location).attr("origin") + "/init/nodes/nodes?nodes_f_nodename="+nodename+"&volatile_filters=true"
  s = "<a class='node16 clickable' target='_blank' href='"+url+"'></a>"
  return s
}

function cell_decorator_dash_link_node(e) {
  var line = $(e).parent(".tl")
  var nodename = line.find("[name$=dash_nodename]").attr("v")
  var s = ""
  s += _cell_decorator_dash_link_node(nodename)
  $(e).html(s)
}

function _cell_decorator_dash_link_checks(nodename) {
  url = $(location).attr("origin") + "/init/checks/checks?checks_f_chk_nodename="+nodename+"&volatile_filters=true"
  s = "<a class='check16 clickable' target='_blank' href='"+url+"'></a>"
  return s
}

function cell_decorator_dash_link_checks(e) {
  var line = $(e).parent(".tl")
  var nodename = line.find("[name$=dash_nodename]").attr("v")
  var s = ""
  s += _cell_decorator_dash_link_checks(nodename)
  $(e).html(s)
}

function _cell_decorator_dash_link_mac_networks(mac) {
  url = $(location).attr("origin") + "/init/nodenetworks/nodenetworks?nodenetworks_f_mac="+mac+"&volatile_filters=true"
  s = "<a class='net16 clickable' target='_blank' href='"+url+"'></a>"
  return s
}

function cell_decorator_dash_link_mac_duplicate(e) {
  var line = $(e).parent(".tl")
  var mac = line.find("[name$=dash_entry]").attr("v").split(" ")[1]
  var s = ""
  s += _cell_decorator_dash_link_mac_networks(mac)
  $(e).html(s)
}

function cell_decorator_dash_link_obsolescence(e, t) {
  var line = $(e).parent(".tl")
  var nodename = line.find("[name$=dash_nodename]").attr("v")
  var s = ""
  url = $(location).attr("origin") + "/init/obsolescence/obsolescence_config?obs_f_obs_type="+t+"&volatile_filters=true"
  s = "<a class='"+t+"16 clickable' target='_blank' href='"+url+"'></a>"
  $(e).html(s)
}

function cell_decorator_dash_links(e) {
  var line = $(e).parent(".tl")
  var dash_type = line.find("[name$=dash_type]").attr("v")
  if (dash_type == "action errors") {
    cell_decorator_dash_link_action_error(e)
  } else if ((dash_type == "node warranty expired") ||
             (dash_type == "node without warranty end date") ||
             (dash_type == "node without asset information") ||
             (dash_type == "node close to warranty end") ||
             (dash_type == "node information not updated")) {
    cell_decorator_dash_link_node(e)
  } else if ((dash_type == "check out of bounds") ||
             (dash_type == "check value not updated")) {
    cell_decorator_dash_link_checks(e)
  } else if (dash_type == "mac duplicate") {
    cell_decorator_dash_link_mac_duplicate(e)
  } else if ((dash_type == "service available but degraded") ||
             (dash_type == "service status not updated") ||
             (dash_type == "service configuration not updated") ||
             (dash_type == "service frozen") ||
             (dash_type == "flex error") ||
             (dash_type == "service unavailable")) {
    cell_decorator_dash_link_svcmon(e)
  } else if (dash_type == "feed queue") {
    cell_decorator_dash_link_feed_queue(e)
  } else if (dash_type.indexOf("os obsolescence") >= 0) {
    cell_decorator_dash_link_obsolescence(e, "os")
  } else if (dash_type.indexOf("obsolescence") >= 0) {
    cell_decorator_dash_link_obsolescence(e, "hw")
  } else if (dash_type.indexOf("comp") == 0) {
    cell_decorator_dash_link_comp_tab(e)
  } else if (dash_type.indexOf("package") == 0) {
    cell_decorator_dash_link_pkg_tab(e)
  }
}

function cell_decorator_action_cron(e) {
  var v = $(e).attr("v")
  var l = []
  if (v == 1) {
      l.push("time16")
  }
  $(e).html("<div class='"+l.join(" ")+"'></div>")
}

function cell_decorator_dash_severity(e) {
  var v = $(e).attr("v")
  var l = []
  if (v == 0) {
      l.push("alertgreen")
  } else if (v == 1) {
      l.push("alertorange")
  } else if (v == 2) {
      l.push("alertred")
  } else if (v == 3) {
      l.push("alertdarkred")
  } else {
      l.push("alertblack")
  }
  $(e).html("<div class='"+l.join(" ")+"' title='"+v+"'></div>")
}

function cell_decorator_form_id(e) {
  var v = $(e).attr("v")
  var s = ""
  url = $(location).attr("origin") + "/init/forms/workflow?wfid="+v+"&volatile_filters=true"
  s = "<a class='clickable' target='_blank' href='"+url+"'></a>"
  $(e).html(s)
}

function cell_decorator_run_log(e) {
  var v = $(e).attr("v")
  if (typeof v === "undefined") {
    var s = ""
  } else {
    var s = "<pre>"+v.replace(/ERR:/g, "<span class='err'>ERR:</span>")+"</pre>"
  }
  $(e).html(s)
}

function cell_decorator_run_status(e) {
  var v = $(e).attr("v")
  var s = ""
  var cl = ""
  var _v = ""
  if (v == 0) {
    cl = "check16"
  } else if (v == 1) {
    cl = "nok"
  } else if (v == 2) {
    cl = "na"
  } else if (v == -15) {
    cl = "kill16"
  } else {
    _v = v
  }
  $(e).html("<div class='"+cl+"'>"+_v+"</div>")
}

function cell_decorator_disk_array(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    return
  }
  var line = $(e).parent(".tl")
  var model = line.find("[name$=_array_model]").attr("v")
  var s = ""
  s = "<div class='clickable'>"+v+"</div>"
  $(e).html(s)
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = line.attr("spansum")
    id = table_id + "_x_" + span_id
    url = $(location).attr("origin") + "/init/disks/ajax_array?array="+v+"&rowid="+id
    toggle_extra(url, id, this, 0)
  })
}

function cell_decorator_disk_array_dg(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    return
  }
  var s = ""
  s = "<div class='clickable'>"+v+"</div>"
  $(e).html(s)
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    var line = $(e).parent(".tl")
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    array = line.find("[name$=_disk_arrayid],[name$=_array_name]").attr("v")
    span_id = line.attr("spansum")
    id = table_id + "_x_" + span_id
    url = $(location).attr("origin") + "/init/disks/ajax_array_dg?array="+array+"&dg="+v+"&rowid="+id
    toggle_extra(url, id, this, 0)
  })
}

function cell_decorator_tag_exclude(e) {
  var v = $(e).attr("v")
  if (v == "empty") {
    v = ""
  }
  $(e).html(v)
  $(window).bind("click", function() {
    $("input.tag_exclude").parent().html(v)
  })
  $(e).bind("click", function(){
    event.stopPropagation()
    i = $("<input class='tag_exclude'></input>")
    var _v = $(this).attr("v")
    if (_v == "empty") {
      _v = ""
    }
    i.val(_v)
    i.bind("keyup", function(){
      if (!is_enter(event)) {
        return
      }
      var url = $(location).attr("origin") + "/init/tags/call/json/tag_exclude"
      var data = {
        "tag_exclude": $(this).val(),
        "tag_id": $(this).parents(".tl").find("[name=tags_c_id]").attr("v")
      }
      var _i = $(this)
      $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function(msg){
          _i.parent().html(data.tag_exclude)
        }
      })
    })
    $(e).empty().append(i)
    i.focus()
  })
}

function cell_decorator_dash_entry(e) {
  var v = $(e).attr("v")
  var s = ""
  s = "<div class='clickable'>"+v+"</div>"
  $(e).html(s)
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    var line = $(e).parent(".tl")
    var nodename = line.children("[name$=dash_nodename]").attr("v")
    var svcname = line.children("[name$=dash_svcname]").attr("v")
    var dash_md5 = line.children("[name$=dash_md5]").attr("v")
    var dash_created = line.children("[name$=dash_created]").attr("v")
    var rowid = line.attr("cksum")
    url = $(location).attr("origin") + "/init/dashboard/ajax_alert_events?dash_nodename="+nodename+"&dash_svcname="+svcname+"&dash_md5="+dash_md5+"&dash_created="+dash_created+"&rowid="+rowid
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = line.attr("spansum")
    id = table_id + "_x_" + span_id
    toggle_extra(url, id, this, 0)
  })
}

function cell_decorator_rset_md5(e) {
  var v = $(e).attr("v")
  var s = ""
  s = "<div class='clickable'>"+v+"</div>"
  $(e).html(s)
  $(e).addClass("corner")
  $(e).click(function(){
    if (get_selected() != "") {return}
    url = $(location).attr("origin") + "/init/compliance/ajax_rset_md5?rset_md5="+v
    table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    span_id = $(e).parent(".tl").attr("spansum")
    id = table_id + "_x_" + span_id
    toggle_extra(url, id, this, 0)
  })
}

function cell_decorator_action_q_ret(e) {
  var v = $(e).attr("v")
  var cl = ["boxed_small"]
  if (v == 0) {
    cl.push("bggreen")
  } else {
    cl.push("bgred")
  }
  var s = ""
  s = "<div class='"+cl.join(" ")+"'>"+v+"</div>"
  $(e).html(s)
}

function cell_decorator_action_q_status(e) {
  var v = $(e).attr("v")
  var st = ""
  var cl = ["boxed_small"]
  if (v == "T") {
    cl.push("bggreen")
    st = i18n.t("decorators.done")
  } else if (v == "R") {
    cl.push("bgred")
    st = i18n.t("decorators.running")
  } else if (v == "W") {
    st = i18n.t("decorators.waiting")
  } else if (v == "Q") {
    st = i18n.t("decorators.queued")
  } else if (v == "C") {
    cl.push("bgdarkred")
    st = i18n.t("decorators.cancelled")
  }
  var s = ""
  s = "<div class='"+cl.join(" ")+"'>"+st+"</div>"
  $(e).html(s)
}

function datetime_age(s) {
  // return age in minutes
  if (typeof s === 'undefined') {
    return
  }
  if (s == 'empty') {
    return
  }
  s = s.replace(/ /, "T")
  var d = new Date(s)
  var now = new Date()
  delta = now.getTime() - d.getTime() - now.getTimezoneOffset() * 60000
  return delta / 60000
}

function _outdated(s, max_age) {
  delta = datetime_age(s)
  if (!delta) {
    return true
  }
  if (delta > max_age) {
    return true
  }
  return false
}

function status_outdated(line) {
  var s = line.children("[cell=1][name$=mon_updated]").attr("v")
  if (typeof s === 'undefined') {
    var s = line.children("[cell=1][name$=status_updated]").attr("v")
  }
  if (typeof s === 'undefined') {
    var s = line.children("[cell=1][name$=_updated]").attr("v")
  }
  return _outdated(s, 15)
}

function cell_decorator_date_no_age(e) {
  v = $(e).attr("v")
  if (typeof v === 'undefined') {
    return
  }
  s = v.split(" ")[0]
  $(e).html(s)
}

function cell_decorator_datetime_no_age(e) {
  cell_decorator_datetime(e)
}

function cell_decorator_date_future(e) {
  cell_decorator_datetime(e)
}

function cell_decorator_datetime_status(e) {
  $(e).attr("max_age", 15)
  cell_decorator_datetime(e)
}

function cell_decorator_datetime_future(e) {
  cell_decorator_datetime(e)
}

function cell_decorator_datetime_daily(e) {
  $(e).attr("max_age", 1440)
  cell_decorator_datetime(e)
}

function cell_decorator_datetime_weekly(e) {
  $(e).attr("max_age", 10080)
  cell_decorator_datetime(e)
}

function cell_decorator_datetime(e) {
  var s = $(e).attr("v")
  var max_age = $(e).attr("max_age")
  var delta = datetime_age(s)

  if (!delta) {
    $(e).html()
    return
  }

  if (delta > 0) {
    var prefix = "-"
  } else {
    var prefix = ""
    delta = -delta
  }

  var hour = 60
  var day = 1440
  var week = 10080
  var month = 43200
  var year = 524520

  if (delta < hour) {
    var cl = "minute icon"
    var text = prefix + i18n.t("table.minute", {"count": Math.floor(delta)})
    var color = "#000000"
  } else if (delta < day) {
    var cl = "hour icon"
    var text = prefix + i18n.t("table.hour", {"count": Math.floor(delta/hour)})
    var color = "#181818"
  } else if (delta < week) {
    var cl = "day icon "
    var text = prefix + i18n.t("table.day", {"count": Math.floor(delta/day)})
    var color = "#333333"
  } else if (delta < month) {
    var cl = "week icon "
    var text = prefix + i18n.t("table.week", {"count": Math.floor(delta/week)})
    var color = "#333333"
  } else if (delta < year) {
    var cl = "month icon"
    var text = prefix + i18n.t("table.month", {"count": Math.floor(delta/month)})
    var color = "#484848"
  } else {
    var cl = "year icon"
    var text = prefix + i18n.t("table.year", {"count": Math.floor(delta/year)})
    var color = "#666666"
  } 

  if ($(e).text() == text) {
    return
  }
  cl += " nowrap"

  if (max_age && (delta > max_age)) {
    cl += " icon-red"
  }
  $(e).html("<div class='"+cl+"' style='color:"+color+"' title='"+s+"'>"+text+"</div>")
}

function cell_decorator_date(e) {
  cell_decorator_datetime(e)
  s = $(e).attr("v")
  $(e).text(s.split(" ")[0])
}

function cell_decorator_env(e) {
  if ($(e).attr("v") != "PRD") {
    return
  }
  s = "<div class='b'>PRD</div>"
  $(e).html(s)
}

function cell_decorator_svc_ha(e) {
  if ($(e).attr("v") != 1) {
    $(e).empty()
    return
  }
  s = "<div class='boxed_small'>HA</div>"
  $(e).html(s)
}

function cell_decorator_size_mb(e) {
  v = $(e).attr("v")
  if (v == "empty") {
    return
  }
  s = "<div class='nowrap'>"+fancy_size_mb(v)+"</div>"
  $(e).html(s)
}

function cell_decorator_size_b(e) {
  v = $(e).attr("v")
  if (v == "empty") {
    return
  }
  s = "<div class='nowrap'>"+fancy_size_b(v)+"</div>"
  $(e).html(s)
}

function cell_decorator_availstatus(e) {
  var line = $(e).parent(".tl")
  var mon_availstatus = $(e).attr("v")
  if (mon_availstatus=="") {
    return
  }
  var mon_containerstatus = line.children("[name$=mon_containerstatus]").attr("v")
  var mon_ipstatus = line.children("[name$=mon_ipstatus]").attr("v")
  var mon_fsstatus = line.children("[name$=mon_fsstatus]").attr("v")
  var mon_diskstatus = line.children("[name$=mon_diskstatus]").attr("v")
  var mon_sharestatus = line.children("[name$=mon_sharestatus]").attr("v")
  var mon_appstatus = line.children("[name$=mon_appstatus]").attr("v")

  if (status_outdated(line)) {
    var cl_availstatus = "status_undef"
    var cl_containerstatus = "status_undef"
    var cl_ipstatus = "status_undef"
    var cl_fsstatus = "status_undef"
    var cl_diskstatus = "status_undef"
    var cl_sharestatus = "status_undef"
    var cl_appstatus = "status_undef"
  } else {
    var cl_availstatus = mon_availstatus.replace(/ /g, '_')
    var cl_containerstatus = mon_containerstatus.replace(/ /g, '_')
    var cl_ipstatus = mon_ipstatus.replace(/ /g, '_')
    var cl_fsstatus = mon_fsstatus.replace(/ /g, '_')
    var cl_diskstatus = mon_diskstatus.replace(/ /g, '_')
    var cl_sharestatus = mon_sharestatus.replace(/ /g, '_')
    var cl_appstatus = mon_appstatus.replace(/ /g, '_')
  }
  var s = "<table>"
  s += "<tr>"
  s += "<td colspan=6 class=\"aggstatus status_" + cl_availstatus + "\">" + mon_availstatus + "</td>"
  s += "</tr>"
  s += "<tr>"
  s += "<td class=status_" + cl_containerstatus + ">vm</td>"
  s += "<td class=status_" + cl_ipstatus + ">ip</td>"
  s += "<td class=status_" + cl_fsstatus + ">fs</td>"
  s += "<td class=status_" + cl_diskstatus + ">dg</td>"
  s += "<td class=status_" + cl_sharestatus + ">share</td>"
  s += "<td class=status_" + cl_appstatus + ">app</td>"
  s += "</tr>"
  s += "</table>"
  $(e).html(s)
}

function cell_decorator_rsetvars(e) {
  var s = $(e).attr("v")
  $(e).html("<pre>"+s.replace(/\|/g, "\n")+"</pre>")
}

function cell_decorator_overallstatus(e) {
  var line = $(e).parent(".tl")
  var mon_overallstatus = $(e).attr("v")
  if (mon_overallstatus=="") {
    return
  }
  var mon_containerstatus = line.children("[name$=mon_containerstatus]").attr("v")
  var mon_availstatus = line.children("[name$=mon_availstatus]").attr("v")
  var mon_hbstatus = line.children("[name$=mon_hbstatus]").attr("v")
  var mon_syncstatus = line.children("[name$=mon_syncstatus]").attr("v")

  if (status_outdated(line)) {
    var cl_overallstatus = "status_undef"
    var cl_availstatus = "status_undef"
    var cl_syncstatus = "status_undef"
    var cl_hbstatus = "status_undef"
  } else {
    var cl_overallstatus = mon_overallstatus.replace(/ /g, '_')
    var cl_availstatus = mon_availstatus.replace(/ /g, '_')
    var cl_syncstatus = mon_syncstatus.replace(/ /g, '_')
    var cl_hbstatus = mon_hbstatus.replace(/ /g, '_')
  }

  var s = "<table>"
  s += "<tr>"
  s += "<td colspan=3 class=\"aggstatus status_" + cl_overallstatus + "\">" + mon_overallstatus + "</td>"
  s += "</tr>"
  s += "<tr>"
  s += "<td class=status_" + cl_availstatus + ">avail</td>"
  s += "<td class=status_" + cl_hbstatus + ">hb</td>"
  s += "<td class=status_" + cl_syncstatus + ">sync</td>"
  s += "</tr>"
  s += "</table>"
  $(e).html(s)
}

function cell_decorator_yaml(e) {
  var s = $(e).attr("v")
  var _e = $("<pre></pre>")
  s = s.replace(/Id:\s*(\w+)/gi, function(x) {
    return '<span class=syntax_red>'+x+'</span>'
  })
  s = s.replace(/(#\w+)/gi, function(x) {
    return '<span class=syntax_red>'+x+'</span>'
  })
  s = s.replace(/(\w+:)/gi, function(x) {
    return '<span class=syntax_green>'+x+'</span>'
  })
  _e.html(s)
  $(e).html(_e)
}

function cell_decorator_appinfo_key(e) {
  var s = $(e).attr("v")
  var _e = $("<div class='boxed_small'></div>")
  _e.text(s)
  if (s == "Error") {
    _e.addClass("bgred")
  } else {
    _e.addClass("bgblack")
  }
  $(e).html(_e)
}

function cell_decorator_appinfo_value(e) {
  var s = $(e).attr("v")
  var _e = $("<span></span>")
  _e.text(s)
  if (is_numeric(s)) {
    _e.addClass("spark16")
    $(e).addClass("corner clickable")
  }
  $(e).bind("click", function() {
    var line = $(e).parent(".tl")
    var span_id = line.attr("spansum")
    var table_id = $(e).parents("table").attr("id").replace(/^table_/, '')
    var id = table_id + "_x_" + span_id
    var params = "svcname="+encodeURIComponent(line.children("[name$=_c_app_svcname]").attr("v"))
    params += "&nodename="+encodeURIComponent(line.children("[name$=_c_app_nodename]").attr("v"))
    params += "&launcher="+encodeURIComponent(line.children("[name$=_c_app_launcher]").attr("v"))
    params += "&key="+encodeURIComponent(line.children("[name$=_c_app_key]").attr("v"))
    params += "&rowid="+encodeURIComponent(id)
    var url = $(location).attr("origin") + "/init/appinfo/ajax_appinfo_log?" + params

    toggle_extra(url, id, e, 0)
  })
  $(e).html(_e)
}

cell_decorators = {
 "yaml": cell_decorator_yaml,
 "rsetvars": cell_decorator_rsetvars,
 "dash_entry": cell_decorator_dash_entry,
 "disk_array_dg": cell_decorator_disk_array_dg,
 "disk_array": cell_decorator_disk_array,
 "size_mb": cell_decorator_size_mb,
 "size_b": cell_decorator_size_b,
 "chk_instance": cell_decorator_chk_instance,
 "chk_value": cell_decorator_chk_value,
 "chk_low": cell_decorator_chk_low,
 "chk_high": cell_decorator_chk_high,
 "action": cell_decorator_action,
 "action_pid": cell_decorator_action_pid,
 "action_status": cell_decorator_action_status,
 "action_end": cell_decorator_action_end,
 "action_log": cell_decorator_action_log,
 "action_cron": cell_decorator_action_cron,
 "rset_md5": cell_decorator_rset_md5,
 "run_status": cell_decorator_run_status,
 "run_log": cell_decorator_run_log,
 "form_id": cell_decorator_form_id,
 "action_q_status": cell_decorator_action_q_status,
 "action_q_ret": cell_decorator_action_q_ret,
 "svcname": cell_decorator_svcname,
 "username": cell_decorator_username,
 "groups": cell_decorator_groups,
 "nodename": cell_decorator_nodename,
 "nodename_no_os": cell_decorator_nodename_no_os,
 "svc_action_err": cell_decorator_svc_action_err,
 "availstatus": cell_decorator_availstatus,
 "overallstatus": cell_decorator_overallstatus,
 "chk_type": cell_decorator_chk_type,
 "svcmon_links": cell_decorator_svcmon_links,
 "forms_links": cell_decorator_forms_links,
 "svc_ha": cell_decorator_svc_ha,
 "env": cell_decorator_env,
 "date_future": cell_decorator_date_future,
 "datetime_future": cell_decorator_datetime_future,
 "datetime_weekly": cell_decorator_datetime_weekly,
 "datetime_daily": cell_decorator_datetime_daily,
 "datetime_status": cell_decorator_datetime_status,
 "datetime_no_age": cell_decorator_datetime_no_age,
 "date_no_age": cell_decorator_date_no_age,
 "dash_severity": cell_decorator_dash_severity,
 "dash_links": cell_decorator_dash_links,
 "tag_exclude": cell_decorator_tag_exclude,
 "_network": cell_decorator_network,
 "boolean": cell_decorator_boolean,
 "status": cell_decorator_status,
 "appinfo_key": cell_decorator_appinfo_key,
 "appinfo_value": cell_decorator_appinfo_value
}


