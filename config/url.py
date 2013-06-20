#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
    '/',                    pre_fix + 'view.index',
    '/tpbtop',              pre_fix + 'view.topview',
    '/tpbtop/.*',           pre_fix + 'view.typeview',
    '/recent',              pre_fix + 'view.recentview',
    '/search',              pre_fix + 'view.searchview',
    '/help',                pre_fix + 'view.simpletpb_help',
    '/resourceinfoid/.*',   pre_fix + 'view.resource_info',
    '/resourcegroup/.*',    pre_fix + 'view.resource_group',    
    '/fetch',               pre_fix + 'daemon.daemon_fetch',
    
    #------------------定时抓取任务--------------------
    '/cron/fetchrecenttpb',     'utils.fetchtpb.index',
    '/cron/fetchtoptpb',        'utils.scheming.index',
    '/cron/fetchoabt',          'utils.fetchoabt.index',
)
