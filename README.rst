Google Appengine ndb Property Generator
=======================================

.. image:: https://travis-ci.org/taxpon/ndb_prop_gen.svg
    :target: https://travis-ci.org/taxpon/ndb_prop_gen

.. image:: https://coveralls.io/repos/github/taxpon/ndb_prop_gen/badge.svg?branch=master
    :target: https://coveralls.io/github/taxpon/ndb_prop_gen?branch=master

Google Appengine ndb Property Generator written in python. You can convert json data into your custom ndb property by this library.


What is this?
-------------
Simple generator of `ndb Property Subclass <https://cloud.google.com/appengine/docs/python/ndb/subclassprop>`_. Using json to define the property of the class.

Source json sample
~~~~~~~~~~~~~~~~~~
.. code-block:: javascript

    {
        "name": "book",
        "class": "Book",
        "props": [
            {
                "name": "title",
                "type": "String",
                "default": ""
            },
            {
                "name": "author",
                "type": "String",
                "default": ""
            },
            {
                "name": "published",
                "type": "DateTime",
                "default": null
            },
            {
                "name": "price",
                "type": "Float",
                "default": 10.0
            },
            {
                "name": "read",
                "type": "Bool",
                "default": false
            }
        ]
    }


Generated python sample
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # -*- coding: utf-8 -*-
    from google.appengine.ext import ndb

    __all__ = ["Book", "BookModel", "BookProperty", "LocalBookProperty"]


    class Book(object):
        def __init__(self, title="", author="", published=None, price=10.0, read=False):
            self._title = title
            self._author = author
            self._published = published
            self._price = price
            self._read = read

        @property
        def title(self):
            return self._title

        @property
        def author(self):
            return self._author

        @property
        def published(self):
            return self._published

        @property
        def price(self):
            return self._price

        @property
        def read(self):
            return self._read

        def _prepare_for_put(self):
            pass

        def _has_repeated(self):
            pass

        def _to_dict(self):
            pass


    class BookModel(ndb.Model):
        title = ndb.StringProperty(default="")
        author = ndb.StringProperty(default="")
        published = ndb.DateTimeProperty()
        price = ndb.FloatProperty(default=10.0)
        read = ndb.BooleanProperty(default=False)


    class BookProperty(ndb.StructuredProperty):
        def __init__(self, **kwds):
            super(BookProperty, self).__init__(BookModel, **kwds)

        def _validate(self, value):
            assert isinstance(value, Book)

        def _to_base_type(self, value):
            return BookModel(
                title=value.title,
                author=value.author,
                published=value.published,
                price=value.price,
                read=value.read,
            )

        def _from_base_type(self, value):
            return Book(
                title=value.title,
                author=value.author,
                published=value.published,
                price=value.price,
                read=value.read,
            )


    class LocalBookProperty(ndb.StructuredProperty):
        def __init__(self, **kwds):
            super(LocalBookProperty, self).__init__(BookModel, **kwds)

        def _validate(self, value):
            assert isinstance(value, Book)

        def _to_base_type(self, value):
            return BookModel(
                title=value.title,
                author=value.author,
                published=value.published,
                price=value.price,
                read=value.read,
            )

        def _from_base_type(self, value):
            return Book(
                title=value.title,
                author=value.author,
                published=value.published,
                price=value.price,
                read=value.read,
            )


Please see the `example <https://github.com/taxpon/ndb_prop_gen/tree/master/example>`_ directory for more examples.

Usage
-----

1. Install ndb_prop_gen via pip

.. code-block:: bash

    pip install ndb_prop_gen


2. Call generate method


* via command line


.. code-block:: bash

    ndb_prop_gen test.json



* via python code


.. code-block:: python

    import ndb_prop_gen as npg  # noqa

    # filename is the json's filename
    npg.generate(filename)



LICENSE
-------
MIT
