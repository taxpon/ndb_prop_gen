import sys
import os

sys.path.append("/".join(os.path.abspath(__file__).split('/')[:-2]))

import ndb_prop_gen as npg  # noqa

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print 'Usage: python %s <config_json>' % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    npg.generate(filename)
