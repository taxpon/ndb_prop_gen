# -*- coding: utf-8 -*-

from common import Indent


class Arg(object):

    def __init__(self, name, prop_type, default):
        self.name = name
        self.prop_type = prop_type
        self.default = None

        if prop_type.lower() == "string":
            if len(default) == 0:
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

        return "{name} = ndb.{prop_type}Property({default_state})".format(
            name=self.name,
            prop_type=self.prop_type,
            default_state=default_state
        )

    @property
    def format_model_args(self):
        return "{} = "
