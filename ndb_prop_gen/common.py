

class Indent(object):
    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return "    " * self.level
