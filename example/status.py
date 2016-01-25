# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

__all__ = ["Status", "StatusModel", "StatusProperty", "LocalStatusProperty"]


class Status(object):
    def __init__(self, unique="", status_code=None, name=None, is_done=False, updated=None):
        self._unique = unique
        self._status_code = status_code
        self._name = name
        self._is_done = is_done
        self._updated = updated

    @property
    def unique(self):
        return self._unique

    @property
    def status_code(self):
        return self._status_code

    @property
    def name(self):
        return self._name

    @property
    def is_done(self):
        return self._is_done

    @property
    def updated(self):
        return self._updated

    def _prepare_for_put(self):
        pass

    def _has_repeated(self):
        pass

    def _to_dict(self):
        pass


class StatusModel(ndb.Model):
    unique = ndb.StringProperty(default="")
    status_code = ndb.IntegerProperty()
    name = I18nStringProperty()
    is_done = ndb.BooleanProperty(default=False)
    updated = ndb.DateTimeProperty()


class StatusProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(StatusProperty, self).__init__(StatusModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Status)

    def _to_base_type(self, value):
        return StatusModel(
            unique=value.unique,
            status_code=value.status_code,
            name=value.name,
            is_done=value.is_done,
            updated=value.updated,
        )

    def _from_base_type(self, value):
        return Status(
            unique=value.unique,
            status_code=value.status_code,
            name=value.name,
            is_done=value.is_done,
            updated=value.updated,
        )


class LocalStatusProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(LocalStatusProperty, self).__init__(StatusModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Status)

    def _to_base_type(self, value):
        return StatusModel(
            unique=value.unique,
            status_code=value.status_code,
            name=value.name,
            is_done=value.is_done,
            updated=value.updated,
        )

    def _from_base_type(self, value):
        return Status(
            unique=value.unique,
            status_code=value.status_code,
            name=value.name,
            is_done=value.is_done,
            updated=value.updated,
        )
