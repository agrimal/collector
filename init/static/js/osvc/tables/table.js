//
// column filter tool: distinct values to filtering string
//
function link_title_table(options) {
	return i18n.t("col.Table") + " " + "<span class='icon_fixed_width "+options.icon+"'>"+i18n.t("table.name."+options.name)+"</span>"
}

function values_to_filter(input, cloud){
	l = []
	var reg = new RegExp("[ ]+$", "g");
	cloud.find("a.cloud_tag").each(function(){
                s = this.text
      		s = s.replace(reg, "")
		if (s == "None") {s = "empty"}
		l.push(s)
	})
        v = '(' + l.join(",") + ')'
	input.val(v)
}

function _invert_filter(v){
	var reg = new RegExp("[|]+", "g");
	var l = v.split(reg);
        if (l.length > 1) {
		for (var i=0; i<l.length; i++) {
			if (l[i][0] == '!') {
				l[i] = l[i].substr(1)
			} else {
				l[i] = '!'+l[i]
			}
		}
		v = l.join("&")
		return v
	} else {
		var reg = new RegExp("[&]+", "g");
		var l = v.split(reg);
		for (var i=0; i<l.length; i++) {
			if (l[i][0] == '!') {
				l[i] = l[i].substr(1)
			} else {
				l[i] = '!'+l[i]
			}
		}
		v = l.join("|")
		return v
	}
}

function keep_inside(box){
	box_off_l = $(box).offset().left
	box_w = $(box).width()
	doc_w = $('body').width()

	// trim the box width to fit the doc
	if ((box_w+20)>doc_w) {
		$(box).css("width", doc_w - 30)
		$(box).css("overflow-x", "auto")
		box_w = $(box).width()
	}

	// align to the right doc border
	if (box_off_l + box_w > doc_w) {
		$(box).offset({"left": doc_w - box_w - 20})
		box_off_l = $(box).offset().left
	}

	// align to the left doc border
	if (box_off_l < 0) {
		$(box).offset({"left": 10})
		box_off_l = $(box).offset().left
	}
}

function click_toggle_vis(e, name, mode){
	$("[name="+name+"]").each(function () {
		if ($(this).css("display") == 'none' || $(this).css("display") == "") {
			$(this).show()
			keep_inside($(this))
			register_pop_up(e, $(this))
		} else {
			$(this).hide()
		}
		$(this).find('input[type=text],textarea,select').filter(':visible:first').focus()
	})
}

function register_pop_up(e, box){
	if (e) {
		// IE event does not support stopPropagation
		if (!e.stopPropagation) {return}
		e.stopPropagation()
	}
	$(document).click(function(e) {
		e = e || event
		var target = e.target || e.srcElement
		if (target.id.match(/^ui-id/)) {
			// combox box click
			return
		}
		try {
			boxtop = box.get(0)
		} catch(e) {
			return
		}
		do {
			if (boxtop == target) {
				// click inside
				return
			}
			target = target.parentNode
		} while(target)
		box.hide()
	})
}

function check_all(name, checked){
	c = document.getElementsByName(name)
	for(i = 0; i < c.length; i++) {
		if (c[i].type == 'checkbox' && c[i].disabled == false) {
			c[i].checked = checked
			c[i].value = checked
		}
	}
}

function sync_ajax(url, inputs, id, f) {
    s = inputs
    var query=""
    for (i=0; i<s.length; i++) {
        if (i > 0) {query=query+"&"}
        e = $("#"+s[i])
        if (e.is('select')) {
           val = e.find(":selected").val()
        } else {
           val = e.val()
        }
        query=query+encodeURIComponent(s[i])+"="+encodeURIComponent(val);
    }
    $.ajax({
         type: "POST",
         url: url,
         data: query,
         context: document.body,
         success: function(msg){
             $("#"+id).html(msg)
             $("#"+id).find("script").each(function(i){
               //eval($(this).text());
               $(this).remove();
             });
             if (f) {
               f()
             }
             $("#"+id).parents(".white_float").each(function(){keep_inside(this)})
             var t = osvc.tables[id]
             if (typeof t === 'undefined') { return }
             t.refresh_child_tables()
             t.on_change()
         }
    })
}

function toggle_extratable(e) {
	var id = toggle_extraline(e)
	var d = $("<table></table>")
	d.uniqueId()
	$("#"+id).empty().append(d)
	return d.attr("id")
}

function toggle_extraline(e) {
	return toggle_extra(null, null, e, null)
}

function toggle_extra(url, id, e, ncols) {
	if ($(e).hasClass("tl")) {
		var line = $(e)
	} else {
		var line = $(e).parents(".tl").first()
	}
	if (!ncols) {
		ncols = line.children("[cell=1]").length
	}
	var extra = $("<tr class='extraline stackable empty_on_pop'></tr>")
	extra.attr("anchor", line.attr("cksum"))
	line.children("td.tools").each(function(){
		extra.append("<td class='tools'></td>")
	})
	if (line.next().is(".extraline")) {
		line.next().remove()
	}
	var td = $("<td colspan="+ncols+"></td>")
	if (id) {
		td.attr("id", id)
	} else {
		td.uniqueId()
		id = td.attr("id")
	}
	extra.append(td)
	extra.insertAfter(line)

	// ajax load url, if specified
	if (url) {
		sync_ajax(url, [], id, function(){
			$("#"+id).removeClass("spinner")
		})
	}
	return id
}

function refresh_plot(url, rowid, id) {
	sync_ajax(url,['begin_'+rowid, 'end_'+rowid], id, function(){})
}

function toggle_plot(url, rowid, id) {
	if ($("#"+id).is(":visible")) {
		$("#"+id).hide()
		$("#refresh_"+id).hide()
		$("#close_"+id).hide()
	} else {
		$("#"+id).show()
		$("#refresh_"+id).show()
		$("#close_"+id).show()
		refresh_plot(url, rowid, id)
	}
}

function get_pos(e) {
	var posx = 0
	var posy = 0
	if (e.pageX || e.pageY) {
		posx = e.pageX
		posy = e.pageY
	} else if (e.clientX || e.clientY) {
		posx = e.clientX + document.body.scrollLeft
			+ document.documentElement.scrollLeft;
		posy = e.clientY + document.body.scrollTop
			+ document.documentElement.scrollTop;
	}
	return [posx, posy]
}

//
// get text selection
//
function get_selected() {
	if (window.getSelection) {
		return window.getSelection().toString()
	} else if (document.getSelection) {
		return document.getSelection().toString()
	} else {
		var selection = document.selection && document.selection.createRange()
		if (selection.text) {
			return selection.text.toString()
		}
		return ""
	}
	return ""
}

//
// Table link url popup
//
function get_view_url() {
	var url = $(location).attr('href')
	if (url.indexOf('?')>0) {
		url=url.substring(0, url.indexOf('?'))
	}
	return url
}




function table_init(opts) {
	var defaults = {
		"pager": {"page": 1},
		"extrarow": false,
		"extrarow_class": "",
		"checkboxes": true,
		"span": ["id"],
		"force_cols": [],
		"hide_cols": [],
		"columns": [],
		"colprops": {},
		"volatile_filters": false,
		"child_tables": [],
		"parent_tables": [],
		"linkable": true,
		"filterable": true,
		"refreshable": true,
		"bookmarkable": true,
		"exportable": true,
		"columnable": true,
		"commonalityable": true,
		"headers": true,
		"wsable": false,
		"pageable": true,
		"on_change": false,
		"events": [],
		"delay": 2000,
		"detached_decorate_cells": true,
		"request_vars": {}
	}

	var t = {
		'options': $.extend({}, defaults, opts),
		'colprops': {},
		'need_refresh': false,
		'delay_refresh': false,
		'id': opts.id,
		'spin_class': 'fa-spin highlight',

		'bind_action_menu': function(){
			return table_bind_action_menu(this)
		},
		'action_menu_param_moduleset': function(){
			return table_action_menu_param_moduleset(this)
		},
		'action_menu_param_module': function(){
			return table_action_menu_param_module(this)
		}
	}

	t.add_filtered_to_visible_columns = function() {
		for (col in t.colprops) {
			if (t.options.hide_cols.indexOf(col) >= 0) {
				if (t.e_tool_column_selector_area) {
					t.e_tool_column_selector_area.find("[colname="+col+"]").prop("disabled", true).prop("checked", false)
				}
				continue
			}
			var val = t.colprops[col].current_filter
			if ((typeof val === "undefined") || (val == "")) {
				continue
			}
			if (t.options.visible_columns.indexOf(col) < 0) {
				t.options.visible_columns.push(col)
				if (t.e_tool_column_selector_area) {
					t.e_tool_column_selector_area.find("[colname="+col+"]").prop("disabled", true)
				}
			} else {
				if (t.e_tool_column_selector_area) {
					t.e_tool_column_selector_area.find("[colname="+col+"]").removeAttr("disabled")
				}
			}
		}
	}

	t.restripe_lines = function() {
		var prev_spansum = ""
		var cls = ["cell1", "cell2"]
		var cl = "cell1"
		var i = 1
		t.e_table.children().children(".tl").each(function(){
			spansum = $(this).attr("spansum")
			if (spansum != prev_spansum) {
				prev_spansum = spansum
				cl = cls[i]
				i = 1 - i
			}
			if ($(this).hasClass(cl)) {
				return
			}
			$(this).removeClass(cls[i]).addClass(cl)
		})
	}

	t.trim_lines = function() {
		perpage = parseInt($("#table_"+t.id).attr("perpage")) + 2
		lines = $("#table_"+t.id).children("tbody").children()
		if (lines.length <= perpage) {
			return
		}
		for (i=perpage; i<lines.length; i++) {
			$(lines[i]).remove()
		}
		lines = null
	}


	//
	// table horizontal scroll
	//
	t.scroll_enable = function() {
		t.scroll_left.click(function(){
			t.e_table.parent().animate({'scrollLeft': '-='+$(window).width()}, 500, t.scroll)
		})
		t.scroll_right.click(function(){
			t.e_table.parent().animate({'scrollLeft': '+='+$(window).width()}, 500, t.scroll)
		})
		t.e_table.parent().bind("scroll", function(){
			t.scroll()
		})
		$(window).resize(function(){
			t.scroll()
		})
		$(".down16,.right16").click(function() {
			t.scroll()
		})
		t.scroll_enable_dom()
	}

	t.scroll = function() {
		t.scroll_disable_dom()
		sticky_relocate(t.e_header, t.e_sticky_anchor)
		var to_p = t.e_table.parent()
		var ww = to_p.width()
		var tw = t.e_table.width()
		var off = to_p.scrollLeft()
		if (ww >= tw) {
			t.scroll_left.hide()
			t.scroll_right.hide()
			t.scroll_enable_dom()
			return
		}
		if (off > 0) {
			t.scroll_left.show()
		} else {
			t.scroll_left.hide()
		}
		if (off+ww+1 < tw) {
			t.scroll_right.show()
		} else {
			t.scroll_right.hide()
		}
		t.scroll_enable_dom()
	}

	t.scroll_enable_dom = function() {
		t.e_table.bind("DOMNodeInserted DOMNodeRemoved", t.scroll)
	}

	t.scroll_disable_dom = function() {
		t.e_table.unbind("DOMNodeInserted DOMNodeRemoved", t.scroll)
	}

	t.add_scrollers = function() {
		t.scroll_left = $("<div id='table_"+t.id+"_left' class='scroll_left'>&nbsp</div>")
		$("#table_"+t.id).prepend(t.scroll_left)
		t.scroll_right = $("<div id='table_"+t.id+"_right' class='scroll_right'>&nbsp</div>")
		$("#table_"+t.id).append(t.scroll_right)
	}

	//
	// column filter tool: invert column filter
	//
	t.invert_column_filter = function(c) {
		var val = t.colprops[c].current_filter
		if (typeof val === "undefined") {
			return
		}
		t.colprops[c].current_filter = _invert_filter(val)
		t.save_column_filters()
	}

	t.stick = function() {
		// bypass conditions
		if (t.div.parents(".tableo").length > 0) {
			return
		}

		var anchor = $("<span></span>")
		anchor.uniqueId()
		anchor.insertBefore(t.e_header)
		t.e_sticky_anchor = anchor
		sticky_relocate(t.e_header, t.e_sticky_anchor)
		$(window).scroll(function(){
			sticky_relocate(t.e_header, t.e_sticky_anchor)
		})
		sticky_relocate(t.e_header, t.e_sticky_anchor)
	}

	t.reset_column_filters = function() {
		if (!t.e_header_filters) {
			return
		}
		t.e_header_filters.find("th").each(function() {
			var input = $(this).find("input")
			var label = $(this).find(".col_filter_label")
			if ((c in t.colprops) && (typeof(t.colprops[c].force_filter) !== "undefined") && (t.colprops[c].force_filter != "")) {
				input.val(t.colprops[c].force_filter)
			} else if ((c in t.colprops) && (typeof(t.colprops[c].default_filter) !== "undefined") && (t.colprops[c].default_filter != "")) {
				input.val(t.colprops[c].default_filter)
			} else {
				input.val("")
			}
			label.empty()
			$(this).find(".clear16,.invert16").hide()
		})
		t.e_header_slim.find("th").each(function() {
			$(this).removeClass("bgblack")
			$(this).removeClass("bgred")
			$(this).removeClass("bgorange")
		})
	}

	t.get_visible_columns = function() {
		// if visible columns is not explicitely set in options
		// fetch it from the db-stored table settings
		if (t.options.visible_columns) {
			return
		}

		// init with default visibility defined in colprops
		if (t.options.default_columns) {
			t.options.visible_columns = t.options.default_columns
		} else {
			t.options.visible_columns = []
			for (key in t.colprops) {
				var d = t.colprops[key]
				if (d.display) {
					t.options.visible_columns.push(key)
				}
			}
		}

		// adjust with db-stored user's table settings
		if (!(t.id in osvc.table_settings.data)) {
			return
		}
		for (col in osvc.table_settings.data[t.id]) {
			if (col == "wsenabled") {
				continue
			}
			if (osvc.table_settings.data[t.id][col]) {
				if (t.options.visible_columns.indexOf(col) < 0) {
					t.options.visible_columns.push(col)
				}
			} else {
				var idx = t.options.visible_columns.indexOf(col)
				if (idx >= 0) {
					t.options.visible_columns.splice(idx, 1)
				}
			}
		}
	}

	t.add_table = function() {
		if (typeof(t.options.divid) === "undefined") {
			// web2py provided table structure
			t.div = $("#"+t.id+" .tableo")
			return
		}
		var container = $("#"+t.options.divid)
		var d = $("<div class='tableo'></div>")
		var toolbar = $("<div class='theader toolbar' name='toolbar'></div>")
		var table_scroll_zone = $("<div class='table_scroll_zone'></div>")
		var table_div = $("<div></div>")
		var table = $("<table></table>")
		d.attr("id", t.id)
		t.div = d
		t.page = t.options.pager.page
		table.attr("id", "table_"+t.id)
		table_scroll_zone.append(table_div)
		table_div.append(table)
		d.append(toolbar)
		d.append(table_scroll_zone)
		container.empty().append(d)
	}

	t.on_change = function() {
		if (!t.options.on_change) {
			return
		}
		t.options.on_change()
	}

	t.refresh_child_tables = function() {
		for (var i=0; i<t.options.child_tables.length; i++) {
			var id = t.options.child_tables[i]
			if (!(id in osvc.tables)) {
				console.log("child table not found in osvc.tables:", id)
				continue
			}
			osvc.tables[id].refresh()
		}
	}

	t.parent_table_data = function(ptid) {
		if (!(ptid in osvc.tables)) {
			console.log("table", t.id, "parent table", ptid, "not found")
			return {}
		}
		var pt = osvc.tables[ptid]
		var data = {}
		for (c in pt.colprops) {
			var current = pt.colprops[c].current_filter
			if ((current != "") && (typeof current !== 'undefined')) {
				data[pt.id+"_f_"+c] = current
			} else if ((typeof(pt.colprops[c].force_filter) !== "undefined") && (pt.colprops[c].force_filter != "")) {
				data[pt.id+"_f_"+c] = pt.colprops[c].force_filter
			}
		}
		return data
	}

	t.parent_tables_data = function() {
		if (!t.options.parent_tables || (t.options.parent_tables.length == 0)) {
			return {}
		}
		var data = {}
		for (var i=0; i<t.options.parent_tables.length; i++) {
			data = $.extend(data, t.parent_table_data(t.options.parent_tables[i]))
		}
		return data
	}

	t.prepare_request_data = function() {
		var data = t.parent_tables_data()
		data.table_id = t.id
		for (c in t.colprops) {
			var fid = t.id+"_f_"+c
			var current = t.colprops[c].current_filter
			if ((current != "") && (typeof current !== 'undefined')) {
				data[fid] = current
			} else if ((typeof(t.colprops[c].force_filter) !== "undefined") && (t.colprops[c].force_filter != "")) {
				data[fid] = t.colprops[c].force_filter
			}
			if (data[fid] && t.colprops[c]._class && (t.colprops[c]._class.indexOf("datetime") >= 0)) {
				data[fid] = t.convert_dates_in_filter(data[fid])
			}
		}
		return data
	}

	t.convert_dates_in_filter = function(s) {
		function convert_date(s) {
			if (s.match(/[mdhsMyY]/)) {
				// must be a delta filter => no conversion needed
				return s
			}
			var l = s.match(/([!<>=]*)(.*)/)
			// ">2016-01".match(/([!<>=]*)(.*)/) returns [">2016-01", ">", "2016-01"]
			return l[1] + osvc_date_to_collector(l[2])
		}

		var l = s.split("&")
		for (var i=0; i<l.length; i++) {
			_l = l[i].split("|")
			for (var j=0; j<_l.length; j++) {
				_l[j] = convert_date(_l[j])
			}
			l[i] = _l.join("|")
		}
		return l.join("&")

	}

	t.has_filter_in_request_vars = function() {
		if (!t.options.request_vars) {
			return false
		}
		for (c in t.colprops) {
			if (t.id+"_f_"+c in t.options.request_vars) {
				return true
			}
		}
		return false
	}

	t.add_column_header_slim = function(tr, c) {
		var th = $("<th></th>")
		th.addClass(t.colprops[c]._class)
		th.attr("col", c)
		tr.append(th)
	}

	t.refresh_column_headers_slim = function() {
		t.e_header_slim.empty()
		t.add_column_headers_slim()
	}

	t.add_column_headers_slim = function() {
		if (t.e_header_slim) {
			var tr = t.e_header_slim
		} else {
			var tr = $("<tr class='theader_slim'></tr>")
			t.e_table.append(tr)
			t.e_header_slim = tr
		}
		if (t.options.checkboxes) {
			tr.append($("<th></th>"))
		}
		if (t.options.extrarow) {
			tr.append($("<th></th>"))
		}
		for (i=0; i<t.options.columns.length; i++) {
			var c = t.options.columns[i]
			if (t.options.visible_columns.indexOf(c) >= 0) {
				t.add_column_header_slim(tr, c)
			}
		}
		tr.bind("click", function() {
			t.e_header_filters.toggle()
		})
	}

	t.init_colprops = function() {
		for (var i=0; i<t.options.columns.length; i++) {
			var c = t.options.columns[i]
			t.colprops[c] = $.extend({}, colprops[c], t.options.colprops[c])
		}
	}

	t._cell_decorator = function(cell, span, line) {
                var col = cell.attr('col')
		if (span && t.options.span.indexOf(col) >= 0) {
			cell.empty()
			return
		}
		var cl = cell.attr('class')
		if (!cl) {
			return
		}
		cl = cl.split(/\s+/)
		for (i=0; i<cl.length; i++) {
			var c = cl[i]
			if (!(c in cell_decorators)) {
				continue
			}
			cell_decorators[c](cell, line)
		}
	}

	t.cell_decorator = function(lines) {
		if (!lines) {
			lines = t.e_table.find("tbody > .tl")
		}
		var spansum1 = null
		lines.each(function(){
			var line = $(this)
			var spansum2 = line.attr("spansum")
			if (spansum1 == spansum2) {
				var span = true
			} else {
				var span = false
			}
			spansum1 = spansum2
			line.children("[cell=1]").each(function(){
				t._cell_decorator($(this), span, line)
			})
		})
		return lines
	}

	t.refresh_column_headers = function() {
		if (!t.options.headers) {
			return
		}
		t.e_header.empty()
		t.add_column_headers()
	}

	t.add_column_headers = function() {
		if (!t.options.headers) {
			return
		}
		if (t.e_header) {
			var tr = t.e_header
		} else {
			var tr = $("<tr class='theader'></tr>")
			t.e_table.prepend(tr)
			t.e_header = tr
		}
		if (t.options.checkboxes) {
			var th = $("<th><div class='fa fa-bars movable'></div></th>")
			th.click(function(e){
				table_action_menu(t, e)
			})
			tr.append(th)
		}
		if (t.options.extrarow) {
			tr.append($("<th></th>"))
		}
		for (i=0; i<t.options.columns.length; i++) {
			var c = t.options.columns[i]
			if (t.options.visible_columns.indexOf(c) >= 0) {
				t.add_column_header(tr, c)
			}
		}
	}

	t.add_column_header = function(tr, c) {
		var th = $("<th></th>")
		th.addClass(t.colprops[c]._class)
		th.attr("col", c)
		th.text(i18n.t("col."+t.colprops[c].title))
		tr.append(th)
	}

	t.add_column_header_input_float = function (c) {
		if (t.e_filter) {
			t.e_filter.remove()
		}
		var input_float = $("<div class='white_float_input stackable' style='width:auto;position:absolute'>")
		input_float.draggable({
			"handle": ".fa-bars"
		})
		var header = $("<h2 class='icon fa-bars'></h2>")
		var input = $("<input class='oi' name='fi'>")
		var value_to_filter_tool = $("<span class='clickable icon values_to_filter'></span><br>")
		var value_pie = $("<div></div>")
		var value_cloud = $("<span></span>")

		var input_id = t.id+"_f_"+c
		if (t.options.request_vars && (input_id in t.options.request_vars)) {
			input.val(t.options.request_vars[input_id])
		} else if (typeof t.colprops[c].current_filter !== "undefined") {
			input.val(t.colprops[c].current_filter)
		}
		input.attr("id", input_id)
		header.text(i18n.t("table.column_filter_header", {"col": i18n.t("col."+t.colprops[c].title)}))
		value_to_filter_tool.attr("title", i18n.t("table.value_to_filter_tool_title")).tooltipster()
		value_pie.attr("id", t.id+"_fp_"+c)
		value_pie.css({"margin-top": "0.8em"})
		value_cloud.attr("id", t.id+"_fc_"+c)
		value_cloud.css({"overflow-wrap": "break-word"})

		input_float.append(header)
		input_float.append(input)
		input_float.append(value_to_filter_tool)
		input_float.append(value_pie)
		input_float.append(value_cloud)

		t.e_filter = input_float
		t.div.append(input_float)

		var url = t.options.ajax_url + "_col_values/"

		// refresh column filter cloud on keyup
		var xhr = null
		input.bind("keyup", function(event) {
			var input = $(this)
			var col = c
			t.colprops[c].current_filter = input.val()

			if (is_enter(event) || is_special_key(event)) {
				return
			}

			// handle slim header colorization
			var current_filter = t.e_header_filters.find("[col="+c+"] > .col_filter_label").attr("title")
			if (current_filter != input.val()) {
				t.e_header_slim.find("[col='"+col+"']").removeClass("bgred").addClass("bgorange")
			} else {
				t.e_header_slim.find("[col='"+col+"']").removeClass("bgorange")
				if (input.val() != "") {
					t.e_header_slim.find("[col='"+col+"']").addClass("bgred")
				}
			}

			clearTimeout(t.refresh_timer)
			t.refresh_timer = setTimeout(function validate(){
				if (xhr) {
					xhr.abort()
				}
				var data = t.prepare_request_data()
				//data[input.attr('id')] = input.val()
				var dest = input.siblings("[id^="+t.id+"_fc_]")
				var pie = input.siblings("[id^="+t.id+"_fp_]")
				pie.height(0)
				_url = url + col
				xhr = $.ajax({
					type: "POST",
					url: _url,
					data: data,
					sync: false,
					context: document.body,
					beforeSend: function(req){
						t.scroll_disable_dom()
						pie.empty()
						dest.empty()
						t.scroll_enable_dom()
						dest.addClass("icon spinner")
					},
					success: function(msg){
						var data = $.parseJSON(msg)
						if (t.colprops[col] && t.colprops[col]._class && t.colprops[col]._class.match(/datetime/)) {
							data = t.convert_cloud_dates(data)
						}
						t.format_values_cloud(dest, data, col)
						t.format_values_pie(pie, data, col)
					}
				})
			}, 1000)
		})

		// validate column filter on <enter> keypress
		input.bind("keypress", function(event) {
			if (is_enter(event)) {
				t.e_filter.remove()
				t.save_column_filters()
				t.refresh_column_filters_in_place()
				t.refresh()
			}
		})

		// values to column filter click
		input.siblings(".values_to_filter").bind("click", function(event) {
			var input = $(this).parent().find("input")
			var ck = input.attr("id").replace("_f_", "_fc_")
			var cloud = $(this).parent().find("#"+ck)
			values_to_filter(input, cloud)
			t.colprops[c].current_filter = input.val()
			t.save_column_filters()
			t.refresh_column_filters_in_place()
			t.refresh()
		})

	}

	t.add_column_header_input = function (tr, c) {
		var th = $("<th></th>")
		//th.addClass(t.colprops[c]._class)
		th.attr("col", c)

		var filter_tool = $("<span class='clickable icon filter16'></span>")
		var invert_tool = $("<span class='clickable hidden icon invert16'></span>")
		var clear_tool = $("<span class='clickable hidden icon clear16'></span>")
		var label = $("<span class='col_filter_label'></span>")

		th.append(filter_tool)
		th.append(invert_tool)
		th.append(clear_tool)
		th.append(label)
		tr.append(th)
	}

	t.add_column_headers_input = function() {
		if (!t.options.headers) {
			return
		}
		if (t.e_header_filters) {
			var tr = t.e_header_filters
		} else {
			var tr = $("<tr class='theader_filters'></tr>")
			t.e_table.prepend(tr)
			t.e_header_filters = tr
		}
		if (!t.options.filterable) {
			tr.hide()
		}
		if (t.options.checkboxes) {
			var mcb_id = t.id+"_mcb"
			var th = $("<th></th>")
			var input = $("<input type='checkbox' class='ocb'></input>")
			input.attr("id", mcb_id)
			var label = $("<label></label>")
			label.attr("for", mcb_id)
			input.bind("click", function() {
				check_all(t.id+"_ck", this.checked)
				t.highlighed_checked_lines()
			})
			th.append(input)
			th.append(label)
			tr.append(th)
		}
		if (t.options.extrarow) {
			tr.append($("<th></th>"))
		}
		for (i=0; i<t.options.columns.length; i++) {
			var c = t.options.columns[i]
			if (t.options.visible_columns.indexOf(c) >= 0) {
				t.add_column_header_input(tr, c)
			}
		}
		t.bind_filter_input_events()
	}

	t.refresh_column_filters = function() {
		t.e_table.find("tr.theader.stick").remove()
		t.e_header_filters.empty()
		t.add_column_headers_input()
		t.refresh_column_filters_in_place()
	}

	t.filter_submit = function(c, val) {
		t.refresh_column_filter(c, val)
		t.refresh()
	}

	t.refresh_column_filter = function(c, val) {
		if (!t.e_header_filters) {
			return
		}
		var th = t.e_header_filters.find("th[col="+c+"]")
		if (th.length == 0) {
			// a bogus col filter in db with no corresponding column
			return
		}

		var label = th.find(".col_filter_label")

		if ((c in t.colprops) && (typeof(t.colprops[c].force_filter) !== "undefined") && (t.colprops[c].force_filter != "")) {
			val = t.colprops[c].force_filter
		}

		if (typeof(val) === "undefined") {
			val = t.colprops[c].current_filter
		} else {
			t.colprops[c].current_filter = val
		}

		// update text in display area
		if (typeof(val) === "undefined") {
			val = ""
		}
		var n = val.length
		if ((n == 0) && (typeof(t.colprops[c].default_filter) !== "undefined") && (t.colprops[c].default_filter != "")) {
			val = t.colprops[c].default_filter
			n = val.length
		}
		if (n > 20) {
			var _val = val.substring(0, 17)+"..."
			label.attr("title", val).tooltipster()
		} else {
			var _val = val
			label.attr("title", "")
			try { label.tooltipster("destroy") } catch(e) {}
		}
		label.text(_val)

		// toggle the clear and invert tools visibility
		if (val == "") {
			th.find(".clear16,.invert16").hide()
		} else {
			th.find(".clear16,.invert16").show()
		}

		if ((c in t.colprops) && (typeof(t.colprops[c].force_filter) !== "undefined") && (t.colprops[c].force_filter != "")) {
			th.find(".clear16,.invert16,.filter16").hide()
		}

		// update the slim header cell colorization
		var th = t.e_header_slim.find("[col="+c+"]")
		th.removeClass("bgblack")
		th.removeClass("bgred")
		th.removeClass("bgorange")
		var cl = ""
		if (val.length > 0) {
			if (!t.options.volatile_filters) {
				th.addClass("bgred")
			} else {
				th.addClass("bgblack")
			}
		}
	}

	t.refresh_column_filters_in_place = function() {
		for (i=0; i<t.options.visible_columns.length; i++) {
			var c = t.options.visible_columns[i]
			t.refresh_column_filter(c)
		}
	}

	t.set_column_filters = function() {
		if (t.options.volatile_filters || t.has_filter_in_request_vars()) {
			return
		}
		if (!(t.id in osvc.table_filters.data)) {
			return
		}
		if (!("current" in osvc.table_filters.data[t.id])) {
			return
		}
		var tf = osvc.table_filters.data[t.id]["current"]
		t.reset_column_filters()
		for (col in tf) {
			var f = tf[col]
			if (col.indexOf(".") >= 0) {
				var k = col.split('.')[1]
			} else {
				var k = col
			}
			t.refresh_column_filter(k, f)
		}
	}

	t.page_submit = function(v){
		t.page = v
		t.refresh()
		t.refresh_column_filters_in_place()
	}

	t.hide_cells = function() {
		for (i=0; i<t.options.columns.length; i++) {
			var c = t.options.columns[i]
			if (t.options.visible_columns.indexOf(c) >= 0) {
				continue
			}
			t.e_table.find("tbody > * > [col="+c+"]").hide()
		}
	}

	t.get_ordered_visible_columns = function() {
		// return visible columns ordered like columns
		var l = []
		for (var i=0; i<t.options.columns.length; i++) {
			var c = t.options.columns[i]
			if (t.options.visible_columns.indexOf(c) < 0 &&
			    t.options.force_cols.indexOf(c) < 0) {
				continue
			}
			l.push(c)
		}
		return l
	}

	t.check_toggle_vis = function(checked, c) {
		if (checked && (t.options.visible_columns.indexOf(c) < 0)) {
			t.options.visible_columns.push(c)
		} else {
			t.options.visible_columns = t.options.visible_columns.filter(function(x){if (x!=c){return true}})
		}
		t.refresh_column_headers_slim()
		t.refresh_column_filters()
		t.refresh_column_headers()
		if (checked) {
			if (t.options.force_cols.indexOf(c) >=0 ) {
				t.e_table.find("tbody > .tl > td[col="+c+"]").show()
			} else {
				t.refresh()
			}
		}
	}

	t.bind_checkboxes = function() {
		$("#table_"+t.id).find("[name="+t.id+"_ck]").each(function(){
			this.value = this.checked
			$(this).click(function(){
				this.value = this.checked
			})
		})
	}

	t.bind_filter_selector = function() {
		$("#table_"+t.id).find("[cell=1]").each(function(){
			$(this).bind("mouseup", function(event) {
				cell = $(event.target)
				if (typeof cell.attr("cell") === 'undefined') {
					cell = cell.parents("[cell=1]").first()
				}
				t.filter_selector(event, cell.attr('col'), $.data(cell[0], 'v'))
			})
			$(this).bind("click", function() {
				t.e_fsr.hide()
			})
		})
	}

	t.cell_fmt = function(k, v) {
		var cl = ""
		var classes = []
		if ((k == "extra") && (typeof(t.options.extrarow_class) !== 'undefined')) {
			classes.push(t.options.extrarow_class)
		}
		if ((k != "extra") && (t.options.visible_columns.indexOf(k) < 0)) {
			classes.push("hidden")
		}
		if (k in t.colprops) {
			if (t.colprops[k]._class) {
				classes = classes.concat(t.colprops[k]._class.split(" "))
			}
			if (t.colprops[k]._dataclass) {
				classes = classes.concat(t.colprops[k]._dataclass.split(" "))
			}
		}
		if (classes.length > 0) {
			var cs = classes.join(' ').replace(/\s+$/, '')
			cl = " class='"+cs+"'"
		}
		if (v == 'empty') {
			var text = ""
		} else {
			var text = v
		}
		var s = $("<td cell='1' col='"+k+"' "+cl+">"+text+"</td>")
		$.data(s[0], "v", v)
		return s
	}

	t.last_checkbox_clicked = null

	t.checkbox_click = function(e) {
		var ref_id = $(e.target).attr("id")
		if (e.shiftKey && t.last_checkbox_clicked) {
			var cbs = t.div.find("input[name="+t.id+"_ck]")
			var start = -1
			var end = -1
			for (var i=0; i<cbs.length; i++) {
				var cb = $(cbs[i])
				if ((cb.attr("id")!=ref_id) && (cb.attr("id")!=t.last_checkbox_clicked)) {
					continue
				}
				if (start < 0) {
					start = i
				} else {
					end = i
				}
			}
			// at least one checkbox between start and end
			for (var i=start+1; i<end; i++) {
				var cb = $(cbs[i])
				cb.prop("checked", !cb.prop("checked"))
			}
		}
		t.last_checkbox_clicked = ref_id
		t.highlighed_checked_lines()
	}
	t.highlighed_checked_lines = function() {
		if ($("#am_"+t.id).length > 0) {
			table_action_menu(t, event)
		}
		t.div.find("input[name="+t.id+"_ck]").each(function(){
			if ($(this).is(":checked")) {
				$(this).parents("tr").first().addClass("tl_checked")
			} else {
				$(this).parents("tr").first().removeClass("tl_checked")
			}
		})
	}

	t.data_to_lines = function (data) {
		var lines = $("<span></span>")
		for (var i=0; i<data.length; i++) {
			var line = $("<tr class='tl h' spansum='"+data[i]['spansum']+"' cksum='"+data[i]['cksum']+"'></tr>")
			var ckid = t.id + "_ckid_" + data[i]['cksum']
			if (t.options.checkboxes) {
				var cb = $("<input class='ocb' value='"+data[i]['checked']+"' type='checkbox' id='"+ckid+"' name='"+t.id+"_ck'>")
				var label = $("<label for='"+ckid+"'></label>")
				var td = $("<td name='"+t.id+"_tools' class='tools'></td>")
				td.append([cb, label])
				line.append(td)
				cb.bind("click", t.checkbox_click)
			}
			if (t.options.extrarow) {
				var k = "extra"
				var v = ""
				var cell = t.cell_fmt(k, v)
				line.append(cell)
			}
			var cols = t.get_ordered_visible_columns()
			for (var j=0; j<cols.length; j++) {
				var k = cols[j]
				var v = data[i]['cells'][j]
				var cell = t.cell_fmt(k, v)
				line.append(cell)
			}
			lines.append(line)
		}
		return lines.children().detach()
	}

	t.refresh_callback = function(msg){
		// don't install the new data if nothing has changed.
		// avoids flickering and useless client load.
		var md5sum = md5(msg)
		if (md5sum == t.md5sum) {
			var msg = ""
			console.log("refresh: data unchanged,", md5sum)
			t.need_refresh = false
			t.unset_refresh_spin()
			return
		}
		console.log("refresh: data changed,", md5sum)
		t.md5sum = md5sum

		// disable DOM insert event trigger for perf
		t.need_refresh = false
		t.scroll_disable_dom()

		try {
			var data = $.parseJSON(msg)
			var pager = data['pager']
			var lines = data['table_lines']
		} catch(e) {
			t.div.html(msg)
			return
		}

		msg = t.data_to_lines(lines)
		if (t.options.detached_decorate_cells) {
			msg = t.cell_decorator(msg)
		}

		// detach extralines
		var extralines = t.e_table.children("tbody").children(".extraline:visible").detach()

		// detach old lines
		var old_lines = $("<tbody></tbody>").append($("#table_"+t.id).children("tbody").children(".tl").detach())

		// insert new lines
		tbody = $("#table_"+t.id).children("tbody")
		tbody.append(msg)

		if (!t.options.detached_decorate_cells) {
			msg = t.cell_decorator(msg)
		}

		// reattach extralines
		extralines.each(function(){
			var cksum = $(this).attr("anchor")
			var new_line = tbody.children(".tl[cksum="+cksum+"]")
			if (new_line.length == 0) {
				// the extraline parent line disappeared
				return
			}
			// the extraline parent line is still there in the new dataset
			var content = $(this).children("td:last").children().detach()
			var id = toggle_extraline(new_line.get(0))
			$("#"+id).append(content)
		})
		extralines.remove()

		tbody.children(".tl").each(function(){
			var new_line = $(this)
			var cksum = new_line.attr("cksum")
			var old_line = $("[cksum="+cksum+"]", old_lines)
			if (old_line.length == 0) {
				// this is a new line : highlight
				new_line.addClass("tohighlight")
				return
			} else if (old_line.length > 1) {
				//alert("The table key is not unique. Please contact the editor.")
				return
			}
			for (i=0; i<old_line.children().length; i++) {
				var new_cell = $(":nth-child("+i+")", new_line)
				if (!new_cell.is(":visible")) {
					continue
				}
				var old_cell = $(":nth-child("+i+")", old_line)
				if ($.data(old_cell[0], "v") == $.data(new_cell[0], "v")) {
					continue
				}
				new_cell.addClass("tohighlight")
			}
		})

		old_lines.remove()

		// clear mem refs
		cksum = null
		msg = null
		new_cell = null
		old_cell = null
		new_line = null
		old_line = null
		old_lines = null

		t.pager(pager)
		t.add_filtered_to_visible_columns()
		t.bind_checkboxes()
		t.bind_filter_selector()
		t.bind_action_menu()
		t.restripe_lines()
		t.hide_cells()
		t.unset_refresh_spin()
		tbody.find("tr.tl").children("td.tohighlight").removeClass("tohighlight").effect("highlight", 1000)
		t.scroll_enable_dom()
		t.scroll()

		t.refresh_child_tables()
		t.on_change()

		if (t.need_refresh) {
			t.e_tool_refresh.trigger("click")
		}
	}

	t.insert = function(data) {
		var params = {
			"table_id": t.id
		}
		for (i=0; i<data.length; i++) {
			try {
				var key = data[i]["key"]
				var val = data[i]["val"]
				var op = data[i]["op"]
				params[t.id+"_f_"+key] = op+val
			} catch(e) {
				return
			}
		}
		for (c in t.colprops) {
			if (c == key) {
				continue
			}
			var current = t.colprops[c].current_filter

			if ((current != "") && (typeof current !== 'undefined')) {
				params[t.id+"_f_"+c] = current
			} else if ((typeof(t.colprops[c].force_filter) !== "undefined") && (t.colprops[c].force_filter != "")) {
				params[t.id+"_f_"+c] = t.colprops[c].force_filter
			}
		}
		params.visible_columns = t.get_ordered_visible_columns().join(',')
		$.ajax({
			type: "POST",
			url: t.options.ajax_url+"/data",
			data: params,
			context: document.body,
			beforeSend: function(req){
				t.set_refresh_spin()
			},
			success: function(msg){
				t.need_refresh = false

				// disable DOM insert event trigger for perf
				t.scroll_disable_dom()

				try {
					var data = $.parseJSON(msg)
					var pager = data['pager']
					var lines = data['table_lines']
				} catch(e) {}

				msg = t.data_to_lines(lines)

				// replace already displayed lines
				modified = []

				n_new_lines = 0

				$(msg).each(function(){
					n_new_lines += 1
					new_line = $(this)
					cksum = new_line.attr("cksum")
					$("#table_"+t.id).find("[cksum="+cksum+"]").each(function(){
						$(this).before(new_line)
						for (i=1; i<$(this).children().length+1; i++) {
							cell = $(":nth-child("+i+")", this)
							if (!cell.is(":visible")) {
								continue
							}
							new_cell = $(":nth-child("+i+")", new_line)
							if ($.data(cell[0], "v") == $.data(new_cell[0], "v")) {
								continue
							}
							new_cell.addClass("highlight")
						}
						$(this).remove()
						modified.push(cksum)
					})
				})

				// insert new lines
				first_line = $("#table_"+t.id).find(".tl").first()
				first_line.before(msg)
				if (msg.length > 0) {
					// remove "no data" lines
					$("#table_"+t.id).find(".nodataline").remove()
				}

				new_line = first_line.prev(".tl")
				while (new_line.length > 0) {
					if (modified.indexOf(new_line.attr("cksum"))>=0) {
						// remove lines already changed in-place
						new_line = new_line.prev()
						new_line.next().remove()
						continue
					}
					// highlight new lines
					new_line.addClass("highlight")
					new_line = new_line.prev(".tl")
				}
				n_new_lines -= modified.length
				t.options.pager.total += n_new_lines

				t.pager()
				t.trim_lines()
				t.restripe_lines()
				t.bind_checkboxes()
				t.bind_filter_selector()
				t.bind_action_menu()
				t.hide_cells()
				t.cell_decorator()

				$(".highlight").each(function(){
					$(this).removeClass("highlight")
					$(this).effect("highlight", 1000)
				})

				t.unset_refresh_spin()
				t.scroll_enable_dom()
				t.scroll()

				t.refresh_child_tables()
				t.on_change()

				// clear mem refs
				cksum = null
				msg = null
				cell = null
				new_cell = null
				new_line = null
				b = null
				modified = null
			}
		})
	}

	t.refresh = function() {
		if (t.div.length > 0 && !t.div.is(":visible")) {
			return
		}
		if (t.delay_refresh || (t.e_tool_refresh && t.e_tool_refresh.length > 0 && t.e_tool_refresh_spin && t.e_tool_refresh_spin.hasClass(t.spin_class))) {
			t.need_refresh = true
			return
		} else {
			t.set_refresh_spin()
		}

		var data = t.prepare_request_data()

		data.visible_columns = t.get_ordered_visible_columns().join(',')
		data[t.id+"_page"] = t.page
		$.ajax({
			type: "POST",
			url: t.options.ajax_url+"/data",
			data: data,
			context: document.body,
			beforeSend: function(req){
				t.div.find(".nodataline>td").text(i18n.t("api.loading"))
			},
			success: t.refresh_callback
		})
	}

	t.link = function() {
		if (t.options.caller) {
			t.link_fn()
		} else {
			t.link_href()
		}
	}

	t.link_fn = function() {
		var options = t.options
		options.volatile_filters = true

		// fset
		var current_fset = $("[name=fset_selector]").find("span").attr("fset_id")
		options.fset_id = current_fset

		// col filters
		for (c in t.colprops) {
			var val = t.colprops[c].current_filter
			if ((val == "") || (typeof val === "undefined")) {
				continue
			}
			options.request_vars[t.id+'_f_'+c] = val
		}
		osvc_create_link(t.options.caller, options, "link_title_table", {"icon": t.options.icon, "name": t.options.name})
	}

	t.link_href = function() {
		var url = get_view_url()
		url = url.replace(/#$/, "")+"?";
		var args = "clear_filters=true&discard_filters=true"

		// fset
		var current_fset = $("[name=fset_selector]").find("span").attr("fset_id")
		args += "&dbfilter="+current_fset

		// col filters
		for (c in t.colprops) {
			var val = t.colprops[c].current_filter
			if ((val == "") || (typeof val === "undefined")) {
				continue
			}
			args += '&'+t.id+"_"+c+"="+encodeURIComponent(val)
		}
		osvc_create_link(url, args, "link_title_table", {"name": t.options.name})
	}

	t.position_on_pointer = function(event, e) {
		var pos = $(event.target).position()
		var szpos = t.div.children(".table_scroll_zone").position()
		e.css({
			"left": pos.left + szpos.left + "px",
			"top": pos.top + szpos.top + $(event.target).height() + "px"
		})
		keep_inside(e[0])
	}

	t.filter_selector = function(e, k, v) {
		if(e.button != 2) {
			return
		}

		// update the column name
		t.e_fsr.find("[name=colname]").remove()
		if (k in colprops) {
			var coldiv = $("<div name='colname'></div>")
			coldiv.html(i18n.t("table.fsr.column", {"col": "<span class='b icon "+colprops[k].img+"'>"+i18n.t("col."+colprops[k].title)+"</span>"}))
			coldiv.insertAfter(t.e_fsr.find("h2"))
		}
	  
		// position the tool
		t.e_fsr.show()
		t.position_on_pointer(e, t.e_fsr)

		// reset selected toggles
		t.e_fsr.find(".bgred").each(function(){
			$(this).removeClass("bgred")
		})

		// get selected text
		try {
			var sel = window.getSelection().toString()
		} catch(e) {
			var sel = document.selection.createRange().text
		}
		if (sel.length == 0) {
			sel = v
		}

		// store original sel
		var _sel = sel

		function mangle_sel(){
			var __sel = _sel
			if (t.e_fsr.find("#fsrwildboth").hasClass("bgred")) {
				__sel = '%' + __sel + '%'
			} else if (t.e_fsr.find("#fsrwildleft").hasClass("bgred")) {
				__sel = '%' + __sel
			} else if (t.e_fsr.find("#fsrwildright").hasClass("bgred")) {
				__sel = __sel + '%'
			}
			if (t.e_fsr.find("#fsrneg").hasClass("bgred")) {
				__sel = '!' + __sel
			}
			return __sel
		}

		t.e_fsr.find("#fsrview").each(function() {
			$(this).text(t.colprops[k].current_filter)
			$(this).unbind()
			$(this).bind("dblclick", function(){
				sel = $(this).text()
				t.colprops[k].current_filter = sel
				t.save_column_filters()
				t.refresh_column_filters_in_place()
				t.refresh()
				t.e_fsr.hide()
			})
			$(this).bind("click", function() {
				cur = $(this).text()
				//cur = sel
				$(this).removeClass("highlight")
				$(this).addClass("b")
				t.colprops[k].current_filter = cur
				t.e_header_slim.find("[col="+k+"]").each(function() {
					$(this).removeClass("bgred")
					$(this).addClass("bgorange")
				})
			})
		})
		t.e_fsr.find("#fsrreset").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(t.colprops[k].current_filter)
					$(this).removeClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrclear").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text("")
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrneg").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				if ($(this).hasClass("bgred")) {
					$(this).removeClass("bgred")
				} else {
					$(this).addClass("bgred")
				}
				sel = mangle_sel()
			})
		})
		t.e_fsr.find("#fsrwildboth").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				if ($(this).hasClass("bgred")) {
					$(this).removeClass("bgred")
				} else {
					t.e_fsr.find("[id^=fsrwild]").each(function(){
						$(this).removeClass("bgred")
					})
					$(this).addClass("bgred")
				}
				sel = mangle_sel()
			})
		})
		t.e_fsr.find("#fsrwildleft").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				if ($(this).hasClass("bgred")) {
					$(this).removeClass("bgred")
				} else {
					t.e_fsr.find("[id^=fsrwild]").each(function(){
						$(this).removeClass("bgred")
					})
					$(this).addClass("bgred")
				}
				sel = mangle_sel()
			})
		})
		t.e_fsr.find("#fsrwildright").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				if ($(this).hasClass("bgred")) {
					$(this).removeClass("bgred")
				} else {
					t.e_fsr.find("[id^=fsrwild]").each(function(){
						$(this).removeClass("bgred")
					})
					$(this).addClass("bgred")
				}
				sel = mangle_sel()
			})
		})
		t.e_fsr.find("#fsreq").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(sel)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrandeq").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				val = cur + '&' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsroreq").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				val = cur + '|' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrsup").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				val = '>' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrandsup").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				val = cur + '&>' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrorsup").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				val = cur + '|>' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrinf").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				val = '<' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrandinf").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				val = cur + '&<' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrorinf").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				val = cur + '|<' + sel
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrempty").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				if (t.e_fsr.find("#fsrneg").hasClass("bgred")) {
					val = '!empty'
				} else {
					val = 'empty'
				}
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrandempty").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				if (t.e_fsr.find("#fsrneg").hasClass("bgred")) {
					val = cur + '&!empty'
				} else {
					val = cur + '&empty'
				}
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
		t.e_fsr.find("#fsrorempty").each(function(){
			$(this).unbind()
			$(this).bind("click", function(){
				cur =  t.colprops[k].current_filter
				if (t.e_fsr.find("#fsrneg").hasClass("bgred")) {
					val = cur + '|!empty'
				} else {
					val = cur + '|empty'
				}
				t.e_fsr.find("#fsrview").each(function(){
					$(this).text(val)
					$(this).addClass("highlight")
				})
			})
		})
	}

	t.add_filterbox = function() {
		if (t.e_fsr) {
			return
		}
		var s = "<span id='fsr"+t.id+"' class='right_click_menu stackable' style='display: none'>"
		s += "<h2 class='icon fa-bars movable'>"+i18n.t("table.filterbox_title")+"</h2>"
		s += "<table>"
		s +=  "<tr>"
		s +=   "<td id='fsrview' colspan=3 style='height:1.3em'></td>"
		s +=  "</tr>"
		s +=  "<tr>"
		s +=   "<td id='fsrclear'>clear</td>"
		s +=   "<td id='fsrreset'>reset</td>"
		s +=   "<td id='fsrneg'>!</td>"
		s +=  "</tr>"
		s +=  "<tr>"
		s +=   "<td id='fsrwildleft'>%..</td>"
		s +=   "<td id='fsrwildright'>..%</td>"
		s +=   "<td id='fsrwildboth'>%..%</td>"
		s +=  "</tr>"
		s +=  "<tr>"
		s +=   "<td id='fsreq'>=</td>"
		s +=   "<td id='fsrandeq'>&=</td>"
		s +=   "<td id='fsroreq'>|=</td>"
		s +=  "</tr>"
		s +=  "<tr>"
		s +=   "<td id='fsrsup'>></td>"
		s +=   "<td id='fsrandsup'>&></td>"
		s +=   "<td id='fsrorsup'>|></td>"
		s +=  "</tr>"
		s +=  "<tr>"
		s +=   "<td id='fsrsinf'><</td>"
		s +=   "<td id='fsrandinf'>&<</td>"
		s +=   "<td id='fsrorinf'>|<</td>"
		s +=  "</tr>"
		s +=  "<tr>"
		s +=   "<td id='fsrempty'>empty</td>"
		s +=   "<td id='fsrandempty'>&empty</td>"
		s +=   "<td id='fsrorempty'>|empty</td>"
		s +=  "</tr>"
		s += "</table>"
		s += "</span>"
		t.e_fsr = $(s)
		t.div.append(t.e_fsr)
		t.e_fsr.draggable({
			"handle": ".fa-bars"
		})
	}

	t.save_column_filters = function() {
		if (t.options.volatile_filters) {
			return
		}
		var data = []
		var del_data = []

		for (c in t.colprops) {
			var val = t.colprops[c].current_filter
			if (val != "" && (typeof val !== "undefined")) {
				// filter value to save
				var d = {
					'bookmark': 'current',
					'col_tableid': t.id,
					'col_name': c,
					'col_filter': val
				}
				data.push(d)
			} else {
				// filter value to delete
				var d = {
					'bookmark': 'current',
					'col_tableid': t.id,
					'col_name': c
				}
				del_data.push(d)
			}
		}

		if (data.length > 0) {
			services_osvcpostrest("R_USERS_SELF_TABLE_FILTERS", "", "", data, function(jd) {
				if (jd.error && (jd.error.length > 0)) {
					osvc.flash.error(services_error_fmt(jd))
				}
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		}
		if (del_data.length > 0) {
			services_osvcdeleterest("R_USERS_SELF_TABLE_FILTERS", "", "", del_data, function(jd) {
				if (jd.error && (jd.error.length > 0)) {
					osvc.flash.error(services_error_fmt(jd))
				}
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		}
	}

	t.unset_refresh_spin = function() {
		if (!t.e_tool_refresh_spin) {
			return
		}
		t.e_tool_refresh_spin.removeClass(t.spin_class)
		t.delay_refresh = true
		t.e_tool_refresh_spin.addClass("grayed")
		setTimeout(function(){
			t.delay_refresh = false
			t.e_tool_refresh_spin.removeClass("grayed")
			if (t.need_refresh) {
				t.refresh()
			}
		}, t.options.delay)
	}

	t.set_refresh_spin = function() {
		if (!t.e_tool_refresh_spin) {
			return
		}
		t.e_tool_refresh_spin.addClass(t.spin_class)
	}

	t.add_ws_handler = function() {
		if (!t.options.events || (t.options.events.length == 0)) {
			return
		}
		console.log("register table", t.id, t.options.events.join(","), "event handler")
		wsh[t.id] = function(data) {
			if (t.options.events.indexOf(data["event"]) < 0) {
				return
			}
			t.refresh()
		}
	}

	t.add_pager = function() {
		if (!t.options.pageable) {
			return
		}
		var e = $("<span class='pager floatw'></span>")
		t.e_toolbar.prepend(e)
		t.e_pager = e
	}

	t.bind_filter_reformat = function() {
		$("#table_"+t.id).find("input").each(function(){
			attr = $(this).attr('id')
			if ( typeof(attr) == 'undefined' || attr == false ) {
				return
			}
			if ( ! attr.match(/nodename/gi) &&
			     ! attr.match(/svcname/gi) &&
			     ! attr.match(/fqdn/gi) &&
			     ! attr.match(/assetname/gi) &&
			     ! attr.match(/svc_id/gi) &&
			     ! attr.match(/node_id/gi) &&
			     ! attr.match(/disk_id/gi) &&
			     ! attr.match(/disk_svcname/gi) &&
			     ! attr.match(/save_svcname/gi)
			) {return}
			$(this).bind("change keyup input", function(){
				if (this.value.match(/\s+/g)) {
					if (this.value.match(/^\(/)) {return}
					this.value = this.value.replace(/\s+/g, ',')
					if (!this.value.match(/^\(/)) {
						this.value = '(' + this.value
					}
					if (!this.value.match(/\)$/)) {
						this.value = this.value + ')'
					}
				}
			})
		})
	}

	t.format_values_cloud = function(span, data, col) {
		span.removeClass("spinner")

		var keys = []
		var max = 0
		var min = Number.MAX_SAFE_INTEGER 
		var delta = 0
		for (key in data) {
			keys.push(key)
			n = data[key]
			if (n > max) max = n
			if (n < min) min = n
		}
		delta = max - min

		// header
		var header = $("<h3></h3>")
		header.text(i18n.t("table.unique_matching_values", {"count": keys.length}))
		span.append(header)

		// 'empty' might not be comparable with other keys type
		if ('empty' in keys) {
			var skeys = keys
			skeys.remove('empty')
			skeys = ['empty'] + skeys.sort()
		} else {
			skeys = keys.sort()
		}

		// candidates
		t.scroll_disable_dom()
		for (var i=0; i<skeys.length ; i++) {
			var key = skeys[i]
			var n = data[key]
			if (delta > 0) {
				var size = 100 + 100. * (n - min) / delta
			} else {
				var size = 100
			}

			e = $("<a class='h cloud_tag' style='font-size:"+size+"%'>"+key+"</a>")
			e.attr("title", i18n.t("table.number_of_occurence", {"count": data[key]})).tooltipster()
			span.append(e)
		}
		t.scroll_enable_dom()
		span.children("a").bind("click", trigger)

		function trigger() {
			span.siblings("input").val($(this).text())
			t.colprops[col].current_filter = $(this).text()
			t.refresh()
			t.refresh_column_filters_in_place()
			t.save_column_filters()
		}
	}

	t.format_values_pie = function(o, data, col) {
		require(["jqplot"], function() {t._format_values_pie(o, data, col)})
	}

	t._format_values_pie = function(o, data, col) {
		o.empty()

		// avoid ploting too difuse datasets and single pie dataset
		var n = Object.keys(data).length
		if ((n > 200) || (n < 2)) {
			return
		}

		o.height("15em")
		o.width("100%")

		// format as jqplot expects
		var l = []
		for (key in data) {
			l.push([key, data[key]])
		}

		l.sort(function(a, b){
			if(a[1] < b[1]) return 1;
			if(a[1] > b[1]) return -1;
			return 0;
		})

		// jqplot pie aspect
		options = {
			grid:{
				background: 'transparent',
				borderColor: 'transparent',
				shadow: false,
				drawBorder: false,
				shadowColor: 'transparent'
			},
			seriesDefaults: {
				sortData: true,
				renderer: $.jqplot.PieRenderer,
				//seriesColors: c,
				rendererOptions: {
					padding: 10,
					sliceMargin: 4,
					dataLabelPositionFactor: 1,
					startAngle: -90,
					dataLabelThreshold: 4,
					dataLabelNudge: 12,
					dataLabels: 'percent',
					showDataLabels: true
				}
			},
			legend: {
				show:false,
			}
		}
		$.jqplot(o.attr('id'), [l], options)
		o.unbind('jqplotDataHighlight')
		o.unbind('jqplotDataUnhighlight')
		o.unbind('jqplotDataClick')
		o.bind('jqplotDataHighlight', function(ev, seriesIndex, pointIndex, data) {
			var val = data[0]
			$(this).next().find("a").each(function(){
				$(this).removeClass("pie_hover")
				if ($(this).text() == val) {
					$(this).addClass("pie_hover")
				}
			})
		})
		o.bind('jqplotDataUnhighlight', function(ev, seriesIndex, pointIndex, data) {
			$(this).next().find("a").removeClass("pie_hover")
		})
		o.bind('jqplotDataClick', function(ev, seriesIndex, pointIndex, data) {
			var val = data[0]
			var input = $(this).siblings("input")
			input.val(val)
			t.colprops[col].current_filter = val
			t.refresh()
			t.refresh_column_filters_in_place()
			t.save_column_filters()
		})
	}

	t.bind_filter_input_events = function() {
		// open filter input on filter icon click
		t.e_header_filters.find("th > .filter16").bind("click", function(event) {
			var c = $(this).parent().attr("col")
			t.add_column_header_input_float(c)
			t.e_filter.show()
			t.position_on_pointer(event, t.e_filter)
			register_pop_up(event, t.e_filter)
			t.e_filter.find("input").focus().trigger("keyup")
		})

		// clear column filter click
		t.e_header_filters.find("th > .clear16").bind("click", function(event) {
			var c = $(this).parent().attr("col")
			if ((c in t.colprops) && (typeof(t.colprops[c].force_filter) !== "undefined") && (t.colprops[c].force_filter != "")) {
				t.colprops[c].current_filter = t.colprops[c].force_filter
			} else if ((c in t.colprops) && (typeof(t.colprops[c].default_filter) !== "undefined") && (t.colprops[c].default_filter != "")) {
				t.colprops[c].current_filter = t.colprops[c].default_filter
			} else {
				t.colprops[c].current_filter = ""
			}
			t.save_column_filters(c)
			t.refresh_column_filters_in_place()
			t.refresh()
		})

		// invert column filter click
		t.e_header_filters.find("th > .invert16").bind("click", function(event) {
			var c = $(this).parent().attr("col")
			t.invert_column_filter(c)
			t.refresh_column_filters_in_place()
			t.refresh()
		})

		t.bind_filter_reformat()
	}

	t.convert_cloud_dates = function(data) {
		var _data = {}
		for (var d in data) {
			_data[osvc_date_from_collector(d)] = data[d]
		}
		return _data
	}

	//
	// table tool: link
	//
	t.add_link = function() {
		if (!t.options.linkable) {
			return
		}
		var e = $("<div class='floatw clickable' name='tool_link'></div>")
		var span = $("<span class='icon link16' data-i18n='table.link'></span>")
		span.attr("title", i18n.t("table.link_help")).tooltipster()
		e.append(span)
		try { e.i18n() } catch(e) {}

		// bindings
		e.bind("click", function() {
			t.link()
		})

		$(this).bind("keypress", function(event) {
			if ($('input').is(":focus")) { return }
			if ($('textarea').is(":focus")) { return }
			if ( event.which == 108 ) {
				t.link()
			}
		})

		t.e_tool_link = e
		t.e_toolbar.prepend(e)
	}

	//
	// table tool: csv export
	//
	t.add_csv = function() {
		if (!t.options.exportable) {
			return
		}

		var e = $("<div class='floatw clickable' name='tool_csv'></div>")
		t.e_tool_csv = e

		var span = $("<span class='icon csv' data-i18n='table.csv'></span>")
		e.append(span)

		e.bind("click", function() {
			var _e = t.e_tool_csv.children("span")
			if (!_e.hasClass("csv")) {
				return
			}
			_e.removeClass("csv").addClass("csv_disabled")
			setTimeout(function() {
				_e.removeClass("csv_disabled").addClass("csv")
			}, 10000)

			var data = t.prepare_request_data()
			var l = []
			for (k in data) {
				l.push(encodeURIComponent(k)+"="+encodeURIComponent(data[k]))
			}
			var q = l.join("&")
			var url = t.options.ajax_url+"/csv"
			if (q.length > 0) {
				url += "?"+q
			}
			document.location.href = url
		})
		try { e.i18n() } catch(e) {}
		t.e_toolbar.prepend(e)
	}

	//
	// table tool: refresh
	//
	t.add_refresh = function() {
		if (!t.options.refreshable) {
			return
		}

		var e = $("<div class='floatw clickable' name='tool_refresh'><span class='fa refresh16'></span><span></span></div>")
		e.children().last().text("  "+i18n.t('table.refresh'))

		// bindings
		e.bind("click", function(){
			t.refresh()
		})

		$(this).bind("keypress", function(event) {
			if ($('input').is(":focus")) { return }
			if ($('textarea').is(":focus")) { return }
			if ( event.which == 114 ) {
				t.refresh()
			}
		})

		t.e_tool_refresh = e
		t.e_tool_refresh_spin = e.find(".refresh16")
		t.e_toolbar.prepend(e)
	}

	//
	// table tool: websocket toggle
	//
	t.add_wsswitch = function() {
		if (!t.options.wsable) {
			return
		}

		// checkbox
		var input = $("<input type='checkbox' class='ocb' />")
		input.uniqueId()
		input.bind("click", function() {
			var current_state
			if ($(this).is(":checked")) {
				current_state = 1
			} else {
				current_state = 0
			}
			var data = {
				"upc_table": t.id,
				"upc_field": "wsenabled",
				"upc_visible": current_state,
			}
			services_osvcpostrest("R_USERS_SELF_TABLE_SETTINGS", "", "", data, function(jd) {
				if (t.need_refresh) {
					t.refresh()
				}
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		})

		// label
		var label = $("<label></label>")
		label.attr("for", input.attr("id"))

		// title
		var title = $("<span data-i18n='table.live' style='padding-left:0.3em;'></span>")
		title.attr("title", i18n.t("table.live_help")).tooltipster()

		// container
		var e = $("<span class='floatw'></span>")
		e.append(input)
		e.append(label)
		e.append(title)
		try { e.i18n() } catch(e) {}

		if (!(t.id in osvc.table_settings.data) || !("wsenabled" in osvc.table_settings.data[t.id]) || osvc.table_settings.data[t.id].wsenabled) {
			input.prop("checked", true)
			t.pager()
		} else {
			input.prop("checked", false)
		}

		t.e_toolbar.prepend(e)
		t.e_wsswitch = e
	}

	//
	// table tool: volatile toggle
	//
	t.add_volatile = function() {
		if (!t.options.headers || !t.options.filterable) {
			return
		}

		// checkbox
		var input = $("<input type='checkbox' class='ocb' />")
		if (t.options.volatile_filters) {
			input.prop("checked", true)
		}
		input.uniqueId()
		input.bind("click", function() {
			var current_state
			if ($(this).is(":checked")) {
				current_state = true
			} else {
				current_state = false
			}
			t.options.volatile_filters = current_state
			t.refresh_column_filters_in_place()
		})

		// label
		var label = $("<label></label>")
		label.attr("for", input.attr("id"))

		// title
		var title = $("<span style='padding-left:0.3em'></span>")
		title.text(i18n.t("table.volatile"))
		title.attr("title", i18n.t("table.volatile_help")).tooltipster()

		// container
		var e = $("<span class='floatw'></span>")
		e.append(input)
		e.append(label)
		e.append(title)

		t.e_toolbar.prepend(e)
	}

	//
	// table tool: commonality
	//
	t.add_commonality = function() {
		if (!t.options.commonalityable) {
			return
		}

		var e = $("<div class='floatw clickable' name='tool_commonality'></div>")
		t.e_tool_commonality = e

		var span = $("<span class='icon common16' data-i18n='table.commonality'></span>")
		span.attr("title", i18n.t("table.commonality_help")).tooltipster()
		e.append(span)

		var area = $("<div class='white_float hidden stackable'></div>")
		area.uniqueId()
		e.append(area)
		t.e_tool_commonality_area = area

		e.bind("click", function(event) {
			if (t.e_tool_commonality_area.is(":visible")) {
				t.e_tool_commonality_area.hide()
				return
			}
			click_toggle_vis(event, t.e_tool_commonality_area.attr("id"), 'block')
			t.e_tool_commonality_area.empty()
			spinner_add(t.e_tool_commonality_area)
			var data = t.prepare_request_data()
			$.ajax({
				type: "POST",
				url: t.options.ajax_url+"/commonality",
				data: data,
				context: document.body,
				success: function(msg){
					t.e_tool_commonality_area.html(format(msg))
				}
			})
		})

		function format(msg) {
			var data = $.parseJSON(msg)
			var table = $("<table></table>")
			var th = $("<tr><th data-i18n='table.pct'></th><th data-i18n='table.column'></th><th data-i18n='table.value'></th></tr>")
			th.i18n()
			table.append(th)
			for (var i=0; i<data.length; i++) {
				var d = data[i]
				var line = $("<tr style='margin:0.3em 0'></tr>")

				// pct
				var pct = $("<td></td>")
				pct.append(_cell_decorator_pct(d[2]))
				line.append(pct)

				// column
				var col = $("<td></td>")
				if (d[0] in t.colprops) {
					col.addClass("nowrap icon_fixed_width "+t.colprops[d[0]].img)
					col.text(i18n.t("col."+t.colprops[d[0]].title))
				} else {
					col.text(d[0])
				}
				line.append(col)

				// val
				var val = $("<td></td>")
				val.text(d[1])
				line.append(val)

				table.append(line)
			}
			return table
		}

		try { e.i18n() } catch(e) {}
		t.e_toolbar.prepend(e)
	}

	//
	// table tool: pager
	//
	t.pager = function(options) {
		if (!t.e_pager) {
			return
		}
		if (options) {
			t.options.pager = options
		}

		if (t.e_wsswitch && t.e_wsswitch.find("input").is(":checked")) {
			var wsswitch = true
		} else {
			var wsswitch = false
		}

		var p_page = parseInt(t.options.pager.page)
		var p_start = parseInt(t.options.pager.start)
		var p_end = parseInt(t.options.pager.end)
		var p_total = parseInt(t.options.pager.total)
		var p_perpage = parseInt(t.options.pager.perpage)
		var max_perpage = 50

		if (t.e_wsswitch && t.e_wsswitch.find("input").is(":checked")) {
			var wsswitch = true
			if (p_perpage > max_perpage) {
				p_perpage = max_perpage
				t.options.pager.perpage = max_perpage
			}
		} else {
			var wsswitch = false
		}

		if ((p_total > 0) && (p_end > p_total)) {
			p_end = p_total
		}
		var s_total = ""
		if (p_total > 0) {
			s_total = "/" + p_total
		}

		// perpage selector
		var l = [20, 50, 100, 500]
		var selector = $("<div name='pager_perpage' class='white_float stackable' style='display:none;max-width:50%;text-align:right;'></div>")
		for (i=0; i<l.length; i++) {
			var v = l[i]
			var entry = $("<span name='perpage_val' class='clickable'>"+v+"</span>")
			if (v == p_perpage) {
				entry.addClass("current_page")
			}
			if (wsswitch && (v > max_perpage)) {
				entry.addClass("grayed")
				entry.removeClass("clickable")
			}
			selector.append(entry)
			selector.append($("<br>"))
		}

		t.e_pager.empty()

		// main pager
		if (p_total == 0) {
			t.e_pager.text("No records found matching filters")
		} else {
			// left arrow
			if (p_page > 1) {
				var left = $("<span name='pager_left'></span>")
				left.text("<< ")
				t.e_pager.append(left)
			}

			// line start - line end
			var center = $("<span name='pager_center'></span>")
			center.text((p_start+1)+"-"+p_end+s_total)
			t.e_pager.append(center)

			// right arrow
			if ((p_total < 0) || ((p_page * p_perpage) < p_total)) {
				var right = $("<span name='pager_right'></span>")
				right.text(" >>")
				t.e_pager.append(right)
			}
		}
		t.e_pager.append(selector)
		keep_inside(selector[0])

		t.e_pager.children("span").each(function () {
			$(this).addClass('current_page clickable')
		})
		t.e_pager.find("[name=pager_right]").click(function(){
			t.page_submit(p_page+1)
		})
		t.e_pager.find("[name=pager_left]").click(function(){
			t.page_submit(p_page-1)
		})
		t.e_pager.find("[name=pager_center]").click(function(){
			t.e_pager.find("[name=pager_perpage]").toggle()
		})
		t.e_pager.find("[name=perpage_val]").click(function(){
			if ($(this).hasClass("grayed")) {
				return
			}
			var new_perpage = parseInt($(this).text())
			var data = {
				"perpage": new_perpage
			}
			services_osvcpostrest("R_USERS_SELF", "", "", data, function(jd) {
				t.page = Math.floor(((p_page - 1) * p_perpage) / new_perpage)+1
				t.refresh()
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		})
	}

	//
	// table tool: column selector
	//
	t.add_column_selector = function() {
		if (!t.options.columnable) {
			return
		}

		var e = $("<div class='floatw clickable' name='tool_column_selector'></div>")
		t.e_tool_column_selector = e

		var span = $("<span class='icon columns' data-i18n='table.columns'></span>")
		e.append(span)
		try { e.i18n() } catch(e) {}

		var area = $("<div class='hidden white_float stackable'></div>")
		e.append(area)
		t.e_tool_column_selector_area = area

		for (var i=0; i<t.options.columns.length; i++) {
			var colname = t.options.columns[i]

			// checkbox
			var input = $("<input type='checkbox' class='ocb' />")
			input.attr("colname", colname)
			input.uniqueId()
			input.bind("click", function() {
				var colname = $(this).attr("colname")
				var current_state
				if ($(this).is(":checked")) {
					current_state = 1
				} else {
					current_state = 0
				}
				var data = {
					"upc_table": t.id,
					"upc_field": colname,
					"upc_visible": current_state,
				}
				if (!current_state) {
					if (t.options.force_cols.indexOf(colname) >=0 ) {
						// don't remove forced columns
						t.e_table.find("tbody > * > [col="+colname+"]").hide()
					} else {
						t.e_table.find("tbody > * > [col="+colname+"]").remove()
					}
					// reset the table data md5 so that toggle on-off-on a column is not interpreted
					// as unchanged data
					t.md5sum = null
				}
				services_osvcpostrest("R_USERS_SELF_TABLE_SETTINGS", "", "", data, function(jd) {
					t.check_toggle_vis(current_state, colname)
				},
				function(xhr, stat, error) {
					osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
				})
			})
			if (t.options.visible_columns.indexOf(colname) >= 0) {
				input.prop("checked", true)
			}

			// filtered columns are always visible
			if (t.e_header_filters) {
				var val = t.colprops[colname].current_filter
				if ((val != "") && (typeof val !== "undefined")) {
					input.prop("disabled", true)
					input.prop("checked", true)
				}
			}

			// label
			var label = $("<label></label>")
			label.attr("for", input.attr("id"))

			// title
			var title = $("<span style='padding-left:0.3em;'></span>")
			title.text(i18n.t("col."+t.colprops[colname].title))
			title.addClass("icon_fixed_width")
			title.addClass(t.colprops[colname].img)

			// container
			var _e = $("<div style='margin:0.3em 0;white-space:nowrap'></div>")
			_e.append(input)
			_e.append(label)
			_e.append(title)

			area.append(_e)
		}

		// bindings
		e.bind("click", function() {
			t.e_tool_column_selector_area.toggle()
		})

		try { e.i18n() } catch(e) {}
		t.e_toolbar.prepend(e)
	}

	//
	// table tool: bookmarks
	//
	t.add_bookmarks = function() {
		if (!t.options.bookmarkable) {
			return
		}

		var e = $("<div class='floatw clickable' name='tool_bookmark'></div>")

		var span = $("<span class='icon bookmark16' data-i18n='table.bookmarks'></span>")
		e.append(span)

		var area = $("<div class='white_float hidden stackable'></div>")
		e.append(area)

		var save = $("<a class='icon add16' data-i18n='table.bookmarks_save'></a>")
		area.append(save)

		var save_name = $("<div class='hidden'><hr><div class='icon edit16' data-i18n='table.bookmarks_save_name'></div><div>")
		area.append(save_name)

		var save_name_input = $("<input style='margin-left:1em' class='oi' />")
		save_name.append(save_name_input)

		area.append("<hr>")

		var listarea = $("<span></span>")
		area.append(listarea)
		t.e_tool_bookmarks_listarea = listarea

		var bookmarks = []
		if (t.id in osvc.table_filters.data) {
			for (var b in osvc.table_filters.data[t.id]) {
				if (b == "current") {
					continue
				}
				bookmarks.push(b)
			}
			bookmarks.sort()
		}

		if (!bookmarks.length) {
			listarea.text(i18n.t("table.bookmarks_no_bookmarks"))
		}

		for (var i=0; i<bookmarks.length; i++) {
			var name = bookmarks[i]
			t.insert_bookmark(name)
		}

		try { e.i18n() } catch(e) {}
		t.e_tool_bookmarks = e
		t.e_tool_bookmarks_area = area
		t.e_tool_bookmarks_save = save
		t.e_tool_bookmarks_save_name = save_name
		t.e_tool_bookmarks_save_name_input = save_name_input

		// bindings
		span.bind("click", function() {
			area.toggle()
		})

		save.bind("click", function() {
			var now = new Date()
			save_name_input.val(print_date(now))
			save_name.toggle("blind")
			save_name_input.focus()
		})

		save_name_input.bind("keyup", function(event) {
			if (!is_enter(event)) {
				return
			}
			var name = $(this).val()
			var data = {
				"col_tableid": t.id,
				"bookmark": name,
			}
			services_osvcpostrest("R_USERS_SELF_TABLE_FILTERS_SAVE_BOOKMARK", "", "", data, function(jd) {
				if (jd.error) {
					osvc.flash.error(services_error_fmt(jd))
					return
				}
				t.insert_bookmark(name)
				t.e_tool_bookmarks_save_name.hide()
				t.e_tool_bookmarks_save.show()
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		})

		t.e_toolbar.prepend(e)
	}

	t.init_current_filters = function() {
		if (!t.options.request_vars) {
			return
		}
		for (key in t.options.request_vars) {
			var c = key.split("_f_")[1]
			if (!(c in t.colprops)) {
				continue
			}
                        t.colprops[c].current_filter = t.options.request_vars[key]
		}
	}

	t.insert_bookmark = function(name) {
		// remove the "no_bookmarks" msg
		if (t.e_tool_bookmarks_listarea.find("p").length == 0) {
			t.e_tool_bookmarks_listarea.text("")
		}

		// append the bookmark to the list area
		var bookmark = $("<p></p>")
		bookmark.append($("<a class='icon bookmark16'>"+name+"</a>"))
		bookmark.append($("<a style='float:right' class='icon del16'>&nbsp;</a>"))
		t.e_tool_bookmarks_listarea.append(bookmark)

		// "del" binding
		bookmark.find(".del16").bind("click", function() {
			var name = $(this).prev().text()
			var line = $(this).parents("p").first()
			var data = {
				"col_tableid": t.id,
				"bookmark": name,
			}
			services_osvcdeleterest("R_USERS_SELF_TABLE_FILTERS", "", "", data, function(jd) {
				if (jd.error) {
					osvc.flash.error(services_error_fmt(jd))
					return
				}
				line.hide("blind", function(){line.remove()})
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		})

		// "load" binding
		bookmark.find(".bookmark16").bind("click", function() {
			var name = $(this).text()
			var data = {
				"col_tableid": t.id,
				"bookmark": name,
			}
			services_osvcpostrest("R_USERS_SELF_TABLE_FILTERS_LOAD_BOOKMARK", "", "", data, function(jd) {
				if (jd.error) {
					osvc.flash.error(services_error_fmt(jd))
					return
				}

				// update the column filters
				t.reset_column_filters()
				for (var i=0; i<jd.data.length; i++) {
					var data = jd.data[i]
					if (data.col_name.indexOf(".") >= 0) {
						var k = data.col_name.split('.')[1]
					} else {
						var k = data.col_name
					}
					var v = data.col_filter
					t.refresh_column_filter(k, v)
				}

				t.refresh()
			},
			function(xhr, stat, error) {
				osvc.flash.error(services_ajax_error_fmt(xhr, stat, error))
			})
		})
	}


	t.refresh_timer = null
	t.init_colprops()
	t.add_table()

	// selectors cache
	t.e_toolbar = t.div.find("[name=toolbar]").first()
	t.e_table = t.div.find("table#table_"+t.id).first()

	osvc.tables[t.id] = t

	$.when(
		osvc.user_loaded
	).then(function(){
		t.get_visible_columns()
		t.init_current_filters()
		t.add_filtered_to_visible_columns()
		t.add_column_headers_slim()
		t.add_column_headers_input()
		t.add_column_headers()
		t.refresh_column_filters_in_place()
		t.add_commonality()
		t.add_column_selector()
		t.add_csv()
		t.add_bookmarks()
		t.add_link()
		t.add_refresh()
		t.add_wsswitch()
		t.add_volatile()
		t.add_pager()
		t.hide_cells()
		t.add_filterbox()
		t.add_scrollers()
		t.scroll_enable()
		t.stick()
		t.add_ws_handler()
		t.set_column_filters()
		t.refresh()
	})

	return t
}

