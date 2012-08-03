#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import alldbname, infodbname
import web
database = "../database/tpbmirror_v2_only_douban.db"
db = web.database(dbn='sqlite', db=database)

"""
    我们需要干以下工作 ：
    以resource_info表为标准，在all_resource表中找到相应的资源id，更新到resource_info表中
  all_resource 表中的extern_info 置为True
   更新每一条记录的hotbank
   hotbank算法如下:
            有resource_info记录的，hotrank + 50
           有评分的 hotrank + 评分*10
    language = "CH"的，评分 + 50
    每一条有介绍的resource，都要更新group_id
    
    以后不论是在all_resource或是resource_info表更新时，只要运行此脚本，就解决问题
"""

def update_douban_all_resource_record():
    #先只更新从豆瓣采集来的信息
    res = db.query('select * from ' + infodbname + ' where source_site=="douban"').list()
    for item in res:
        #将all_resource表中的hotrank、extern及resource_info_id填上
        hotrank = str(50 + item['rating'] * 10)
        db.query('update ' + alldbname + 
                 ' set extern_info="True", hotrank=hotrank+' + hotrank + ',resource_info_id=' + str(item['resource_info_id']) +
                 ' where resource_id==' + str(item['resource_id']))

def update_mtime_all_resource_record():
    #首先从resource_info表中取出数据来
    res = db.query('select * from '+ infodbname + ' where source_site=="mtime" order by resource_info_id DESC').list()
    groupid = 7881
    for item in res:
        is_group = False
        hotrank = str(100 + item['rating'] * 10) 
        try:
            #来源于时光网
            #先用resource_info中的英文名在all_resource中找到相应的记录
            if item['local_name']:
                aka = item['aka'].replace('"', '')
                resource_info = db.query('select * from ' + alldbname + ' where resource_name like "%' + aka + '%"' +  ' and language=="CH" and extern_info=="False" and typeL1=="Video" limit 50').list()
                
                #对得到的每条记录
                for info in resource_info:
                    #首先更新all_resource中的内容 hotbank + extern_info + groupid + resource_info_id
                    db.query('update ' + alldbname + ' set extern_info="True", hotrank=hotrank+' + hotrank + ', resource_info_id=' + str(item['resource_info_id']) +
                             ' where resource_id==' + str(info['resource_id']))
                    
                    #接着判断有没有group_id
                    if info['group_id'] == -1:
                        is_group = True
                        db.query('update ' + alldbname + ' set group_id=' + str(groupid) + ' where resource_id==' + str(info['resource_id']))

                #groupid增加
                if is_group:
                    groupid = groupid + 1
                    is_group = False
                       
            else:
                continue
        except:
            continue

    #language为'CH'的，用sql语句更新就可以



if __name__ == '__main__':
    update_mtime_all_resource_record()
