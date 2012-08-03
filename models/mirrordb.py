#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import db
from config.settings import hotrank_weighted, hot_tags
from config.settings import perpage, total_count_limit
from config.settings import alldbname, infodbname
from hashlib import md5
import memcache

mc = memcache.Client(['tcp://memcached-memorybox.dotcolud.com:23928'], debug=0)

def add_record_to_all_resource(dbname, resource_name = 'N/A', typeL1 = 'none', 
                               typeL2 = 'none', magnet = '', size = 'Unknown', hotrank = 50, extern_info = 'False', 
                               language = 'EN', ed2k = ''):
    "插入记录"
    db.insert(dbname, resource_name = resource_name, typeL1 = typeL1, typeL2 = typeL2, magnet = magnet, size = size, 
              hotrank = hotrank, extern_info = extern_info, language = language, ed2k = ed2k)
    
def get_recent_records(offset):
    "取得最近抓取的记录"    
    sql_query = 'select * from ' + alldbname + ' order by fetch_time DESC limit ' + str(perpage) + ' offset ' + str(offset)
    return _memchache_get_records(sql_query)
    
def get_top_records(typeL1 = 'Video', typeL2 = None, offset = 0):
    "取得指定类别的记录"
    sql_query = ''
    if typeL2:
#        return db.select(dbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
#            typeL2=typeL2, currtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))), 
#            where = 'typeL1=$typeL1 and typeL2=$typeL2 and fetch_time > $currtime', limit=limit).list()
#        return db.select(alldbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
#            typeL2 = typeL2), where = 'typeL1=$typeL1 and typeL2=$typeL2', order = 'hotrank DESC, fetch_time DESC', limit=limit).list()            
        
        sql_query = 'select * from ' + alldbname +  ' where typeL1=="' + typeL1 + '" and typeL2=="' + typeL2 + '" order by hotrank DESC,  fetch_time DESC, resource_name ASC limit ' + str(perpage) + ' offset ' + str(offset)
        sql_query_count = 'select COUNT(*) AS count from ' + alldbname +  ' where typeL1=="' + typeL1 + '" and typeL2=="' + typeL2 + '"'
    else:
        sql_query = 'select * from ' + alldbname +  ' where typeL1=="' + typeL1 + '" order by hotrank DESC, fetch_time DESC, resource_name ASC limit ' + str(perpage) + ' offset ' + str(offset) 
        sql_query_count = 'select COUNT(*) AS count from ' + alldbname +  ' where typeL1=="' + typeL1 + '"'
    #memcache缓存  
    records =  _memchache_get_records(sql_query)
    records_count = _memchache_get_records(sql_query_count)[0]['count']
    records_count = records_count > total_count_limit and total_count_limit or records_count
    return records, records_count

def get_hot_types():
    "取得当前热门分类(typeL2)"
    sql_query = 'select typeL1,typeL2,avg(hotrank) from all_resource where hotrank<>0 group by typeL2 order by avg(hotrank) DESC limit ' + str(hot_tags)
    return _memchache_get_records(sql_query, time = 20)

def search_all_resource(name, resource_type = 'All', limit=200):
    "全站搜索"
    if resource_type == 'All':
        return db.select(alldbname, where = 'resource_name like "%' + name + '%"', order = "resource_name ASC, hotrank DESC, fetch_time DESC", limit = limit).list()
    else:
        return db.select(alldbname, 
            where = 'typeL1 = "' + resource_type + '" and resource_name like "%' + name + '%"', order = "resource_name ASC, hotrank DESC, fetch_time DESC", limit = limit).list()

def get_resource_group(resource_info_id):
    "获取相近资源记录"
    return db.select(alldbname, where = 'resource_info_id==' + str(resource_info_id), order = "resource_name ASC, hotrank DESC, fetch_time DESC").list()

def get_extern_info(resource_info_id = -1):
    "获取资源的详细信息"
    res =  db.query('select * from ' + infodbname + ' where resource_info_id ==' + str(resource_info_id)).list()
    return res

def set_score_value(resource_id, score_type):
    "设置用户评分"
    
    #首先还要记录hotrank分值
    hotrank_addend = 0;
    if score_type == "score_like":
        hotrank_addend = "+" + str(1 * hotrank_weighted)
    elif score_type == "score_bury":
        hotrank_addend = str(-1 * hotrank_weighted)
    #更新hotrank分值，更新用户"顶/踩"的数据
    sql_query = "update " + alldbname +" set " + score_type + "= " + score_type + "+1, hotrank=hotrank" + hotrank_addend + " where resource_id==" + resource_id
    db.query(sql_query)
    
def get_score_value(resource_id, score_type):
    "获取用户评分"
    sql_query = "select " + score_type + " from " + alldbname + " where resource_id==" + resource_id
    res =   db.query(sql_query).list()[0]
    return str(res[score_type])
        
    
def _memchache_get_records(sql_query, time = 5):
    "memcache缓存,time默认为5分钟"
    
    hash一下，为了key键分布更均衡
    key = md5(sql_query.encode('UTF-16')).hexdigest()
    res = mc.get(key)
    if not res:
        res = db.query(sql_query).list()
        mc.set(key, res, 60 * time) #存100分钟

    res = db.query(sql_query).list()
    return res
