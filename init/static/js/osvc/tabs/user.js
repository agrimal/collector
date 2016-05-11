//
// user
//
function user_tabs(divid, options) {
  var o = tabs(divid)
  o.options = options

  o.load(function(){
    var i = 0

    if (!("user_id" in o.options) && ("fullname" in o.options)) {
      services_osvcgetrest("R_SEARCH", "", {"substring": o.options.fullname}, function(jd) {
        var users = jd.data.users.data
        for (var i=0; i<users.length; i++) {
          var user = users[i]
          if (user.fullname == o.options.fullname) {
            o.options.user_id = user.id
            break
          }
        }
        o._load()
      })
    } else {
      o._load()
    }
  })

  o._load = function() {
    o.closetab.children("p").text(o.options.fullname ? o.options.fullname : o.options.user_id)

    // tab properties
    i = o.register_tab({
      "title": "node_tabs.properties",
      "title_class": "icon guy16"
    })
    o.tabs[i].callback = function(divid) {
      user_properties(divid, o.options)
    }

    o.set_tab(o.options.tab)
  }
  return o
}


function user_properties(divid, options) {
	var o = {}

	// store parameters
	o.divid = divid
	o.div = $("#"+divid)
	o.options = options

	o.init = function() {
		o.info_username = o.div.find("#username")
		o.info_first_name = o.div.find("#first_name")
		o.info_last_name = o.div.find("#last_name")
		o.info_perpage = o.div.find("#perpage")
		o.info_email = o.div.find("#email")
		o.info_phone_work = o.div.find("#phone_work")
		o.info_email_log_level = o.div.find("#email_log_level")
		o.info_email_notifications = o.div.find("#email_notifications")
		o.info_im_type = o.div.find("#im_type")
		o.info_im_notifications = o.div.find("#im_notifications")
		o.info_im_log_level = o.div.find("#im_log_level")
		o.info_im_username = o.div.find("#im_username")
		o.info_manager = o.div.find("#manager")
		o.info_primaryg = o.div.find("#primary_group")
		o.info_quota_app = o.div.find("#quota_app")
		o.info_lfilter = o.div.find("#lock_filter")
		o.info_filterset = o.div.find("#filterset")
		o.info_org_groups_title = o.div.find("#org_groups_title")
		o.info_priv_groups_title = o.div.find("#priv_groups_title")
		o.info_org_groups = o.div.find("#org_groups")
		o.info_priv_groups = o.div.find("#priv_groups")
		o.info_resp_apps_title = o.div.find("#resp_apps_title")
		o.info_visible_apps_title = o.div.find("#visible_apps_title")
		o.info_resp_apps = o.div.find("#resp_apps")
		o.info_visible_apps = o.div.find("#visible_apps")

		o.load_user()
		o.load_fset()
	}

	o.load_fset = function() {
		// AutoComplete and bind filter set
		var fset = []
		services_osvcgetrest("R_FILTERSETS", "", {"limit": "0", "meta": "0", "orderby": "fset_name"}, function(jd) {
			var fsets = {"": {"id": 0, "label": ""}}
			var pg = [{"id": 0, "label": ""}]
			for (var i=0; i<jd.data.length; i++) {
				fsets[jd.data[i].fset_name] = jd.data[i]
				pg.push({
					"id": jd.data[i].id,
					"label": jd.data[i].fset_name
				})
			}
			o.info_filterset.addClass("clickable")
			o.info_filterset.hover(
				function() {
					$(this).addClass("editable")
				},
				function() {
					$(this).removeClass("editable")
				}
			)
			o.info_filterset.bind("click", function() {
				//$(this).unbind("mouseenter mouseleave click")
				if ($(this).siblings().find("form").length > 0) {
					$(this).siblings().show()
					$(this).siblings().find("input[type=text]:visible,select").focus()
					$(this).hide()
					return
				}
				var e = $("<td><form><input class='oi' type='text'></input></form></td>")
				e.css({"padding-left": "0px"})
				var input = e.find("input")
				input.uniqueId() // for date picker
				input.attr("pid", $(this).attr("id"))
				input.attr("value", $(this).text())
				input.autocomplete({
					source: pg,
					minLength: 0,
					select: function(event, ui) {
						event.preventDefault()
						o.set_filterset(ui.item.label, ui.item.id)
					}
				})
				e.find("form").submit(function(event) {
					event.preventDefault()
					var val = input.val()
					if (!(val in fsets)) {
						return
					}
					var fset_id = fsets[val].id
					o.set_filterset(val, fset_id)
				})
				input.bind("blur", function(){
					$(this).parents("td").first().siblings("td").show()
					$(this).parents("td").first().hide()
				})
				$(this).parent().append(e)
				$(this).hide()
				input.focus()
			})
		})

	}

	o.load_user = function() {
		services_osvcgetrest("R_USER", [o.options.user_id], "", function(jd) {
			o._load_user(jd.data[0])
		})
	}

	o._load_user = function(data) {
		o.info_username.html(data.username)
		o.info_first_name.html(data.first_name)
		o.info_last_name.html(data.last_name)
		o.info_perpage.html(data.perpage)
		o.info_email.html(data.email)
		o.info_phone_work.html(data.phone_work)
		o.info_email_log_level.html(data.email_log_level)
		o.info_im_type.html(data.im_type)
		o.info_im_username.html(data.im_username)
		o.info_im_log_level.html(data.im_log_level)
		o.info_quota_app.html(data.quota_app)

		// lock filter
		if (data.lock_filter == true) {
			o.info_lfilter.attr('class', 'fa toggle-on')
		} else {
			o.info_lfilter.attr('class','fa toggle-off')
		}
		if (data.email_notifications == true) {
			o.info_email_notifications.attr('class', 'fa toggle-on')
		} else {
			o.info_email_notifications.attr('class','fa toggle-off')
		}
		if (data.im_notifications == true) {
			o.info_im_notifications.attr('class', 'fa toggle-on')
		} else {
			o.info_im_notifications.attr('class','fa toggle-off')
		}

		user_org_membership({
			"tid": o.info_org_groups,
			"user_id": data.id,
			"title": "user_properties.org_groups",
			"e_title": o.info_org_groups_title
		})
		user_priv_membership({
			"tid": o.info_priv_groups,
			"user_id": data.id,
			"title": "user_properties.priv_groups",
			"e_title": o.info_priv_groups_title
		})

		tab_properties_generic_list({
			"request_service": "R_USER_APPS_RESPONSIBLE",
			"request_parameters": [data.id],
			"limit": "0",
			"key": "app",
			"title": "user_properties.resp_apps",
			"e_title": o.info_resp_apps_title,
			"e_list": o.info_resp_apps,
			"lowercase": false
		})
		tab_properties_generic_list({
			"request_service": "R_USER_APPS_PUBLICATION",
			"request_parameters": [data.id],
			"limit": "0",
			"key": "app",
			"title": "user_properties.visible_apps",
			"e_title": o.info_visible_apps_title,
			"e_list": o.info_visible_apps,
			"lowercase": false
		})

		services_osvcgetrest("R_USER_FILTERSET", [o.options.user_id], "", function(jd) {
			if (!jd.data || (jd.data.length == 0)) {
				return
			}
			o.info_filterset.text(jd.data[0].fset_name)
		})

		o.load_groups()

	}

	o.load_groups = function() {
	   	services_osvcgetrest("R_USER_PRIMARY_GROUP", [o.options.user_id], {"meta": "false", "limit": "0"}, function(jd) {
			if (jd.data.length != 1) {
				return
			}
			var current_primary = jd.data[0].role
			o.info_primaryg.text(current_primary)
		})
		services_osvcgetrest("/users/%1/groups", [o.options.user_id], {"meta": "false", "limit": "0"}, function(jd) {
			var data = jd.data
			var org_groups = {}
			var priv_groups = {}

			for (var i=0; i<data.length; i++) {
				var d = data[i]
				if (d.privilege == true) {
					priv_groups[d.role] = d
				} else {
					org_groups[d.role] = data[i]
				}
			}

			// manager
			if ("Manager" in priv_groups) {
				o.info_manager.attr('class', 'fa toggle-on')
			} else {
				o.info_manager.attr('class', 'fa toggle-off')
			}

			tab_properties_generic_updater({
				"div": o.div,
				"post": function(data, callback, error_callback) {
					services_osvcpostrest("R_USER", [o.options.user_id], "", data, callback, error_callback)
				}
			})
			tab_properties_generic_boolean({
				"div": o.info_lfilter,
				"privileges": ["Manager","UserManager"],
				"post": function(data, callback, error_callback) {
					services_osvcpostrest("R_USER", [o.options.user_id], "", data, callback, error_callback)
				}
			})
			tab_properties_generic_autocomplete({
				"div": o.info_email_log_level,
				"post": function(_data, callback, error_callback) {
					services_osvcpostrest("R_USER", [o.options.user_id], "", _data, callback, error_callback)
				},
				"get": function(callback) {
					var data = ["debug", "info", "warning", "error", "critical"]
					callback(data)
				}
			})
			tab_properties_generic_autocomplete({
				"div": o.info_im_log_level,
				"post": function(_data, callback, error_callback) {
					services_osvcpostrest("R_USER", [o.options.user_id], "", _data, callback, error_callback)
				},
				"get": function(callback) {
					var data = ["debug", "info", "warning", "error", "critical"]
					callback(data)
				}
			})
			tab_properties_generic_autocomplete({
				"div": o.info_im_type,
				"post": function(_data, callback, error_callback) {
					services_osvcpostrest("R_USER", [o.options.user_id], "", _data, callback, error_callback)
				},
				"get": function(callback) {
					var data = [{"label": "gtalk", "value": 1}]
					callback(data)
				}
			})
			tab_properties_generic_autocomplete_org_group_id({
				"div": o.info_primaryg,
				"user_id": o.options.user_id,
				"post": function(_data, callback, error_callback) {
					services_osvcpostrest("R_USER_PRIMARY_GROUP_SET", [o.options.user_id, _data.primary_group], "", "", callback, error_callback)
				}
			})
		})
	}

	o.set_filterset = function(label, fset_id) {
		if (fset_id == 0) {
			services_osvcdeleterest("R_USER_FILTERSET", [o.options.user_id], "","", function(jd) {
				if (jd.error && jd.error.length > 0) {
					o.info_filterset.next().hide()
					o.info_filterset.text(jd.error).show()
					return
				}
				o.info_filterset.next().hide()
				o.info_filterset.text(label).show()
			},
			function() {})
		} else {
			services_osvcpostrest("R_USER_FILTERSET_SET", [o.options.user_id, fset_id], "","", function(jd) {
				if (jd.error && jd.error.length > 0) {
					o.info_filterset.next().hide()
					o.info_filterset.text(jd.error).show()
					return
				}
				o.info_filterset.next().hide()
				o.info_filterset.text(label).show()
			},
			function() {})
		}
	}

	o.div.load("/init/static/views/user_properties.html", function() {
		o.div.i18n()
		o.init()
	})

	return o
}


