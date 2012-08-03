#!/usr/bin/env python
# coding: utf-8
import web
import models

database = "database/tpbmirror.db"
db = web.database(dbn='sqlite', db=database)

util_database = "../database/tpbmirror.db"
util_db = web.database(dbn='sqlite', db = util_database)

#数据表名
alldbname = 'all_resource'
infodbname = 'resource_info'

#用户 "顶/踩"的加权分数
hotrank_weighted = 50

#默认从oabt抓回来的初始分数
hotrank_oabt_weighted = 100

#默认从tpb抓回来的初始分数
hotrank_tpb_weighted = 50

hotrank_top_weighted = 90

#首页显示的"热点"标签数量
hot_tags = 18

#每页显示的记录条数
perpage = 40

#检索时默认检索条目
total_count_limit = 1000

#显示最近更新的条目
recent_count_limit = 1000

render = web.template.render('templates/', cache=False)

web.config.debug = False

config = web.storage(
    static = '/static',
    site_name = 'simpletpb',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

