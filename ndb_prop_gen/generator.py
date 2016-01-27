# -*- coding: utf-8 -*-

from error import JsonFormatError
from arg import Arg
from common import ind1
from common import ind2
from common import ind3


class _PropGen(object):
    def __init__(self, conf):
        self.filename = ""
        self.class_list = []
        self.arg_list = []
        self.conf = conf
        self.contents = ""


class Header(_PropGen):
    def create_header(self):
        t = '# -*- coding: utf-8 -*-\n'
        t += 'from google.appengine.ext import ndb\n\n'
        t += '__all__ = ["{}", "{}", "{}", "{}"]\n\n\n'.format(
            self.class_list[0], self.class_list[1], self.class_list[2], self.class_list[3]
        )
        return "# -*- coding: utf-8 -*-\n" +\
               "from google.appengine.ext import ndb\n\n" +\
               '__all__ = ["{}", "{}", "{}", "{}"]\n\n\n'.format(
                   self.class_list[0],
                   self.class_list[1],
                   self.class_list[2],
                   self.class_list[3]
               )


class BaseClass(_PropGen):
    def _create_base_class_args(self):
        return ", ".join(map(lambda x: x.class_arg, self.arg_list))

    def _create_base_class_init(self):
        return \
            ind1("def __init__(self, {args}):\n".format(args=self._create_base_class_args())) +\
            reduce(lambda _t, x: _t + ind2("{}\n").format(x.class_init), self.arg_list, "") +\
            "\n"

    def _create_base_class_property(self):
        return reduce(lambda t, x: t + "{}\n".format(x.class_property), self.arg_list, "")

    def _create_base_class_prepare_for_put(self):
        return ind1("def _prepare_for_put(self):\n") + ind2("pass\n\n")

    def _create_base_class_has_repeated(self):
        return ind1("def _has_repeated(self):\n") + ind2("pass\n\n")

    def _create_base_class_to_dict(self):
        return ind1("def _to_dict(self):\n") + ind2("pass\n\n") + ind1("to_dict = _to_dict\n\n")

    def create_base_class(self):
        return "class {}(object):\n".format(self.class_list[0]) +\
               self._create_base_class_init() +\
               self._create_base_class_property() +\
               self._create_base_class_prepare_for_put() +\
               self._create_base_class_has_repeated() +\
               self._create_base_class_to_dict() +\
               "\n"


class BaseModel(_PropGen):
    def _create_base_model_init_props(self):
        return reduce(lambda t, x: t + ind1("{}\n".format(x.model_init)), self.arg_list, "")

    def create_base_model(self):
        return "class {}(ndb.Model):\n".format(self.class_list[1]) +\
               self._create_base_model_init_props() +\
               "\n\n"


class StructuredProperty(_PropGen):
    def _create_sp_init(self, local=False):
        return \
            ind1("def __init__(self, **kwds):\n") +\
            ind2("super({name1}, self).__init__({name2}, **kwds)\n\n".format(
                name1=self.class_list[2] if not local else self.class_list[3],
                name2=self.class_list[1]
            ))

    def _create_sp_validate(self):
        return \
            ind1("def _validate(self, value):\n") +\
            ind2("assert isinstance(value, {})\n\n".format(self.class_list[0]))

    def _create_sp_to_base_type(self):
        t = ind1("def _to_base_type(self, value):\n")
        t += ind2("return {}(\n".format(self.class_list[1]))
        for arg in self.arg_list:
            t += ind3("{name}=value.{name},\n".format(name=arg.name))
        t += ind2(")\n\n")
        return t

    def _create_sp_from_base_type(self):
        t = ind1("def _from_base_type(self, value):\n")
        t += ind2("return {}(\n".format(self.class_list[0]))
        for arg in self.arg_list:
            t += ind3("{name}=value.{name},\n".format(name=arg.name))
        t += ind2(")\n\n")
        return t

    def create_structured_property(self, local=False):
        t = "class {name}(ndb.StructuredProperty):\n".format(
            name=self.class_list[2] if not local else self.class_list[3]
        )

        t += self._create_sp_init(local)
        t += self._create_sp_validate()
        t += self._create_sp_to_base_type()
        t += self._create_sp_from_base_type()
        t += "\n"
        return t


class PropertyGenerator(Header, BaseClass, BaseModel, StructuredProperty):
    def validate(self):
        tl_attr = ("name", "class", "props")
        for attr in tl_attr:
            if attr not in self.conf:
                raise JsonFormatError("{} is required.".format(attr))

        self.filename = "{}.py".format(self.conf["name"])
        self.class_list = [
            "{}".format(self.conf["class"]),
            "{}Model".format(self.conf["class"]),
            "{}Property".format(self.conf["class"]),
            "Local{}Property".format(self.conf["class"]),
        ]

        for prop in self.conf["props"]:
            self.arg_list.append(Arg(prop["name"], prop["type"], prop["default"]))

    def create_contents(self):
        self.contents = self.create_header()
        self.contents += self.create_base_class()
        self.contents += self.create_base_model()
        self.contents += self.create_structured_property()
        self.contents += self.create_structured_property(local=True)
        self.contents = self.contents[:-2]

    def write(self):
        with open(self.filename, "w") as f:
            f.write(self.contents)
