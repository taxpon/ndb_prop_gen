import unittest
from ndb_prop_gen.common import ind1
from ndb_prop_gen.common import ind2
from ndb_prop_gen.common import ind3


class TestIndent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_class_indent(self):
        self.assertEqual(ind1("test"), "    test")
        self.assertEqual(ind2("test"), "        test")
        self.assertEqual(ind3("test"), "            test")

if __name__ == "__main__":
    unittest.main()
