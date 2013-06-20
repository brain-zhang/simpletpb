#! /usr/bin/env python
#coding=utf-8
from config.url import urls
from config.settings import render
import os
import web
import sae

def notfound():
    return web.notfound(render.error("Hi,不要乱推门，乖 ...",'/'))

app = web.application(urls, globals())
app.notfound = notfound
application = sae.create_wsgi_app(app.wsgifunc())    
