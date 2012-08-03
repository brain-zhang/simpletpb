#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from utils import fetchtpb
from config.settings import render
from config.settings import alldbname

class daemon_fetch():
    "抓取功能"
    
    urllist = []
    dbname = alldbname

    def GET(self):
        return render.daemon('等待抓取完毕')

    def POST(self):
        del self.urllist[:]
        startURL = web.input().startURL
        if not startURL.endswith('/'):
            #格式化地址
            startURL = startURL + '/'

        if startURL.find('browse') > 0:
            self.dbname = alldbname
            for i in range(100):
                self.urllist.append(startURL + str(i) + '/3/')
        elif startURL.find('top') > 0:
            self.dbname = alldbname
            if startURL.endswith('top/'):
                self.urllist = fetchtpb.get_topURL(startURL)
            else:
                self.urllist.append(startURL)
        else:
            return render.error('输入URL错误，只接受browse页面及top页面', None)

        print self.urllist, self.dbname

        for url in self.urllist:
            fetchtpb.fetch(url, self.dbname)
        return render.daemon('抓取完毕')
