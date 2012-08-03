#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import db
from config.settings import render
from utils import scheming


class testdb():
    
    def GET(self):
        db.insert('top', resource_name=u'MagicZhang', typeL1='movie', typeL2='kongfu', magnet='zz', size='10B')


class testfetchtop():
    
    def GET(self):
        scheming.scheming_fetch_tpb_top()

class testfetchall():

    def GET(self):
        scheming.scheming_fetch_tpb_all()

if __name__ == '__main__':
    a = testfetchall()
    a.GET()
