import unittest
from ndb_prop_gen.arg import Arg
from ndb_prop_gen.arg import find_prop_type


sample_property = """\
    @property
    def sample_float(self):
        return self._sample_float
"""


class TestArg(unittest.TestCase):

    def setUp(self):
        self.sample1 = Arg("sample_float", "Float", 0.0)
        self.sample2 = Arg("sample_string", "string", "")
        pass

    def tearDown(self):
        pass

    def test_find_prop_type(self):
        # non fuzzy
        self.assertEqual(find_prop_type("float"), "ndb.Float")

        # fuzzy
        self.assertEqual(find_prop_type("int"), "ndb.Integer")
        self.assertEqual(find_prop_type("Int"), "ndb.Integer")
        self.assertEqual(find_prop_type("integer"), "ndb.Integer")
        self.assertEqual(find_prop_type("integer"), "ndb.Integer")

        # non ndb
        self.assertEqual(find_prop_type("Original"), "Original")

    def test_class_arg(self):
        self.assertEqual(self.sample1.class_arg, "sample_float=0.0")
        self.assertEqual(self.sample2.class_arg, "sample_string=\"\"")

    def test_class_init(self):
        self.assertEqual(self.sample1.class_init, "self._sample_float = sample_float")
        self.assertEqual(self.sample2.class_init, "self._sample_string = sample_string")

    def test_class_property(self):
        self.assertEqual(self.sample1.class_property, sample_property)

    def test_model_init(self):
        self.assertEqual(self.sample1.model_init, "sample_float = ndb.FloatProperty(default=0.0)")
        self.assertEqual(self.sample2.model_init, "sample_string = ndb.StringProperty(default=\"\")")

if __name__ == "__main__":
    unittest.main()
