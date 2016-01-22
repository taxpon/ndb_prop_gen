# -*- coding: utf-8 -*-
import sys
import json

from error import JsonFormatError
from arg import Arg
from common import Indent


class PropertyGenerator(object):

    def __init__(self, conf):
        self.filename = ""
        self.class_list = []
        self.arg_list = []
        self.conf = conf

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

    def write(self):
        contents = '# -*- coding: utf-8 -*-\n'
        contents += 'from google.appengine.ext import ndb\n\n'
        contents += '__all__ = ["{}", "{}", "{}", "{}"]\n\n\n'.format(
            self.class_list[0], self.class_list[1], self.class_list[2], self.class_list[3]
        )

        # Class
        contents += 'class {}(object):\n'.format(self.class_list[0])
        contents += '{ind1}def __init__(self, {props}):\n'.format(
            props=", ".join(map(lambda x: x.class_arg, self.arg_list)),
            ind1=Indent(1)
        )

        for arg in self.arg_list:
            contents += '{ind2}{prop}\n'.format(ind2=Indent(2), prop=arg.class_init)
        contents += '\n'

        for arg in self.arg_list:
            contents += "{}\n".format(arg.class_property)
        contents += '\n'

        # Model
        contents += "class {}(ndb.Model):\n".format(self.class_list[1])
        for arg in self.arg_list:
            contents += "{ind1}{prop}\n".format(ind1=Indent(1), prop=arg.model_init)
        contents += '\n'

        # StructuredProperty


        with open(self.filename, "w") as f:
            f.write(contents)



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print 'Usage: python %s <config_json>' % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    loaded_conf = ""
    with open(filename) as f:
        loaded_conf = f.read()

    pg = PropertyGenerator(json.loads(loaded_conf))
    pg.validate()
    pg.write()
