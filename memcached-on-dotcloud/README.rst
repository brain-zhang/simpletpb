Memcached On dotCloud
=====================

This recipe provides memcached for dotCloud.
While it will allow you to use memcached with your dotCloud app, it has
three caveats:

#. There is no support for authentication. Well, memcached itself `does
   not support authentication anyway <http://code.google.com/p/memcached/wiki/FAQ#How_does_memcached%27s_authentication_mechanisms_work?>`_,
   so this should not be a big surprise. If you need to secure access
   to your memcached, you need to subscribe to dotCloud's Enterprise Plan
   (at least for now). At some point, we will also provide recipes allowing
   secure operation under the Free and Pro plan.
#. The address of your memcached server won't show up in ``environment.json``.
   This limitation will soon be lifted; but meanwhile, you have to hardcode
   your memcached server address in your app.
#. As a consequence of the previous point, scaling is not officially
   supported. While you can get it to work with a few tricks, we recommend
   that you wait a bit for official scaled memcached support if you need it.

If this didn't deter you from using memcached on dotCloud, then read ahead!


How It Works
------------

It uses the ``custom`` service type, which allows custom package install.
It also uses the all-new "custom TCP port" feature to expose the memcached
port.


How To Use It (Standalone)
--------------------------

Just use our (un)patented Clone-And-DotCloud-Push method::

  git clone git://github.com/jpetazzo/memcached-on-dotcloud.git
  dotcloud push memcached memcached-on-dotcloud

At the end of the push, run ``dotcloud info memcached.memcached`` to see
the connection parameters::

  -   name: memcached
      url: tcp://memcached-myusername.dotcloud.com:12345

 

How To Use It (In Your App)
---------------------------

Add the ``dotcloud.yml`` supplied here to your own ``dotcloud.yml``.
Push as usual, and use ``dotcloud info`` at the end of the push to
see the host and port number to use to connect to your memcached
service. Enjoy!
