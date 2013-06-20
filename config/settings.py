#!/usr/bin/env python
# coding: utf-8
import web
import models
import os

#如果是在本地调试，请打开此开关，如果上传到sae，请置为False
LOCAL_DEBUG = False
LOCAL_MYSQL_DEBUG = False

if LOCAL_DEBUG:
    database = "database/tpbmirror.db"
    db = web.database(dbn='sqlite', db=database)

    util_database = "../database/tpbmirror.db"
    util_db = web.database(dbn='sqlite', db = util_database)

    templates_root = 'templates'
else:
    import sae
    app_root = os.path.dirname(__file__)
    templates_root = os.path.join(app_root, '../templates')
    db = web.database(dbn='mysql', db=sae.const.MYSQL_DB, host=sae.const.MYSQL_HOST, 
        port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS)
    util_db = db

if LOCAL_MYSQL_DEBUG:
    db = web.database(dbn='mysql', db='simpletpb', host='127.0.0.1', port=3306, user='root', pw='')
    util_db = db
    templates_root = 'templates'

render = web.template.render(templates_root, cache=False)

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

web.config.debug = True

config = web.storage(
    static = '/static',
    site_name = 'simpletpb',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

