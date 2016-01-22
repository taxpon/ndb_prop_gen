# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

__all__ = ["Book", "BookModel", "BookProperty", "LocalBookProperty"]


class Book(object):
        def __init__(self, title="", author="", published=None, price=10.0, read=False)
    self._title = title
    self._author = author
    self._published = published
    self._price = price
    self._read = read
