data = {
 'nodes': {
   'title': 'Nodes',
   'batchs': [
     {
       'url': URL(r=request, c='cron', f='cron_update_virtual_asset'),
       'comment': "Copy the location and power feed information from hypervisors to virtual machine nodes table entries",
     },
   ],
 },
 'parsers': {
   'title': 'Parsers',
   'batchs': [
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_evas'),
       'comment': "Insert EVA arrays data from uploads",
     },
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_syms'),
       'comment': "Insert Symmetrix arrays data from uploads",
     },
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_dcss'),
       'comment': "Insert DataCore arrays data from uploads",
     },
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_ibmsvcs'),
       'comment': "Insert IBM SVC arrays data from uploads",
     },
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_hp3pars'),
       'comment': "Insert HP 3par arrays data from uploads",
     },
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_necisms'),
       'comment': "Insert NEC ISM arrays data from uploads",
     },
     {
       'url': URL(r=request, a='feed',  c='default', f='insert_brocades'),
       'comment': "Insert Brocade switches data from uploads",
     },
   ],
 },
 'disks': {
   'title': 'Disks',
   'batchs': [
     {
       'url': URL(r=request, c='disks', f='refresh_b_disk_app'),
       'comment': "Refresh the data table linking disks as viewed by the nodes with the disks as viewed by the storage arrays.",
     },
     {
       'url': URL(r=request, c='disks', f='purge_diskinfo'),
       'comment': "Purge the disk information table",
     },
   ],
 },
 'stats': {
   'title': 'Statistics',
   'batchs': [
     {
       'url': URL(r=request, c='cron', f='cron_stat_day'),
       'comment': "Collect per filterset site statistics",
     },
     {
       'url': URL(r=request, c='cron', f='cron_stat_day_svc'),
       'comment': "Collect per filterset service statistics",
     },
     {
       'url': URL(r=request, c='cron', f='cron_stat_day_disk_app'),
       'comment': "Collect per application code disk allocations",
     },
   ],
 },
 'alerts': {
   'title': 'Alerts',
   'batchs': [
     {
       'url': URL(r=request, c='cron', f='cron_alerts_daily'),
       'comment': "Daily alert janitoring",
     },
     {
       'url': URL(r=request, a='feed', c='default', f='update_save_checks'),
       'comment': "Refresh save checks thresholds and alerts",
     },
     {
       'url': URL(r=request, a='feed', c='default', f='update_dash_checks_all'),
       'comment': "Refresh checks alerts",
     },
   ],
 },
 'obsolescence': {
   'title': 'Obsolescence',
   'batchs': [
     {
       'url': URL(r=request, c='obsolescence', f='_update_dash_obs_os_alert'),
       'comment': "Refresh os alerts",
     },
     {
       'url': URL(r=request, c='obsolescence', f='_update_dash_obs_os_warn'),
       'comment': "Refresh os warnings",
     },
     {
       'url': URL(r=request, c='obsolescence', f='_update_dash_obs_hw_alert'),
       'comment': "Refresh hardware alerts",
     },
     {
       'url': URL(r=request, c='obsolescence', f='_update_dash_obs_hw_warn'),
       'comment': "Refresh hardware warnings",
     },
     {
       'url': URL(r=request, c='obsolescence', f='purge_dash_obs_without'),
       'comment': "Purge obsolescence alerts and warnings",
     },
   ],
 },
}

def batchs():
    d = []
    for section, sdata in data.items():
        d.append(H1(T(sdata['title'])))
        for bdata in sdata['batchs']:
            _d = LI(A(
               P(bdata['comment']),
               _href=bdata['url'],
               _class="clickable",
            ))
            d.append(_d)
    return dict(table=DIV(d, _class="batchs"))

