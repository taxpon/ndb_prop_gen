# -*- coding: utf-8 -*-

from common import Indent


def find_prop_type(type_name):

    no_fuzzy = ("float", "text", "blob", "date", "key", "user", "structured", "json", "pickle", "generic", "computed")
    for name in no_fuzzy:
        if type_name.lower() == name:
            return "ndb.{}".format(name.capitalize())

    fuzzy = (
        (("integer", "int"), "Integer"),
        (("boolean", "bool"), "Boolean"),
        (("string", "str"), "String"),
        (("datetime", ), "DateTime"),
        (("geopt", "geo"), "GeoPt"),
        (("blobkey", ), "BlobKey"),
        (("localstructured", "ls"), "LocalStructured"),
    )
    for name in fuzzy:
        if type_name.lower() in name[0]:
            return "ndb.{}".format(name[1])

    return type_name


class Arg(object):

    def __init__(self, name, prop_type, default):
        self.name = name
        self.prop_type = find_prop_type(prop_type)
        self.default = None

        if self.prop_type == "ndb.String":
            if not default or len(default) == 0:
                self.default = "\"\""

        if self.default is None:
            self.default = default

    @property
    def class_arg(self):
        return "{}={}".format(self.name, self.default)

    @property
    def class_init(self):
        return "self._{name} = {name}".format(name=self.name)

    @property
    def class_property(self):
        return "    @property\n" \
               "    def {name}(self):\n" \
               "        return self._{name}\n".format(name=self.name)

    @property
    def model_init(self):
        default_state = ""
        if self.default is not None:
            default_state = "default={}".format(self.default)

        return "{name} = {prop_type}Property({default_state})".format(
            name=self.name,
            prop_type=self.prop_type,
            default_state=default_state
        )
