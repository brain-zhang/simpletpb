#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import web
from BeautifulSoup import BeautifulSoup
from getopt import *
import sys
import time

class CFetchmtime():
    """
            抓取时光网的影视信息
            使用方法:
            python fetchmtime.py <begin> <end>
            如:python fetchmtime.py 10000 20000
            是抓取编号为10000-20000间的影视信息
            时光网的电影编号从10001开始，结束编号大概超过了99999
    """
    
    def __init__(self, url):
        self.url = url
        database = "../database/tpbmirror.db"
        self.db = web.database(dbn='sqlite', db=database)

    def magic_fetch_and_insert(self):
#        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                   'Accept-Encoding': 'gzip, deflate',
#                   'Accept-Language': 'zh-cn,zh;q=0.5',
#                   'Connection': 'keep-alive',
#                   'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'}
#        req = urllib2.Request(self.url, headers=headers)
        doc = urllib2.urlopen(self.url, timeout=10).read()

        page_soup = BeautifulSoup.BeautifulSoup(doc)
        mtimeURL = self.url
        director= 'Unknown'
        pubdate = ''
        aka_name = ''
        country = 'Unknown'
        summary='Unknown'
        rating = 0
        imgURL=''
        eng_name=''
        
        try:
            main_div = page_soup.findAll(name='div',
                        attrs={'pan':'M08_Movie_Overview_Detail', 'pn':'M08_Movie_Overview'})
            aka_name = main_div[0].contents[1].contents[0]
            aka_name = aka_name.split('-')[0].strip()
        except:
            pass
        
        try:
            country = main_div[0].contents[3].contents[1].contents[1].contents[2].contents[0].replace('&nbsp', '')
        except:
            pass
            
        try:
            summary_div = page_soup.findAll(name='div', attrs={'class':'ml15 lh18 mr15'})
            summary = summary_div[0].contents[1].text
        except:
            pass
        
        try:
            rating_div = page_soup.findAll(name = 'dd', attrs={'id':'ratingLoadingRegion'})
            rating = rating_div[0].contents[1].contents[1].contents[1].text
        except:
            pass
        
        try:
            img_div = page_soup.findAll(name='img', attrs={'class':'movie_film_img fl'})
            imgURL = img_div[0]['src']
        except:
            pass
        
        try:
            director_div = page_soup.findAll(name='ul', attrs={'class':'lh20'})
            director = director_div[0].contents[1].contents[3].text
            pubdate = director_div[0].contents[7].contents[3].text
        except:
            pass
            
        try:    
            eng_name = page_soup.findAll(name='span', attrs={'class':'ml9 px24'})[0].text
        except:
            pass
                
        print aka_name, country, summary, imgURL, director, pubdate, eng_name
        resource_id = -1
        
#        try:
#            res = self.db.query(r'select * from all_resource where typeL2=="Movies" and resource_name like "%' + eng_name + '%"').list()
#            if res:
#                resource_id = res[0]['resource_id']
#        except:
#            pass
            
        self.db.insert('mtime_info', resource_id=resource_id, typeL1='Video', aka=aka_name, mtimeURL=mtimeURL, imgURL=imgURL, eng_name=eng_name,
                  rating=rating, country=country, summary=summary, pubdate=pubdate, director=director, source_site='mtime')
        

if __name__ == '__main__':
    opts, args = getopt(sys.argv[1:], "limit=")
    print args[0], args[1]
    urllist = ['http://movie.mtime.com/' + str(i) for i in range(int(args[0]), int(args[1]))]
    #urllist = ['http://movie.mtime.com/10001']
    for url in urllist:
        try:
            print url
            mtime = CFetchmtime(url)
            mtime.magic_fetch_and_insert()
        except:
            print "magic_fetch_Err."
          
#        print url
#        mtime = CFetchmtime(url)
#        mtime.magic_fetch_and_insert()       
