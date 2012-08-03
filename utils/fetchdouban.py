#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import time
from xml.dom import minidom
import web

class CFetchDouban():
    """
        从豆瓣上抓取电影、音乐的评论及评分
    """
    
    _movie_info = {}
    _music_info = {}
    _book_info = {}
    
    database = "../database/tpbmirror.db"
    db = web.database(dbn='sqlite', db=database)   
    
    support_type = {'Audio':'http://api.douban.com/music/subjects',
                    'Movie':'http://api.douban.com/movie/subjects',
                    'Other':'http://api.douban.com/book/subjects'
                    }
    
    def __init__(self, resource_type):
        self.rtype = resource_type

    def _get_resource_by_name(self, name):
        #音乐(Audio)，电影(Movie)，书籍 (other)
        query_url = self.support_type[self.rtype] + '?q=' + name + '&max-results=1'
        try:
            self.rxml = minidom.parseString(urllib2.urlopen(query_url, timeout=10).read()) 
        except:
            print 'Search url failed, url:%s' % (query_url)
            
    def get_movie_info(self):
        try:
            real_xml_url = self.rxml.documentElement.getElementsByTagName('id')[0].childNodes[0].data
            doc = urllib2.urlopen(real_xml_url, timeout=10).read()
            real_xml_dom = minidom.parseString(doc).documentElement
    
            #获取信息
            db_attribute_list = real_xml_dom.getElementsByTagName('db:attribute')
            for item in db_attribute_list:
                if item.getAttribute('name') == u'pubdate':
                    self._movie_info['pubdate'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'country':
                    self._movie_info['country'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'director':
                    self._movie_info['director'] = item.childNodes[0].data 
                elif item.getAttribute('name') == u'aka':
                    self._movie_info['aka'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'title':
                    self._movie_info['local_name'] = item.childNodes[0].data                       
    
            try:
                self._movie_info['summary'] = real_xml_dom.getElementsByTagName('summary')[0].childNodes[0].data
                self._movie_info['doubanURL'] = real_xml_dom.getElementsByTagName('link')[1].getAttribute('href')
                self._movie_info['imgURL'] = real_xml_dom.getElementsByTagName('link')[2].getAttribute('href')
                self._movie_info['rating'] = real_xml_dom.getElementsByTagName('gd:rating')[0].getAttribute('average')
            except:
                print 'get movie info Err, url:%s' % (real_xml_url)
                return None

            return self._movie_info
        except:
            print "Err, Don't find the movie"
            return None
        
    def fetch_movie_info(self):
        res = self.db.select('all_resource', where='is_spider="False" and extern_info="False" and typeL2="TV shows" or typeL2="Movies" and extern_info="False"').list()
        #res = db.query('select * from allsource where allsource.resource_id not in (select resource_id from doubaninfo) and typeL1="Video" and typeL2="Movies" or typeL2="TV shows"')
        for item in res:
            if self.db.select('resource_info', where='resource_id = "' + str(item['resource_id']) + '"'):
                continue;
            name = item['resource_name']
            #pattern = re.compile(r'\w{4,}(?=(\-|\[|1080p|BDRip|\(HD|\(\d+|\(720|TS|DvDRip|720p)*)')
            #match = pattern.match(name) and pattern.match(name).group() or name
            #print match
            self._get_resource_by_name(name)
            movie_info = self.get_movie_info()
            if movie_info:
                try:
                    print movie_info
                    resource_info_id = self.db.insert('resource_info', resource_id=item['resource_id'], typeL1='Video',
                              pubdate=movie_info['pubdate'], summary=movie_info['summary'], country=movie_info['country'],
                              director=movie_info['director'], aka=movie_info['aka'], local_name=movie_info['local_name'], sourceURL=movie_info['doubanURL'],
                              imgURL=movie_info['imgURL'], rating=float(movie_info['rating']))
                    self.db.query('update all_resource set hotrank=hotrank +' + str(float(movie_info['rating']) * 10) + ', extern_info="True", resource_info_id=' + str(resource_info_id) +' where resource_id==' + str(item['resource_id']))
                except:           
                    print 'Err, insert db failed' 
                    pass
            self.db.query('update all_resource set is_spider="True" where resource_id==' + str(item['resource_id']))
            time.sleep(10)
    
    def _get_music_info(self):
        try:
            real_xml_url = self.rxml.documentElement.getElementsByTagName('id')[0].childNodes[0].data
            doc = urllib2.urlopen(real_xml_url, timeout=10).read()
            real_xml_dom = minidom.parseString(doc).documentElement

            #获取信息
            db_attribute_list = real_xml_dom.getElementsByTagName('db:attribute')
            for item in db_attribute_list:
                if item.getAttribute('name') == u'pubdate':
                    self._music_info['pubdate'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'country':
                    self._music_info['country'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'director':
                    self._music_info['director'] = item.childNodes[0].data 
                elif item.getAttribute('name') == u'aka':
                    self._music_info['aka'] = item.childNodes[0].data     
                elif item.getAttribute('name') == u'title':
                    self._music_info['local_name'] = item.childNodes[0].data                                  

            try:
                self._music_info['summary'] = real_xml_dom.getElementsByTagName('summary')[0].childNodes[0].data
                self._music_info['doubanURL'] = real_xml_dom.getElementsByTagName('link')[1].getAttribute('href')
                self._music_info['imgURL'] = real_xml_dom.getElementsByTagName('link')[2].getAttribute('href')
                self._music_info['rating'] = real_xml_dom.getElementsByTagName('gd:rating')[0].getAttribute('average')
            except:
                print 'get movie info Err, url:%s' % (real_xml_url)
                return None
    
            return self._music_info
        except:
            print "Err, Don't find the music"
            return None
 
    def fetch_music_info(self):
        res = self.db.select('all_resource', where='is_spider="False" and typeL2="Music" and extern_info="False"').list()
        #res = db.query('select * from allsource where allsource.resource_id not in (select resource_id from doubaninfo) and typeL1="Video" and typeL2="Movies" or typeL2="TV shows"')
        for item in res:
            if self.db.select('resource_info', where='resource_id = "' + str(item['resource_id']) + '"'):
                continue;
            name = item['resource_name']
            self._get_resource_by_name(name)
            music_info = self._get_music_info()
            if music_info:
                try:
                    print music_info
                    resource_info_id = self.db.insert('resource_info', resource_id=item['resource_id'], typeL1='Audio',
                              pubdate=music_info['pubdate'], summary=music_info['summary'], country=music_info['country'],
                              director=music_info['director'], aka=music_info['aka'], local_name=music_info['local_name'], sourceURL=music_info['doubanURL'],
                              imgURL=music_info['imgURL'], rating=float(music_info['rating']))
                    self.db.query('update all_resource set hotrank=hotrank +' + str(float(music_info['rating']) * 10) + ', extern_info="True", resource_info_id=' + str(resource_info_id) + ' where resource_id==' + str(item['resource_id']))
                except:           
                    print 'Err, insert db failed' 
                    pass
            self.db.query('update all_resource set is_spider="True" where resource_id==' + str(item['resource_id']))
                
            time.sleep(10)

if __name__ == '__main__':
    movie = CFetchDouban('Movie')
    print movie.fetch_movie_info()
    
