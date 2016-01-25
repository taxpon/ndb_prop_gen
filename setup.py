from setuptools import setup
from setuptools import find_packages

import ndb_prop_gen

setup(
    name=ndb_prop_gen.__name__,
    packages=find_packages(exclude=['tests*', 'example']),
    version=ndb_prop_gen.__version__,
    author=ndb_prop_gen.__author__,
    author_email=ndb_prop_gen.__email__,
    description="Google Appengine ndb Property Generator written in python. " +
                "You can convert json data into your custom ndb property by this library.",
    url=ndb_prop_gen.__url__,
    license=ndb_prop_gen.__license__,
    scripts=['bin/ndb_prop_gen'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Code Generators"
    ]
)
