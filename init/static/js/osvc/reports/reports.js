function metric(divid, options) {
	var o = {}
	o.options = options
	o.div = $("#"+divid)

	o.load = function load() {
		// metric area
		var div = $("<div class='reports_section'></div>")
		if (options.width) {
			div.css({"flex": "1 1 "+options.width})
		}
		o.div.append(div)

		// link
		var title_h = $("<h3></h3>")
		var title_link = $("<span class='clickable icon link16'>&nbsp;</span>")
		title_link.bind("click", function() {  
			osvc_create_link("metric", o.options, "link.metric")
		})
		title_h.append(title_link)
		div.append(title_h)

		// title
		if (o.options.Title && o.options.Title != "") {
			title_h.append(o.options.Title)
		}

		// desc
		if (o.options.Desc !== undefined && o.options.Desc != "") {
			var desc = $("<div></div>")
			desc.text(o.options.Desc)
			div.append(desc)
		}

		// metric table area
		o.table = $("<table class='reports_table'></table>")
		div.append(o.table)

		// render table
		o.render_table()

	}

	o.render_table = function() {
		services_osvcgetrest("R_GET_REPORT_METRIC_SAMPLES", [o.options.metric_id], {"meta": "false", "limit": "0"}, function(jd) {
			if (jd.error && (jd.error.length > 0)) {
				osvc.flash.error(services_error_fmt(jd))
				return
			}
			var data = jd.data
			if (!data || data.length == 0) {
				o.table.text(i18n.t("metrics.no_data"))
			}

			var objname = []

			// table header
			var header = $("<tr></tr>")
			o.table.append(header)
			for (var key in data[0]) {
				var th = $("<th></th>")
				th.text(key)
				header.append(th)
				objname.push(key)
			}

			// table data
			for (var i=0; i<data.length; i++) {
				var point = data[i]
				var tr = $("<tr></tr>")
				for (var j=0; j<objname.length; j++) {
					var name = objname[j]
					var val = point[name]
					if (val == null) {
						continue
					}
					var td = $("<td></td>")
					td.text(val)
					tr.append(td)
				}
				o.table.append(tr)
			}
		})
	}

	o.load()
}

function chart(divid, options) {
	var o = {}
	o.options = options
	o.div = $("#"+divid)

	o.load = function load() {
		// chart area
		var div = $("<div class='reports_section'></div>")
		if (options.width) {
			div.css({"flex": "1 1 "+options.width})
		}
		o.div.append(div)

		// link
		var title_link = $("<span class='clickable icon link16'></span>")
		var title_h = $("<h3></h3>")
		title_link.bind("click", function() {  
			osvc_create_link("chart", o.options, "link.chart")
		})
		title_h.append(title_link)
		div.append(title_h)

		// title
		if (o.options.Title && o.options.Title != "") {
			title_h.append(o.options.Title)
		}

		// desc
		if (o.options.Desc !== undefined && o.options.Desc != "") {
			var desc = $("<div></div>")
			desc.text(o.options.Desc)
			div.append(desc)
		}

		// chart plot area
		var plot_div = $("<div style='height:400px;box-sizing:border-box'>")
		plot_div.uniqueId()
		div.append(plot_div)

		// chart
		o.plot(plot_div.attr("id"))

	}

	o.plot = function(id) {
		$.jqplot.config.enablePlugins = true
		services_osvcgetrest("R_GET_REPORT_CHART_SAMPLES", [o.options.chart_id], {"meta": "false", "limit": "2000"}, function(jd) {
			if (jd.error && (jd.error.length > 0)) {
				osvc.flash.error(services_error_fmt(jd))
				return
			}
			var data = jd.data
			var keys = {}
			var definition = jd.chart_definition
			var metric_definition = {}
			var stackSeries = definition.Options.stack
			var series = []
			var series_data = {}
			var max = 0
			var unit = ""
			var dates = {}
			var series_dates = {}

			for (var i=0; i<definition.Metrics.length; i++) {
				var m = definition.Metrics[i]
				metric_definition[m.metric_id] = m
				if (m.unit) {
					unit = m.unit
				}
			}

			for (var i=0; i<data.length; i++) {
				var point = data[i]
				if (!(point.date in dates)) {
					dates[point.date] = null
				}
				var key = point.metric_id+"-"+point.instance
				if (!(key in keys)) {
					series_dates[key] = {}
					keys[key] = {
					  "metric_id": point.metric_id,
					  "instance": point.instance
					}
					series_data[key] = []
				}
				if (stackSeries) {
					series_dates[key][point.date] = point
				}
				max = Math.max(max, point.value)
			}

			var divisor = best_unit_mb(max, unit)
			if (!stackSeries) {
				for (var i=0; i<data.length; i++) {
					var point = data[i]
					var key = point.metric_id+"-"+point.instance
					series_data[key].push([point.date, point.value/divisor['div']])
				}
			} else {
				// fix data series for stacking, which need aligned data points
				// and apply the divisor to the values
				for (var d in dates) {
					for (var key in series_dates) {
						var serie_dates = series_dates[key]
						if (d in serie_dates) {
							var point = serie_dates[d]
							series_data[key].push([point.date, point.value/divisor['div']])
						} else {
							if (series_data[key].length == 0) {
								var val = 0
							} else {
								var val = series_data[key][series_data[key].length-1].value
								if (val) {
									val /= divisor['div']
								}
							}
							series_data[key].push([d, val])
						}
					}
				}
			}

			var series_list = Object.keys(series_data).map(function (key) {
				return series_data[key]
			})

			if (Object.keys(keys).length > 1) {
				legend = {
				  renderer: $.jqplot.EnhancedLegendRenderer,
				  rendererOptions: {
				    numberRows: 0,
				    numberColumns: 10
				  },
				  show: true,
				  placement: "outside",
				  location: 's',
				  fontSize : '1',
				  rowSpacing : '0.05em',
				  yoffset: 40
				}
			} else {
				legend = {
				  show: false
				}
			}
			for (key in keys) {
				var kc = keys[key]
				if (kc.instance) {
					var label = kc.instance
				} else {
					var label = metric_definition[kc.metric_id].label
				}
				var serie = {
				  'label': label,
				  'shadow': metric_definition[kc.metric_id].shadow,
				  'fill': metric_definition[kc.metric_id].fill
				}
				series.push(serie)
			}
			delete metric_definition
			delete series_dates
			delete series_data
			delete data
	
			p = $.jqplot(id, series_list, {
				stackSeries: stackSeries,
				cursor:{
				  zoom:true,
				  showTooltip:false
				},
				legend: legend,
				grid: {
				  borderWidth: 0.5,
				  shadowOffset: 1.0,
				  shadowWidth: 2
				},
				seriesDefaults: {
				  breakOnNull : true,
				  shadowAngle: 135,
				  shadowOffset: 1.0,
				  shadowWidth: 2,
				  markerOptions: {show: false}
				},
				series: series,
				axes: {
				  xaxis: {
				    renderer: $.jqplot.DateAxisRenderer,
				    numberTicks: 5,
				    tickOptions:{
				      formatString:'%y %b,%d'
				    }
				  },
				  yaxis: {
				    min: 0,
				    tickOptions:{
				      formatString: divisor['fmt']+' '+divisor['unit']
				    }
				  }
				}
			})
			var report_section = $("#"+id).parents(".reports_section").first()
			var legend_height = $("#"+id).find(".jqplot-table-legend").height()
                        if (legend_height > 0) {
				report_section.css({"padding-bottom": 50+legend_height})
			}
		})
	}

	require(["jqplot"], function(){
		o.load()
	})
}

function report(divid, options) {
	var o = {}
	o.options = options
	o.div = $("#"+divid)

	o.create = function() {
		// report area
		o.report_div = $("<div class='reports_div'></div>")
		if (o.options.pad) {
			o.report_div.css({"padding": "1em"})
		}
		o.div.append(o.report_div)

		// title
		var title_link = $("<span class='clickable icon link16'></span>")
		var title_h = $("<h1></h1>")
		title_h.append(title_link)
		title_h.append(o.definition.Title)
		o.report_div.append(title_h)

		// bind the report link click
		title_link.bind("click", function() { 
			osvc_create_link("report", {"report_id" : o.options.report_id }, "link.report")
		})
 	}

	o.load_sections = function() {
		for(var i=0; i<o.definition.Sections.length; i++) {
			var section = o.definition.Sections[i]

			// section area
			var section_div = $("<div style='display:flex;flex-flow:row wrap'></div>")
			section_div.uniqueId()
			o.report_div.append(section_div)

			// title
			if (section.Title !== undefined) {
				var title_h = $("<h3 class='line' style='text-align:left;padding: 0.3em;flex:1 1 100%'></h3>")
				var title_span = $("<span class='icon menu16'></span>")
				title_span.text(section.Title)
				title_h.append(title_span)
				section_div.append(title_h)
			}

			// desc
			if (section.Desc !== undefined) {
				section_div.append("<div style='padding:1em;flex:1 1 100%'>" + section.Desc + "</div>")
			}

			// charts reports
			if (section.Charts !== undefined) {
				for(var l=0; l<section.Charts.length; l++) {
					chart(section_div.attr("id"), section.Charts[l])
				}
			}
			// metrics reports
			if (section.Metrics !== undefined) {
				for (var l=0; l<section.Metrics.length; l++) {
					metric(section_div.attr("id"), section.Metrics[l])
				}
			}
			// flat children support
			if (section.children !== undefined) {
				for (var l=0; l<section.children.length; l++) {
					var child = section.children[l]
					if ("metric_id" in child) {
						metric(section_div.attr("id"), child)
					} else if ("chart_id" in child) {
						chart(section_div.attr("id"), child)
					} else if ("Function" in child) {
						var div = $("<div class='reports_section'></div>")
						div.uniqueId()
						if (child.width) {
							div.css({"flex": "1 1 "+child.width})
						}
						section_div.append(div)

						if ("Args" in child) {
							var options = child.Args
						} else {
							var options = {}
						}
						window[child.Function](div.attr("id"), options)
					}
				}
			}
		}
	}

	o.load = function() {
		services_osvcgetrest("/reports/%1/definition", [o.options.report_id], {"meta": "false", "limit": "0"}, function(jd) {
			if (jd.error && (jd.error.length > 0)) {
				osvc.flash.error(services_error_fmt(jd))
				return
			}
			o.definition = jd.data
			o.create()
			o.load_sections()
		})
	}

	o.load()
}

function reports(divid, options)
{
	var o = {}
	o.options = options
	o.divid = divid
	o.div = $("#"+divid)
  
	o.current_reports = 0

	o.init = function init() {
		o.div_reports_header = o.div.find("#reports_header")
		o.div_reports_data = o.div.find("#reports_data")
		o.ql_link = o.div.find("#reports_ql_link")
		o.reports_select = o.div_reports_header.find("#reports_select")

		o.div_reports_data.bind("click", function () {
			o.reports_select.animate({ left: "-13em" }, 300, "linear")
		})

		o.reports_select.hover(function() {
			o.reports_select.animate({ left: "0" }, 300, "linear")
		},
		function() {
			o.reports_select.animate({ left: "-13em" }, 300, "linear")
		})
		o.reports_select.bind("click", function() {
			o.reports_select.animate({ left: "0" }, 300, "linear")
		})
		o.load()
	}

	o.load = function load() {
		// Init Select Report
		services_osvcgetrest("R_GET_REPORTS", "", {"meta": "false", "limit": "0"}, function(jd) {
			if (jd.error && (jd.error.length > 0)) {
				osvc.flash.error(services_error_fmt(jd))
				return
			}
			var data = jd.data
			if (data.length == 0) {
				return
			}
			o.build_selection(data)
			o.load_selected(data[0].id)
			o.select_report(data[0].id); 
		})
	}

	o.select_report = function select_report(report_id) {
		o.current_reports = report_id
		o.reports_select.find(".report_button_div_active").removeClass("report_button_div_active")
		o.reports_select.find("[report_id="+o.current_reports+"]").addClass("report_button_div_active")
	}

	o.refresh = function refresh(report_id) {
		o.div_reports_data.empty()
		o.load_selected(report_id)
		o.select_report(report_id)
	}

	o.build_selection = function build_selection(data) {
		var sect_div = $("<div style='clear:both'></div>")
		o.reports_select.empty()
		o.reports_select.append(sect_div)

		for (var i=0; i<data.length; i++) {
			var faccess = $("<div class='report_button_div'></div>")
			faccess.attr("report_id", data[i].id)
			faccess.text(data[i].report_name)
			faccess.bind("click", function(event) {
				var report_id = $(this).attr("report_id")
				o.refresh(report_id)
			})
			sect_div.append(faccess)
		}
	}

	o.load_selected = function(report_id) {
		o.report_id = report_id
		report("reports_data", {"report_id": report_id})
	}

	o.div.load("/init/static/views/reports.html", function() {
		o.init()
	})

	return o
}

