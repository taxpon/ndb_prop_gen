import json
import sys
import os

sys.path.append("/".join(os.path.abspath(__file__).split('/')[:-2]))

from ndb_prop_gen.generator import PropertyGenerator  # noqa


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
    pg.create_contents()
    pg.write()
