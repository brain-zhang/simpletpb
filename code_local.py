#!/usr/bin/env python
# coding: utf-8
from config.url import urls
from config.settings import render
import web

app = web.application(urls, globals())

def notfound():
    return web.notfound(render.error("Hi,这个页面掉入了宇宙的漩涡，二次纪元后才会重新出现...", '/'))

app.notfound = notfound

if __name__ == "__main__":
    app.run()
