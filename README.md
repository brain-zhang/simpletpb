simpletpb Introduction
=====================

Author
----------------
This project was created and lead by memorybox <memoryboxes@gmail.com>.

About simpletpb
----------------

python + webpy搭建的爬虫，用于镜像海盗湾。 目前运行在sae上。

http://simpletpbmirror.sinaapp.com/

这是初学Python时的习作。采用web.py，定期爬取海盗湾的资源，并从豆瓣上抓取相应的资源信息匹配。可运行于sae及dotcloud平台上。

部署
------------

执行 `script/app_simpletpbmirror.sql`，在sae mysql中生成需要的表；修改config.yaml，设置自动抓取的时间；在sae中开启memcache。OK


License
------------

simpletpb is released under BSD license.

