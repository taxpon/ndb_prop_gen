import unittest
from ndb_prop_gen.generator import _PropGen
from ndb_prop_gen.generator import PropertyGenerator
from ndb_prop_gen.error import JsonFormatError


class TestBase(unittest.TestCase):

    def setUp(self):
        self.sample = PropertyGenerator({
            "name": "person",
            "class": "Person",
            "props": [
                {
                    "name": "first_name",
                    "type": "str",
                    "default": ""
                },
                {
                    "name": "last_name",
                    "type": "str",
                    "default": ""
                },
                {
                    "name": "age",
                    "type": "int",
                    "default": 0
                }
            ]
        })
        self.sample.validate()

        self.error_sample = PropertyGenerator({
            "name": "person",
            "class": "Person"
        })

    def test_init(self):
        conf = "conf"
        pg = _PropGen(conf)
        self.assertEqual(pg.conf, conf)


class TestHeader(TestBase):

    def test_create_header(self):
        self.assertEqual(self.sample.create_header(),
                         """\
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

__all__ = ["Person", "PersonModel", "PersonProperty", "LocalPersonProperty"]


"""
                         )


class TestBaseClass(TestBase):
    def setUp(self):
        super(TestBaseClass, self).setUp()

    def test_create_args(self):
        self.assertEqual(
            self.sample._create_base_class_args(),
            "first_name=\"\", last_name=\"\", age=0"
        )

    def test_create_base_class_init(self):
        self.assertEqual(
            self.sample._create_base_class_init(),
            """\
    def __init__(self, first_name=\"\", last_name=\"\", age=0):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age\n
"""
        )

    def test_create_base_class_property(self):
        self.assertEqual(
            self.sample._create_base_class_property(),
            """\
    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def age(self):
        return self._age

"""
        )

    def test_create_base_class_prepare_for_put(self):
        self.assertEqual(
            self.sample._create_base_class_prepare_for_put(),
            """\
    def _prepare_for_put(self):
        pass

"""
        )

    def test_create_base_class_has_repeated(self):
        self.assertEqual(
            self.sample._create_base_class_has_repeated(),
            """\
    def _has_repeated(self):
        pass

"""
        )

    def test_create_base_class_to_dict(self):
        self.assertEqual(
            self.sample._create_base_class_to_dict(),
            """\
    def _to_dict(self):
        pass

"""
        )

    def test_create_base_class(self):
        self.assertEqual(
            self.sample.create_base_class(),
            """\
class Person(object):
    def __init__(self, first_name=\"\", last_name=\"\", age=0):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def age(self):
        return self._age

    def _prepare_for_put(self):
        pass

    def _has_repeated(self):
        pass

    def _to_dict(self):
        pass


"""
        )


class TestBaseModel(TestBase):
    def test_create_base_model_init_props(self):
        self.assertEqual(
            self.sample._create_base_model_init_props(),
            """\
    first_name = ndb.StringProperty(default=\"\")
    last_name = ndb.StringProperty(default=\"\")
    age = ndb.IntegerProperty(default=0)
"""
        )

    def test_create_base_model(self):
        self.assertEqual(
            self.sample.create_base_model(),
            """\
class PersonModel(ndb.Model):
    first_name = ndb.StringProperty(default=\"\")
    last_name = ndb.StringProperty(default=\"\")
    age = ndb.IntegerProperty(default=0)


"""
        )


class TestStructuredProperty(TestBase):
    def test_create_sp_init(self):
        self.assertEqual(
            self.sample._create_sp_init(),
            """\
    def __init__(self, **kwds):
        super(PersonProperty, self).__init__(PersonModel, **kwds)

"""
        )
        self.assertEqual(
            self.sample._create_sp_init(local=True),
            """\
    def __init__(self, **kwds):
        super(LocalPersonProperty, self).__init__(PersonModel, **kwds)

"""
        )

    def test_create_sp_validate(self):
        self.assertEqual(
            self.sample._create_sp_validate(),
            """\
    def _validate(self, value):
        assert isinstance(value, Person)

"""
        )

    def test_create_sp_to_base_type(self):
        self.assertEqual(
            self.sample._create_sp_to_base_type(),
            """\
    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

"""
        )

    def test_create_sp_from_base_type(self):
        self.assertEqual(
            self.sample._create_sp_from_base_type(),
            """\
    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

"""
        )

    def test_create_structured_property(self):
        self.assertEqual(
            self.sample.create_structured_property(),
            """\
class PersonProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(PersonProperty, self).__init__(PersonModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Person)

    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )


"""
        )
        self.assertEqual(
            self.sample.create_structured_property(local=True),
            """\
class LocalPersonProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(LocalPersonProperty, self).__init__(PersonModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Person)

    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )


"""
        )


class TestPropertyGenerator(TestBase):

    def test_validate_error(self):
        self.assertRaises(JsonFormatError, self.error_sample.validate)

    def test_create_contents(self):
        self.sample.create_contents()
        self.assertEqual(self.sample.contents,
                         """\
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

__all__ = ["Person", "PersonModel", "PersonProperty", "LocalPersonProperty"]


class Person(object):
    def __init__(self, first_name=\"\", last_name=\"\", age=0):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def age(self):
        return self._age

    def _prepare_for_put(self):
        pass

    def _has_repeated(self):
        pass

    def _to_dict(self):
        pass


class PersonModel(ndb.Model):
    first_name = ndb.StringProperty(default=\"\")
    last_name = ndb.StringProperty(default=\"\")
    age = ndb.IntegerProperty(default=0)


class PersonProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(PersonProperty, self).__init__(PersonModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Person)

    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )


class LocalPersonProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(LocalPersonProperty, self).__init__(PersonModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Person)

    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )
""")

    def test_write(self):
        from mock import mock_open, patch
        self.sample.create_contents()
        m_open = mock_open()
        with patch("__builtin__.open", m_open) as mock_file:
            self.sample.write()

        m_open.assert_called_once_with(self.sample.filename, "w")
        handle = m_open()
        handle.write.assert_called_once_with("""\
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

__all__ = ["Person", "PersonModel", "PersonProperty", "LocalPersonProperty"]


class Person(object):
    def __init__(self, first_name=\"\", last_name=\"\", age=0):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def age(self):
        return self._age

    def _prepare_for_put(self):
        pass

    def _has_repeated(self):
        pass

    def _to_dict(self):
        pass


class PersonModel(ndb.Model):
    first_name = ndb.StringProperty(default=\"\")
    last_name = ndb.StringProperty(default=\"\")
    age = ndb.IntegerProperty(default=0)


class PersonProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(PersonProperty, self).__init__(PersonModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Person)

    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )


class LocalPersonProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(LocalPersonProperty, self).__init__(PersonModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, Person)

    def _to_base_type(self, value):
        return PersonModel(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )

    def _from_base_type(self, value):
        return Person(
            first_name=value.first_name,
            last_name=value.last_name,
            age=value.age,
        )
""")


if __name__ == "__main__":
    unittest.main()
