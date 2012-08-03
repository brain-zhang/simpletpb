#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import time
from getopt import *
import sys
from BeautifulSoup import BeautifulSoup
from config.settings import hotrank_oabt_weighted
from config.settings import util_db


class CFetchoabt():
    """
            抓取oabt的资源
            使用方法:
            python fetchoabt.py
             因为oabt每天的更新不多，每天定时运行一次就行了
    """
    
    _movie_info = {}
    
    def __init__(self, url):
        self.url = url

    def magic_fetch_and_insert(self):

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-cn,zh;q=0.5',
                   'Connection': 'keep-alive',
                   'Cookie': '37cs_user=37cs13650143833; Hm_lvt_ce396a90f02f136fc25a1bfc9138c834=1331695718366; 37cs_show=1%2C26; PHPSESSID=r3okpuu9o47bt9u32epkii08i2; 37cs_pidx=4; Hm_lpvt_ce396a90f02f136fc25a1bfc9138c834=1331695718366',
                   'Host': 'oabt.org',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'}
        req = urllib2.Request(self.url, headers=headers)
        doc = urllib2.urlopen(req, timeout = 10).read()

        page_soup = BeautifulSoup.BeautifulSoup(doc)
        tables = page_soup.findAll('table', cellspacing="0")
        tables = tables[3].contents[4:]
        for tr in tables:
            size = tr.contents[1].contents[9].contents[0] #size
            typeL2 = tr.contents[1].contents[1].contents[0].contents[0] #type
            typeL1 = 'Video'
            if typeL2 == u'泰剧':
                typeL2 = 'PC Games'
                typeL1 = 'Games'
            resource_name = tr.contents[1].contents[3].contents[0].contents[0] #name
            magnet = tr.contents[1].contents[5].contents[1]['href'] #magnet
            ed2k = tr.contents[1].contents[5].contents[2]['ed2k'] #ed2k
            try:
                util_db.insert('all_resource', resource_name = resource_name,
                                                 typeL1 = typeL1, typeL2 = typeL2, magnet = magnet, size = size, 
                                                 hotrank = hotrank_oabt_weighted, extern_info = 'False', language = 'CH', ed2k = ed2k)
            except:
                print "insert Err"
        print 'OK'

""""
抓取oabt
使用方法:
    python fetchoabt.py <begin> <end>
                                                                开始页     结束页
"""
if __name__ == '__main__':
    opts, args = getopt(sys.argv[1:], "limit=")
    print args[0], args[1]
    urllist = ['http://oabt.org/index.php?page=' + str(i) for i in range(int(args[0]), int(args[1]) - int(args[0]) + 1)]
    for url in urllist:
        try:
            oabt = CFetchoabt(url)
            oabt.magic_fetch_and_insert()
            time.sleep(10)
        except:
            print "Err,url:%s" % (url)
            continue
            
        
