
__version__ = "0.0.4"
__author__ = "Takuro Wada"
__email__ = "taxpon@gmail.com"
__url__ = "https://github.com/taxpon/ndb_prop_gen"
__license__ = "MIT"


def generate(filename):
    import json
    from generator import PropertyGenerator

    with open(filename) as f:
        loaded_conf = f.read()

    pg = PropertyGenerator(json.loads(loaded_conf))
    pg.validate()
    pg.create_contents()
    pg.write()
