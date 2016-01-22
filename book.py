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


class BookModel(ndb.Model):
    title = ndb.StringProperty(default="")
    author = ndb.StringProperty(default="")
    published = ndb.DateTimeProperty()
    price = ndb.FloatProperty(default=10.0)
    read = ndb.BoolProperty(default=False)

