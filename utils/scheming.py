#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fetchtpb
from config.settings import alldbname

def scheming_fetch_tpb_top():
    "抓取Top100功能"

    startURL = 'http://labaia.ws/top/'
    urllist = fetchtpb.get_topURL(startURL)
    print urllist

    for url in urllist:
        fetchtpb.fetch(url)

def scheming_fetch_tpb_all():
    "抓取所有页面功能"

    startURL = 'http://labaia.ws/browse/'
    urllist = fetchtpb.get_allURL(startURL)

    for url in urllist:
        try:
            fetchtpb.fetch(url, alldbname)
        except:
            print 'fetch err url:%s' %(url)
            continue

class index():
    def GET(self):
        scheming_fetch_tpb_top()
        return 'OK'

    def POST(self):
        scheming_fetch_tpb_top()
        return 'OK'

if __name__ == '__main__':
    scheming_fetch_tpb_top()
