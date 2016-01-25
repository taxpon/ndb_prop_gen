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
