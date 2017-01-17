function variable_tabs(divid, options) {
	var o = tabs(divid)
	o.options = options
	o.options.bgcolor = osvc.colors.comp
	o.options.icon = "comp16"
	o.link = {
		"fn": arguments.callee.name,
		"parameters": o.options,
		"title": "format_title",
		"title_args": {
			"type": "variable",
			"name": o.options.variable_name
		}
	}

	o.load(function() {
		o._load()
	})

	o._load = function() {
		var title = o.options.variable_name
		
		o.closetab.text(title)

		i = o.register_tab({
			"title": "variable_tabs.content",
			"title_class": "icon comp16"
		})
		o.tabs[i].callback = function(divid) {
			variable_content(divid, o.options)
		}

		o.set_tab(o.options.tab)
	}

	return o
}

function variable_content(divid, options) {
	var o = {}
	o.options = options
	o.div = $("#"+divid)
	o.link = {
		"fn": arguments.callee.name,
		"parameters": o.options,
		"title": "format_title",
		"title_args": {
			"type": "variable",
			"id": o.options.variable_id,
			"name": o.options.variable_name
		}
	}

	o.init = function() {
		o.var_name = o.div.find("#var_name")
		o.var_class = o.div.find("#var_class")
		o.var_updated = o.div.find("#var_updated")
	}

	o.rulesets = {}
	var head = {}

	services_osvcgetrest("R_COMPLIANCE_RULESET_VARIABLE", [o.options.ruleset_id, o.options.variable_id], "", function(jd) {
		if (!jd && jd.error) {
			o.div.html(services_error_fmt(jd))
			return
		}
		var div = $("<div style='padding:1em'></div>")
		o.area = div
		o.div.append(div)
		o.render(jd.data[0])
		osvc_tools(o.div, {
			"link": o.link
		})
	},
	function() {
		o.div.html(services_ajax_error_fmt(xhr, stat, error))
	})

	o.render = function(variable) {
		try {
			var data = $.parseJSON(variable.var_value)
		} catch(e) {
			var data = variable.var_value
		}

		o.var_name.append(variable.var_name)

		o.var_class.append(variable.var_class)

		var p2 = $("<p></p>")
		var last_mod = $("<span>"+i18n.t("variable_tabs.var_last_mod")+"</span>")
		var fullname = $("<span fullname='"+variable.var_author+"'>"+variable.var_author+"</span>")
		var mod_date = $("<span>"+i18n.t("variable_tabs.var_mod_on")+" "+variable.var_updated+"</span>")
		p2.append([last_mod, " " ,fullname, " ", mod_date])
		fullname.osvc_fullname()
		o.var_updated.append(p2)

		var form_div = $("<div></div>")
		form_div.uniqueId()
		o.area.append(form_div)
		form(form_div.attr("id"), {
			"data": data,
			"var_id": variable.id,
			"rset_id": variable.ruleset_id,
			"display_mode": true,
			"digest": true,
			"form_name": variable.var_class,
			"disable_edit": false
		})
		o.area.append("<br>")

		tab_properties_generic_updater({
			"div": o.div,
			"privileges": ["Manager", "CompManager"],
			"post": function(_data, callback, error_callback) {
				services_osvcpostrest("/compliance/rulesets/%1/variables/%2", [variable.ruleset_id, variable.id], "", _data, callback, error_callback)
			}
		})

	}
	o.div.load("/init/static/views/variable_content.html?v="+osvc.code_rev, function() {
		o.div.i18n()
		o.init()
	})

	return o
}
