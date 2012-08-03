#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
 
import memcache
 
if __name__ == '__main__':
    mc = memcache.Client(['127.0.0.1:12000'],debug=0)
    mc.set("foo","bar")
    value = mc.get("foo")
    print value
