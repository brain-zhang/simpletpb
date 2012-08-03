#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from config.settings import render
from config.settings import perpage
from config.settings import recent_count_limit
from models import mirrordb

def _score_like_or_bury():
    #从数据库中选择like_count或bury_count，再加1  
    mirrordb.set_score_value(web.input()['resource_id'], web.input()['scoretype'])
    return mirrordb.get_score_value(web.input()['resource_id'], web.input()['scoretype'])

class index():
    "显示主页面"
    def GET(self):
        return render.index(mirrordb.get_hot_types())
    
class recentview():
    "显示最近收录的检索页面"
    def GET(self):
        #处理分页
        params = web.input()
        curr_page  = params.page if hasattr(params, 'page') else 1
        offset = (int(curr_page) - 1) * perpage
        
        results = mirrordb.get_recent_records(offset)
        #计算一共有多少页
        pages = recent_count_limit / perpage
        #上一页/下一页
        lastpage = int(curr_page) - 1
        nextpage = int(curr_page) + 1
    
        page_list=[]
        total = pages
        for p in range(0,10):
            page_list.append(p + int(curr_page))
            
        return render.view(results, page_list, total, lastpage, nextpage)
    
    def POST(self):
        try:
            return _score_like_or_bury()
        except:
            pass    

class topview():
    "显示Top100的检索页面"
    def GET(self):
        results = mirrordb.get_top_records()
        return render.view(results, [], 0, 0, 0)
    
    def POST(self):
        try:
            return _score_like_or_bury()
        except:
            pass
        
 
class searchview():
    "显示搜索结果页"
    def GET(self):
        search_type = web.input().searchtype
        search_name = web.input().wd 
        results = mirrordb.search_all_resource(resource_type=search_type, name=search_name)
        return render.view(results, [], 0, 0, 0)
    
    def POST(self):
        try:
            return _score_like_or_bury()
        except:
            pass    

class typeview():
    "根据传入的url决定检索的类别，如访问toptpb/Audio/Music，则表示检索/Audio/Music项"
    def GET(self):
        urltype_str = web.ctx.path
        urltypes = urltype_str.split('/')[2:]
        typeL1 = urltypes[0]
        typeL2 = (len(urltypes) > 1) and urltypes[1] or None
        
        #hack手段，因为 这一分类下有反斜杠
        if(typeL2 == "IOS (iPad"):
            typeL2 = "IOS (iPad/iPhone)"

        #如果url中有'_'符号，替换为空格
        typeL1 = typeL1.replace('_', ' ')
        if typeL2:
            typeL2 = typeL2.replace('_', ' ')

        #处理分页
        params = web.input()
        curr_page  = params.page if hasattr(params, 'page') else 1
        offset = (int(curr_page) - 1) * perpage
        
        results, count = mirrordb.get_top_records(typeL1, typeL2, offset)
        #计算一共有多少页
        pages = count / perpage
        #上一页/下一页
        lastpage = int(curr_page) - 1
        nextpage = int(curr_page) + 1
    
        page_list=[]
        total = pages
        for p in range(0,10):
            page_list.append(p + int(curr_page))
            
        return render.view(results, page_list, total, lastpage, nextpage, typeL1, typeL2)
    
    def POST(self):
        try:
            return _score_like_or_bury()
        except:
            pass
    
class resource_info():
    "根据传入的resource_info_id检索资源信息"
    def GET(self):
        try:
            resource_info_id_str = web.ctx.path
            resource_info_id = int(resource_info_id_str.split('/')[2])
            result = mirrordb.get_extern_info(resource_info_id)
            return render.resource_info(result[0])
        except:
            return render.error("没有找到您要的信息，我们会尽快录入", "/")
        
class resource_group():
    "根据传来的resource_info_id检索资源的下载信息"
    def GET(self):
        try:
            resource_info_id_str = web.ctx.path
            resource_info_id = int(resource_info_id_str.split('/')[2])
            results = mirrordb.get_resource_group(resource_info_id) 
            return render.view(results, [], 0, 0, 0) 
        except:
            return render.error("没有找到您要的信息，我们会尽快录入", "/")    
        
    def POST(self):
        try:
            return _score_like_or_bury()
        except:
            pass                 
            
class simpletpb_help():
    
    def GET(self):
        "显示help页面"
        return render.help()

if __name__ == '__main__':
    topview.GET()
