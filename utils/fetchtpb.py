#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from getopt import *
import sys
from BeautifulSoup import BeautifulSoup
from config.settings import util_db
from config.settings import hotrank_tpb_weighted, hotrank_top_weighted

from models import mirrordb
from config.settings import alldbname

def get_topURL(startURL):
    "获取startURL页面上的所有链接，仅限于top页面"
    topfp = urllib2.urlopen(startURL)
    pattern = re.compile("top/[0-9]+")
    while True:
        s = topfp.read()
        if not s:
            break
        urls = pattern.findall(s)
        urls = ["http://labaia.ws/" + url for url in urls]
        topfp.close()
        return urls

def get_allURL(startURL):
    "获取startURL页面上的所有链接，仅限于browse页面"
    print startURL
    allfp = urllib2.urlopen(startURL)
    pattern = re.compile("browse/[0-9]+")
    s = allfp.read()
    urls = pattern.findall(s)
    urls = ["http://labaia.ws/" + url + '/' for url in urls]
    allfp.close()

    totalurls = []
    for url in urls:
        for i in range(100):
            for ii in range(2, 15):
                totalurls.append(url + str(i) + '/' + str(ii) + '/')
    return totalurls

def get_recent_url(begin, end, startURL = 'http://labaia.ws/recent/'):
    url_base = startURL
    urllist = []
    for i in range(begin, end - begin + 1):
        urllist.append(url_base + str(i))
    return urllist
    

def fetch(url, dbname = alldbname):
    """
        根据指定的url抓取资源信息，存到数据库中
        此页面必须是直接有链接的页面
    """ 
    try:
        doc = urllib2.urlopen(url, timeout=10)
    except:
        print 'open url Err, url:%s' % (url)
        return    
    try:
        soup = BeautifulSoup.BeautifulSoup(doc.read())
        souptrs = BeautifulSoup.BeautifulSoup(str(soup.findAll('tr'))) 
    except:
        print 'BeautifulSoup Err' 
        return
    
    for tr in souptrs.contents[2:]:
        if hasattr(tr, 'name'):
            #获取资源名称，类别，链接地址及大小
            i = 0
            try:
                acollect = tr.findAll('a')
                typeL1 = ''.join(acollect[0].contents)
                typeL2 = ''.join(acollect[1].contents)
                #改一下分类名
                if typeL2 == 'PC' and typeL1 == 'Games':
                    typeL2 = 'PC Games'
                name = ''.join(acollect[2].contents)
                magnet = acollect[3]['href']
                font = tr.findAll('font')
                sizelazy = ''.join(font[0].contents[0])
                #获取大小，不用费心看了，严重依赖于格式
                size = sizelazy[sizelazy.find('Size') + 5:sizelazy.find('iB') + 2].replace(ur'&nbsp;', '')
                
                #判定hotrank
                hotrank = hotrank_tpb_weighted
                if url.find('top') > 0:
                    hotrank += hotrank_top_weighted
                
                print "name:%s, typeL1:%s, typeL2:%s, size:%s" % (name, typeL1, typeL2, size)
                util_db.insert('all_resource', resource_name = name,
                                                 typeL1 = typeL1, typeL2 = typeL2, magnet = magnet, size = size, 
                                                 hotrank = hotrank, extern_info = 'False', language = 'EN', ed2k = '')
            except:
                i = i + 1
                print 'fetch resouce url Err, url:%s' % (url) 
                if i > 3:
                    break
                
#just for test                
def fetch_all(urllist, begin, end):
    for url in urllist:
        try:
            fetch(url, dbname=alldbname, begin=begin, end=end)
        except:
            print 'fetch err url:%s' % (url)
            continue

def fetch_recent(begin, end):
    for url in get_recent_url(begin, end):
        try:
            fetch(url, dbname=alldbname)
        except:
            print 'fetch err url:%s' % (url)
            continue

""""
抓取海盗湾
使用方法:
    python fetchtpb.py <begin> <end>
        海盗湾的资源总分类大概在100-700间，也就是你只能输入100-700间的范围
"""
if __name__ == '__main__':
    opts, args = getopt(sys.argv[1:], "limit=")
    print args[0], args[1]
#    fetch('http://labaia.ws/top/602')
#    startURL = 'http://labaia.ws/browse/'
#    urllist = get_allURL(startURL) 
    fetch_recent(int(args[0]), int(args[1]))

