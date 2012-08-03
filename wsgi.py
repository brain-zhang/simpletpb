#!/usr/bin/env python
# coding: utf-8
import web
from config.url import urls
from config.settings import render

#urls = ("/.*", "hello")
app = web.application(urls, globals())

def notfound():
    return web.notfound(render.error("Hi,这个页面掉入了宇宙的漩涡，二次纪元后才会重新出现...",'/'))

app.notfound = notfound


# But make this file runnable with Python for local dev mode
if __name__ == "__main__":
    app.run()
else:
    # Turn our web.py app into a WSGI app
    web.debug = False
    application = app.wsgifunc()
