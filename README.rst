Django-Cache-URL
~~~~~~~~~~~~~~~~

.. image:: https://secure.travis-ci.org/ghickman/django-cache-url.png?branch=master
   :target: http://travis-ci.org/ghickman/django-cache-url

This simple Django utility allows you to utilize the
`12factor <http://www.12factor.net/backing-services>`_ inspired
``CACHE_URL`` environment variable to configure your Django application.

This was built with inspiration from rdegges'
`django-heroku-memcacheify <https://github.com/rdegges/django-heroku-memcacheify>`_
as a way to use CACHE_URL in apps that aren't necessarily hosted on Heroku.

The internals borrow heavily from kennethreitz's
`dj-database-url <https://github.com/kennethreitz/dj-database-url>`_.


Supported caches
----------------

Support currently exists for Local-memory, database, file, memcached (including
pymemcached and djangopylibmc), redis (including hiredis).

Installation
------------
Installation is simple too::

    $ pip install django-cache-url

Usage
-----
Configure your cache in ``settings.py`` from ``CACHE_URL``::

    CACHES = {'default': django_cache_url.config()}

Defaults to local memory cache if ``CACHE_URL`` isn't set.

Parse an arbitrary Cache URL::

    CACHES = {'default': django_cache_url.parse('memcache://...')}


URL schema
----------

* locmem (default): ``'locmem://[NAME]'``
* db: ``'db://TABLE_NAME'``
* dummy: ``'dummy://'``
* file: ``'file:///PATH/TO/FILE'``
* memcached: ``'memcached://HOST:PORT'`` [#memcache]_
* pymemcached: ``'pymemcached://HOST:PORT'`` For use with the `python-memcached`_ library. Useful if you're using Ubuntu <= 10.04.
* djangopylibmc: ``'djangopylibmc://HOST:PORT'`` For use with SASL based setups such as Heroku.
* redis: ``'redis://[USER:PASSWORD@]HOST:PORT[:DB]'`` or ``'redis:///PATH/TO/SOCKET[:DB]'`` For use with `django-redis`_.
* hiredis ``'hiredis://[USER:PASSWORD@]HOST:PORT[:DB]'`` or ``'hiredis:///PATH/TO/SOCKET[:DB]'`` For use with django-redis library using HiredisParser.

All cache urls support optional cache arguments by using a query string, e.g.: ``'memcached://HOST:PORT?key_prefix=site1'``. See the Django `cache arguments documentation`_.

.. [#memcache] To specify multiple instances, separate the the ``HOST:PORT``` pair
               by commas, e.g: ``'memcached://HOST1:PORT1,HOST2:PORT2``

.. _django-redis: https://github.com/niwibe/django-redis
.. _python-memcached: https://github.com/linsomniac/python-memcached
.. _cache arguments documentation: https://docs.djangoproject.com/en/dev/topics/cache/#cache-arguments
