# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import environ
import unittest

import django_cache_url


class TestDatabaseCache(unittest.TestCase):
    backend = 'django.core.cache.backends.db.DatabaseCache'

    def test_url(self):
        url = 'db://super_caching_table'
        config = django_cache_url.parse(url)
        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'super_caching_table')

    def test_url_args(self):
        url = 'db://super_caching_table?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'super_caching_table')
        self.assertEqual(config['KEY_PREFIX'], 'site1')


class TestDummyCache(unittest.TestCase):
    backend = 'django.core.cache.backends.dummy.DummyCache'

    def test_url(self):
        url = 'dummy://'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '')

    def test_url_args(self):
        url = 'dummy://?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '')
        self.assertEqual(config['KEY_PREFIX'], 'site1')


class TestFileCache(unittest.TestCase):
    backend = 'django.core.cache.backends.filebased.FileBasedCache'

    def test_url(self):
        url = 'file:///path/to/file'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '/path/to/file')

    def test_url_args(self):
        url = 'file:///path/to/file?timeout=5'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '/path/to/file')
        self.assertEqual(config['TIMEOUT'], '5')


class TestLocMemCache(unittest.TestCase):
    backend = 'django.core.cache.backends.locmem.LocMemCache'

    def test_url(self):
        url = 'locmem://'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '')

    def test_url_args(self):
        url = 'locmem://?timeout=5'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '')
        self.assertEqual(config['TIMEOUT'], '5')

    def test_url_with_name(self):
        url = 'locmem://unique-snowflakes'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unique-snowflakes')

    def test_url_with_name_args(self):
        url = 'locmem://unique-snowflakes?timeout=5'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unique-snowflakes')
        self.assertEqual(config['TIMEOUT'], '5')


class TestMemcachedCache(unittest.TestCase):
    backend = 'django.core.cache.backends.memcached.PyLibMCCache'

    def test_url(self):
        url = 'memcached://127.0.0.1:11211'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '127.0.0.1:11211')
        self.assertEqual(config.get('KEY_PREFIX'), None)

    def test_url_args(self):
        url = 'memcached://127.0.0.1:11211?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '127.0.0.1:11211')
        self.assertEqual(config.get('KEY_PREFIX'), 'site1')

    def test_url_multiple_hosts(self):
        url = 'memcached://127.0.0.1:11211,192.168.0.100:11211?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], '127.0.0.1:11211;192.168.0.100:11211')
        self.assertEqual(config.get('KEY_PREFIX'), 'site1')

    def test_socket(self):
        url = 'memcached:///path/to/socket'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unix:/path/to/socket')
        self.assertEqual(config.get('KEY_PREFIX'), None)

    def test_socket_args(self):
        url = 'memcached:///path/to/socket?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unix:/path/to/socket')
        self.assertEqual(config['KEY_PREFIX'], 'site1')


class TestRedisCache(unittest.TestCase):
    backend = 'redis_cache.cache.RedisCache'

    def test_url(self):
        url = 'redis://localhost:6379'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'localhost:6379:0')
        self.assertEqual(config.get('OPTIONS'), None)
        self.assertEqual(config.get('KEY_PREFIX'), None)

    def test_url_password(self):
        url = 'redis://user:pass@localhost:6379/'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'localhost:6379:0')
        self.assertEqual(config['OPTIONS']['PASSWORD'], 'pass')

    def test_url_args(self):
        url = 'redis://user:pass@localhost:6379:1/?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'localhost:6379:1')
        self.assertEqual(config['OPTIONS']['PASSWORD'], 'pass')
        self.assertEqual(config['KEY_PREFIX'], 'site1')

    def test_socket(self):
        url = 'redis:///path/to/socket'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unix:/path/to/socket:0')
        self.assertEqual(config.get('OPTIONS'), None)
        self.assertEqual(config.get('KEY_PREFIX'), None)

    def test_socket_args(self):
        url = 'redis:///path/to/socket:1?key_prefix=site1'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unix:/path/to/socket:1')
        self.assertEqual(config.get('OPTIONS'), None)
        self.assertEqual(config['KEY_PREFIX'], 'site1')


class TestHiredisCache(unittest.TestCase):
    backend = 'redis_cache.cache.RedisCache'

    def test_url(self):
        url = 'hiredis://localhost:6379/'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'localhost:6379:0')
        self.assertEqual(config.get('KEY_PREFIX'), None)
        self.assertEqual(config['OPTIONS']['PARSER_CLASS'],
                      'redis.connection.HiredisParser')

    def test_socket(self):
        url = 'hiredis:///path/to/socket'
        config = django_cache_url.parse(url)

        self.assertEqual(config['BACKEND'], self.backend)
        self.assertEqual(config['LOCATION'], 'unix:/path/to/socket:0')
        self.assertEqual(config.get('KEY_PREFIX'), None)
        self.assertEqual(config['OPTIONS']['PARSER_CLASS'],
                      'redis.connection.HiredisParser')


class TestConfigOptions(unittest.TestCase):
    def setUp(self):
        try:
            del environ['CACHE_URL']
        except KeyError:
            pass

    def test_env_var(self):
        environ['CACHE_URL'] = 'memcached://127.0.0.1:11211/'
        backend = 'django.core.cache.backends.memcached.PyLibMCCache'
        config = django_cache_url.config()

        self.assertEqual(config['BACKEND'], backend)
        self.assertEqual(config['LOCATION'], '127.0.0.1:11211')

    def test_setting_env_var_name(self):
        environ['HERP'] = 'memcached://127.0.0.1:11211/'
        backend = 'django.core.cache.backends.memcached.PyLibMCCache'
        config = django_cache_url.config(env='HERP')

        self.assertEqual(config['BACKEND'], backend)
        self.assertEqual(config['LOCATION'], '127.0.0.1:11211')


if __name__ == '__main__':
    unittest.main()
