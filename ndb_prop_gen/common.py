

def ind1(text):
    return "{}{}".format(Indent(1), text)


def ind2(text):
    return "{}{}".format(Indent(2), text)


def ind3(text):
    return "{}{}".format(Indent(3), text)


class Indent(object):
    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return "    " * self.level
